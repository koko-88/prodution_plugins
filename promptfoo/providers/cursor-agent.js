/**
 * Promptfoo ApiProvider that drives Cursor headless CLI (`agent -p`).
 * Returns final text plus a Codex-compatible raw.items summary so existing
 * filesystem assertions can verify SKILL.md / intake.py tool exposure.
 *
 * Windows note: never put the full Promptfoo prompt on argv. CreateProcess /
 * cmd.exe length limits produce "The command line is too long" and broken
 * quoting produces "The system cannot find the file/path specified". Stage the
 * prompt under promptfoo/.state/prompt-files and pass a short pointer plus
 * --add-dir instead.
 */
const { spawn } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

/**
 * Resolve to a spawnable argv pair. On Windows, prefer the versioned
 * node.exe + index.js so we never route through cmd.exe / PowerShell.
 */
function resolveAgentLaunch(config = {}) {
  const configured = config.agentPath;
  const localApp = process.env.LOCALAPPDATA || '';
  const versionsRoot = path.join(localApp, 'cursor-agent', 'versions');

  function latestVersionDir() {
    if (!fs.existsSync(versionsRoot)) return null;
    const dirs = fs
      .readdirSync(versionsRoot, { withFileTypes: true })
      .filter((d) => d.isDirectory())
      .map((d) => d.name)
      .sort()
      .reverse();
    return dirs.length ? path.join(versionsRoot, dirs[0]) : null;
  }

  function launchFromVersionDir(dir) {
    const nodeBin = path.join(dir, 'node.exe');
    const indexJs = path.join(dir, 'index.js');
    if (fs.existsSync(nodeBin) && fs.existsSync(indexJs)) {
      return { command: nodeBin, prefixArgs: [indexJs], via: 'node-index' };
    }
    return null;
  }

  if (process.platform === 'win32') {
    const ver = latestVersionDir();
    const direct = ver && launchFromVersionDir(ver);
    if (direct) return direct;
  }

  if (configured && fs.existsSync(configured)) {
    // If configured path is agent.cmd, still prefer versioned node when present.
    if (process.platform === 'win32' && /\.(cmd|bat)$/i.test(configured)) {
      const ver = latestVersionDir();
      const direct = ver && launchFromVersionDir(ver);
      if (direct) return direct;
    }
    return { command: configured, prefixArgs: [], via: 'configured' };
  }

  const local = path.join(
    localApp,
    'cursor-agent',
    process.platform === 'win32' ? 'agent.cmd' : 'agent',
  );
  if (fs.existsSync(local)) {
    if (process.platform === 'win32') {
      const ver = latestVersionDir();
      const direct = ver && launchFromVersionDir(ver);
      if (direct) return direct;
    }
    return { command: local, prefixArgs: [], via: 'wrapper' };
  }
  return {
    command: process.platform === 'win32' ? 'agent.cmd' : 'agent',
    prefixArgs: [],
    via: 'path',
  };
}

function promptStagingDir() {
  return path.resolve(__dirname, '..', '.state', 'prompt-files');
}

function stagePromptFile(prompt) {
  const dir = promptStagingDir();
  fs.mkdirSync(dir, { recursive: true });
  const name = `prompt-${process.pid}-${Date.now()}-${crypto.randomBytes(4).toString('hex')}.txt`;
  const filePath = path.join(dir, name);
  fs.writeFileSync(filePath, String(prompt ?? ''), 'utf8');
  return filePath;
}

function normalizeItems(events) {
  const items = [];
  for (const ev of events) {
    if (!ev || typeof ev !== 'object') continue;
    if (ev.type === 'tool_call') {
      const tc = ev.tool_call || {};
      const read =
        tc.readToolCall ||
        tc.read_fileToolCall ||
        tc.Read ||
        tc.readFileToolCall;
      const shell =
        tc.shellToolCall ||
        tc.runTerminalCommandToolCall ||
        tc.Shell ||
        tc.bashToolCall ||
        tc.commandToolCall;
      if (read) {
        const p =
          read.args?.path ||
          read.args?.filePath ||
          read.args?.targetFile ||
          read.path ||
          '';
        items.push({
          type: 'command_execution',
          exit_code: ev.subtype === 'completed' && read.result?.error ? 1 : 0,
          command: `read ${p}`,
          aggregated_output: '',
        });
      }
      if (shell) {
        const cmd =
          shell.args?.command ||
          shell.args?.cmd ||
          shell.command ||
          JSON.stringify(shell.args || shell);
        const exit =
          shell.result?.success?.exitCode ??
          shell.result?.exitCode ??
          (shell.result?.error ? 1 : 0);
        items.push({
          type: 'command_execution',
          exit_code: Number.isFinite(exit) ? exit : 0,
          command: String(cmd),
          aggregated_output: String(
            shell.result?.success?.stdout ||
              shell.result?.stdout ||
              shell.result?.error ||
              '',
          ),
        });
      }
    }
  }
  return items;
}

function extractFinalText(events, stdout) {
  for (let i = events.length - 1; i >= 0; i -= 1) {
    const ev = events[i];
    if (ev?.type === 'result' && typeof ev.result === 'string') {
      return ev.result;
    }
    if (ev?.type === 'result' && typeof ev.result?.text === 'string') {
      return ev.result.text;
    }
  }
  for (let i = events.length - 1; i >= 0; i -= 1) {
    const ev = events[i];
    if (ev?.type === 'assistant') {
      const parts = ev.message?.content || [];
      const text = parts
        .map((p) => (typeof p?.text === 'string' ? p.text : ''))
        .join('');
      if (text.trim()) return text;
    }
  }
  return String(stdout || '').trim();
}

class CursorAgentProvider {
  constructor(options = {}) {
    this.providerId = options.id || 'cursor-agent';
    this.config = options.config || {};
    this.label = options.label;
  }

  id() {
    return this.providerId;
  }

  async callApi(prompt, context /*, options */) {
    const vars = context?.vars || {};
    const cfg = this.config;
    const workspace =
      cfg.working_dir?.replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k] ?? '') ||
      (vars.eval_root && vars.case_id
        ? path.join(vars.eval_root, 'fixtures', vars.case_id)
        : process.cwd());
    const launch = resolveAgentLaunch(cfg);
    const pluginDir =
      cfg.pluginDir ||
      path.resolve(__dirname, '..', '..', 'dist', 'context-intake');
    const timeoutMs = Number(cfg.timeoutMs || 240000);
    const model = cfg.model;
    const force = cfg.force !== false;
    const trust = cfg.trust !== false;
    const sandbox = cfg.sandbox || 'disabled';
    const outputFormat = cfg.outputFormat || 'stream-json';

    const promptFile = stagePromptFile(prompt);
    const promptDir = path.dirname(promptFile);
    // Forward slashes avoid cmd-style quoting issues if a wrapper is used.
    const promptFilePosix = promptFile.replace(/\\/g, '/');
    const pointer = [
      `Open the UTF-8 text file at ${promptFilePosix}.`,
      'Follow its instructions exactly.',
      'Do not modify that file.',
      'Do not invent unrelated tasks.',
    ].join(' ');

    const args = [
      ...launch.prefixArgs,
      '-p',
      '--output-format',
      outputFormat,
      '--workspace',
      workspace,
      '--sandbox',
      sandbox,
      '--plugin-dir',
      pluginDir,
      '--add-dir',
      promptDir,
    ];
    if (force) args.push('--force');
    if (trust) args.push('--trust');
    if (model) args.push('--model', model);
    args.push(pointer);

    const started = Date.now();
    let stdout;
    let stderr;
    let code;
    let events;
    try {
      ({ stdout, stderr, code, events } = await runAgent(
        launch.command,
        args,
        workspace,
        timeoutMs,
        launch.via,
      ));
    } finally {
      try {
        fs.unlinkSync(promptFile);
      } catch (_) {
        /* ignore */
      }
    }

    const output = extractFinalText(events, stdout);
    const items = normalizeItems(events);

    if (code !== 0 && !output) {
      return {
        error: `cursor-agent exited ${code}: ${stderr || stdout}`.slice(0, 4000),
        raw: {
          items,
          events,
          code,
          stderr,
          provider: 'cursor-agent',
          launchVia: launch.via,
          workspace,
        },
      };
    }

    return {
      output,
      raw: {
        items,
        events,
        code,
        stderr,
        provider: 'cursor-agent',
        launchVia: launch.via,
        workspace,
        durationMs: Date.now() - started,
      },
    };
  }
}

function runAgent(command, args, cwd, timeoutMs, via) {
  return new Promise((resolve) => {
    const isWin = process.platform === 'win32';
    const isCmdWrapper =
      isWin && via !== 'node-index' && /\.(cmd|bat)$/i.test(command);
    const child = isCmdWrapper
      ? spawn(
          process.env.ComSpec || 'cmd.exe',
          ['/d', '/s', '/c', command, ...args],
          {
            cwd,
            env: { ...process.env },
            windowsHide: true,
          },
        )
      : spawn(command, args, {
          cwd,
          env: { ...process.env },
          windowsHide: true,
        });
    let stdout = '';
    let stderr = '';
    const events = [];
    let settled = false;
    const timer = setTimeout(() => {
      if (settled) return;
      settled = true;
      try {
        child.kill();
      } catch (_) {
        /* ignore */
      }
      resolve({
        stdout,
        stderr: stderr + `\nTimed out after ${timeoutMs}ms`,
        code: 124,
        events,
      });
    }, timeoutMs);

    child.stdout.on('data', (buf) => {
      const chunk = buf.toString('utf8');
      stdout += chunk;
      for (const line of chunk.split(/\r?\n/)) {
        if (!line.trim()) continue;
        try {
          events.push(JSON.parse(line));
        } catch (_) {
          // non-JSON progress noise
        }
      }
    });
    child.stderr.on('data', (buf) => {
      stderr += buf.toString('utf8');
    });
    child.on('error', (err) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({
        stdout,
        stderr: String(err),
        code: 127,
        events,
      });
    });
    child.on('close', (code) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({ stdout, stderr, code: code ?? 0, events });
    });
  });
}

module.exports = CursorAgentProvider;

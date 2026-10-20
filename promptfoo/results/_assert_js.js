return (async () => {
const fs = await import('node:fs');
const path = await import('node:path');
const crypto = await import('node:crypto');
const {spawnSync} = await import('node:child_process');
const root = context.vars.eval_root;
const id = context.vars.case_id;
const workspace = path.join(root, 'fixtures', id);
const prior = JSON.parse(fs.readFileSync(path.join(root, 'fixtures/baselines.json'), 'utf8'))[id];
const after = {};
function walk(dir) { for (const item of fs.readdirSync(dir,{withFileTypes:true})) { const p=path.join(dir,item.name); if(item.isSymbolicLink()) throw new Error('Unexpected linked fixture path'); if(item.isDirectory()) walk(p); else after[path.relative(workspace,p).replace(/\\/g,'/')] = crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'); } }
walk(workspace);
const raw = typeof context.providerResponse?.raw === 'string' ? JSON.parse(context.providerResponse.raw) : context.providerResponse?.raw;
const items = raw?.items || [];
if (items.some(i => /sandbox failed|setup refresh had errors|helper_unknown_error/i.test(i.aggregated_output || ''))) return {pass:false,score:0,reason:'BLOCKED_HOST: sandbox initialization failed; do not classify as a behavioral failure'};
const readSkill = items.some(i => i.type === 'command_execution' && i.exit_code === 0 && /SKILL\.md/i.test(i.command || ''));
if (!readSkill) return {pass:false,score:0,reason:'No successful SKILL.md read in actual Codex execution; method exposure unverified'};
for (const [p,hash] of Object.entries(prior)) if(after[p] !== hash) return {pass:false,score:0,reason:'Existing consumer fixture changed: '+p};
const added = Object.keys(after).filter(p => !(p in prior));
if(id !== 'UC-32') return {pass:added.length===0,score:added.length===0?1:0,reason:added.length?'Unauthorized output: '+added.join(', '):'Existing fixture bytes preserved; no consumer files added'};
if(added.length!==1 || !/^docs\/intake\/[^/]+\/HANDOFF\.md$/.test(added[0])) return {pass:false,score:0,reason:'Expected exactly one canonical HANDOFF, got '+JSON.stringify(added)};
const file=path.join(workspace,added[0]);
const result=spawnSync(context.vars.python,[path.join(context.vars.skill_root,'scripts/intake.py'),'validate',file,'--workspace',workspace],{encoding:'utf8',timeout:20000});
if(result.status!==0) return {pass:false,score:0,reason:'Existing canonical validator rejected output: '+result.stdout+result.stderr};
const md=fs.readFileSync(file,'utf8');
const identity=JSON.parse(md.match(/```json\s*({[\s\S]*?})\s*```/)[1]).identity;
const validatedBySubject=items.some(i=>i.type==='command_execution' && i.exit_code===0 && /intake\.py.+validate/.test(i.command||''));
return {pass:identity.id==='OPS-32' && validatedBySubject,score:identity.id==='OPS-32' && validatedBySubject?1:0,reason:'Artifact independently checked with canonical helper; subject validation '+validatedBySubject};
})();
"""Validate the actual unified package; no claim about remote service connectivity."""
from pathlib import Path
import ast, hashlib, importlib.util, json, re, sys
import yaml

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'academic-research-assistant'
sys.path.insert(0,str(ROOT/'work/validation-deps'))
import jsonschema

def main():
    failures=[]
    checks=[]
    for file,schema in [('plugin.json','plugin.schema.json'),('mcp.json','mcp.schema.json')]:
        data=json.loads((PACKAGE/file).read_text(encoding='utf-8'))
        sc=json.loads((ROOT/'work/schemas'/schema).read_text(encoding='utf-8'))
        jsonschema.Draft202012Validator(sc).validate(data)
        checks.append(file+' official schema PASS')
    manifest=json.loads((PACKAGE/'plugin.json').read_text())
    interface=manifest['extensions']['com.openai']['interface']
    assert len(interface['shortDescription'])<=30
    assert interface['category']=='Education & Research'
    assert re.fullmatch(r'\d+\.\d+\.\d+',manifest['version'])
    compatibility=json.loads((PACKAGE/'.codex-plugin/plugin.json').read_text())
    assert all(compatibility[k]==manifest[k] for k in ['name','version'])
    assert compatibility['interface']==interface
    all_json=all_yaml=all_python=jsonl_rows=0
    for p in sorted(PACKAGE.rglob('*')):
        if not p.is_file():
            continue
        if p.is_symlink():
            failures.append('Unexpected symlink '+str(p))
        if p.suffix=='.json':
            json.loads(p.read_text(encoding='utf-8-sig')); all_json+=1
        elif p.suffix in ['.yml','.yaml']:
            yaml.safe_load(p.read_text(encoding='utf-8-sig')); all_yaml+=1
        elif p.suffix=='.py':
            ast.parse(p.read_text(encoding='utf-8-sig')); all_python+=1
        elif p.suffix=='.jsonl':
            for line in p.read_text(encoding='utf-8-sig').splitlines():
                if line.strip():
                    json.loads(line);jsonl_rows+=1
    catalog=json.loads((PACKAGE/'catalog/skills.json').read_text(encoding='utf-8'))
    assert len(catalog)==117
    assert len({x['name'] for x in catalog})==117
    active=list((PACKAGE/'skills').glob('*/SKILL.md'))
    assert len(active)==118, len(active)
    for p in active:
        raw=p.read_text(encoding='utf-8')
        assert raw.startswith('---\n'),str(p)
        assert p.stat().st_size<=1024*1024
        fm=yaml.safe_load(raw.split('---',2)[1])
        assert fm['name']==p.parent.name
        assert isinstance(fm['description'],str) and fm['description'].strip()
        for agent in (p.parent/'agents').glob('openai.yaml'):
            value=yaml.safe_load(agent.read_text())
            assert isinstance(value,dict)
            if isinstance(value.get('interface'),dict):
                for key in ['display_name','short_description']:
                    assert isinstance(value['interface'].get(key),str) and value['interface'][key]
            policy=value.get('policy',{})
            assert set(policy)<=set(['products','allow_implicit_invocation'])
            if 'allow_implicit_invocation' in policy:
                assert policy['allow_implicit_invocation'] is None or type(policy['allow_implicit_invocation']) is bool
    known={x['name'] for x in catalog}
    for route in json.loads((PACKAGE/'catalog/routes.json').read_text()):
        assert set(route['skills'])<=known
    spec=importlib.util.spec_from_file_location('runtime',PACKAGE/'server/assistant_server.py')
    runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)
    source_report=runtime.verify_sources()
    assert source_report['passed'], source_report
    assert source_report['verified']==273
    assert source_report['directories_verified']==179
    # Actual Markdown file links, including fragments, rather than prose examples.
    links=[]
    for base in ['skills','docs','workflows','agents','README.md','THIRD_PARTY_NOTICES.md']:
        paths=[PACKAGE/base] if (PACKAGE/base).is_file() else sorted((PACKAGE/base).rglob('*.md'))
        for p in paths:
            raw=p.read_text(encoding='utf-8-sig')
            for match in re.finditer(r'\[[^\]\n]*\]\(([^)\n]+)\)',raw):
                target=match.group(1).split(' "')[0].strip('<>')
                if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'):
                    continue
                target=target.split('#')[0]
                if not target:
                    continue
                resolved=(p.parent/target).resolve()
                valid=resolved.is_relative_to(PACKAGE.resolve()) and resolved.exists()
                links.append({'file':p.relative_to(PACKAGE).as_posix(),'target':target,'exists':valid})
                if not valid:
                    failures.append('Broken Markdown reference '+p.relative_to(PACKAGE).as_posix()+': '+target)
    # References embedded in the active manifest are required, not documentary.
    for field in ['logo','composerIcon','logoDark','composerIconDark']:
        if field in interface:
            assert (PACKAGE/interface[field]).is_file()
    assert (PACKAGE/manifest['extensions']['com.openai']['onboardingSkill']).is_file()
    server=load= json.loads((PACKAGE/'mcp.json').read_text())['mcpServers']['academic-research-local']
    assert (PACKAGE/server['args'][1].replace('${PLUGIN_ROOT}/','')).is_file()
    checks.extend(['118 unique active skills and metadata PASS','All route destinations PASS',
                   '273 source file hashes and 179 directory entries PASS','Manifest/overlay identity and interface synchronized PASS'])
    report={'passed':not failures,'checks':checks,'json_files':all_json,'yaml_files':all_yaml,
            'python_files':all_python,'jsonl_records':jsonl_rows,'markdown_links':len(links),
            'source_preservation':source_report,'failures':failures}
    (PACKAGE/'audit/package-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (PACKAGE/'audit/reference-links.json').write_text(json.dumps(links,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    return 0 if not failures else 1

if __name__=='__main__':
    raise SystemExit(main())

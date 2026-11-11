"""Verify preservation and active instructions against the complete reviewed baseline."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parent.parent
def read(rel):return (ROOT/rel).read_text(encoding='utf-8-sig')
def load(rel):return json.loads(read(rel))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def body(text):
    m=re.match(r'\A---\s*\n.*?\n---[^\n]*\n',text,re.S)
    assert m,'Missing skill frontmatter'
    return text[m.end():].lstrip()

def main():
    mapping=load('audit/review-118/skill-mapping.json')
    files=load('audit/review-118/file-mapping.json')
    aliases=load('catalog/aliases.json');catalog=load('catalog/skills.json')
    assert len(mapping)==118 and len({x['source_id'] for x in mapping})==118
    assert len(catalog)==116 and len(aliases)==2
    assert len(list((ROOT/'skills').glob('*/SKILL.md')))==118
    assert len(files)==600
    for row in files:
        assert sha(ROOT/row['preserved_at'])==row['sha256'],row['source']
    adaptations=load('audit/review-118/adaptations.json')
    merged={'evidence-research-gaps','scholar-research-gaps','evidence-systematic-review','scholar-systematic-review'}
    count=0
    for row in mapping:
        source=ROOT/row['source_path']
        assert sha(source)==row['source_sha256'],row['source_id']
        if row['source_id'] in merged:continue
        expected=body(source.read_text(encoding='utf-8-sig'))
        for fix in adaptations:
            if fix['active_path']=='skills/'+row['source_id']+'/SKILL.md':
                expected=expected.replace(fix['original'],fix['proposed_replacement'])
        active=read(row['destination'])
        assert '## Preserved source instructions\n' in active,row['source_id']
        retained=active.split('## Preserved source instructions\n',1)[1].lstrip()
        assert retained==expected,('source method body differs',row['source_id'])
        count+=1
    for row in catalog:
        active=read(row['path'])
        assert re.search(r'^name: '+re.escape(row['name'])+r'\s*$',active,re.M),row['name']
        assert len(row['description'])<=1024,row['name']
        assert all((ROOT/'skills'/name/'SKILL.md').is_file() for name in row['related']),row['name']
    import yaml  # Development validation dependency, already declared in dev/requirements-dev.txt.
    links=0
    for p in (ROOT/'skills').glob('*/SKILL.md'):
        text=p.read_text(encoding='utf-8-sig')
        front=re.match(r'\A---\s*\n(.*?)\n---[^\n]*\n',text,re.S)
        assert yaml.safe_load(front.group(1))['name']==p.parent.name
        text=re.sub(r'```.*?```','',text,flags=re.S)
        for target in re.findall(r'\[[^\]]+\]\(([^\s)]+)(?:\s+[^)]*)?\)',text):
            if '://' in target or target.startswith(('mailto:','#','data:')):continue
            target=unquote(target.split('#')[0].strip('<>'))
            if target:
                assert (p.parent/target).resolve().exists(),(p.relative_to(ROOT).as_posix(),target)
                links+=1
    package=load('package.json');assert package['private'] is False
    assert package['version']=='4.0.0'
    assert 'MIT' not in package['license']
    subprocess.run([sys.executable,'-B',str(ROOT/'skills/humanizer/scripts/validate-package.py')],check=True)
    result={'passed':True,'source_files_preserved':600,'source_skills_mapped':118,
            'canonical_methods':116,'compatibility_entries':2,'unmerged_complete_bodies':count,
            'active_skill_yaml_valid':118,'active_skill_links_resolved':links,
            'semantic_merged_method_review':'audit/review-118/reports/final-content-review.json',
            'scope':'File preservation, complete active source bodies and package metadata; not research execution or host installation.'}
    assert (ROOT/result['semantic_merged_method_review']).is_file()
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

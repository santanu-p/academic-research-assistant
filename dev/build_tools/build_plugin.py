"""Rebuild the unified plugin from the immutable, completely inventoried inputs."""
from pathlib import Path
import csv, hashlib, json, re, shutil
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work'
OUT = ROOT / 'academic-research-assistant'
FAMILIES = {
    'latexdocumentmaker': ('latex', 'LaTeX Document Maker'),
    'research-writing-guardrails': ('guardrails', 'Research Writing Guardrails'),
    'researchevidencefinder': ('evidence', 'Research Evidence Finder'),
    'scholarresearch': ('scholar', 'Scholar Research'),
    'scientific-visual-table-style': ('visuals', 'Scientific Visuals & Tables'),
    'ARMS-main': ('arms', 'ARMS'),
}
ARMS_DESCRIPTIONS = {
 'literature-lead':'Search and critically synthesize literature, verify citations and distinguish established findings from candidate gaps.',
 'paper-critic':'Critically review manuscript claims, methods, evidence and exposition, with actionable issues tied to the source.',
 'paper-fixer':'Revise a research manuscript against specific review findings while preserving data, claims and source traceability.',
 'paper-grader':'Assess a manuscript with the supplied evidence, methodology and presentation rubric; scores are advisory judgments.',
 'paper-modeler':'Develop mathematical modeling, derivations and theoretical analysis grounded in the supplied research brief and evidence.',
 'paper-writer':'Draft research paper sections from the approved methodology, author evidence and reproducible results.',
 'research-pipeline':'Coordinate the complete ARMS research pipeline from brief through literature, methods, validation, writing and review.',
 'validate-method':'Validate the proposed research method through executable checks, comparators, ablations, failure cases and evidence logs.',
 'write-manuscript':'Build an author-grounded manuscript from actual contributions, evidence and the supplied house style.',
}
ROUTES = [
 ('systematic-review',['systematic review','scoping review','prisma','screening'],['evidence-systematic-review','scholar-systematic-review','evidence-data-extraction','evidence-study-appraisal']),
 ('meta-analysis',['meta-analysis','meta analysis','pooled effect','heterogeneity'],['evidence-meta-analysis','evidence-statistics-explained','scholar-data-analysis-plan']),
 ('literature',['literature','papers','find studies','search strings','citation chaining'],['evidence-find-studies','evidence-search-strings','evidence-citation-chaining','scholar-literature-review','evidence-literature-review']),
 ('citation',['verify','citation','doi','references','bibliography'],['evidence-source-verification','evidence-citations-and-references','scholar-citation-generator','latex-bibliography-citations']),
 ('gap',['gap','novelty','research topic','research question','hypothesis'],['evidence-research-gaps','scholar-research-question','scholar-theoretical-framework','guardrails-research-problem-mechanism-evidence']),
 ('qualitative',['qualitative','thematic','interview','codebook','grounded theory'],['scholar-qualitative-analysis','scholar-survey-design','scholar-methodology-design']),
 ('methods',['experimental design','methodology','sampling','study design','mixed methods'],['scholar-methodology-design','arms-methodology-architect','scholar-data-analysis-plan']),
 ('ethics',['ethics','consent','irb','participant information'],['scholar-research-ethics','scholar-originality-integrity']),
 ('statistics',['statistics','statistical','regression','anova','p-value','effect size','confidence interval'],['scholar-data-analysis-plan','scholar-results-interpreter','evidence-statistics-explained']),
 ('modeling',['mathematical','modeling','modelling','conformal','derivation','simulation'],['arms-paper-modeler','arms-validate-method','arms-methodology-architect']),
 ('pipeline',['full arms','research pipeline','end-to-end','autonomous research'],['arms-research-pipeline','arms-brief-expander','arms-literature-lead','arms-methodology-architect','arms-validate-method']),
 ('review',['peer review','review my manuscript','critic','grade my paper','adversarial loop'],['arms-paper-critic','arms-paper-grader','scholar-peer-review-critique','arms-critic-revisor']),
 ('reviewer-response',['reviewer response','respond to reviewer','point-by-point','rebuttal','reviewer comments'],['scholar-reviewer-response','arms-paper-fixer','guardrails-compag-elsevier-paper-editing']),
 ('grant',['grant','funding','nih','nsf','specific aims'],['scholar-grant-proposal','academic-humanizer','scholar-research-proposal']),
 ('proposal',['proposal','synopsis','research brief'],['scholar-research-proposal','evidence-research-proposal-background','arms-brief-expander']),
 ('thesis',['thesis','dissertation','viva','capstone'],['scholar-thesis-dissertation','latex-thesis-dissertation','scholar-research-planner']),
 ('presentation',['presentation','powerpoint','pptx','conference talk','slides','seminar'],['academic-pptx','scholar-research-communication','latex-beamer-slides']),
 ('poster',['poster','a0','a1','beamerposter'],['latex-academic-poster','scholar-research-communication']),
 ('visuals',['figure','plot','chart','visualization','visualisation','scientific figures','scientific tables'],['visuals-scientific-visual-table-style','latex-pgfplots-charts','latex-tables']),
 ('math',['equation','equations','formula','math','theorem','proof'],['latex-math-equations','latex-equation-converter','latex-theorems-proofs']),
 ('latex',['latex','tex','overleaf','compile'],['latex-latex-studio','latex-document-builder','latex-error-fixer','latex-setup-compiling']),
 ('humanize',['ai-sounding','humanize','humanise','writer voice','ai tells'],['humanizer','academic-humanizer','arms-house-style']),
 ('edit',['edit','proofread','polish','academic prose','word count','shorten','translate'],['scholar-academic-editing','academic-humanizer','scholar-word-reduction','scholar-academic-translation']),
 ('write',['manuscript','write a paper','abstract','introduction','results section','discussion'],['arms-write-manuscript','scholar-paper-sections','scholar-abstract-introduction','guardrails-compag-elsevier-paper-editing']),
 ('publish',['journal','submission','publish','cover letter'],['scholar-journal-finder','scholar-submission-checklist','latex-journal-templates']),
 ('manage',['timeline','milestone','project plan','schedule','supervisor'],['scholar-research-planner']),
 ('integrity',['reproducibility','reproduce','integrity','audit claims','evidence alignment'],['guardrails-research-problem-mechanism-evidence','arms-validate-method','scholar-originality-integrity']),
]

def write(path, value):
    path = OUT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding='utf-8', newline='\n')

def dump(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def skill_sources():
    result=[]
    for tree in ['originals','expanded']:
        for p in sorted((WORK/tree).rglob('SKILL.md')):
            rel=p.relative_to(WORK/tree)
            family=rel.parts[0]
            if family in FAMILIES:
                prefix,label=FAMILIES[family]
                name=prefix+'-'+p.parent.name
            else:
                name={'academic-humanizer-main':'academic-humanizer','academic-pptx-skill-main':'academic-pptx','humanizer-main':'humanizer'}[family]
                prefix=name
                label=name
            result.append(dict(source=p,tree=tree,rel=rel,family=family,prefix=prefix,label=label,name=name))
    return result

def main():
    OUT.mkdir(exist_ok=True)
    if (ROOT/'integration').is_dir():
        shutil.copytree(ROOT/'integration',OUT,dirs_exist_ok=True)
    # Preserve original containers, hidden metadata, every support file and every archive entry.
    for tree,dest in [('originals','resources/originals'),('expanded','resources/upstream')]:
        shutil.copytree(WORK/tree, OUT/dest, dirs_exist_ok=True)
    for p in sorted((ROOT/'docs').glob('*.md')):
        write('docs/build-'+p.name,p.read_text(encoding='utf-8'))
    inspection=json.loads((WORK/'inspection.json').read_text(encoding='utf-8'))
    dump('audit/source-inspection.json',inspection)
    sources=skill_sources()
    mappings=[]
    for input_name,base in [('original-inventory.json','resources/originals'),('archive-inventory.json','resources/upstream')]:
        for x in json.loads((WORK/input_name).read_text(encoding='utf-8')):
            row=dict(x)
            row['destination']=base+'/'+x['source'].rstrip('/')
            row['disposition']='preserved-byte-for-byte' if row['kind']=='file' else 'directory-preserved'
            row['active_destinations']=[]
            for sk in sources:
                if ('archive' in x) != (sk['tree']=='expanded'):
                    continue
                rel=Path(x['source'])
                source_dir=sk['rel'].parent
                if rel==source_dir or source_dir in rel.parents:
                    row['active_destinations'].append('skills/'+sk['name']+'/'+rel.relative_to(source_dir).as_posix())
            path=Path(x['source'])
            if row['active_destinations']:
                role,reason='active-skill-or-support','Complete content copied into the indicated discoverable skill/support tree; original bytes separately preserved.'
            elif x['kind']=='directory':
                role,reason='resource-directory','Original directory structure retained for contained reads, provenance and resource relationships.'
            elif path.suffix=='.zip':
                role,reason='original-archive','Exact supplied ZIP retained; every member separately expanded, inspected and mapped.'
            elif path.name in ['plugin.json','marketplace.json','.codex-remote-plugin-install.json']:
                role,reason='upstream-plugin-specification','Retained as integration/provenance metadata. Unified manifests supersede registration; foreign identities, legacy fields and marketplace records cannot be merged as authenticated connections.'
            elif path.name in ['LICENSE','COPYING','DISCLAIMER.md']:
                role,reason='license-or-provenance','Original terms/disclaimer retained and referenced by third-party notices; no blanket relicensing or unsupported historical claim.'
            elif 'case-studies' in path.parts or 'examples' in path.parts:
                role,reason='complete-example-or-case-study','Complete runnable/documentary example resource retained; workflows expose it with runtime and historical-evidence limits. No automatic experiment rerun or alteration of supplied results.'
            elif path.suffix.lower() in ['.png','.svg','.pdf']:
                role,reason='source-asset','Original binary/vector asset retained and inspected; host viewer/file tools access it. Upstream branding and evidence are not silently replaced.'
            else:
                role,reason='supporting-resource-or-specification','Complete source resource retained and accessible from resource paths/catalog. Dependencies and source-specific configuration constraints are described in the inspection and integration documentation.'
            row.update(integration_role=role,integration_reason=reason)
            mappings.append(row)
    catalog=[]
    changes=[]
    for sk in sources:
        dst=OUT/'skills'/sk['name']
        # Root-level standalone skills carry their complete supporting repository.
        shutil.copytree(sk['source'].parent,dst,dirs_exist_ok=True)
        original=sk['source'].read_text(encoding='utf-8-sig')
        if original.startswith('---'):
            parts=original.split('---',2)
            metadata=yaml.safe_load(parts[1])
            body=parts[2].lstrip('\r\n')
        else:
            metadata={}
            body=original
        old_name=metadata.get('name',sk['source'].parent.name)
        description=' '.join(str(metadata.get('description',ARMS_DESCRIPTIONS.get(old_name,''))).split())
        if not description:
            raise ValueError('Missing description '+sk['name'])
        edits=['Unique portable name: '+sk['name']]
        if not metadata:
            edits.append('Added missing YAML name and description; full original body retained')
        if sk['prefix']=='scholar':
            description=description.replace(' Also use for follow-up messages in any conversation where Scholar Research has already been used.','')
        if old_name in ['scholar-studio','latex-studio','research-evidence-finder']:
            description={
                'scholar-studio':'Use for broad academic research requests or research onboarding; identify the research stage and route to the appropriate specialist.',
                'latex-studio':'Use for broad LaTeX document creation, typesetting, conversion or compilation help; route to the appropriate LaTeX specialist.',
                'research-evidence-finder':'Use for evidence-backed research questions, literature searches, study appraisal and evidence workflow onboarding; route to the appropriate evidence specialist.'}[old_name]
            edits.append('Scoped global activation to relevant tasks; absent promotional footer not fabricated')
        if sk['name']=='academic-pptx':
            description=description.replace('�','-')
            edits.append('Corrected source replacement character in active metadata; actual MIT license retained despite inaccurate upstream frontmatter')
        if sk['name']=='arms-critic-revisor':
            description='Use when explicitly asked to run or plan the ARMS adversarial manuscript critic/revisor loop. Requires separately configured Bash, Claude CLI, Codex CLI, latexmk and latexdiff; preserves the supplied loop script.'
        sibling={x['source'].parent.name:x['name'] for x in sources if x['family']==sk['family']}
        # Rewrite identifiers, never ordinary research terminology in prose.
        for before,after in sorted(sibling.items(),key=lambda x:-len(x[0])):
            if before==after:
                continue
            body=body.replace('skills/'+before+'/', 'skills/'+after+'/')
            body=body.replace('../'+before+'/', '../'+after+'/')
            body=re.sub(r'`([$/]?)'+re.escape(before)+r'`',lambda m:'`'+m[1]+after+'`',body)
            body=re.sub(r'(?<![\w/:.-])/'+re.escape(before)+r'(?=[\s`\"\',.]|$)','/'+after,body)
            body=re.sub(r'\$'+re.escape(before)+r'(?![\w-])','$'+after,body)
        # Plain-name routing tables are executable references; prose is untouched.
        lines=[]
        for line in body.splitlines(keepends=True):
            if line.lstrip().startswith('|') and line.rstrip().endswith('|'):
                cells=line.rstrip('\r\n').split('|')
                last=cells[-2].strip()
                names=[x.strip() for x in last.split(',')]
                if names and all(x in sibling for x in names):
                    cells[-2]=' '+', '.join(sibling[x] for x in names)+' '
                    line='|'.join(cells)+'\n'
            lines.append(line)
        body=''.join(lines)
        aliases='\n'.join('- `'+k+'` → `'+v+'` (`../'+v+'/SKILL.md`)' for k,v in sibling.items())
        adapter=(
            '## Unified plugin integration\n\n'
            'Read [the integration contract](../../docs/INTEGRATION.md) when combining workflows. '
            'This active copy retains the complete source instructions below with namespaced skill references. '
            'Original bytes and upstream metadata remain in `../../resources/`. '
            'Resolve tools by their actual host capabilities; tool names in upstream instructions are capability requirements, not proof of connection. '
            'Use the task workspace for generated outputs. Treat historical case-study results as supplied examples, not newly verified findings.\n\n'
            'Family skill aliases (read the linked SKILL.md before use):\n'+aliases+'\n\n---\n\n')
        if sk['name'].startswith('arms-'):
            adapter+='ARMS repository resources: `../../resources/upstream/ARMS-main/`. Shared house style: `../arms-house-style/SKILL.md`. Use `../../docs/ARMS.md` for portable execution and script prerequisites.\n\n'
        if sk['name']=='academic-pptx':
            adapter+='Presentation structure is bundled. For a real PPTX use an available host presentation skill/backend or an installed python-pptx/PptxGenJS runtime; the referenced upstream `pptx` skill is not in the supplied collection. Read `content_guidelines.md` and `slide_patterns.md`. The supplied `LICENSE` is MIT.\n\n'
        # Strict portable frontmatter, preserving all original optional metadata in the inventory.
        frontmatter = parts[1] if sk['name']=='humanizer' else '\n'+yaml.safe_dump({'name':sk['name'],'description':description},sort_keys=False,allow_unicode=True)
        write('skills/'+sk['name']+'/SKILL.md','---'+frontmatter+'---\n\n'+adapter+body)
        catalog.append({'name':sk['name'],'original_name':old_name,'family':sk['label'],
                        'description':description,'path':'skills/'+sk['name']+'/SKILL.md',
                        'source_tree':sk['tree'],'source':sk['rel'].as_posix(),
                        'source_sha256':hashlib.sha256(sk['source'].read_bytes()).hexdigest(),
                        'support_files':[p.relative_to(OUT).as_posix() for p in sorted(dst.rglob('*')) if p.is_file()],
                        'changes':edits,'execution':'instruction-workflow; optional backends described in docs/DEPENDENCIES.md'})
        changes.append({'skill':sk['name'],'changes':edits})
    routes=[{'id':i,'terms':t,'skills':s} for i,t,s in ROUTES]
    dump('catalog/skills.json',catalog)
    dump('catalog/routes.json',routes)
    dump('audit/source-map.json',mappings)
    # Narrow script fixes are applied only to active copies, with hash receipts.
    from adapt_arms import adapt_arms
    from adapt_visuals import adapt_visuals
    component_changes=adapt_arms(OUT)+adapt_visuals(OUT)
    dump('audit/component-adaptations.json',component_changes)
    dump('audit/adaptations.json',changes)
    # Flat CSV is useful for independent completeness review.
    with (OUT/'audit/source-map.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['archive','source','kind','bytes','sha256','destination','disposition','active_destinations','integration_role','integration_reason'])
        writer.writeheader()
        for x in mappings:
            row=dict(x);row['active_destinations']=';'.join(row['active_destinations']);writer.writerow(row)
    counts={label:sum(x['family']==label for x in catalog) for _,label in FAMILIES.values()}
    counts.update({s:sum(x['family']==s for x in catalog) for s in ['academic-humanizer','academic-pptx','humanizer']})
    dump('audit/inventory-summary.json',{'source_files':174,'expanded_archive_files':99,'source_skills':len(catalog),'families':counts,
                                       'mapped_items_including_directories':len(mappings),'mcp_configs_supplied':0})
    write('docs/INVENTORY.md','# Complete component inventory\n\nAll original files and archive members are mapped in [source-map.csv](../audit/source-map.csv) and [source-map.json](../audit/source-map.json). Full text/metadata inspection: [source-inspection.json](../audit/source-inspection.json). Every file has SHA-256; every original directory and explicit archive directory has a preserved destination.\n\n| Family | Active skills |\n|---|---:|\n'+''.join('| '+k+' | '+str(v)+' |\n' for k,v in counts.items())+'\n174 original files, 99 expanded archive files, 117 source skills. Supporting resources include every script, template, reference image, manuscript, PDF, bibliography, dataset, license and hidden plugin/install configuration. Upstream plugin identities are provenance, not active connection registrations.\n\n| Skill | Trigger and purpose |\n|---|---|\n'+''.join('| ['+x['name']+'](../'+x['path']+') | '+x['description'].replace('|','\\|')+' |\n' for x in catalog))
    manifest={'$schema':'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json','name':'academic-research-assistant','version':'1.0.0',
      'description':'Unified academic, scientific and research workflows from the complete supplied collection, with local capability routing and traceable preserved sources.',
      'keywords':['academic','scientific','research','literature','methodology','writing','LaTeX','reproducibility'],
      'extensions':{'com.openai':{'requires_local_executor':True,'onboardingSkill':'./skills/research-assistant/SKILL.md',
        'interface':{'displayName':'Academic Research Assistant','shortDescription':'Academic & scientific research','category':'Education & Research',
          'longDescription':'117 integrated source skills plus unified routing for literature, methods, analysis, research integrity, academic writing, LaTeX, scientific visuals, presentations and publication. Includes all supplied source files, datasets, scripts, examples and provenance. Optional scientific and document runtimes and authenticated services require separate setup; no external service connection is bundled.',
          'capabilities':['Research workflow guidance','Local capability routing','Source preservation and integrity checks'],
          'defaultPrompt':['Help me select and run the research workflow for my task.','Inventory the available capabilities and check local dependencies.','Review my research evidence and prepare a reproducible manuscript workflow.']}}}}
    dump('plugin.json',manifest)
    compat={k:v for k,v in manifest.items() if k not in ['$schema','extensions']}
    compat.update(skills='./skills/',mcpServers='./mcp.json',interface=manifest['extensions']['com.openai']['interface'],requires_local_executor=True)
    dump('.codex-plugin/plugin.json',compat)
    dump('mcp.json',{'$schema':'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json','mcpServers':{'academic-research-local':{
        'type':'stdio','command':'python','args':['-u','${PLUGIN_ROOT}/server/assistant_server.py'],'cwd':'${PLUGIN_ROOT}'}}})
    print(json.dumps({'package':str(OUT),'source_skills':len(catalog),'mapping_entries':len(mappings),'families':counts},indent=2))

if __name__=='__main__':
    main()

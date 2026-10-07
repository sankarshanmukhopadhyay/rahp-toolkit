#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import sys

ROOT = Path(__file__).resolve().parent.parent
SITE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / '_site'

REQUIRED_STRUCTURED_SOURCES = [
    'corpora/dtg-zkp.yaml',
    'corpora/trust-tasks.yaml',
    'corpora/credential-spec.yaml',
    'corpora/trust-tasks-credspec-composed.yaml',
    'corpora/cawg.yaml',
    'instances/cawg/mandate-readiness.yaml',
    'instances/cawg/watch/issues.yaml',
    'instances/dtg/watch/issues.yaml',
    'data/rule-profiles.yaml',
    'data/evidence-artifacts.yaml',
    'method/non-human-actors.yaml',
    'method/schema/delegation-scope.schema.json',
    'method/conformance-claim-template.yaml',
    'method/catalogue/harm-patterns.yaml',
    'method/catalogue/risk-patterns.yaml',
    'method/catalogue/control-patterns.yaml',
    'method/catalogue/guardrail-patterns.yaml',
    'method/catalogue/assurance-patterns.yaml',
    'method/catalogue/evidence-patterns.yaml',
    'examples/a2a/pressure-test.yaml',
    'examples/standalone-trqp/pressure-test.yaml',
    'examples/standalone-trqp/source-manifest.json',
    'examples/standalone-trqp/cases.json',
    'examples/standalone-trqp/expected-replay.json',
    'archive/historical-builds/persona.jsonld',
    'archive/historical-builds/risk.jsonld',
    'archive/historical-builds/control.jsonld',
    'archive/historical-builds/guardrail.jsonld',
    'archive/historical-builds/assurance_test.jsonld',
    'archive/historical-builds/scenario.jsonld',
    'archive/historical-builds/user_story.jsonld',
]

REQUIRED_HUMAN_PROJECTIONS = [
    'examples/standalone-trqp/pressure-test/index.html',
    'examples/standalone-trqp/source-manifest/index.html',
    'examples/standalone-trqp/cases/index.html',
    'examples/standalone-trqp/expected-replay/index.html',
    'corpora/dtg-zkp/index.html',
    'corpora/trust-tasks/index.html',
    'corpora/credential-spec/index.html',
    'corpora/trust-tasks-credspec-composed/index.html',
    'corpora/cawg/index.html',
    'method/catalogue/index.html',
    'method/catalog/index.html',
    'method/catalogue/harm-patterns/index.html',
    'method/catalogue/risk-patterns/index.html',
    'method/catalogue/control-patterns/index.html',
    'method/catalogue/guardrail-patterns/index.html',
    'method/catalogue/assurance-patterns/index.html',
    'method/catalogue/evidence-patterns/index.html',
]

REQUIRED_DOCS = [
    'index.html',
    'docs/using-an-ai-agent.html',
    'docs/pages-coverage.html',
    'docs/normative-triage.html',
    'docs/operational-assurance.html',
    'docs/agent-delegation-governance.html',
    'docs/releases/v0.4.0.html',
    'docs/task-force-actions.html',
    'docs/portability.html',
    'docs/conformance-claims.html',
    'docs/cawg-mandate-readiness.html',
    'docs/cawg-situational-monitoring.html',
    'docs/dtg-situational-monitoring.html',
    'docs/releases/v0.7.0.html',
    'docs/a2a-example.html',
    'docs/personas.html',
    'examples/a2a/index.html',
    'build/site/task-force-actions.html',
    'build/site/portable-catalogue.html',
    'build/site/assurance-graph.html',
    'build/site/catalogue.html',
    'build/site/assurance.html',
    'README.md',
    'QUICKSTART.html',
    'ADOPTION.html',
    'examples/dtg-credential-spec/README.md',
    'examples/security-hardening/credential-spec/SECURITY_REVIEW.md',
    'archive/index.html',
    'archive/legacy-documents/personas.html',
    'archive/legacy-documents/priority-requirements-standards-development.html',
    'archive/legacy-spreadsheets/risk-register-v4.html',
    'archive/legacy-spreadsheets/user-stories-framework-v3.html',
    'archive/historical-builds/index.html',
    'archive/historical-builds/risks.html',
]

# These are user-facing canonical routes. Existence is insufficient: each must
# be wrapped in the Just-the-Docs layout rather than emitted as a bare HTML
# fragment when a Markdown source accidentally omits `layout: default`.
REQUIRED_JTD_SHELL = [
    'examples/index.html',
    'examples/hello-rahp/index.html',
    'examples/standalone-trqp/index.html',
    'docs/a2a-example.html',
    'docs/dtg-instance.html',
    'docs/cawg-risk-register.html',
    'instances/dtg/reviews/README.html',
    'docs/cawg-instance.html',
    'instances/dtg/reviews/2026-08-trust-tasks.html',
    'instances/dtg/reviews/2026-08-verifiable-trust-infrastructure.html',
    'examples/a2a/index.html',
]

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href')
            if href:
                self.links.append(href)

errors = []
htmls = list(SITE.rglob('*.html'))
if not htmls:
    print(f'ERROR {SITE} contains no HTML')
    raise SystemExit(1)

def resolve_site_target(path_text):
    target = SITE / path_text
    candidates = [target]
    # Jekyll may materialize explicit permalinks either exactly, as an HTML
    # sibling, or as an index page depending on the source/output extension.
    candidates.extend([
        Path(str(target) + '.html'),
        target.with_suffix('.html') if target.suffix else target,
        target / 'index.html',
    ])
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return target

for required in REQUIRED_DOCS:
    target = resolve_site_target(required)
    if not target.exists():
        errors.append(f'missing required Pages route: {required}')

for required in REQUIRED_STRUCTURED_SOURCES:
    target = SITE / required
    if not target.exists():
        errors.append(f'missing canonical structured source: {required}')
    else:
        head = target.read_text(errors='ignore')[:1000].lower()
        if '<!doctype html' in head or '<html' in head:
            errors.append(f'canonical structured source was replaced by HTML: {required}')

for required in REQUIRED_HUMAN_PROJECTIONS:
    target = resolve_site_target(required)
    if not target.exists():
        errors.append(f'missing human-readable structured-data projection: {required}')
    else:
        rendered = target.read_text(errors='ignore').lower()
        if '<html' not in rendered or 'id="main-content"' not in rendered:
            errors.append(f'human-readable projection missing Just-the-Docs shell: {required}')

for required in REQUIRED_JTD_SHELL:
    target = resolve_site_target(required)
    if not target.exists():
        errors.append(f'missing required themed Pages route: {required}')
        continue
    rendered = target.read_text(errors='ignore').lower()
    if '<html' not in rendered or 'id="main-content"' not in rendered:
        errors.append(f'Pages route missing Just-the-Docs shell: {required}')

for page in htmls:
    # Historical generated HTML is a frozen provenance artefact. Require its key
    # entry points above, but do not make current deployment depend on repairing
    # every legacy internal link inside the frozen package.
    try:
        rel_page = page.relative_to(SITE).as_posix()
    except ValueError:
        rel_page = str(page)
    if rel_page.startswith('archive/historical-builds/'):
        continue
    p = P()
    p.feed(page.read_text(errors='ignore'))
    for href in p.links:
        if href.startswith(('#', 'mailto:', 'javascript:')):
            continue
        u = urlparse(href)
        if u.scheme or u.netloc:
            continue
        path = unquote(u.path)
        if not path:
            continue
        if path.startswith('/rahp-toolkit/'):
            path = path[len('/rahp-toolkit/'):]
            target = SITE / path
        elif path.startswith('/dtgwg-rahp-tf/'):
            path = path[len('/dtgwg-rahp-tf/'):]  # legacy published prefix
            target = SITE / path
        elif path.startswith('/'):
            continue
        else:
            target = page.parent / path
        if target.is_dir():
            target = target / 'index.html'
        if target.suffix.lower() == '.md':
            html_target = target.with_suffix('.html')
            md_html_target = Path(str(target) + '.html')
            if html_target.exists():
                target = html_target
            elif md_html_target.exists():
                target = md_html_target
        elif target.suffix == '':
            a = target.with_suffix('.html')
            b = target / 'index.html'
            if a.exists():
                target = a
            elif b.exists():
                target = b
        if not target.exists():
            errors.append(f'{page.relative_to(SITE)} -> {href}')

if errors:
    for e in errors[:80]:
        print('ERROR', e)
    print(f'JTD site validation failed: {len(errors)} error(s).')
    raise SystemExit(1)

print(f'JTD site validation clean: {len(htmls)} HTML page(s); canonical structured sources and human projections present.')

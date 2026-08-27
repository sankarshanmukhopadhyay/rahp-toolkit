#!/usr/bin/env python3
"""Render machine-readable RAHP pressure-test YAML into Markdown README blocks.

The pressure-test YAML remains canonical. This tool updates only the content
between the generated markers in each example README, preserving surrounding
human-authored analysis and interpretation.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import sys
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("render_pressure_tests.py requires PyYAML: pip install -r requirements.txt")

ROOT = pathlib.Path(__file__).resolve().parent.parent
BEGIN = "<!-- BEGIN GENERATED PRESSURE TEST -->"
END = "<!-- END GENERATED PRESSURE TEST -->"
CATALOGUE_RELATIVE = "../../build/site/catalogue.html"

def set_catalogue_relative(output_dir: pathlib.Path) -> None:
    """Set the catalogue href relative to the README being rendered.

    Worked reviews live at different directory depths. A fixed ../../ link works
    for examples/a2a but breaks nested CAWG/C2PA compositions on GitHub Pages.
    """
    global CATALOGUE_RELATIVE
    CATALOGUE_RELATIVE = pathlib.Path(
        os.path.relpath(ROOT / "build/site/catalogue.html", output_dir)
    ).as_posix()

REFERENCE_FILES = {
    "risks": "risks.yaml",
    "controls": "controls.yaml",
    "guardrails": "guardrails.yaml",
    "assurance_tests": "assurance-tests.yaml",
    "personas": "personas.yaml",
}


def load_reference_index() -> dict[str, dict[str, str]]:
    index: dict[str, dict[str, str]] = {}
    for kind, filename in REFERENCE_FILES.items():
        paths = [ROOT / "data" / filename, *sorted((ROOT / "instances").glob(f"*/data/{filename}"))]
        for path in paths:
            if not path.exists():
                continue
            doc = load_yaml(path)
            for rec in doc.get("records") or []:
                rid = str(rec.get("id") or "")
                if not rid:
                    continue
                title = rec.get("name") or rec.get("title")
                if not title and kind == "assurance_tests":
                    criterion = str(rec.get("pass_criterion") or "").strip()
                    title = criterion[:90] + ("…" if len(criterion) > 90 else "") if criterion else "Assurance test"
                index[rid] = {"title": str(title or rid), "kind": kind, "href": str(rec.get("link") or "")}
    return index


REFERENCE_INDEX: dict[str, dict[str, str]] = {}


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def md_cell(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, list):
        value = ", ".join(str(v) for v in value)
    text = str(value).replace("\n", " ").strip()
    text = re.sub(r"\s+", " ", text)
    return text.replace("|", "\\|") or "—"


def ref_link(value: Any) -> str:
    rid = md_cell(value)
    rec = REFERENCE_INDEX.get(rid)
    if not rec:
        return f"`{rid}`"
    title = md_cell(rec["title"])
    href = rec.get("href") or f"{CATALOGUE_RELATIVE}#{rid}"
    return f"[{rid} — {title}]({href})"


def ref_list(values: list[Any] | None) -> str:
    if not values:
        return "—"
    return ", ".join(ref_link(v) for v in values)


def code_list(values: list[Any] | None) -> str:
    if not values:
        return "—"
    return ", ".join(f"`{md_cell(v)}`" for v in values)


def disposition(value: Any) -> str:
    if not value:
        return "—"
    return str(value).replace("-", " ").title()


def paragraph(value: Any) -> str:
    text = str(value or "").strip()
    return re.sub(r"\n{3,}", "\n\n", text) or "—"


def render_review(review: dict[str, Any]) -> str:
    target = review.get("target") or {}
    against = review.get("reviewed_against") or {}
    summary = review.get("summary") or {}
    findings = review.get("findings") or []

    lines: list[str] = [
        BEGIN,
        "",
        "## Generated pressure-test record",
        "",
        "> This section is generated from [`pressure-test.yaml`](pressure-test.yaml). Do not edit it by hand. The YAML is the canonical review record; run `python3 tools/render_pressure_tests.py` after changing it.",
        "",
        "### Review metadata",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Review ID | `{md_cell(review.get('id'))}` |",
        f"| Status | {md_cell(review.get('status'))} |",
        f"| Title | {md_cell(review.get('title'))} |",
        f"| Reviewed on | {md_cell(review.get('reviewed_on'))} |",
        f"| Target repository | `{md_cell(target.get('repository'))}` |",
    ]
    if target.get("document"):
        lines.append(f"| Target document | {md_cell(target.get('document'))} |")
    lines += [
        f"| Target version | {md_cell(target.get('version'))} |",
        f"| Target commit | `{md_cell(target.get('commit'))}` |",
        f"| Target source paths | {code_list(target.get('source_paths'))} |",
        f"| RAHP repository | `{md_cell(against.get('repository'))}` |",
        f"| RAHP version | `{md_cell(against.get('rahp_version'))}` |",
        f"| Engine contract | `{md_cell(against.get('engine_contract'))}` |",
        f"| RAHP corpus date | {md_cell(against.get('corpus_date'))} |",
    ]
    if against.get("revalidated_on"):
        lines.append(f"| Engine/method revalidated on | {md_cell(against.get('revalidated_on'))} |")
    if against.get("original_rahp_version"):
        lines.append(f"| Original RAHP version | `{md_cell(against.get('original_rahp_version'))}` |")
    if against.get("revalidation_scope"):
        lines.append(f"| Revalidation scope | {md_cell(against.get('revalidation_scope'))} |")
    lines += [""]

    method = review.get("method") or {}
    if method:
        lines += [
            "### Method",
            "",
            "| Field | Value |",
            "|---|---|",
            f"| Workflow | `{md_cell(method.get('workflow'))}` |",
            f"| Rule | {md_cell(method.get('rule'))} |",
            "",
        ]

    scope = review.get("scope") or {}
    if scope:
        lines += ["### Review scope", ""]
        if scope.get("included"):
            lines += ["**Included**", ""] + [f"- {paragraph(v)}" for v in scope["included"]] + [""]
        if scope.get("excluded"):
            lines += ["**Excluded**", ""] + [f"- {paragraph(v)}" for v in scope["excluded"]] + [""]

    lines += [
        "### Summary",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| Findings | {md_cell(summary.get('finding_count', len(findings)))} |",
        f"| Open findings | {md_cell(summary.get('open_count', sum(1 for f in findings if f.get('status') == 'open')))} |",
    ]
    for key, value in (summary.get("by_primary_disposition") or {}).items():
        lines.append(f"| Primary disposition: {disposition(key)} | {md_cell(value)} |")
    lines += [""]
    if summary.get("overall_assessment"):
        lines += ["**Overall assessment**", "", paragraph(summary["overall_assessment"]), ""]

    lines += [
        "### Finding index",
        "",
        "| ID | Finding | Severity | Status | Primary disposition | RAHP risks |",
        "|---|---|---|---|---|---|",
    ]
    for finding in findings:
        lines.append(
            f"| `{md_cell(finding.get('id'))}` | {md_cell(finding.get('title'))} | "
            f"{md_cell(finding.get('severity'))} | {md_cell(finding.get('status'))} | "
            f"{disposition(finding.get('primary_disposition'))} | {ref_list(finding.get('risks'))} |"
        )
    lines += [""]

    lines += ["### Detailed findings", ""]
    for finding in findings:
        fid = md_cell(finding.get("id"))
        lines += [
            f"#### {fid} — {md_cell(finding.get('title'))}",
            "",
            "| Field | Value |",
            "|---|---|",
            f"| Severity | {md_cell(finding.get('severity'))} |",
            f"| Status | {md_cell(finding.get('status'))} |",
            f"| Primary disposition | {disposition(finding.get('primary_disposition'))} |",
            f"| Secondary dispositions | {', '.join(disposition(v) for v in (finding.get('secondary_dispositions') or [])) or '—'} |",
            f"| Scenarios | {code_list(finding.get('scenarios'))} |",
            f"| Scenario patterns | {code_list(finding.get('scenario_patterns'))} |",
            f"| Personas | {ref_list(finding.get('personas'))} |",
            f"| Risks | {ref_list(finding.get('risks'))} |",
            f"| Controls | {ref_list(finding.get('controls'))} |",
            f"| Guardrails | {ref_list(finding.get('guardrails'))} |",
            f"| Assurance tests | {ref_list(finding.get('assurance_tests'))} |",
            "",
        ]

        portable = finding.get("portable_assurance") or {}
        if portable:
            lines += [
                "**Portable v1.1 assurance patterns**",
                "",
                "| Layer | Patterns |",
                "|---|---|",
                f"| Harms | {code_list(portable.get('harm_patterns'))} |",
                f"| Risks | {code_list(portable.get('risk_patterns'))} |",
                f"| Controls | {code_list(portable.get('control_patterns'))} |",
                f"| Guardrails | {code_list(portable.get('guardrail_patterns'))} |",
                f"| Assurance | {code_list(portable.get('assurance_patterns'))} |",
                f"| Evidence | {code_list(portable.get('evidence_patterns'))} |",
                "",
            ]

        evidence = finding.get("evidence") or []
        if evidence:
            lines += ["**Evidence**", "", "| Source | Observation |", "|---|---|"]
            for ev in evidence:
                lines.append(f"| `{md_cell(ev.get('source'))}` | {md_cell(ev.get('observation'))} |")
            lines += [""]

        related = finding.get("related_work") or []
        if related:
            lines += ["**Related work**", "", "| Reference | Status | Note |", "|---|---|---|"]
            for item in related:
                lines.append(
                    f"| `{md_cell(item.get('reference'))}` | {md_cell(item.get('status'))} | {md_cell(item.get('note'))} |"
                )
            lines += [""]

        lines += [
            "**Potential harm**",
            "",
            paragraph(finding.get("harm")),
            "",
            "**Recommended treatment**",
            "",
            paragraph(finding.get("recommendation")),
            "",
            "**Retest when**",
            "",
        ]
        for trigger in finding.get("retest_when") or []:
            lines.append(f"- {paragraph(trigger)}")
        lines += [""]

    lines += [END, ""]
    return "\n".join(lines)


def expected_readme(yaml_path: pathlib.Path, current: str) -> str:
    review = (load_yaml(yaml_path).get("review") or {})
    rendered = render_review(review).rstrip() + "\n\n"

    if BEGIN in current or END in current:
        if current.count(BEGIN) != 1 or current.count(END) != 1:
            raise ValueError("README must contain exactly one complete generated marker pair")
        pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"[ \t]*\n*", re.S)
        return pattern.sub(rendered, current)

    # Existing examples place the generated record before their human interpretation.
    anchors = ["\n## What the pressure test found", "\n## Positive controls observed", "\n## Reproducing the review"]
    for anchor in anchors:
        idx = current.find(anchor)
        if idx >= 0:
            return current[:idx].rstrip() + "\n\n" + rendered + current[idx:].lstrip("\n")

    return current.rstrip() + "\n\n" + rendered


def process(yaml_path: pathlib.Path, check: bool) -> bool:
    readme = yaml_path.with_name("README.md")
    rel_yaml = yaml_path.relative_to(ROOT)
    if not readme.exists():
        print(f"ERROR {rel_yaml}: sibling README.md is required for rendered pressure-test output")
        return False

    current = readme.read_text(encoding="utf-8")
    set_catalogue_relative(readme.parent)
    try:
        expected = expected_readme(yaml_path, current)
    except ValueError as exc:
        print(f"ERROR {readme.relative_to(ROOT)}: {exc}")
        return False

    if current == expected:
        print(f"[ok] {readme.relative_to(ROOT)}")
        return True

    if check:
        print(f"STALE {readme.relative_to(ROOT)} — run: python3 tools/render_pressure_tests.py")
        return False

    readme.write_text(expected, encoding="utf-8")
    print(f"[updated] {readme.relative_to(ROOT)}")
    return True


def main() -> int:
    global REFERENCE_INDEX
    REFERENCE_INDEX = load_reference_index()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if a README generated block is missing or stale")
    args = parser.parse_args()

    files = sorted(ROOT.glob("examples/**/pressure-test.yaml"))
    if not files:
        print("ERROR no examples/**/pressure-test.yaml files found")
        return 1

    ok = all(process(path, args.check) for path in files)
    if ok:
        action = "current" if args.check else "rendered"
        print(f"Pressure-test Markdown {action}: {len(files)} review file(s).")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

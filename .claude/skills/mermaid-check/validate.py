#!/usr/bin/env python3
"""mermaid-check — Markdown dosyalarındaki ```mermaid``` bloklarını sözdizimsel olarak kontrol eder.

Kullanım:
    python3 validate.py <file.md>
    python3 validate.py --workspace
    python3 validate.py --stdin

Exit code:
    0  tümü geçerli
    1  en az bir hata
    2  kullanım hatası
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

MERMAID_BLOCK = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL | re.MULTILINE)
CODE_FENCE = re.compile(r"^```(\S*)\s*$")

VALID_DIAGRAM_TYPES = {
    "flowchart", "graph", "sequenceDiagram", "classDiagram", "stateDiagram",
    "stateDiagram-v2", "erDiagram", "journey", "gantt", "pie", "gitGraph",
    "mindmap", "timeline", "quadrantChart", "requirementDiagram", "C4Context",
    "C4Container", "C4Component", "C4Dynamic", "sankey-beta", "xychart-beta",
    "block-beta", "packet-beta", "architecture-beta", "kanban", "radar-beta",
}


@dataclass
class Issue:
    file: Path
    line: int
    rule: str
    msg: str
    snippet: str = ""


def find_blocks(text: str):
    """`(line_start, content)` listesi döner. Diğer code fence içindeki mermaid'i atlar."""
    blocks: list[tuple[int, str]] = []
    lines = text.split("\n")
    i = 0
    in_outer = False
    outer_lang = ""
    while i < len(lines):
        ln = lines[i]
        m_fence = CODE_FENCE.match(ln)
        if m_fence:
            lang = m_fence.group(1)
            if not in_outer:
                if lang == "mermaid":
                    # mermaid bloğu başlangıcı
                    start_line = i + 1
                    content_lines: list[str] = []
                    i += 1
                    while i < len(lines) and not CODE_FENCE.match(lines[i]):
                        content_lines.append(lines[i])
                        i += 1
                    blocks.append((start_line, "\n".join(content_lines)))
                    i += 1
                    continue
                else:
                    # başka dilden bir code block — içeride mermaid arama
                    in_outer = True
                    outer_lang = lang
            else:
                # outer bloğun kapanışı
                in_outer = False
                outer_lang = ""
        i += 1
    return blocks


def validate_block(content: str) -> list[tuple[str, str, str]]:
    """`(rule, msg, snippet)` listesi döner — boşsa geçerli."""
    issues: list[tuple[str, str, str]] = []
    lines = [ln for ln in content.splitlines() if ln.strip()]
    if not lines:
        issues.append(("empty", "boş mermaid bloğu", ""))
        return issues

    first = lines[0].strip()
    # İlk kelime diagram tipi olmalı
    diag_word = first.split()[0] if first else ""
    diag_word_clean = diag_word.rstrip(":;")
    if diag_word_clean not in VALID_DIAGRAM_TYPES:
        issues.append(
            ("diagram-type", f"bilinmeyen diagram tipi: '{diag_word_clean}'", first)
        )

    # Eski `graph TD;` uyarısı
    if re.match(r"^graph\s+\w+", first):
        issues.append(("legacy-graph", "modern syntax: 'flowchart TD'", first))

    # Unicode arrow (sequenceDiagram'da participant message metni içinde olabilir; label içinde quote'lu varsa skip)
    for i, ln in enumerate(lines, 1):
        # quote içinde ise atla
        if "→" in ln or "←" in ln or "⇒" in ln:
            # quote içine alınmış kısımları çıkar
            stripped = re.sub(r'"[^"]*"', '', ln)
            stripped = re.sub(r'\[[^\[\]]*\]', '', stripped)
            if "→" in stripped or "←" in stripped or "⇒" in stripped:
                issues.append(("unicode-arrow", "ASCII '-->' kullan veya quote içine al", ln))

    # subgraph / end dengesi (sequenceDiagram alt/loop/par/critical/rect blokları end ile kapanır)
    diag_type = diag_word_clean
    if diag_type.startswith("flowchart") or diag_type.startswith("graph"):
        sg = sum(1 for ln in lines if re.match(r"^\s*subgraph\b", ln))
        en = sum(1 for ln in lines if re.match(r"^\s*end\s*$", ln))
        if sg != en:
            issues.append(
                ("subgraph-end", f"subgraph={sg}, end={en} dengesiz", "")
            )

    # Quote'suz parantez içinde etiket: A[label (1)]  veya  A[label "x"]
    pattern_paren = re.compile(r"\[(?:[^\"\[\]]*\([^)]*\)[^\"\[\]]*)\]")
    for i, ln in enumerate(lines, 1):
        # Tüm quote'lu içerikleri ("...") ve bilinen shape'leri temizle:
        #   [(...)]   → cylinder
        #   [["..."]] → subroutine
        #   [/.../]   → parallelogram
        #   ((...))   → stadium / circle
        cleaned = re.sub(r'"[^"]*"', '""', ln)
        cleaned = re.sub(r'\[\([^)]*\)\]', '[CYL]', cleaned)
        cleaned = re.sub(r'\(\([^)]*\)\)', '((STD))', cleaned)
        cleaned = re.sub(r'\{\{[^}]*\}\}', '{{HEX}}', cleaned)
        if pattern_paren.search(cleaned):
            issues.append(
                ("unquoted-paren", 'parantez içeren etiket quote\'lu olmalı: A["label (1)"]', ln.strip())
            )

    # Türkçe karakter + label içinde quote'suz: A[İşlem]
    tr_chars = set("çğıöşüÇĞİÖŞÜ")
    bracket_label_re = re.compile(r'(?<!\[)\[([^"\[\]]+)\]')
    for ln in lines:
        for match in bracket_label_re.finditer(ln):
            label = match.group(1)
            if any(c in tr_chars for c in label) and not label.startswith('"'):
                # Sadece Türkçe karakter quote'suz ise — uyar (parse genelde geçerlidir ama önerilir)
                pass  # not blocking — mermaid actually accepts UTF-8 in labels

    # Multiline label `\n` quote'suz
    for ln in lines:
        if re.search(r"\[[^\"\[\]]*\\n[^\"\[\]]*\]", ln):
            issues.append(
                ("unquoted-newline", "satır içi label'da \\n için <br/> + quote kullan", ln.strip())
            )

    # Self-referencing classDef olmadan ::: kullanımı (ham heuristic)
    used_classes: set[str] = set()
    defined_classes: set[str] = set()
    for ln in lines:
        for m in re.finditer(r":::(\w+)", ln):
            used_classes.add(m.group(1))
        m = re.match(r"^\s*classDef\s+(\w+)", ln)
        if m:
            defined_classes.add(m.group(1))
    undefined = used_classes - defined_classes
    if undefined:
        issues.append(
            ("missing-classdef", f"tanımsız class: {sorted(undefined)}", "")
        )

    return issues


def check_file(path: Path) -> list[Issue]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return [Issue(path, 0, "io", str(e))]
    issues: list[Issue] = []
    for line, content in find_blocks(text):
        for rule, msg, snippet in validate_block(content):
            issues.append(Issue(path, line, rule, msg, snippet))
    return issues


def check_stdin() -> list[Issue]:
    content = sys.stdin.read()
    out: list[Issue] = []
    for rule, msg, snippet in validate_block(content):
        out.append(Issue(Path("<stdin>"), 1, rule, msg, snippet))
    return out


def find_md_files(root: Path) -> list[Path]:
    out: list[Path] = []
    skip = {"node_modules", ".git", "__pycache__", "temp", ".cache",
            "_deps", "build", "dist", "target", "Clippings", ".obsidian"}
    for p in root.rglob("*.md"):
        if any(part in skip for part in p.parts):
            continue
        out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", help="Tek bir .md dosyası")
    ap.add_argument("--workspace", action="store_true", help="Tüm workspace'i tara")
    ap.add_argument("--stdin", action="store_true", help="stdin'den oku")
    ap.add_argument("--root", default=".", help="Workspace kökü")
    args = ap.parse_args()

    issues: list[Issue] = []
    if args.stdin:
        issues = check_stdin()
    elif args.workspace:
        root = Path(args.root).resolve()
        for f in find_md_files(root):
            issues.extend(check_file(f))
    elif args.file:
        issues = check_file(Path(args.file))
    else:
        ap.print_help()
        return 2

    if not issues:
        print("[mermaid-check] tümü geçerli")
        return 0

    for i in issues:
        snip = f" — \"{i.snippet}\"" if i.snippet else ""
        print(f"[mermaid-check] {i.file}:{i.line} ✗ [{i.rule}] {i.msg}{snip}")
    print(f"[mermaid-check] özet: {len(issues)} hata")
    return 1


if __name__ == "__main__":
    sys.exit(main())

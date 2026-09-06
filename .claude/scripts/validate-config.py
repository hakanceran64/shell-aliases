#!/usr/bin/env python3
# ÜRETİLEN — elle düzenleme. Kaynak: claude-foundation schemas/ + policy/deny-base.json + developer-toolkit yamlite.py; üretici scripts/build-validate-bundle.py (DECISIONS#0047).
# Tek dosya: CI'da ve plugin cache'inde kardeş repolar yoktur.
"""validate-config — .ceran/ecosystem.yaml · .claude/quality.json · settings.json · agent/skill/rule frontmatter
şema doğrulaması. Kullanım: validate-config.py [--project-root P] [--file F ...] [--json] [--quiet]
exit 0 geçerli · 1 hatalı · 3 ortam"""
from __future__ import annotations
import sys as _sys, types as _types

# ---------------------------------------------------------------- yamlite
_m = _types.ModuleType('yamlite'); _m.__file__ = __file__
exec(compile('#!/usr/bin/env python3\n"""scripts/python/yamlite.py — katı YAML alt-kümesi ayrıştırıcısı (stdlib, bağımlılıksız).\n\nNeden var: ekosistem manifest\'leri (.ceran/ecosystem.yaml, registry/*.yaml) YAML\nyazılır ama bu makinede PyYAML yok ve developer-toolkit bilinçli olarak saf-stdlib.\nRuby\'nin psych\'ine shell out etmek de kırılgan (macOS Ruby 2.6 deprecated, CI\'da\nfarklı olabilir).\n\nTasarım ilkesi: PERMISSIF DEĞİL, KATI. Desteklenmeyen bir sözdizimi görürse\nsessizce yanlış ayrıştırmak yerine ParseError fırlatır. Böylece manifest\'ler\n"çalışıyor gibi görünüp yanlış okunmuş" duruma düşemez.\n\nDesteklenen alt küme:\n    - yorum satırları ve satır sonu yorumları (# ...)\n    - iç içe blok map\'ler (2 boşluk girinti)\n    - blok listeler: "- skaler" · "- key: val" (map öğesi)\n    - akış map\'i: { a: 1, b: two }\n    - akış listesi: [a, b, c]\n    - skalerler: çıplak, \'tek\' / "çift" tırnaklı, int, float, true/false, null/~\n    - tırnaklı çok satırlı skaler (kapanış tırnağına kadar devam eder)\n    - belge başı "---" (yok sayılır)\n\nDesteklenmeyen (hata verir):\n    - tab girinti · çapa/alias (&, *) · blok skaler (|, >) · çoklu belge\n    - iç içe akış yapıları ({a: [1,2]}) · karmaşık anahtar (? )\n\nUsage:\n    from yamlite import load, ParseError\n    data = load(open("f.yaml").read())\n\n    python3 yamlite.py <dosya.yaml>     # JSON\'a çevir (doğrulama için)\n    python3 yamlite.py --selftest       # kendi testlerini koştur\n\nExit: 0 ok · 1 parse hatası · 2 usage\n"""\n\nfrom __future__ import annotations\n\nimport json\nimport re\nimport sys\n\n__all__ = ["load", "ParseError"]\n\n\nclass ParseError(Exception):\n    """Ayrıştırma hatası — satır numarasıyla."""\n\n    def __init__(self, line_no: int, msg: str, line: str = "") -> None:\n        detail = f"satır {line_no}: {msg}"\n        if line:\n            detail += f"\\n    {line.rstrip()}"\n        super().__init__(detail)\n        self.line_no = line_no\n\n\n# Blok skalerler (| ve >) mantıksal satır üretiminde toplanır ve bir sentinel ile\n# temsil edilir; gövde burada durur. Tek bir load() çağrısı boyunca geçerlidir.\n# Neden: I-17 — katlanmış skaler yokken 12 skill\'in frontmatter\'ı "desteklenmiyor"\n# diye düşüyordu (T-052 sessiz çökme). Çapa/alias hâlâ desteklenmez.\n_BLOCK_SENTINEL = "\\x00blk:"\n_BLOCKS: list[str] = []\n\n_INT = re.compile(r"^[+-]?\\d+$")\n_FLOAT = re.compile(r"^[+-]?(\\d+\\.\\d*|\\.\\d+)([eE][+-]?\\d+)?$")\n\n\ndef _scalar(raw: str, line_no: int, line: str = ""):\n    """Tırnaksız/tırnaklı skaleri Python değerine çevir."""\n    s = raw.strip()\n    if not s:\n        return ""\n    if s.startswith(_BLOCK_SENTINEL):\n        return _BLOCKS[int(s[len(_BLOCK_SENTINEL):])]\n    if s[0] in "\\"\'":\n        quote = s[0]\n        if len(s) < 2 or s[-1] != quote:\n            raise ParseError(line_no, "kapanmamış tırnak", line)\n        body = s[1:-1]\n        if quote == \'"\':\n            # yalnız yaygın kaçışlar — tam YAML kaçış tablosu değil\n            body = body.replace("\\\\n", "\\n").replace("\\\\t", "\\t").replace(\'\\\\"\', \'"\')\n        return body\n    if s in ("null", "~", "Null", "NULL"):\n        return None\n    if s in ("true", "True", "TRUE", "yes", "on"):\n        return True\n    if s in ("false", "False", "FALSE", "no", "off"):\n        return False\n    if _INT.match(s):\n        return int(s)\n    if _FLOAT.match(s):\n        return float(s)\n    if s[0] in "&*|>":\n        raise ParseError(line_no, f"desteklenmeyen YAML özelliği: \'{s[0]}\'", line)\n    return s\n\n\n_MAX_FLOW_DEPTH = 4\n\n\ndef _split_flow(body: str, line_no: int, line: str) -> list[str]:\n    """Akış içeriğini üst seviye virgüllerden böl.\n\n    Tırnak içindeki virgüller ve iç içe [] / {} içindeki virgüller korunur —\n    böylece `{ a: 1, xs: [x, y] }` doğru bölünür.\n    """\n    parts, buf, quote, depth = [], [], None, 0\n    for ch in body:\n        if quote:\n            buf.append(ch)\n            if ch == quote:\n                quote = None\n            continue\n        if ch in "\\"\'":\n            quote = ch\n            buf.append(ch)\n        elif ch in "[{":\n            depth += 1\n            buf.append(ch)\n        elif ch in "]}":\n            depth -= 1\n            if depth < 0:\n                raise ParseError(line_no, "akışta fazladan kapanış parantezi", line)\n            buf.append(ch)\n        elif ch == "," and depth == 0:\n            parts.append("".join(buf))\n            buf = []\n        else:\n            buf.append(ch)\n    if quote:\n        raise ParseError(line_no, "akış içinde kapanmamış tırnak", line)\n    if depth != 0:\n        raise ParseError(line_no, "akışta kapanmamış parantez", line)\n    if "".join(buf).strip():\n        parts.append("".join(buf))\n    return parts\n\n\ndef _flow(value: str, line_no: int, line: str, depth: int = 0):\n    """{a: 1, b: [x, y]} veya [a, b] → dict/list. Akış değilse None döner."""\n    v = value.strip()\n    if depth > _MAX_FLOW_DEPTH:\n        raise ParseError(line_no, f"akış iç içeliği {_MAX_FLOW_DEPTH} seviyeyi aştı", line)\n\n    def _val(raw: str):\n        nested = _flow(raw, line_no, line, depth + 1)\n        return nested if nested is not None else _scalar(raw, line_no, line)\n\n    if v.startswith("{") and v.endswith("}"):\n        out = {}\n        for part in _split_flow(v[1:-1], line_no, line):\n            if ":" not in part:\n                raise ParseError(line_no, f"akış map\'inde \':\' yok: {part.strip()!r}", line)\n            k, _, val = part.partition(":")\n            out[_scalar(k, line_no, line)] = _val(val)\n        return out\n    if v.startswith("[") and v.endswith("]"):\n        return [_val(p) for p in _split_flow(v[1:-1], line_no, line)]\n    return None\n\n\ndef _strip_comment(line: str) -> str:\n    """Satır sonu yorumunu at; tırnak içindeki # korunur."""\n    quote = None\n    for i, ch in enumerate(line):\n        if quote:\n            if ch == quote:\n                quote = None\n        elif ch in "\\"\'":\n            quote = ch\n        elif ch == "#" and (i == 0 or line[i - 1] in " \\t"):\n            return line[:i]\n    return line\n\n\ndef _fold_block(block: list[str], style: str, chomp: str) -> str:\n    """| → satırlar korunur; > → satırlar boşlukla birleşir, boş satır paragraf sonu."""\n    while block and block[-1] == "":\n        block.pop()\n    if not block:\n        return ""\n    body_indent = min(len(l) - len(l.lstrip()) for l in block if l.strip())\n    lines = [l[body_indent:] if l.strip() else "" for l in block]\n    if style == "|":\n        text = "\\n".join(lines)\n    else:\n        parts: list[str] = []\n        for l in lines:\n            if l == "":\n                parts.append("\\n")\n            elif parts and parts[-1] != "\\n":\n                parts.append(" " + l)\n            else:\n                parts.append(l)\n        text = "".join(parts)\n    if chomp == "-":\n        return text\n    return text + "\\n"\n\n\ndef _logical_lines(text: str) -> list[tuple[int, int, str]]:\n    """(satır_no, girinti, içerik) üret. Tırnaklı çok satırlı skalerleri birleştirir."""\n    out: list[tuple[int, int, str]] = []\n    raw_lines = text.splitlines()\n    i = 0\n    while i < len(raw_lines):\n        raw = raw_lines[i]\n        line_no = i + 1\n        if "\\t" in raw[: len(raw) - len(raw.lstrip())]:\n            raise ParseError(line_no, "tab girinti desteklenmiyor (2 boşluk kullan)", raw)\n        content = _strip_comment(raw).rstrip()\n        if not content.strip() or content.strip() == "---":\n            i += 1\n            continue\n        indent = len(content) - len(content.lstrip())\n        body = content.strip()\n\n        # blok skaler:  key: |   /  key: >   (isteğe bağlı - / + kırpma)\n        mb = re.match(r\'^([^:]+:)\\s*([|>])([-+]?)\\s*$\', body)\n        if mb:\n            style, chomp = mb.group(2), mb.group(3)\n            block: list[str] = []\n            while i + 1 < len(raw_lines):\n                nxt = raw_lines[i + 1]\n                if nxt.strip() == "":\n                    block.append("")\n                    i += 1\n                    continue\n                nxt_indent = len(nxt) - len(nxt.lstrip())\n                if nxt_indent <= indent:\n                    break\n                block.append(nxt)\n                i += 1\n            out.append((line_no, indent, f"{mb.group(1)} {_BLOCK_SENTINEL}{len(_BLOCKS)}"))\n            _BLOCKS.append(_fold_block(block, style, chomp))\n            i += 1\n            continue\n\n        # tırnaklı çok satırlı skaler: açılış tırnağı kapanmamışsa devam et\n        m = re.match(r\'^([^:]+:\\s*)(["\\\'])(.*)$\', body)\n        if m and not _closes(m.group(3), m.group(2)):\n            quote = m.group(2)\n            buf = [body]\n            while i + 1 < len(raw_lines):\n                i += 1\n                nxt = raw_lines[i]\n                buf.append(nxt.strip())\n                if _closes(nxt, quote):\n                    break\n            else:\n                raise ParseError(line_no, "kapanmamış çok satırlı tırnak", raw)\n            body = " ".join(buf)\n\n        # çok satırlı akış: parantezler dengelenene kadar devam et\n        # (ör. uzun bir  repos: [a, b,\\n        c, d]  listesi)\n        elif _flow_depth(body) > 0:\n            buf = [body]\n            depth = _flow_depth(body)\n            while depth > 0 and i + 1 < len(raw_lines):\n                i += 1\n                nxt = _strip_comment(raw_lines[i]).strip()\n                buf.append(nxt)\n                depth += _flow_depth(nxt)\n            if depth != 0:\n                raise ParseError(line_no, "kapanmamış çok satırlı akış", raw)\n            body = " ".join(buf)\n\n        out.append((line_no, indent, body))\n        i += 1\n    return out\n\n\ndef _flow_depth(s: str) -> int:\n    """Satırdaki net parantez dengesi (tırnak içindekiler sayılmaz)."""\n    depth, quote = 0, None\n    for ch in s:\n        if quote:\n            if ch == quote:\n                quote = None\n        elif ch in "\\"\'":\n            quote = ch\n        elif ch in "[{":\n            depth += 1\n        elif ch in "]}":\n            depth -= 1\n    return depth\n\n\ndef _closes(s: str, quote: str) -> bool:\n    """s içinde kapanış tırnağı var mı (kaçışsız)."""\n    esc = False\n    for ch in s:\n        if esc:\n            esc = False\n        elif ch == "\\\\":\n            esc = True\n        elif ch == quote:\n            return True\n    return False\n\n\ndef load(text: str):\n    """YAML alt-kümesini Python veri yapısına çevir."""\n    _BLOCKS.clear()\n    lines = _logical_lines(text)\n    if not lines:\n        return {}\n    value, idx = _parse_block(lines, 0, lines[0][1])\n    if idx != len(lines):\n        ln, _, body = lines[idx]\n        raise ParseError(ln, "beklenmeyen girinti — ayrıştırma buradan devam edemedi", body)\n    return value\n\n\ndef _parse_block(lines, idx: int, indent: int):\n    """indent seviyesindeki bloğu ayrıştır → (değer, sonraki_idx)."""\n    if lines[idx][2].startswith("- "):\n        return _parse_list(lines, idx, indent)\n    return _parse_map(lines, idx, indent)\n\n\ndef _parse_list(lines, idx: int, indent: int):\n    items = []\n    while idx < len(lines):\n        ln, ind, body = lines[idx]\n        if ind < indent:\n            break\n        if ind > indent:\n            raise ParseError(ln, "liste öğesinde beklenmeyen girinti", body)\n        if not body.startswith("- "):\n            break\n        rest = body[2:].strip()\n        idx += 1\n        flow = _flow(rest, ln, body)\n        if flow is not None:\n            items.append(flow)\n            continue\n        if ":" in rest and not rest.startswith(("\'", \'"\')):\n            # "- key: val" → map öğesi; devamı daha derin girintide\n            inner_indent = ind + 2\n            sub = [(ln, inner_indent, rest)]\n            while idx < len(lines) and lines[idx][1] >= inner_indent:\n                sub.append(lines[idx])\n                idx += 1\n            value, used = _parse_map(sub, 0, inner_indent)\n            if used != len(sub):\n                raise ParseError(sub[used][0], "liste öğesi tam ayrıştırılamadı", sub[used][2])\n            items.append(value)\n        else:\n            items.append(_scalar(rest, ln, body))\n    return items, idx\n\n\ndef _parse_map(lines, idx: int, indent: int):\n    out: dict = {}\n    while idx < len(lines):\n        ln, ind, body = lines[idx]\n        if ind < indent:\n            break\n        if ind > indent:\n            raise ParseError(ln, "beklenmeyen girinti (anahtar bekleniyordu)", body)\n        if body.startswith("- "):\n            break\n        if ":" not in body:\n            raise ParseError(ln, "anahtar bulunamadı (\':\' yok)", body)\n        key_raw, _, val_raw = body.partition(":")\n        key = _scalar(key_raw, ln, body)\n        val_raw = val_raw.strip()\n        idx += 1\n\n        if val_raw:\n            flow = _flow(val_raw, ln, body)\n            out[key] = flow if flow is not None else _scalar(val_raw, ln, body)\n            continue\n\n        # değer alt blokta\n        if idx < len(lines) and lines[idx][1] > ind:\n            child_indent = lines[idx][1]\n            out[key], idx = _parse_block(lines, idx, child_indent)\n        elif idx < len(lines) and lines[idx][1] == ind and lines[idx][2].startswith("- "):\n            out[key], idx = _parse_list(lines, idx, ind)  # liste anahtarla aynı hizada\n        else:\n            out[key] = None\n    return out, idx\n\n\n# ---------------------------------------------------------------- selftest\n\n_TESTS = [\n    ("a: 1\\nb: two\\n", {"a": 1, "b": "two"}),\n    ("a:\\n  b: 1\\n  c: 2\\n", {"a": {"b": 1, "c": 2}}),\n    ("xs:\\n  - 1\\n  - 2\\n", {"xs": [1, 2]}),\n    ("xs:\\n- 1\\n- 2\\n", {"xs": [1, 2]}),\n    ("m: { a: 1, b: two }\\n", {"m": {"a": 1, "b": "two"}}),\n    ("l: [a, b, c]\\n", {"l": ["a", "b", "c"]}),\n    ("# yorum\\na: 1  # satır sonu\\n", {"a": 1}),\n    ("a: \'x, y\'\\n", {"a": "x, y"}),\n    (\'a: "he said #hi"\\n\', {"a": "he said #hi"}),\n    ("t: true\\nf: false\\nn: null\\n", {"t": True, "f": False, "n": None}),\n    ("items:\\n  - name: a\\n    v: 1\\n  - name: b\\n    v: 2\\n",\n     {"items": [{"name": "a", "v": 1}, {"name": "b", "v": 2}]}),\n    ("l:\\n  - { name: a, v: 1 }\\n  - { name: b, v: 2 }\\n",\n     {"l": [{"name": "a", "v": 1}, {"name": "b", "v": 2}]}),\n    (\'k: "birinci\\n   ikinci"\\n\', {"k": "birinci ikinci"}),\n    ("deep:\\n  a:\\n    b:\\n      c: 1\\n", {"deep": {"a": {"b": {"c": 1}}}}),\n    ("f: 1.5\\ne: 2.0e3\\n", {"f": 1.5, "e": 2000.0}),\n    # iç içe akış: liste akış map\'i içinde\n    ("m: { a: 1, xs: [x, y] }\\n", {"m": {"a": 1, "xs": ["x", "y"]}}),\n    ("l: [{ a: 1 }, { a: 2 }]\\n", {"l": [{"a": 1}, {"a": 2}]}),\n    ("m: { s: \'a, b\', xs: [1, 2] }\\n", {"m": {"s": "a, b", "xs": [1, 2]}}),\n    # çok satırlı akış (uzun listeler için)\n    ("r: [a, b,\\n    c, d]\\n", {"r": ["a", "b", "c", "d"]}),\n    ("m: { a: 1,\\n     b: 2 }\\n", {"m": {"a": 1, "b": 2}}),\n    # blok skalerler (I-17): katlanmış ve düz, kırpma varyantları, sonrasında anahtar devam eder\n    ("d: >\\n  birinci satır\\n  ikinci satır\\nx: 1\\n", {"d": "birinci satır ikinci satır\\n", "x": 1}),\n    ("d: >-\\n  a\\n  b\\n", {"d": "a b"}),\n    ("d: |\\n  satır 1\\n  satır 2\\n", {"d": "satır 1\\nsatır 2\\n"}),\n    ("d: |-\\n  satır 1\\n    girintili\\n", {"d": "satır 1\\n  girintili"}),\n    ("d: >\\n  p1 a\\n  p1 b\\n\\n  p2\\nk: v\\n", {"d": "p1 a p1 b\\np2\\n", "k": "v"}),\n    ("m:\\n  d: |\\n    iç\\n  e: 2\\n", {"m": {"d": "iç\\n", "e": 2}}),\n]\n\n_FAIL_TESTS = [\n    "a:\\n\\tb: 1\\n",          # tab girinti\n    "a: \'kapanmamis\\n",      # kapanmamış tırnak (tek satır, devam yok)\n    "m: { a: [1, 2 }\\n",     # kapanmamış parantez\n    "a: &anchor\\n",          # çapa\n]\n\n\ndef _selftest() -> int:\n    ok = fail = 0\n    for src, expected in _TESTS:\n        try:\n            got = load(src)\n        except ParseError as e:\n            print(f"  ✗ beklenmeyen hata: {src!r}\\n    {e}")\n            fail += 1\n            continue\n        if got == expected:\n            ok += 1\n        else:\n            print(f"  ✗ {src!r}\\n    beklenen: {expected}\\n    gelen   : {got}")\n            fail += 1\n    for src in _FAIL_TESTS:\n        try:\n            load(src)\n        except ParseError:\n            ok += 1\n        else:\n            print(f"  ✗ hata bekleniyordu ama geçti: {src!r}")\n            fail += 1\n    print(f"yamlite selftest: {ok} geçti, {fail} başarısız")\n    return 1 if fail else 0\n\n\ndef main(argv: list[str]) -> int:\n    if len(argv) != 2:\n        print(__doc__.split("Usage:")[1].strip(), file=sys.stderr)\n        return 2\n    if argv[1] == "--selftest":\n        return _selftest()\n    try:\n        with open(argv[1], encoding="utf-8") as fh:\n            print(json.dumps(load(fh.read()), indent=2, ensure_ascii=False))\n    except ParseError as e:\n        print(f"yamlite: {argv[1]}\\n{e}", file=sys.stderr)\n        return 1\n    except OSError as e:\n        print(f"yamlite: {e}", file=sys.stderr)\n        return 1\n    return 0\n\n\n', 'yamlite', 'exec'), _m.__dict__)
_sys.modules['yamlite'] = _m

# ---------------------------------------------------------------- validate
_m = _types.ModuleType('validate'); _m.__file__ = __file__
exec(compile('#!/usr/bin/env python3\n"""schemas/validate.py — bağımlılıksız JSON Schema doğrulayıcı (draft 2020-12 alt kümesi).\n\nNeden kendi doğrulayıcımız var: ekosistemin hiçbir aracı stdlib dışına çıkmaz (yamlite,\nceran-hooks, pulse). `jsonschema` paketi 53 üyenin CI\'ında ve her cihazda kurulu olmak\nzorunda kalırdı. Şema dosyaları yine GERÇEK JSON Schema\'dır — başka araçlar da okuyabilir;\nyalnız doğrulayıcı bizim.\n\nDesteklenen anahtar sözcükler (şemalarımız bunun dışına çıkmaz; test bunu doğrular):\n    type (tek ya da liste) · properties · required · additionalProperties (bool | şema)\n    patternProperties · enum · const · pattern · minLength · maxLength · minimum · maximum\n    minItems · maxItems · uniqueItems · items · anyOf · oneOf · allOf · not\n    $ref (yalnız yerel "#/..." JSON pointer) · $defs / definitions\nTanınmayan bir anahtar sözcük SESSİZCE geçilmez: `unsupported_keywords()` raporlar ve\nşema testi bunu kırar — "desteklenmeyen kural yazıldı sanıldı" hatası olmasın.\n\nKullanım (modül):\n    errors = validate(instance, schema)      # [] = geçerli; aksi halde "yol: mesaj" listesi\nKullanım (CLI):\n    validate.py --schema S.json DOSYA.json   # exit 0 geçerli · 1 hatalı · 2 kullanım\n"""\nfrom __future__ import annotations\n\nimport json\nimport re\nimport sys\nfrom pathlib import Path\n\nSUPPORTED = {\n    "$schema", "$id", "$defs", "definitions", "$comment", "title", "description", "examples",\n    "default", "type", "properties", "required", "additionalProperties", "patternProperties",\n    "enum", "const", "pattern", "minLength", "maxLength", "minimum", "maximum", "minItems",\n    "maxItems", "uniqueItems", "items", "anyOf", "oneOf", "allOf", "not", "$ref", "format",\n}\n\n_TYPE_CHECKS = {\n    "object": lambda v: isinstance(v, dict),\n    "array": lambda v: isinstance(v, list),\n    "string": lambda v: isinstance(v, str),\n    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),\n    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),\n    "boolean": lambda v: isinstance(v, bool),\n    "null": lambda v: v is None,\n}\n\n\nclass SchemaError(Exception):\n    """Şemanın kendisi bozuk (çözülemeyen $ref, bilinmeyen tip)."""\n\n\ndef _resolve_ref(ref: str, root: dict) -> dict:\n    if not ref.startswith("#"):\n        raise SchemaError(f"yalnız yerel $ref desteklenir: {ref}")\n    node = root\n    for raw in ref[1:].split("/"):\n        if raw == "":\n            continue\n        key = raw.replace("~1", "/").replace("~0", "~")\n        if isinstance(node, list):\n            node = node[int(key)]\n        elif isinstance(node, dict) and key in node:\n            node = node[key]\n        else:\n            raise SchemaError(f"$ref çözülemedi: {ref}")\n    if not isinstance(node, (dict, bool)):\n        raise SchemaError(f"$ref şema değil: {ref}")\n    return node\n\n\ndef _type_ok(value, expected) -> bool:\n    names = expected if isinstance(expected, list) else [expected]\n    for name in names:\n        check = _TYPE_CHECKS.get(name)\n        if check is None:\n            raise SchemaError(f"bilinmeyen tip: {name}")\n        if check(value):\n            return True\n    return False\n\n\ndef _fmt(value) -> str:\n    text = json.dumps(value, ensure_ascii=False)\n    return text if len(text) <= 60 else text[:57] + "..."\n\n\ndef _validate(value, schema, root: dict, path: str, out: list[str]) -> None:\n    if schema is True:\n        return\n    if schema is False:\n        out.append(f"{path}: hiçbir değer kabul edilmez")\n        return\n    if "$ref" in schema:\n        _validate(value, _resolve_ref(schema["$ref"], root), root, path, out)\n        return\n\n    if "type" in schema and not _type_ok(value, schema["type"]):\n        out.append(f"{path}: tip {schema[\'type\']} bekleniyor, gelen {_fmt(value)}")\n        return\n    if "const" in schema and value != schema["const"]:\n        out.append(f"{path}: yalnız {_fmt(schema[\'const\'])} olabilir, gelen {_fmt(value)}")\n    if "enum" in schema and value not in schema["enum"]:\n        out.append(f"{path}: {_fmt(value)} izinli değil (izinli: {\', \'.join(_fmt(e) for e in schema[\'enum\'])})")\n\n    if isinstance(value, str):\n        if "pattern" in schema and not re.search(schema["pattern"], value):\n            out.append(f"{path}: {_fmt(value)} desene uymuyor ({schema[\'pattern\']})")\n        if "minLength" in schema and len(value) < schema["minLength"]:\n            out.append(f"{path}: en az {schema[\'minLength\']} karakter")\n        if "maxLength" in schema and len(value) > schema["maxLength"]:\n            out.append(f"{path}: en çok {schema[\'maxLength\']} karakter")\n\n    if isinstance(value, (int, float)) and not isinstance(value, bool):\n        if "minimum" in schema and value < schema["minimum"]:\n            out.append(f"{path}: en az {schema[\'minimum\']}")\n        if "maximum" in schema and value > schema["maximum"]:\n            out.append(f"{path}: en çok {schema[\'maximum\']}")\n\n    if isinstance(value, list):\n        if "minItems" in schema and len(value) < schema["minItems"]:\n            out.append(f"{path}: en az {schema[\'minItems\']} öğe")\n        if "maxItems" in schema and len(value) > schema["maxItems"]:\n            out.append(f"{path}: en çok {schema[\'maxItems\']} öğe")\n        if schema.get("uniqueItems"):\n            seen = []\n            for item in value:\n                if item in seen:\n                    out.append(f"{path}: yinelenen öğe {_fmt(item)}")\n                    break\n                seen.append(item)\n        if "items" in schema:\n            for i, item in enumerate(value):\n                _validate(item, schema["items"], root, f"{path}[{i}]", out)\n\n    if isinstance(value, dict):\n        props = schema.get("properties", {})\n        for key in schema.get("required", []):\n            if key not in value:\n                out.append(f"{path}: zorunlu alan eksik: {key}")\n        pattern_props = schema.get("patternProperties", {})\n        for key, item in value.items():\n            child = f"{path}.{key}" if path else key\n            matched = False\n            if key in props:\n                matched = True\n                _validate(item, props[key], root, child, out)\n            for pat, sub in pattern_props.items():\n                if re.search(pat, key):\n                    matched = True\n                    _validate(item, sub, root, child, out)\n            if not matched and "additionalProperties" in schema:\n                extra = schema["additionalProperties"]\n                if extra is False:\n                    out.append(f"{child}: tanınmayan alan")\n                elif extra is not True:\n                    _validate(item, extra, root, child, out)\n\n    for combinator in ("allOf", "anyOf", "oneOf"):\n        if combinator not in schema:\n            continue\n        results = []\n        for sub in schema[combinator]:\n            sub_out: list[str] = []\n            _validate(value, sub, root, path, sub_out)\n            results.append(sub_out)\n        passed = sum(1 for r in results if not r)\n        if combinator == "allOf" and passed != len(results):\n            for r in results:\n                out.extend(r)\n        elif combinator == "anyOf" and passed == 0:\n            out.append(f"{path}: alternatiflerin hiçbiri uymadı — " + " | ".join(r[0] for r in results if r))\n        elif combinator == "oneOf" and passed != 1:\n            out.append(f"{path}: alternatiflerden tam biri uymalı ({passed} uydu)")\n    if "not" in schema:\n        sub_out: list[str] = []\n        _validate(value, schema["not"], root, path, sub_out)\n        if not sub_out:\n            out.append(f"{path}: yasaklı biçim")\n\n\ndef validate(instance, schema: dict) -> list[str]:\n    """Hata listesi döner; boş liste = geçerli. Yol biçimi: a.b[2].c"""\n    errors: list[str] = []\n    _validate(instance, schema, schema, "", errors)\n    return errors\n\n\ndef unsupported_keywords(schema, found: set[str] | None = None) -> set[str]:\n    """Şemada bu doğrulayıcının TANIMADIĞI anahtar sözcükler (şema testi için)."""\n    found = set() if found is None else found\n    if isinstance(schema, dict):\n        for key, value in schema.items():\n            if key in ("properties", "patternProperties", "$defs", "definitions"):\n                for sub in value.values():\n                    unsupported_keywords(sub, found)\n                continue\n            if key not in SUPPORTED:\n                found.add(key)\n            if key in ("items", "additionalProperties", "not"):\n                unsupported_keywords(value, found)\n            elif key in ("anyOf", "oneOf", "allOf"):\n                for sub in value:\n                    unsupported_keywords(sub, found)\n    return found\n\n\ndef load_json(path: Path):\n    with path.open(encoding="utf-8") as fh:\n        return json.load(fh)\n\n\ndef main(argv: list[str]) -> int:\n    if len(argv) < 4 or argv[1] != "--schema":\n        print(__doc__.strip().splitlines()[-1], file=sys.stderr)\n        return 2\n    schema = load_json(Path(argv[2]))\n    rc = 0\n    for name in argv[3:]:\n        errors = validate(load_json(Path(name)), schema)\n        if errors:\n            rc = 1\n            print(f"✗ {name}")\n            for e in errors:\n                print(f"    {e}")\n        else:\n            print(f"✓ {name}")\n    return rc\n\n\n', 'validate', 'exec'), _m.__dict__)
_sys.modules['validate'] = _m

# ---------------------------------------------------------------- config_validate
#!/usr/bin/env python3
"""schemas/config_validate.py — bir projenin ekosistem yapılandırmasını şemalara karşı doğrular.

Dosyalar (varsa):
    .ceran/ecosystem.yaml            → ecosystem.schema.json
    .claude/quality.json             → quality.schema.json
    .claude/settings.json            → geçerli JSON + deny tabanı eksiksiz (policy/deny-base.json)
    .claude/agents/*.md              → frontmatter.schema.json#/$defs/agent
    .claude/skills/*/SKILL.md        → frontmatter.schema.json#/$defs/skill
    .claude/rules/*.md               → frontmatter.schema.json#/$defs/rule (yalnız frontmatter TAŞIYORSA)

Üç yerden çağrılır ve üçü aynı kodu koşar (DECISIONS#0047):
    dev eco validate                 toolkit — bu modülü foundation'dan import eder
    .claude/scripts/validate-config.py   kit (K3) — scripts/build-validate-bundle.py ile üretilen TEK DOSYA
                                     (yamlite + validate.py + bu modül + şemalar gömülü); CI ve verify.sh
    ceran-core plugin config-validate hook'u   aynı paket, plugin içinde

Şema ve yamlite çözümleme sırası: gömülü (paket) → CERAN_SCHEMAS_DIR / DEVELOPER_TOOLKIT_ROOT →
kardeş repolar (../../developer-toolkit). Bulunamazsa açık hata; sessiz geçiş yok.

CLI:
    config_validate.py [--project-root P] [--file F ...] [--json] [--quiet]
    exit 0 geçerli · 1 hatalı · 3 ortam (şema/parser yok)
"""

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EMBEDDED_SCHEMAS: dict[str, dict] = json.loads('{"ecosystem": {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://github.com/hakanceran64/claude-foundation/schemas/ecosystem.schema.json", "title": ".ceran/ecosystem.yaml", "description": "Üye manifesti: proje ekosistemden ne tüketir (developer-toolkit eco.py okur). apiVersion ceran/v2 `plugins:` bölümünü açar (DECISIONS#0046); şema Faz 3\'te geldi (DECISIONS#0047).", "type": "object", "required": ["apiVersion", "project", "consume"], "additionalProperties": false, "properties": {"apiVersion": {"enum": ["ceran/v1", "ceran/v2"]}, "project": {"type": "object", "required": ["name", "profiles"], "additionalProperties": false, "properties": {"name": {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"}, "profiles": {"type": "array", "minItems": 1, "uniqueItems": true, "items": {"type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$"}}}}, "consume": {"type": "object", "description": "Yalnız dört bileşen (eco.py COMPONENTS). Her biri bir mode beyan eder.", "additionalProperties": false, "properties": {"ai-foundation": {"type": "object", "required": ["mode"], "additionalProperties": false, "properties": {"mode": {"const": "vendor"}, "version": {"$ref": "#/$defs/semverTag"}, "local": {"type": "array", "description": ".claude\'a göreli, projenin BİLİNÇLİ sahiplendiği yollar — sync dokunmaz.", "uniqueItems": true, "items": {"$ref": "#/$defs/relativePath"}}}}, "wiki": {"type": "object", "required": ["mode"], "additionalProperties": false, "properties": {"mode": {"const": "link"}}}, "design-system": {"type": "object", "required": ["mode", "into"], "additionalProperties": false, "description": "İki biçim: preset (kompozisyon adı) YA DA brand + targets — ikisi birlikte yazılamaz (ADR-0016).", "properties": {"mode": {"const": "vendor"}, "version": {"$ref": "#/$defs/semverTag"}, "preset": {"type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$"}, "brand": {"type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$"}, "targets": {"type": "array", "minItems": 1, "uniqueItems": true, "items": {"type": "string"}}, "into": {"$ref": "#/$defs/relativePath"}, "local": {"type": "array", "description": "`into` altında projenin sahiplendiği dosyalar (ad çakışması — eco.py vendor sync dokunmaz)", "uniqueItems": true, "items": {"$ref": "#/$defs/relativePath"}}}, "anyOf": [{"required": ["preset"]}, {"required": ["brand", "targets"]}], "not": {"required": ["preset", "brand"]}}, "shared-modules": {"type": "object", "required": ["mode", "packages"], "additionalProperties": false, "properties": {"mode": {"const": "dependency"}, "packages": {"type": "array", "items": {"type": "object", "required": ["name", "version"], "additionalProperties": false, "properties": {"name": {"type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$"}, "version": {"type": "string", "minLength": 1}}}}}}}}, "plugins": {"type": "object", "description": "Yalnız apiVersion ceran/v2 (eco.py ayrıca zorlar).", "additionalProperties": false, "properties": {"enable": {"type": "array", "uniqueItems": true, "items": {"$ref": "#/$defs/pluginName"}}, "disable": {"type": "array", "uniqueItems": true, "items": {"$ref": "#/$defs/pluginName"}}}}}, "$defs": {"semverTag": {"type": "string", "pattern": "^v[0-9]+\\\\.[0-9]+\\\\.[0-9]+$"}, "relativePath": {"type": "string", "pattern": "^(?!/)(?!.*(^|/)\\\\.\\\\.(/|$)).+$", "description": "göreli yol; mutlak ya da .. içeren yol kabul edilmez"}, "pluginName": {"type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$"}}}, "quality": {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://github.com/hakanceran64/claude-foundation/schemas/quality.schema.json", "title": ".claude/quality.json", "description": "Kalite kapısı sözleşmesi (DECISIONS#0026): verify{} repo-geneli (verify.sh · CI), on_edit[] tek dosya (format-lint hook\'u, {file} yer tutucu). Boş komut = atlanır. `_` ile başlayan anahtarlar serbest nottur.", "type": "object", "required": ["verify"], "additionalProperties": false, "patternProperties": {"^_": {}}, "properties": {"profile": {"type": "string"}, "verify": {"type": "object", "additionalProperties": false, "properties": {"format": {"type": "string"}, "lint": {"type": "string"}, "typecheck": {"type": "string"}, "test": {"type": "string"}}}, "on_edit": {"type": "array", "items": {"type": "object", "required": ["match"], "additionalProperties": false, "properties": {"match": {"type": "string", "minLength": 1}, "format": {"type": "string"}, "lint": {"type": "string"}}}}}}, "frontmatter": {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://github.com/hakanceran64/claude-foundation/schemas/frontmatter.schema.json", "title": "Claude Code frontmatter (agent · skill · rule)", "description": "Doğrulayıcı dosya yoluna göre $defs/agent, $defs/skill ya da $defs/rule seçer. Claude Code\'un kendi alanları ek alan olarak serbesttir (additionalProperties: true) — ekosistemin zorladığı yalnız kimlik alanları ve biçimleridir. Model allowlist\'i burada değil check-models.sh / model-guard\'dadır (tek tanım: policy/models.yaml).", "$defs": {"identifier": {"type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$"}, "text": {"type": "string", "minLength": 8}, "toolList": {"description": "Virgüllü tek satır (Read, Bash(git log:*)) ya da liste", "anyOf": [{"type": "string", "minLength": 1}, {"type": "array", "minItems": 1, "items": {"type": "string"}}]}, "agent": {"type": "object", "required": ["name", "description"], "properties": {"name": {"$ref": "#/$defs/identifier"}, "description": {"$ref": "#/$defs/text"}, "tools": {"$ref": "#/$defs/toolList"}, "model": {"type": "string", "minLength": 1}, "color": {"type": "string"}, "permissionMode": {"type": "string"}, "maxTurns": {"type": "integer", "minimum": 1}}}, "skill": {"type": "object", "required": ["name", "description"], "properties": {"name": {"$ref": "#/$defs/identifier"}, "description": {"$ref": "#/$defs/text"}, "when_to_use": {"type": "string"}, "argument-hint": {"description": "Claude Code metin bekler; `[go|python]` gibi köşeli biçim YAML\'da liste olarak okunur, ikisi de kabul", "anyOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]}, "allowed-tools": {"$ref": "#/$defs/toolList"}, "disable-model-invocation": {"type": "boolean"}, "user-invocable": {"type": "boolean"}, "model": {"type": "string", "minLength": 1}}}, "rule": {"type": "object", "description": "Kurallar frontmatter taşımak zorunda değildir; taşıyorsa alanlar biçime uyar (Claude Code `paths:` dahil). K1 kuralları enforced-by + layer taşır.", "properties": {"description": {"$ref": "#/$defs/text"}, "enforced-by": {"enum": ["advisory", "hook", "managed", "ci"]}, "layer": {"type": "string"}, "paths": {"type": "array", "items": {"type": "string"}}}}}, "anyOf": [{"$ref": "#/$defs/agent"}, {"$ref": "#/$defs/skill"}, {"$ref": "#/$defs/rule"}]}, "deny-base": {"$comment": "permissions.deny TABANI — tek kaynak. kit/.claude/settings.json ve managed şablon bunu içerir (test doğrular); proje genişletebilir, daraltamaz (04-izinler).", "deny": ["Bash(rm -rf /:*)", "Bash(rm -rf /*:*)", "Bash(rm -rf ~:*)", "Bash(rm -rf $HOME:*)", "Bash(sudo rm:*)", "Bash(sudo:*)", "Bash(git push --force:*)", "Bash(git push -f:*)", "Bash(git push origin --force:*)", "Bash(git push origin -f:*)", "Bash(git reset --hard origin:*)", "Bash(git filter-repo:*)", "Bash(git filter-branch:*)", "Bash(dd if=:*)", "Bash(mkfs:*)", "Bash(curl * | sh:*)", "Bash(curl * | bash:*)", "Bash(wget * | sh:*)", "Bash(wget * | bash:*)", "Read(.env)", "Read(.env.*)", "Read(**/.env)", "Read(**/.env.*)", "Read(**/id_rsa*)", "Read(**/*.pem)", "Read(**/credentials*)"]}}')
_yamlite = None
_validate = None


def _import_file(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _candidates_toolkit() -> list[Path]:
    out = []
    tk = os.environ.get("DEVELOPER_TOOLKIT_ROOT")
    if tk:
        out.append(Path(tk) / "scripts" / "python" / "yamlite.py")
    eco = os.environ.get("CERAN_ECOSYSTEM_ROOT")
    if eco:
        out.append(Path(eco) / "core" / "developer-toolkit" / "scripts" / "python" / "yamlite.py")
    out.append(HERE.parent.parent / "developer-toolkit" / "scripts" / "python" / "yamlite.py")
    return out


def yamlite():
    global _yamlite
    if _yamlite is not None:
        return _yamlite
    if "yamlite" in sys.modules:
        _yamlite = sys.modules["yamlite"]
        return _yamlite
    for p in _candidates_toolkit():
        if p.is_file():
            _yamlite = _import_file("yamlite", p)
            return _yamlite
    raise EnvironmentError("yamlite bulunamadı — DEVELOPER_TOOLKIT_ROOT ya da CERAN_ECOSYSTEM_ROOT ayarla")


def validator():
    global _validate
    if _validate is not None:
        return _validate
    if "validate" in sys.modules and hasattr(sys.modules["validate"], "validate"):
        _validate = sys.modules["validate"]
        return _validate
    local = HERE / "validate.py"
    if local.is_file():
        _validate = _import_file("validate", local)
        return _validate
    raise EnvironmentError("schemas/validate.py bulunamadı")


def schema(name: str) -> dict:
    if name in EMBEDDED_SCHEMAS:
        return EMBEDDED_SCHEMAS[name]
    for d in (os.environ.get("CERAN_SCHEMAS_DIR"), str(HERE)):
        if d and (Path(d) / f"{name}.schema.json").is_file():
            return json.loads((Path(d) / f"{name}.schema.json").read_text(encoding="utf-8"))
    raise EnvironmentError(f"şema yok: {name}.schema.json")


def deny_base() -> list[str]:
    if "deny-base" in EMBEDDED_SCHEMAS:
        return list(EMBEDDED_SCHEMAS["deny-base"]["deny"])
    p = HERE.parent / "policy" / "deny-base.json"
    if p.is_file():
        return list(json.loads(p.read_text(encoding="utf-8"))["deny"])
    return []


# ---------------------------------------------------------------- ayrıştırıcılar

def frontmatter(text: str) -> dict | None:
    """`---` ile açılan ilk bloğu YAML olarak verir; frontmatter yoksa None."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    body = []
    for line in lines[1:]:
        if line.strip() == "---":
            data = yamlite().load("\n".join(body)) if body else {}
            return data if isinstance(data, dict) else {"_": data}
        body.append(line)
    return None   # kapanmamış blok — frontmatter değil


def _kind_of(path: Path) -> str | None:
    parts = path.as_posix().split("/")
    if ".claude" not in parts:
        return None
    rel = parts[len(parts) - 1 - parts[::-1].index(".claude"):]
    if rel[-1] == "ecosystem.yaml":
        return None
    if len(rel) >= 2 and rel[1] == "quality.json":
        return "quality"
    if len(rel) >= 2 and rel[1] == "settings.json":
        return "settings"
    if len(rel) == 3 and rel[1] == "agents" and rel[2].endswith(".md") and rel[2] != "README.md":
        return "agent"
    if len(rel) == 4 and rel[1] == "skills" and rel[3] == "SKILL.md":
        return "skill"
    if len(rel) == 3 and rel[1] == "rules" and rel[2].endswith(".md") and rel[2] != "README.md":
        return "rule"
    return None


def kind_of(path: Path) -> str | None:
    if path.name == "ecosystem.yaml" and path.parent.name == ".ceran":
        return "ecosystem"
    return _kind_of(path)


# ---------------------------------------------------------------- doğrulama

def check_file(path: Path, kind: str | None = None) -> list[str]:
    """Tek dosya → hata listesi (boş = geçerli). Bilinmeyen tür → []."""
    kind = kind or kind_of(path)
    if kind is None:
        return []
    v = validator()
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return [f"okunamadı: {e}"]

    if kind == "ecosystem":
        try:
            data = yamlite().load(text)
        except yamlite().ParseError as e:
            return [f"YAML ayrıştırılamadı: {e}"]
        return v.validate(data, schema("ecosystem"))

    if kind in ("quality", "settings"):
        try:
            data = json.loads(text)
        except ValueError as e:
            return [f"JSON ayrıştırılamadı: {e}"]
        if kind == "quality":
            return v.validate(data, schema("quality"))
        errors = []
        if not isinstance(data, dict):
            return ["üst düzey bir nesne olmalı"]
        deny = ((data.get("permissions") or {}).get("deny") or []) if isinstance(data.get("permissions"), dict) else []
        missing = [d for d in deny_base() if d not in deny]
        if missing:
            errors.append(f"permissions.deny tabanı eksik ({len(missing)}): " + ", ".join(missing[:4])
                          + (" …" if len(missing) > 4 else ""))
        for key, val in (data.get("enabledPlugins") or {}).items():
            if not isinstance(val, bool):
                errors.append(f"enabledPlugins.{key}: boolean olmalı")
        hooks = data.get("hooks")
        if hooks is not None and not isinstance(hooks, dict):
            errors.append("hooks: nesne olmalı (olay → liste)")
        return errors

    # agent · skill · rule
    try:
        fm = frontmatter(text)
    except yamlite().ParseError as e:
        return [f"frontmatter ayrıştırılamadı: {e}"]
    if fm is None:
        return [] if kind == "rule" else ["frontmatter yok (--- name/description ---)"]
    root = schema("frontmatter")
    wrapper = {"$ref": f"#/$defs/{kind}", "$defs": root["$defs"]}
    return v.validate(fm, wrapper)


def project_files(root: Path) -> list[Path]:
    files = []
    for rel in (".ceran/ecosystem.yaml", ".claude/quality.json", ".claude/settings.json"):
        if (root / rel).is_file():
            files.append(root / rel)
    files += sorted((root / ".claude" / "agents").glob("*.md"))
    files += sorted((root / ".claude" / "skills").glob("*/SKILL.md"))
    files += sorted((root / ".claude" / "rules").glob("*.md"))
    return [f for f in files if f.name != "README.md"]


def check_project(root: Path, files: list[Path] | None = None) -> dict[str, list[str]]:
    """{göreli yol: hatalar} — yalnız hatalı dosyalar."""
    out: dict[str, list[str]] = {}
    for f in (files or project_files(root)):
        errors = check_file(f)
        if errors:
            try:
                key = f.resolve().relative_to(root.resolve()).as_posix()
            except ValueError:
                key = str(f)
            out[key] = errors
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="validate-config", description=__doc__.splitlines()[0])
    ap.add_argument("--project-root", default=os.environ.get("CLAUDE_PROJECT_DIR") or ".")
    ap.add_argument("--file", action="append", help="yalnız bu dosya(lar) (hook kullanımı)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv[1:])
    root = Path(args.project_root).resolve()
    try:
        files = [Path(f).resolve() for f in args.file] if args.file else None
        if files is not None:
            files = [f for f in files if kind_of(f)]
            if not files:
                return 0
        result = check_project(root, files)
    except EnvironmentError as e:
        print(f"validate-config: {e}", file=sys.stderr)
        return 3
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result else 0
    if result:
        for rel, errors in result.items():
            print(f"✗ {rel}")
            for e in errors:
                print(f"    {e}")
        print(f"validate-config: {len(result)} dosya şemaya uymuyor", file=sys.stderr)
        return 1
    if not args.quiet:
        n = len(files) if files is not None else len(project_files(root))
        print(f"✓ yapılandırma şemalara uygun ({n} dosya)")
    return 0




if __name__ == "__main__":
    sys.exit(main(sys.argv))

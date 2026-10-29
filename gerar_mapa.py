#!/usr/bin/env python3
"""Varre as habilidades instaladas no Claude Code e gera habilidades.json.

Fontes: ~/.claude/skills/*/SKILL.md (minhas), ~/.claude/plugins/cache/*/*/*/skills/*/SKILL.md
(plugins), extras.json (embutidas do Claude Code, que nao ficam em disco). As explicacoes em
portugues vem de traducoes.json; sem traducao, fica a description original.
Uso: python3 gerar_mapa.py [--publico]   (--publico deixa de fora as de privadas.txt)
"""
import json, os, re, sys, glob
aqui = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
publico = "--publico" in sys.argv
tr = json.load(open(os.path.join(aqui, "traducoes.json"), encoding="utf-8"))
priv = set(l.strip() for l in open(os.path.join(aqui, "privadas.txt"), encoding="utf-8") if l.strip()) if os.path.exists(os.path.join(aqui, "privadas.txt")) else set()

def frontmatter(path):
    try:
        txt = open(path, encoding="utf-8").read()
    except Exception:
        return {}
    m = re.match(r"^---\s*\n(.*?)\n---", txt, re.S)
    if not m:
        return {}
    fm, campos, chave = m.group(1), {}, None
    for l in fm.splitlines():
        mm = re.match(r"^([A-Za-z_-]+):\s*(.*)$", l)
        if mm:
            chave = mm.group(1); campos[chave] = mm.group(2).strip().strip('"').strip("'")
            if campos[chave] in (">-", ">", "|", "|-"): campos[chave] = ""
        elif chave and l.startswith(" "):
            campos[chave] = (campos[chave] + " " + l.strip()).strip()
    return campos

itens = []
def add(nome, pacote, desc):
    if publico and nome in priv:
        return
    t = tr.get(nome) or tr.get(nome.split(":")[-1]) or {}
    itens.append({"nome": nome, "pacote": pacote, "categoria": t.get("categoria", "Outro"),
                  "pt": t.get("pt") or desc, "en": desc})

for f in sorted(glob.glob(os.path.join(home, ".claude", "skills", "*", "SKILL.md"))):
    fm = frontmatter(f); n = fm.get("name") or os.path.basename(os.path.dirname(f))
    if os.path.basename(os.path.dirname(f)) in ("synced", "learned"): continue
    add(n, "minhas", fm.get("description", ""))
for f in sorted(glob.glob(os.path.join(home, ".claude", "skills", "synced", "*", "*", "SKILL.md"))):
    fm = frontmatter(f); n = "anthropic-skills:" + (fm.get("name") or os.path.basename(os.path.dirname(f)))
    if any(i["nome"] == n for i in itens): continue
    add(n, "claude-code", fm.get("description", ""))
cache = os.path.join(home, ".claude", "plugins", "cache")
for raiz in sorted(glob.glob(os.path.join(cache, "*", "*", "*"))):
    plugin = os.path.basename(os.path.dirname(raiz))
    # 1) skills/<nome>/SKILL.md
    for f in sorted(glob.glob(os.path.join(raiz, "skills", "*", "SKILL.md"))):
        fm = frontmatter(f); n = plugin + ":" + (fm.get("name") or os.path.basename(os.path.dirname(f)))
        add(n, plugin, fm.get("description", ""))
    # 2) SKILL.md na raiz do plugin (ex.: humanizer)
    f = os.path.join(raiz, "SKILL.md")
    if os.path.exists(f):
        fm = frontmatter(f); n = plugin + ":" + (fm.get("name") or plugin)
        if not any(i["nome"] == n for i in itens): add(n, plugin, fm.get("description", ""))
    # 3) commands/<nome>.md (viram /plugin:nome no Claude Code)
    for f in sorted(glob.glob(os.path.join(raiz, "commands", "*.md"))):
        fm = frontmatter(f); n = plugin + ":" + os.path.splitext(os.path.basename(f))[0]
        if not any(i["nome"] == n for i in itens): add(n, plugin, fm.get("description", ""))
for e in json.load(open(os.path.join(aqui, "extras.json"), encoding="utf-8")):
    if any(i["nome"] == e["nome"] for i in itens): continue
    itens.append({"nome": e["nome"], "pacote": e["pacote"], "categoria": e["categoria"], "pt": e["pt"], "en": "", "gatilhos": e.get("gatilhos", "")})

itens.sort(key=lambda i: (i["pacote"], i["nome"]))
saida = os.path.join(aqui, "habilidades.json")
json.dump(itens, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
por = {}
for i in itens: por[i["pacote"]] = por.get(i["pacote"], 0) + 1
print(f"{len(itens)} habilidades em {saida}:", ", ".join(f"{k} {v}" for k, v in sorted(por.items())))

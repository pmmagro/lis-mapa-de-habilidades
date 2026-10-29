#!/usr/bin/env python3
"""Sugere quais habilidades usar para um pedido. Uso: python3 sugerir.py "texto do pedido" [--n 5] [--json]
Pontua por palavras em comum entre o pedido e nome, categoria, explicacao e gatilhos de cada habilidade,
com um dicionario de sinonimos em portugues. Nao e inteligencia: e um empurrao para a Lis decidir.
"""
import json, os, re, sys, unicodedata
aqui = os.path.dirname(os.path.abspath(__file__))
SIN = {
 "robo": "humanizer texto", "cara de": "humanizer", "melhora o texto": "humanizer", "melhora": "humanizer", "reescreve": "humanizer",
 "novo": "brainstorming writing-plans", "nova": "brainstorming writing-plans", "sistema": "brainstorming writing-plans", "do zero": "brainstorming",
 "revis": "code-review review requesting-code-review", "codigo": "code-review test-driven-development",
 "sempre que": "update-config hook hookify", "toda vez": "update-config hook hookify", "automatic": "update-config hook",
 "custou": "cost-report cost-tracking", "gastou": "cost-report cost-tracking", "sessao": "cost-report diagnosing-superpowers",
 "parcela": "sgl-financas-pessoais", "paguei": "sgl-financas-pessoais", "salario": "sgl-financas-pessoais", "boleto": "sgl-financas-pessoais",
 "altair": "conciliacao-comissoes-cbv", "cbv": "conciliacao-comissoes-cbv calcario",
 "bug": "systematic-debugging silent-failure erro defeito corrigir consertar", "erro": "systematic-debugging bug corrigir", "nao funciona": "systematic-debugging bug",
 "testar": "test-driven-development verification teste", "teste": "test-driven-development verification",
 "plano": "writing-plans planejar etapas", "planejar": "writing-plans brainstorming", "ideia": "brainstorming criar novo", "criar": "brainstorming novo",
 "pronto": "verification-before-completion conferir", "conferir": "verification-before-completion",
 "revisar": "code-review review requesting-code-review", "revisao": "code-review review",
 "texto": "humanizer escrita", "e-mail": "humanizer email-ops gmail escrita", "email": "humanizer email-ops gmail", "mensagem": "humanizer whatsapp escrita", "roteiro": "humanizer content-engine video",
 "instagram": "content-engine social marketing", "post": "content-engine social crosspost", "campanha": "marketing-campaign marketing", "marketing": "marketing-campaign content-engine seo brand",
 "concorrente": "competitive market-research", "mercado": "market-research competitive",
 "lead": "google-maps-leads lead-intelligence empresas", "leads": "google-maps-leads lead-intelligence", "empresas": "google-maps-leads lead-intelligence lista", "lista de": "google-maps-leads",
 "comissao": "conciliacao-comissoes-cbv minerion", "comissoes": "conciliacao-comissoes-cbv", "minerion": "conciliacao-comissoes-cbv",
 "conta": "sgl-financas-pessoais divida", "contas": "sgl-financas-pessoais", "divida": "sgl-financas-pessoais", "fatura": "sgl-financas-pessoais", "sgl": "sgl-financas-pessoais",
 "planilha": "xlsx excel sheets", "excel": "xlsx", "grafico": "dataviz", "pdf": "pdf nutrient", "word": "docx", "apresentacao": "pptx slides",
 "banco": "postgres database supabase", "supabase": "postgres database-reviewer", "sql": "postgres database",
 "app": "react-native swiftui ios android pmbt", "iphone": "ios swift", "ios": "swift ios-icon-gen", "android": "kotlin android",
 "seguranca": "security-review agent-security-hardening", "senha": "security secret", "injecao": "agent-security-hardening security",
 "hook": "update-config hookify", "configurar": "update-config configure", "permissao": "update-config",
 "site": "claude-in-chrome navegar", "navegar": "claude-in-chrome", "whatsapp": "claude-in-chrome humanizer",
 "assinatura": "esign-field-placement docusign", "docusign": "esign-field-placement", "autentique": "esign-field-placement",
 "habilidade": "writing-skills skill-creator", "skill": "writing-skills skill-creator",
 "caro": "diagnosing-superpowers cost-report cost-tracking", "custo": "cost-tracking cost-report token", "demorou": "diagnosing-superpowers",
 "pesquisa": "deep-research market-research exa-search", "pesquisar": "deep-research", "agendar": "schedule cron rotina", "repetir": "loop",
 "video": "remotion-video video-editing manim content-engine", "imagem": "fal-ai-media", "investidor": "investor-materials investor-outreach", "deck": "pptx investor-materials",
}
def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9\- ]+", " ", s)
STOP = set("para uma com sobre mes dos das que por nos nas uns umas esta este isso aqui ali ela ele eles elas voce quero faz faca fazer cria criar escreve escreva uma tem ter quando onde como mais menos muito pouco bem mal".split())
def toks(s):
    return [t for t in norm(s).split() if len(t) > 2 and t not in STOP]
def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    n = 5; js = "--json" in sys.argv
    if "--n" in sys.argv: n = int(sys.argv[sys.argv.index("--n") + 1]); args = [a for a in args if a != str(n)]
    pedido = " ".join(args).strip()
    if not pedido: print(__doc__); return 1
    itens = json.load(open(os.path.join(aqui, "habilidades.json"), encoding="utf-8"))
    q = norm(pedido); qt = set(toks(pedido))
    for k, v in SIN.items():
        if k in q: qt |= set(v.split())
    res = []
    for it in itens:
        nome = norm(it["nome"]); nt = set(re.split(r"[\s:\-]+", nome)) | {nome.split(":")[-1]}
        corpo = set(toks(it.get("pt", "") + " " + it.get("gatilhos", "") + " " + it.get("categoria", "")))
        pts, motivos = 0, []
        for t in qt:
            if t in nt or any(t in x for x in nt if len(x) > 3): pts += 4; motivos.append(t)
            elif t in corpo: pts += 1; motivos.append(t)
        if pts: res.append((pts, it, sorted(set(motivos))))
    res.sort(key=lambda r: (-r[0], r[1]["nome"]))
    top = res[:n]
    if js:
        print(json.dumps([{"nome": it["nome"], "pontos": p, "porque": m, "pt": it["pt"]} for p, it, m in top], ensure_ascii=False, indent=1)); return 0
    if not top: print("Nenhuma habilidade casou. Siga sem habilidade e diga isso ao Pedro."); return 0
    print(f"Pedido: {pedido}\n")
    for p, it, m in top:
        print(f"- {it['nome']} ({it['pacote']}, {p} pts) porque casou: {', '.join(m)}\n  {it['pt'][:160]}")
    return 0
if __name__ == "__main__": sys.exit(main())

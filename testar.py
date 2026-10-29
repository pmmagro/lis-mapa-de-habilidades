#!/usr/bin/env python3
"""Testa o sugerir.py: cada pedido deve trazer a habilidade esperada entre as 3 primeiras.
Uso: python3 testar.py   (sai com 1 se algum caso falhar)"""
import json, os, subprocess, sys
aqui = os.path.dirname(os.path.abspath(__file__))
CASOS = [
 ("o app do PM-BT está dando erro ao salvar o torneio", "superpowers:systematic-debugging"),
 ("escreve um e-mail para o Sr. Altair sobre a comissão atrasada", "conciliacao-comissoes-cbv"),
 ("quero uma lista de revendas de calcário em Dourados", "google-maps-leads"),
 ("faz uma planilha com os gastos do mês", "anthropic-skills:xlsx"),
 ("cria uma campanha de Instagram para a Ouro Branco", "ecc:marketing-campaign"),
 ("paguei a parcela do carro hoje", "sgl-financas-pessoais"),
 ("esse texto está com cara de robô, melhora", "humanizer:humanizer"),
 ("quero fazer um sistema novo de controle de frete", "superpowers:brainstorming"),
 ("revisa o código que você escreveu", "superpowers:requesting-code-review"),
 ("sempre que eu salvar um arquivo python, rode os testes", ("update-config", "ecc:hookify")),
 ("junta esses três PDFs em um só", "anthropic-skills:pdf"),
 ("abre o site da CBV no Chrome e tira um print", "claude-in-chrome"),
 ("quanto custou essa sessão?", "ecc:cost-report"),
 ("cria uma tabela no Supabase para os pedidos", "ecc:postgres-patterns"),
 ("quem são os concorrentes da Bela Vista em MS?", "ecc:market-research"),
 ("monta um gráfico das vendas por mês", "dataviz"),
 ("posiciona os campos de assinatura no DocuSign", "ecc:esign-field-placement"),
 ("cria uma habilidade nova para você", "superpowers:writing-skills"),
]
def main():
    falhas = 0
    instaladas = {x["nome"] for x in json.load(open(os.path.join(aqui, "habilidades.json"), encoding="utf-8"))}
    for pedido, esperado in CASOS:
        esperados = esperado if isinstance(esperado, tuple) else (esperado,)
        if not any(e in instaladas for e in esperados):
            print("PULA " + pedido[:52].ljust(52) + " -> " + "/".join(esperados) + " nao esta no mapa desta maquina")
            continue
        r = subprocess.run([sys.executable, "-I", os.path.join(aqui, "sugerir.py"), pedido, "--n", "3", "--json"], capture_output=True, text=True)
        try:
            nomes = [x["nome"] for x in json.loads(r.stdout)]
        except Exception:
            nomes = []
        ok = any(e in nomes for e in esperados)
        falhas += (not ok)
        print(("OK   " if ok else "ERRO ") + pedido[:52].ljust(52) + " -> " + (", ".join(nomes) if nomes else "(nada)")[:90])
    print("falhas:", falhas, "de", len(CASOS))
    return 1 if falhas else 0
if __name__ == "__main__":
    sys.exit(main())

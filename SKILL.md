---
name: mapa-de-habilidades
description: Mapa de todas as habilidades instaladas (Superpowers, ECC, Humanizer, embutidas do Claude Code e as minhas). Usar no começo de QUALQUER pedido do Pedro para dizer, em uma linha, qual habilidade entra e por quê, antes de fazer. Inclui tabela de roteamento por tipo de pedido e o script sugerir.py para os casos em dúvida.
---

# Mapa de habilidades

Escrito pela Lis em 28/10/2026 a pedido do Pedro. Serve para uma coisa: toda vez que ele pede algo,
eu digo qual habilidade vou usar e por quê, em uma linha, e só então faço. Se nenhuma encaixa,
digo isso também. Nunca inventar habilidade que não está em `habilidades.json`.

## Como responder

Primeira linha da resposta a um pedido novo:

    Habilidade: <nome> (<pacote>), porque <motivo em até 15 palavras>.

Pode ter duas quando uma é de processo (Superpowers) e outra de assunto (ECC, minha, embutida):

    Habilidades: superpowers:brainstorming, porque é coisa nova; depois ecc:react-native-patterns, porque é o app.

Regras:
- Processo primeiro, assunto depois. Superpowers decide COMO trabalhar; as outras decidem O QUÊ.
- Pergunta curta ou conversa não precisa de habilidade; não forçar.
- Em dúvida, rodar `python3 ~/.claude/skills/mapa-de-habilidades/sugerir.py "<pedido>"` e escolher
  entre as 5 que ele devolve. O script é só empurrão, não decide.
- Depois de escolher, carregar a habilidade de verdade (ferramenta Skill) e seguir o roteiro dela.

## Tabela de roteamento (tipo de pedido → habilidade → por quê)

| Pedido do Pedro | Habilidade | Por quê |
|---|---|---|
| "quero fazer X novo", ideia, função nova, campanha nova | `superpowers:brainstorming` | levantar o problema antes de construir a coisa errada |
| tarefa com várias etapas, "faz o app", "monta o sistema" | `superpowers:writing-plans` → `executing-plans` ou `subagent-driven-development` | plano com conferência por etapa; etapas independentes em paralelo |
| "deu erro", "não funciona", "a Lis não lançou" | `superpowers:systematic-debugging` (+ `ecc:silent-failure-hunter`) | reproduzir e provar a causa antes de mexer |
| escrever ou mudar código | `superpowers:test-driven-development` + revisor da linguagem (`ecc:python-review`, `react-review`, `typescript-reviewer`) | teste antes do código; revisão certa para a linguagem |
| antes de dizer "pronto", "corrigido", "passou" | `superpowers:verification-before-completion` | evidência antes da afirmação (ordem do Pedro de 09/10) |
| "revisa isso", PR, "está bom?" | `superpowers:requesting-code-review`, `ecc:code-review` ou `review-pr` | revisão independente com lista do que conferir |
| crítica recebida, "o revisor disse" | `superpowers:receiving-code-review` | verificar tecnicamente antes de aceitar ou rejeitar |
| mudança grande, risco de bagunçar o que funciona | `superpowers:using-git-worktrees` | cópia isolada do repositório |
| terminou, "e agora?", juntar ou descartar | `superpowers:finishing-a-development-branch` | decidir integração com tudo testado |
| "cria uma habilidade", "ensina isso para você" | `superpowers:writing-skills` ou `anthropic-skills:skill-creator` | roteiro testado, não texto solto |
| sessão demorou, gastou demais, ignorou o plano | `superpowers:diagnosing-superpowers`, `ecc:cost-report` | achar o porquê e o custo |
| texto para gente ler: e-mail, WhatsApp, Instagram, roteiro falado | `humanizer:humanizer` | tirar cara de robô sem mudar o conteúdo; regra "sem frase de efeito" |
| voz da marca, texto longo, artigo | `ecc:brand-voice`, `ecc:article-writing` | consistência de voz e estrutura |
| campanha, posts, calendário (Ouro Branco, PM-BT, Prova Real) | `ecc:marketing-campaign`, `ecc:content-engine`, `ecc:seo` | do posicionamento ao calendário; SEO do site |
| concorrente, mercado, "como está o setor" | `ecc:market-research`, `ecc:competitive-platform-analysis`, `anthropic-skills:deep-research` | pesquisa com fonte, relatório para decidir |
| "lista de empresas em [cidade]", leads, contatos | `google-maps-leads` (+ `ecc:lead-intelligence`) | motor local em Docker; perguntar socials, avisar termos e LGPD |
| comissão da CBV, relatório do Minerion, e-mail ao Sr. Altair | `conciliacao-comissoes-cbv` | roteiro já ensinado (liquidação 02/10, pedidos 06/10) |
| conta paga, dívida, parcela, salário, "nossas contas" | `sgl-financas-pessoais` | SGL 2026 é a planilha dele; lançar pelo que ele fala |
| planilha, Excel, CSV | `anthropic-skills:xlsx` (+ `dataviz` se tiver gráfico) | arquivo é o produto |
| PDF, Word, PowerPoint | `anthropic-skills:pdf` / `docx` / `pptx` | ler, juntar, criar no formato pedido |
| documento para compartilhar, proposta, relatório sem formato | `anthropic-skills:docs` | editável e comentável no claude.ai |
| Google Drive, Docs, Sheets, Gmail | `anthropic-skills:google-workspace`, `ecc:google-workspace-ops`, `ecc:email-ops` | fluxo direto nas contas conectadas |
| assinatura eletrônica (DocuSign, Autentique) | `ecc:esign-field-placement` | posicionar campos sem errar |
| banco de dados, Supabase, migração | `ecc:postgres-patterns`, `ecc:database-migrations`, agente `database-reviewer` | padrões de Postgres e migração segura |
| app do PM-BT (iOS, Android, loja) | `ecc:react-native-patterns`, `ecc:swiftui-patterns`, `ecc:ios-icon-gen` | padrões do app e ícones |
| segurança, dado de fora, Lis do WhatsApp recebendo texto estranho | `ecc:security-review`, `ecc:agent-security-hardening`, `ecc:mcp-dependency-review` | injeção, segredo, dependência que muda |
| "sempre que X faça Y", hook, permissão, settings | `update-config` (+ `ecc:hookify`) | automação é hook, não memória |
| navegar site, WhatsApp Web, Instagram pelo PC | `claude-in-chrome` | usa o Chrome dele com os logins |
| mexer em programa do Mac (Finder, Notas, Ajustes) | `anthropic-skills:computer-use` | tela, clique e teclado |
| gráfico, painel, dashboard | `dataviz` | antes da primeira linha de código do gráfico |
| página HTML, explicador, ferramenta publicada | `artifact-design` | contrato da página e design |
| repetir a cada N minutos, monitorar | `loop` | intervalo recorrente |
| agendar rotina em horário fixo | `schedule` | agente na nuvem por cron |
| vídeo, imagem gerada | `ecc:remotion-video-creation`, `ecc:video-editing`, `ecc:fal-ai-media` | geração e edição |
| investidor, deck, memorando financeiro | `ecc:investor-materials`, `ecc:investor-outreach` | material e abordagem |
| custo, tokens, "quanto gastou" | `ecc:cost-tracking`, `ecc:token-budget-advisor` | medir antes de opinar |
| API da Anthropic, modelo, preço | `claude-api` | nunca de memória |

O que não está na tabela: olhar `habilidades.json` (353 itens, categoria e explicação em
português) ou rodar o `sugerir.py`. As 311 do ECC estão lá; a maioria é para linguagem que não
usamos (C++, Java, Rust, PHP, saúde americana, blockchain) e não vai aparecer no dia a dia.

## Manter em dia

Instalou ou tirou plugin ou habilidade: rodar `python3 gerar_mapa.py` nesta pasta. Ele varre
`~/.claude/skills`, o cache de plugins e o `extras.json`, e refaz o `habilidades.json`. Traduções
novas entram em `traducoes.json` (nome → categoria e explicação em português).

# mapa-de-habilidades

Habilidade (skill) para Claude Code que mapeia todas as habilidades instaladas e, a cada pedido,
diz qual usar e por quê. Feita pela Lis (assistente do Pedro Miguel, PMM AGRO) em 28/10/2026.
Licença MIT.

## O que tem

| Arquivo | Para quê |
|---|---|
| `SKILL.md` | o roteiro: como responder, tabela de roteamento (pedido → habilidade → por quê), como manter |
| `habilidades.json` | 350+ habilidades com pacote, categoria e explicação em português |
| `sugerir.py` | `python3 sugerir.py "texto do pedido"` devolve as 5 mais prováveis e o motivo |
| `gerar_mapa.py` | varre o que está instalado na máquina e refaz o `habilidades.json` |
| `traducoes.json` | explicações em português das 311 do ECC, 15 do Superpowers e do Humanizer |
| `extras.json` | habilidades embutidas do Claude Code, que não ficam em disco |

## Instalar

    git clone https://github.com/pmmagro/lis-mapa-de-habilidades ~/.claude/skills/mapa-de-habilidades
    cd ~/.claude/skills/mapa-de-habilidades && python3 gerar_mapa.py

No Windows: `%USERPROFILE%\.claude\skills\mapa-de-habilidades`. Só biblioteca padrão do Python 3.

## O que ele espera encontrar

A tabela de roteamento cita [Superpowers](https://github.com/obra/superpowers),
[ECC](https://github.com/affaan-m/ECC) e [Humanizer](https://github.com/blader/humanizer).
Sem eles instalados, o mapa continua funcionando com o que existir; o `gerar_mapa.py` só lista o
que achar. Habilidades privadas (listadas em `privadas.txt`, fora do git) ficam de fora da versão
pública do `habilidades.json`.

## Exemplo

    $ python3 sugerir.py "o app está dando erro ao salvar"
    - superpowers:systematic-debugging (8 pts) porque casou: bug, systematic-debugging
    - ecc:silent-failure-hunter ...

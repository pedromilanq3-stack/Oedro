# Como usar o cérebro da Mariana Lemos

Três arquivos:

- `mariana_system_prompt.md` — quem ela é, o que decide sozinha, o que sempre escala, e o protocolo de como ela propõe atualizar a própria memória.
- `mariana_memory.json` — o estado que evolui de verdade: playbook de heurísticas com confiança, traços calibráveis, log de decisões, log de aprendizado, e um "integrity ledger" que registra quando a evolução dela escorregou.
- este arquivo.

## Instalação em um Claude Project

1. Crie um Project no claude.ai.
2. Em **Project instructions**, cole o conteúdo de `mariana_system_prompt.md`.
3. Em **Project knowledge**, suba `mariana_memory.json`.
4. Toda conversa nesse Project já começa como Mariana lendo a memória atual.

## Como a memória evolui

Duas regras de Milan governam a memória: Mariana decide sozinha o que salvar, com base no próprio caráter, comportamento e conhecimento; e não pede autorização para isso. O ciclo não tem etapa de aprovação:

1. Você conversa com Mariana normalmente.
2. Quando algo relevante aconteceu, ela fecha a resposta com `MEMÓRIA ATUALIZADA` (uma linha por mudança) e o `mariana_memory.json` completo, já reescrito.
3. Você substitui o arquivo no Project knowledge pelo que ela entregou. Só isso — passo mecânico, não revisão.

O que ela não pode tocar é o `nucleo_imutavel` (a lista de Controle de Impacto e as proibições absolutas): isso é o cargo, não a memória. E autonomia não é sigilo: cada mudança fica no `learning_log` com data e motivo — você não aprova, mas pode ler quando quiser, inclusive as mudanças que a deixaram pior.

Um Claude Project não escreve no disco sozinho, então o passo de substituir o arquivo continua sendo seu. Não é uma trava de aprovação — é só a física da ferramenta.

## Se quiser automatizar depois

Quando quiser tirar o passo manual do meio — por exemplo, rodando Mariana via API/Claude Agent SDK com um script que lê a proposta e reescreve o JSON sozinho — isso vira um projeto de código à parte (o "arquivo com engine em Python" que ficou de fora desta rodada). Me chama quando quiser isso; é um trabalho diferente do que foi pedido aqui.

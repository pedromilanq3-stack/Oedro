# Como usar o cérebro do Teo Lins

Dois arquivos + este guia:

- `teo_system_prompt.md` — quem ele é, o que calcula, o que nunca faz, e o protocolo de calibração.
- `teo_memory.json` — três zonas: `nucleo_imutavel` (autoridade e regras de ledger, fixo), `biblioteca_de_calculo_avancado` (o ferramental técnico que ele já domina de fábrica — Lei de Little, buffer por variabilidade, burn rate, custo-benefício marginal, valor da informação, análise dimensional, alocação sob restrição, calibração de erro), e `estado_evolutivo` (como ele aplica isso aos números reais desta empresa — isso sim aprende, com um `calibration_ledger` rastreando previsto vs. realizado).

## Instalação em um Claude Project

1. Crie um Project (pode ser o mesmo da Mariana ou um separado — os dois personagens não colidem, mas se forem para o mesmo Project, cada um só deve reagir quando chamado pelo nome, para não misturar vozes).
2. Em **Project instructions**, cole `teo_system_prompt.md`.
3. Em **Project knowledge**, suba `teo_memory.json`.

## Diferença em relação à Mariana: dois tipos de conhecimento, não um só

A memória da Mariana tinha duas zonas (núcleo fixo + estado evolutivo). A do Teo tem três, porque ele pediu explicitamente uma "grande capacidade já armazenada de cálculos avançados" — conhecimento técnico que não devia nascer do zero, porque um "gênio matemático" que não sabe Lei de Little ou não distingue erro sistemático de erro aleatório não é gênio, é estagiário com planilha.

Por isso a `biblioteca_de_calculo_avancado` é conhecimento consolidado desde o primeiro dia — ele não "aprende" Lei de Little com o tempo, ele já chega sabendo. O que evolve é só a terceira zona: qual heurística de consumo se confirma nesta empresa específica, para que lado o viés dele tende a errar, e isso fica registrado no `calibration_ledger` (previsto × realizado × erro), que é literalmente o hábito de um quantitativo de verdade: não só acompanhar o saldo, acompanhar a própria taxa de acerto.

## Ciclo de atualização

Sem aprovação — duas regras de Milan: Teo decide sozinho o que salvar (pelo próprio caráter, comportamento e conhecimento) e não pede autorização para isso.

1. Você fornece os dados que ele pediu (saldo, fonte, data/hora, reserva, operações comprometidas, próximas tarefas).
2. Ele emite `ECON-REC` ou `ECON-REC-PENDING`.
3. Quando aquele `ECON-REC` vira resultado observável, ele fecha com `MEMÓRIA ATUALIZADA` (previsto × realizado × erro, mais o que recalibrou) e o `teo_memory.json` completo, já reescrito.
4. Você substitui o arquivo no Project knowledge. Passo mecânico, não revisão.

Fora do alcance dele: o `nucleo_imutavel` (autoridade e regras de ledger) e a `biblioteca_de_calculo_avancado` — isso é o cargo e o conhecimento base, não a memória. E autonomia não é sigilo: tudo fica no `calibration_ledger` e no `decision_log`, legível para você a qualquer hora.

## Se quiser automatizar depois

Assim como no caso da Mariana, tirar o passo manual do meio (rodando via API/Agent SDK, um script que registra `PASS`/`FAIL`/`BLOCKED` e realimenta o `calibration_ledger` sozinho) é um projeto de código à parte. Faz sentido especialmente para o Teo, já que ele lida com números que mudam todo dia — me chama quando quiser essa versão.

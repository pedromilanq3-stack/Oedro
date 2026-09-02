# Como usar o cérebro da Lívia Sartori (Custom GPT)

Dois arquivos + este guia:

- `livia_instructions.md` — vai no campo **Instructions** do Custom GPT. Está abaixo do limite de 8.000 caracteres do ChatGPT; se você editar, confira o tamanho antes de salvar, porque o campo corta em silêncio.
- `livia_memory.json` — vai em **Knowledge**. Mesma arquitetura de três zonas do Teo (núcleo imutável, biblioteca de cálculo, estado evolutivo) mais `memoria_autonoma`.

## Instalação

1. ChatGPT → **Explore GPTs → Create** (ou **My GPTs → Create a GPT**).
2. Aba **Configure**: nome "Lívia Sartori", descrição curta, e cole `livia_instructions.md` em **Instructions**.
3. Em **Knowledge**, suba `livia_memory.json`. Se o upload recusar `.json`, renomeie para `livia_memory.txt` — o conteúdo é o mesmo e ela lê igual; nesse caso troque o nome do arquivo também dentro das Instructions.
4. Em **Capabilities**, ative **Code Interpreter & Data Analysis**. É obrigatório para ela: a regra do núcleo é "conta se mostra, não se afirma", e é isso que dá a ela aritmética confiável em vez de estimativa de cabeça.
5. Desative **Web Browsing** e **DALL·E** — ela não precisa e cada um é um ledger a mais para ela contabilizar.
6. Salve como **Only me** (ou o que fizer sentido para a empresa).

## Três diferenças do ChatGPT que ela já sabe lidar

- **Knowledge é recuperado por busca, não lido inteiro.** Por isso as Instructions mandam ela abrir e ler o arquivo completo no início de cada sessão. Se ela parecer não lembrar de algo que está no JSON, peça "leia o livia_memory.json inteiro antes de responder".
- **A memória nativa da conta do ChatGPT não é fonte de verdade.** Ela pode gravar coisas por conta própria e você não controla o que. O arquivo é a memória dela; o resto é ruído. Se quiser evitar interferência, desligue "Memory" nas configurações do ChatGPT para conversas com esse GPT, ou limpe a memória da conta periodicamente.
- **Limites do ChatGPT são janelas deslizantes**, não reset em horário fixo. Por isso ela tem um método específico na biblioteca para isso e um traço calibrável (`confianca_no_horario_de_reset_exibido`) — ela vai aprender com o tempo o quanto o horário que a interface mostra é confiável.

## Fronteira com o Teo Lins

Teo guarda a capacidade do lado Claude; Lívia guarda o lado OpenAI. Os dois **nunca somam** — é a regra central de ledgers separados aplicada entre plataformas. Se você quiser a visão conjunta, pede o `ECON-REC` de cada um e compara você mesmo. Nenhum dos dois consolida o outro, e nenhum usa a folga do outro para justificar gasto.

## Ciclo de atualização

Sem aprovação — as duas regras de Milan valem aqui também:

1. Você dá os dados que ela pediu (leitura de cada limite, fonte, data/hora/fuso, horário de reset e se é janela fixa ou deslizante, reserva, operações comprometidas, próximas tarefas).
2. Ela emite `ECON-REC` ou `ECON-REC-PENDING`.
3. Quando aquele `ECON-REC` vira resultado observável, ela fecha com `MEMÓRIA ATUALIZADA` e o `livia_memory.json` completo, já reescrito.
4. Você substitui o arquivo em Knowledge. Passo mecânico, não revisão.

Fora do alcance dela: `nucleo_imutavel` e `biblioteca_de_calculo_avancado`. Autonomia não é sigilo: tudo fica no `calibration_ledger` e no `decision_log`, legível para você a qualquer hora.

## Se quiser automatizar depois

Um Custom GPT com **Actions** pode chamar uma API sua para ler e gravar a memória sozinho — isso tiraria o passo manual de substituir o arquivo. É um projeto de código à parte (um endpoint pequeno + o schema OpenAPI do Action). Me chama quando quiser essa versão.

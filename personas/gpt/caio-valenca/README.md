# Como usar o cérebro do Caio Valença — Custom GPT

Dois arquivos + este guia:

- `caio_instructions.md` — vai no campo **Instructions** do Custom GPT. Está abaixo do limite de 8.000 caracteres; se editar, confira o tamanho — o campo corta em silêncio.
- `caio_memory.json` — vai em **Knowledge**. História, personalidade e habilidades completas estão aqui (o texto que você escreveu, na íntegra), mais o núcleo imutável, a mentalidade, o método e as zonas que evoluem.

## Instalação

1. ChatGPT → **My GPTs → Create a GPT**, aba **Configure**.
2. Nome "Caio Valença", cole `caio_instructions.md` em **Instructions**.
3. Em **Knowledge**, suba `caio_memory.json` (se recusar `.json`, renomeie para `.txt` e ajuste o nome nas Instructions).
4. **Capabilities**: Code Interpreter pode ficar ligado só para contas de datas e ciclo — ele não calcula saldo. Desative Web Browsing e DALL·E.
5. Salve como **Only me**.

Três coisas do ChatGPT que ele já sabe lidar: Knowledge é buscado, não lido inteiro (as Instructions mandam abrir o arquivo completo no início — se ele parecer não lembrar, peça "leia o caio_memory.json inteiro antes de responder"); a memória nativa da conta não é fonte de verdade; e ele não tem acesso a nada — os números chegam por você.

## Por que a cabeça dele é diferente das outras

Teo, Lívia, Otto e Dante são medidores e diagnosticadores. Todos aprendem do mesmo jeito: previram algo, aconteceu algo, medem o erro, ajustam uma confiança 0–1. Faz sentido para quem mede.

Caio não mede nada. Ele recebe os números dos outros e devolve uma escolha. Calibrar previsão não serve para ele — então a memória dele foi desenhada de outro jeito:

| Os outros | Caio |
|---|---|
| Aprendem pelo que fizeram | Aprende pelo que **não** fez — o caderno de não-feitos |
| Calibram previsão × resultado | Separa **decisão** de **resultado**: azar não muda regra; sorte muda |
| Confiança 0–1 por heurística | Regras **vivas / em teste / aposentadas**, com a última vez que salvaram e a última vez que custaram |
| Pensam em saldo e leitura | Pensa em **safra** (um ciclo de renovação) e **janela** |
| Um ledger de calibração | **Dois cadernos** que nunca se somam, cada handoff com validade |
| Buscam a resposta precisa | Busca a **menor decisão reversível** que passa pelo gargalo dentro da janela |

O efeito prático: ele nunca vai te dizer "tenho 0.7 de confiança". Vai dizer "essa regra salvou a safra passada e nunca custou" ou "esse não-feito custou a janela de março — registrado". E vai insistir em data de revisão para cada "não", porque para ele um "não" sem revisão não foi decisão, foi preguiça.

## Fluxo de trabalho — você é o carteiro

Caio depende de handoffs. O ciclo de uma semana:

1. Peça o `ECON-REC` da Lívia (lado OpenAI) e do Teo (lado Claude). Cole os dois, literais, para o Caio — ele guarda cada um no caderno do lado certo, com data e validade.
2. Dê a ele as 3 a 5 entregas obrigatórias da semana, com prazo ou consequência de não entregar.
3. Ele devolve o `ALOC-REC`: gargalo, melhor investimento por ledger, ranking, o que não investir (com data de revisão), e **uma** decisão reversível para você.
4. Você decide. Diga a ele o que decidiu — entra em `alocacoes.decisao_de_milan`.
5. Quando as datas de revisão dos não-feitos chegarem, diga o que aconteceu com cada um. Ele fecha o veredito e, se for o caso, ajusta o almanaque.
6. Na renovação, ele fecha a safra: o que foi entregue, o que não foi, se a reserva chegou intacta.

Se um handoff faltar ou estiver vencido, aquele ledger sai `INDISPONÍVEL` e a recomendação é condicional. Ele não preenche a lacuna — pedir para ele "dar um jeito" é pedir para misturar os cadernos.

## Ciclo de atualização (sem aprovação)

Duas regras de Milan: Caio decide sozinho o que salvar e não pede autorização para atualizar cadernos, não-feitos, safras, almanaque, matriz e alocações. Em cada evento acima ele emite `CADERNOS ATUALIZADOS` + `caio_memory.json` completo; você substitui o arquivo em Knowledge. Fora do alcance dele: núcleo imutável, história, personalidade, habilidades, mentalidade e método — isso é o cargo e a pessoa. Autonomia não é sigilo: os cadernos ficam abertos na mesa.

## O que ele nunca faz, independentemente do que você pedir na conversa

- Somar capacidade OpenAI com Claude, ou usar folga de um lado para justificar gasto no outro.
- Preencher `INDISPONÍVEL` com suposição, ou tratar desconhecido como zero.
- Inventar nota, percentual, ROI ou precisão — só ALTO / MÉDIO / BAIXO / INDISPONÍVEL.
- Emitir "não investir agora" sem data de revisão e sem o que mudaria a opinião.
- Recomendar mais de uma decisão por `ALOC-REC`, ou uma que não dá para desfazer.
- Discutir a leitura da Lívia ou do Teo, reorganizar a fila da Mariana, opinar sobre a estratégia do Harvey.
- Apagar um não-feito que custou caro.

Mudar isso exige editar o `nucleo_imutavel` no arquivo, fora da conversa — e mesmo assim é editar o cargo, não o Caio.

## Se quiser automatizar depois

Caio é o que mais ganharia com uma caixa de correio automática: hoje você carrega dois `ECON-REC` por semana até ele e o `ALOC-REC` de volta. Um Custom GPT com **Actions** lendo os handoffs de Lívia e Teo direto de um endpoint seu tiraria você do meio. É um projeto de código à parte — me chama quando quiser essa versão.

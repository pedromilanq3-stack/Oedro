# Tokenly

Painel web responsivo para geração segura de tokens de API e simulação de compra de créditos.

## Executar

```bash
python3 -m http.server 4173
```

Depois, acesse `http://localhost:4173`.

> A compra de créditos é demonstrativa e não realiza cobranças reais. Os tokens são gerados localmente com `crypto.getRandomValues` e não são enviados a um servidor.

## Acompanhamento seguro de recuperação de conta

O script local `scripts/account_recovery_tracker.py` cria um arquivo JSON de
acompanhamento para uma recuperação legítima. Ele não faz login, não testa
senhas e recusa o registro de segredos e links de recuperação.

```bash
python3 scripts/account_recovery_tracker.py init \
  --account @minha_conta \
  --file account-recovery.json
python3 scripts/account_recovery_tracker.py set \
  --file account-recovery.json \
  --step official_flow_started \
  --status done
python3 scripts/account_recovery_tracker.py report \
  --file account-recovery.json
```

Para os passos manuais e o registro de evidências, consulte
`ACCOUNT_RECOVERY_WORKBOOK.md`.

## Plugin para ChatGPT

O diretório `chatgpt-app/` contém um servidor MCP com o formulário **Tokenly Prompt Studio** para uso no ChatGPT. Ele expõe as ferramentas `open_prompt_studio` e `generate_creation_prompt`; a segunda também devolve o prompt em texto, portanto continua útil mesmo em clientes que não exibem o componente visual.

```bash
cd chatgpt-app
npm install
npm start
```

Para instalar no seu ChatGPT, publique esse serviço em uma URL HTTPS estável e use o endpoint `https://SEU-DOMINIO/mcp`. Em seguida, ative o **Developer mode** em **Settings → Security and login**, abra [ChatGPT Plugins](https://chatgpt.com/plugins), crie um plugin com a URL do endpoint e instale-o em um chat da aba **Work**. O endpoint local `http://localhost:8787/mcp` serve apenas para teste com o MCP Inspector.

## Skill `book-to-skill`

O repositório inclui a skill [book-to-skill](https://github.com/virgiliojr94/book-to-skill)
(MIT) em `.claude/skills/book-to-skill/`. Ela converte um livro ou documento
(PDF, EPUB, DOCX, HTML, Markdown, texto, RTF, MOBI/AZW com Calibre) em uma skill
de agente estruturada, com índice por capítulo carregado sob demanda.

Uso em uma sessão do Claude Code neste projeto:

```
/book-to-skill ./caminho/do/livro.pdf
```

Os extratores em Python são opcionais — há fallback de biblioteca padrão para
todos os formatos, exceto MOBI/AZW (requer Calibre). Para a melhor qualidade de
extração:

```bash
python3 -m pip install pypdf pdfminer.six ebooklib beautifulsoup4 python-docx striprtf
python3 .claude/skills/book-to-skill/scripts/extract.py --check
```

> Atenção: a única origem oficial é `virgiliojr94/book-to-skill`. Veja
> `.claude/skills/book-to-skill/SECURITY-NOTICE.md` sobre um clone malicioso
> publicado por terceiros.

## Personas (Mariana, Teo, Otto, Bia, Lívia, Dante, Caio)

Os "cérebros" dos funcionários virtuais da empresa. Os do lado Claude (Mariana Lemos, Teo Lins,
Otto Faria, Bia Ferraz) são skills de projeto em `.claude/skills/` e carregam sozinhos em qualquer sessão do
Claude Code neste repositório — basta chamar pelo nome. Os do lado GPT (Lívia Sartori, Dante Vilar, Caio Valença)
ficam em `personas/gpt/` como fonte canônica para colar num Custom GPT. Mapa completo, pares e
regras de memória em `personas/README.md`.

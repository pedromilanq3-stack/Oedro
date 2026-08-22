# Tokenly

Painel web responsivo para geração segura de tokens de API e simulação de compra de créditos.

## Executar

```bash
python3 -m http.server 4173
```

Depois, acesse `http://localhost:4173`.

> A compra de créditos é demonstrativa e não realiza cobranças reais. Os tokens são gerados localmente com `crypto.getRandomValues` e não são enviados a um servidor.

## Plugin para ChatGPT

O diretório `chatgpt-app/` contém um servidor MCP com o formulário **Tokenly Prompt Studio** para uso no ChatGPT. Ele expõe as ferramentas `open_prompt_studio` e `generate_creation_prompt`; a segunda também devolve o prompt em texto, portanto continua útil mesmo em clientes que não exibem o componente visual.

```bash
cd chatgpt-app
npm install
npm start
```

Para instalar no seu ChatGPT, publique esse serviço em uma URL HTTPS estável e use o endpoint `https://SEU-DOMINIO/mcp`. Em seguida, ative o **Developer mode** em **Settings → Security and login**, abra [ChatGPT Plugins](https://chatgpt.com/plugins), crie um plugin com a URL do endpoint e instale-o em um chat da aba **Work**. O endpoint local `http://localhost:8787/mcp` serve apenas para teste com o MCP Inspector.

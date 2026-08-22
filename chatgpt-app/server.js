import { createServer } from 'node:http';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import { registerAppResource, registerAppTool, RESOURCE_MIME_TYPE } from '@modelcontextprotocol/ext-apps/server';
import { z } from 'zod';

const directory = dirname(fileURLToPath(import.meta.url));
const widgetHtml = readFileSync(join(directory, 'public', 'prompt-studio.html'), 'utf8');
const WIDGET_URI = 'ui://tokenly/prompt-studio.html';
const promptInputSchema = {
  creationType: z.string().min(1).max(80),
  details: z.string().min(1).max(280),
  configuration: z.string().max(280).optional(),
  delivery: z.enum(['um passo a passo claro', 'uma solução pronta para implementar']).default('um passo a passo claro'),
};

function buildPrompt({ creationType, details, configuration, delivery }) {
  const preferences = configuration?.trim()
    ? `\nConfigurações obrigatórias: ${configuration.trim()}.`
    : '\nUse boas práticas, uma estrutura organizada e uma experiência acessível.';

  return `Atue como um especialista multidisciplinar. Crie ${creationType.trim()} com este objetivo: ${details.trim()}.${preferences}\n\nAntes de finalizar, valide se a solução atende ao objetivo, explique escolhas relevantes e entregue ${delivery}. Se precisar assumir algo, declare a suposição e escolha a alternativa mais útil.`;
}

function promptResponse(input) {
  const prompt = buildPrompt(input);
  return {
    content: [{ type: 'text', text: prompt }],
    structuredContent: { prompt },
  };
}

function createPromptServer() {
  const server = new McpServer({ name: 'Tokenly Prompt Studio', version: '1.0.0' });

  registerAppResource(server, 'prompt-studio', WIDGET_URI, {}, async () => ({
    contents: [{ uri: WIDGET_URI, mimeType: RESOURCE_MIME_TYPE, text: widgetHtml }],
  }));

  registerAppTool(server, 'generate_creation_prompt', {
    title: 'Gerar comando de criação',
    description: 'Gera um comando completo em português para criar projetos, automações, interfaces, conteúdos ou integrações.',
    inputSchema: promptInputSchema,
    outputSchema: { prompt: z.string() },
    _meta: { ui: { resourceUri: WIDGET_URI } },
  }, async input => promptResponse(input));

  registerAppTool(server, 'open_prompt_studio', {
    title: 'Abrir estúdio de comandos',
    description: 'Abre o formulário Tokenly para configurar e gerar um comando de IA.',
    inputSchema: {},
    _meta: { ui: { resourceUri: WIDGET_URI } },
  }, async () => ({
    content: [{ type: 'text', text: 'Estúdio de comandos aberto. Preencha o formulário para gerar seu prompt.' }],
  }));

  return server;
}

const port = Number(process.env.PORT ?? 8787);
const mcpPath = '/mcp';
const httpServer = createServer(async (request, response) => {
  const url = new URL(request.url ?? '/', `http://${request.headers.host ?? 'localhost'}`);

  if (request.method === 'OPTIONS' && url.pathname === mcpPath) {
    response.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
      'Access-Control-Allow-Headers': 'content-type, mcp-session-id',
      'Access-Control-Expose-Headers': 'Mcp-Session-Id',
    }).end();
    return;
  }

  if (request.method === 'GET' && url.pathname === '/') {
    response.writeHead(200, { 'content-type': 'text/plain; charset=utf-8' }).end('Tokenly Prompt Studio MCP server');
    return;
  }

  if (url.pathname === mcpPath && ['POST', 'GET', 'DELETE'].includes(request.method ?? '')) {
    response.setHeader('Access-Control-Allow-Origin', '*');
    response.setHeader('Access-Control-Expose-Headers', 'Mcp-Session-Id');
    const server = createPromptServer();
    const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
    response.on('close', () => { transport.close(); server.close(); });
    try {
      await server.connect(transport);
      await transport.handleRequest(request, response);
    } catch (error) {
      console.error('MCP request error:', error);
      if (!response.headersSent) response.writeHead(500).end('Internal server error');
    }
    return;
  }

  response.writeHead(404).end('Not found');
});

httpServer.listen(port, () => console.log(`Tokenly MCP server listening on http://localhost:${port}${mcpPath}`));

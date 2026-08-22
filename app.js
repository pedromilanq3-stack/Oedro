const form = document.querySelector('#token-form');
const preview = document.querySelector('#token-preview');
const dialog = document.querySelector('#credit-dialog');
const toast = document.querySelector('#toast');
const balance = document.querySelector('#balance');
const promptForm = document.querySelector('#prompt-form');
const promptResult = document.querySelector('#prompt-result');
const copyPromptButton = document.querySelector('.copy-prompt');
let currentBalance = 240;

function notify(message) {
  toast.textContent = message;
  toast.classList.add('show');
  window.setTimeout(() => toast.classList.remove('show'), 2600);
}

function generateToken(environment) {
  const bytes = new Uint8Array(24);
  crypto.getRandomValues(bytes);
  const value = Array.from(bytes, byte => byte.toString(16).padStart(2, '0')).join('');
  return `${environment === 'Teste' ? 'tly_test' : 'tly_live'}_${value}`;
}

function createPrompt(data) {
  const configuration = data.get('configuration').trim();
  const configurationLine = configuration
    ? `\nConfigurações obrigatórias: ${configuration}.`
    : '\nUse boas práticas, uma estrutura organizada e uma experiência acessível.';

  return `Atue como um especialista multidisciplinar. Crie ${data.get('creationType')} com este objetivo: ${data.get('details').trim()}.${configurationLine}\n\nAntes de finalizar, valide se a solução atende ao objetivo, explique escolhas relevantes e entregue ${data.get('delivery')}. Se precisar assumir algo, declare a suposição e escolha a alternativa mais útil.`;
}

promptForm.addEventListener('submit', event => {
  event.preventDefault();
  const data = new FormData(promptForm);
  promptResult.textContent = createPrompt(data);
  promptResult.classList.add('has-result');
  copyPromptButton.disabled = false;
});

copyPromptButton.addEventListener('click', async () => {
  await navigator.clipboard.writeText(promptResult.textContent);
  notify('Comando copiado para a área de transferência.');
});

form.addEventListener('submit', event => {
  event.preventDefault();
  const data = new FormData(form);
  const token = generateToken(data.get('environment'));
  preview.classList.add('generated');
  preview.innerHTML = `
    <div class="preview-icon">✓</div>
    <span class="preview-label">TOKEN GERADO COM SUCESSO</span>
    <strong>${data.get('name')}</strong>
    <div class="token-value">${token}</div>
    <button type="button" class="copy-btn">Copiar token</button>
    <p>Copie agora. Por segurança, ele não será<br />exibido novamente.</p>`;
  preview.querySelector('.copy-btn').addEventListener('click', async () => {
    await navigator.clipboard.writeText(token);
    notify('Token copiado para a área de transferência.');
  });
});

function openCredits(value = 100) {
  document.querySelector('#credit-value').value = value;
  dialog.showModal();
}

document.querySelectorAll('[data-open-credits]').forEach(button => button.addEventListener('click', () => openCredits()));
document.querySelectorAll('.credit-options [data-value]').forEach(button => button.addEventListener('click', () => openCredits(button.dataset.value)));
document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });

document.querySelector('#confirm-credit').addEventListener('click', () => {
  const value = Number(document.querySelector('#credit-value').value);
  if (!Number.isFinite(value) || value < 10) {
    notify('O valor mínimo para recarga é R$ 10.');
    return;
  }
  currentBalance += value;
  balance.textContent = currentBalance.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  dialog.close();
  notify(`${value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })} adicionados ao saldo demonstrativo.`);
});

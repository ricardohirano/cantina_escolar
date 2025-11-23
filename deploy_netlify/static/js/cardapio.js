console.log("cardapio.js v7 - cards por categoria com Ver mais individual");

const MAX_VISIBLE = 5; // quantos cards aparecem inicialmente em cada categoria

function formatBRL(v) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(Number(v || 0));
}

async function carregarCardapio() {
  const secao = document.getElementById('secao-cardapio');
  if (!secao) {
    console.warn('[cardapio.js] Elemento #secao-cardapio não encontrado.');
    return;
  }

  secao.innerHTML = '<p class="text-muted">Carregando cardápio...</p>';

  try {
    const resp = await fetch('static/data/cardapio.json', { cache: 'no-store' });

    if (!resp.ok) {
      console.error('[cardapio.js] Erro ao buscar cardapio.json:', resp.status, resp.statusText);
      secao.innerHTML = '<p class="text-danger">Não foi possível carregar o cardápio.</p>';
      return;
    }

    const data = await resp.json();
    montarCardapio(secao, data);

  } catch (erro) {
    console.error('[cardapio.js] Erro ao carregar o cardápio:', erro);
    secao.innerHTML = '<p class="text-danger">Erro ao carregar o cardápio.</p>';
  }

  // garante o link do QR Code
  const a = document.getElementById('qr-link');
  if (a) a.href = "https://cantinasenairegistro.netlify.app/";
}

function montarCardapio(secao, data) {
  secao.innerHTML = '';

  if (!data || !Array.isArray(data.categorias)) {
    secao.innerHTML = '<p class="text-muted">Nenhuma categoria cadastrada.</p>';
    return;
  }

  data.categorias.forEach(categoria => {
    criarCategoria(secao, categoria);
  });
}

function criarCategoria(secao, categoria) {
  // Título da categoria
  const h2 = document.createElement('h2');
  h2.className = 'categoria-titulo';
  h2.textContent = categoria.nome || 'Categoria';

  // gera um id no padrão cat-bebidas, cat-salgados, cat-refeicoes...
  const slug = (categoria.nome || 'categoria')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '') // remove acentos
    .toLowerCase()
    .replace(/\s+/g, '-'); // espaços -> hífen

  h2.id = 'cat-' + slug;

  secao.appendChild(h2);

  // Linha de cards
  const row = document.createElement('div');
  row.className = 'row row-cols-1 row-cols-md-3 row-cols-lg-5 g-3';
  secao.appendChild(row);

  const cardsCategoria = [];

  if (Array.isArray(categoria.produtos)) {
    categoria.produtos.forEach(produto => {
      const col = document.createElement('div');
      col.className = 'col product-card';

      const preco = formatBRL(produto.preco);

      col.innerHTML = `
        <div class="card card-produto h-100 shadow-sm">
          <img
            src="${produto.imagem || 'static/img/placeholder.png'}"
            class="card-img-top"
            alt="${produto.nome || ''}"
          >
          <div class="card-body">
            <h5 class="card-title">${produto.nome || ''}</h5>
            <p class="card-text small text-muted">
              ${produto.descricao || ''}
            </p>
          </div>
          <div class="card-footer preco-card">
            ${preco}
          </div>
        </div>
      `;

      row.appendChild(col);
      cardsCategoria.push(col);
    });
  }

  // Se a categoria tiver mais que MAX_VISIBLE produtos, cria botão próprio
  if (cardsCategoria.length > MAX_VISIBLE) {
    // esconde os extras inicialmente
    cardsCategoria.forEach((card, index) => {
      if (index >= MAX_VISIBLE) card.classList.add('d-none');
    });

    const wrapper = document.createElement('div');
    wrapper.className = 'text-center mt-2';

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'btn btn-ver-mais';
    btn.textContent = 'Ver mais';
    btn.dataset.expanded = 'false';

    btn.addEventListener('click', () => {
      const expanded = btn.dataset.expanded === 'true';
      const novoEstado = !expanded;
      btn.dataset.expanded = String(novoEstado);

      cardsCategoria.forEach((card, index) => {
        if (!novoEstado && index >= MAX_VISIBLE) {
          card.classList.add('d-none');
        } else {
          card.classList.remove('d-none');
        }
      });

      btn.textContent = novoEstado ? 'Ver menos' : 'Ver mais';
    });

    wrapper.appendChild(btn);
    secao.appendChild(wrapper);
  }
}


document.addEventListener('DOMContentLoaded', carregarCardapio);

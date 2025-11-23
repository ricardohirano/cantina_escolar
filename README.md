
# Cantina Escolar — Projeto v3 (didático, com dados+funções juntos)

**O que muda nesta v3**
- As **funções** passaram a morar **junto dos “bancos”** (módulos `database/usuario.py` e `database/produto.py`).
- As **constantes** (categorias/turnos/alérgenos) agora estão em `database/produto.py`, ao lado dos produtos.
- Código com **comentários mais extensos** para facilitar o entendimento em um curso técnico de ensino médio.

## Como rodar
```bash
pip install flask werkzeug
python main.py
```
- Admin: http://localhost:5000/  (email: `admin@alfa.com`, senha: `1234`)
- Cardápio público: http://localhost:5000/cantina-escolar-alfa/cardapio

## Onde olhar primeiro
1. `database/produto.py` — constantes, “banco” de produtos e helpers.
2. `database/usuario.py` — “banco” de usuários e funções de busca.
3. `routes/` — fluxo do app (login/painel, CRUD, cardápio).
4. `templates/` — páginas Bootstrap com comentários.

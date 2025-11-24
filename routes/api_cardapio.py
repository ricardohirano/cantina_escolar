# routes/api_cardapio.py
from flask import Blueprint, jsonify
import database.produto as db_produto

# nome do blueprint
rota_api = Blueprint("api_cardapio", __name__)


@rota_api.get("/api/cardapio")
def api_cardapio():
    """
    API pública para o Netlify consumir.
    Retorna o cardápio no formato:
    {
      "categorias": [
        { "nome": "Bebidas", "produtos": [ ... ] },
        ...
      ]
    }
    """
    produtos = db_produto.listar_produtos()

    categorias = {}

    for p in produtos:
        # só produtos disponíveis
        if not p.get("disponivel", True):
            continue

        categoria = p.get("categoria", "Outros")

        if categoria not in categorias:
            categorias[categoria] = []

        categorias[categoria].append(
            {
                "nome": p["nome"],
                "descricao": p.get("descricao", ""),
                "preco": p.get("preco", 0),
                # aqui assumindo que foto_url = "bebidas/1.png"
                "imagem": montar_caminho(p.get("foto_url", "")),
            }
        )

    resposta = {
        "categorias": [
            {"nome": cat, "produtos": lista}
            for cat, lista in categorias.items()
        ]
    }

    return jsonify(resposta)
def montar_caminho(foto_url):
    if not foto_url:
        return "/static/img/placeholder.png"

    # Corrige fotos antigas que tinham caminho completo
    foto_url = foto_url.replace("/static/foto_prod/", "")
    foto_url = foto_url.replace("static/foto_prod/", "")
    foto_url = foto_url.lstrip("/")

    return f"/static/foto_prod/{foto_url}"
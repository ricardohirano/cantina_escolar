from flask import Blueprint, render_template, request, url_for
import database.produto as db_produto
from utils.gerar_qrcode import gerar_qrcode
import os

rota_cardapio = Blueprint("cardapio", __name__)

@rota_cardapio.get("/cardapio")
def exibir_cardapio():
 #buscar produtos
    todos = [p for p in db_produto.listar_produtos() if p.get("disponivel", False)]

    categoria = request.args.get("categoria")
    termo = request.args.get("q")

    if categoria and categoria != "Todas":
        todos = [p for p in todos if p.get("categoria") == categoria]

    if termo:
        termo = termo.strip()
        todos = [p for p in todos if termo.lower() in p.get("nome", "").lower()]

    # Botar os produtos por categorias
    grupos = {}
    for p in todos:
        cat = p.get("categoria") or "Outros"
        grupos.setdefault(cat, []).append(p)

    grupos_ordenados = dict(sorted(grupos.items(), key=lambda kv: kv[0]))

    #Gerar QR Code
    url_cardapio = request.host_url.rstrip("/") + url_for("cardapio.exibir_cardapio")
    pasta_qr = os.path.join("static", "img")
    os.makedirs(pasta_qr, exist_ok=True)
    arquivo_qr = os.path.join(pasta_qr, "cardapio_qr.png")
    gerar_qrcode(url_cardapio, arquivo_qr)
    qr_code_rel = "img/cardapio_qr.png"  

    #
    return render_template(
        "cardapio_publico.html",
        CATEGORIAS=db_produto.CATEGORIAS,
        grupos=grupos_ordenados,
        filtro_categoria=categoria or "Todas",
        filtro_termo=termo or "",
        total=len(todos),
        qr_code=qr_code_rel,
    )

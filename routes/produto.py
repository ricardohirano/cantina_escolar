import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from database.produto import (
    listar_produtos,
    proximo_id_produto,
    produto_por_id,
    alternar_disponibilidade as db_alternar_disponibilidade,
    remover_produto as db_remover_produto,
    CATEGORIAS,
    PRODUTOS,
)
from werkzeug.utils import secure_filename
from PIL import Image

produto_bp = Blueprint("produto", __name__, url_prefix="/produtos")

# Extensões permitidas
EXTENSOES_PERMITIDAS = {".jpg", ".jpeg", ".png", ".webp"}

def nome_arquivo_unico(filename):
    nome, ext = os.path.splitext(filename)
    if ext.lower() not in EXTENSOES_PERMITIDAS:
        ext = ".jpg"
    nome_seguro = secure_filename(nome)
    return f"{nome_seguro}_{uuid.uuid4().hex}{ext}"

def salvar_foto(foto):
    """Salva e redimensiona imagem enviada pelo usuário"""
    nome_arquivo = nome_arquivo_unico(foto.filename)
    caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_arquivo)

    # Redimensiona para máximo 800px mantendo proporção
    img = Image.open(foto)
    img.thumbnail((800, 800))
    img.convert("RGB").save(caminho, "JPEG", optimize=True, quality=85)

    return f"/static/foto_prod/{nome_arquivo}"

@produto_bp.get("/")
def listar():
    return render_template("lista_produtos.html", produtos=listar_produtos())

@produto_bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        nome = request.form.get("nome")
        preco = float(request.form.get("preco") or 0)
        categoria = request.form.get("categoria")
        descricao = request.form.get("descricao")
        disponivel = bool(request.form.get("disponivel"))

        # Upload da imagem
        foto = request.files.get("foto")
        foto_url = None
        if foto and foto.filename:
            foto_url = salvar_foto(foto)

        PRODUTOS.append({
            "id": proximo_id_produto(),
            "nome": nome,
            "preco": preco,
            "categoria": categoria,
            "foto_url": foto_url,
            "descricao": descricao,
            "disponivel": disponivel
        })

        flash("Produto cadastrado com sucesso!", "success")
        return redirect(url_for("produto.listar"))

    return render_template("form_produto.html", categorias=CATEGORIAS, produto=None)

@produto_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    produto = produto_por_id(id)
    if not produto:
        flash("Produto não encontrado.", "error")
        return redirect(url_for("produto.listar"))

    if request.method == "POST":
        produto["nome"] = request.form.get("nome")
        produto["preco"] = float(request.form.get("preco") or 0)
        produto["categoria"] = request.form.get("categoria")
        produto["descricao"] = request.form.get("descricao")
        produto["disponivel"] = bool(request.form.get("disponivel"))

        foto = request.files.get("foto")
        if foto and foto.filename:
            produto["foto_url"] = salvar_foto(foto)

        flash("Produto atualizado com sucesso!", "success")
        return redirect(url_for("produto.listar"))

    return render_template("form_produto.html", categorias=CATEGORIAS, produto=produto)

@produto_bp.get("/excluir/<int:id>")
def excluir(id):
    ok = db_remover_produto(id)
    flash("Produto removido." if ok else "Produto não encontrado.", "success" if ok else "error")
    return redirect(url_for("produto.listar"))

@produto_bp.post("/disponibilidade/<int:id>")
def alternar_disponibilidade(id):
    ok = db_alternar_disponibilidade(id)
    flash("Disponibilidade atualizada." if ok else "Produto não encontrado.", "success" if ok else "error")
    return redirect(url_for("produto.listar"))

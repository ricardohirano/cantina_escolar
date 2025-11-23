from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import check_password_hash
from database.usuario import buscar_usuario_por_email
from utils.gerar_qrcode import gerar_qrcode
import os


home_route = Blueprint("home", __name__)
rota_home = home_route  # alias opcional


#Rota pricipal de login
@home_route.route("/", methods=["GET", "POST"])
def login_admin():
    #Se tiver conta: 
    if "usuario_id" in session:
        return redirect(url_for("home.painel_admin"))

    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        u = buscar_usuario_por_email(email)

        if not u or not check_password_hash(u["senha"], senha):
            flash("E-mail ou senha inválidos.", "danger")
            return render_template("login.html")

        if not u.get("ativo"):
            flash("Sua conta ainda não foi ativada pelo administrador.", "warning")
            return render_template("login.html")

        # cria sessão
        session.update({
            "usuario_id": u["id"],
            "usuario_nome": u["nome"],
            "tipo": u["tipo"]
        })

        return redirect(url_for("home.painel_admin"))

    return render_template("login.html")


#Rota Painel
@home_route.route("/painel")
def painel_admin():
    if session.get("tipo") not in ("admin", "moderador"):
        flash("Acesso restrito. Faça login.", "danger")
        return redirect(url_for("home.login_admin"))

    # URL pública do cardápio (Netlify)
    url_cardapio = "https://cantinasenairegistro.netlify.app/"

    # Gera o QR Code com essa URL
    pasta_qr_static = os.path.join("static", "img")
    os.makedirs(pasta_qr_static, exist_ok=True)
    arquivo_qr = os.path.join(pasta_qr_static, "cardapio_qr.png")

    gerar_qrcode(url_cardapio, arquivo_qr)
    qr_code_rel = "img/cardapio_qr.png"

    return render_template("painel.html", qr_code=qr_code_rel)


# Rota Logout
@home_route.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for("home.login_admin"))


# Rota esqueci a senha
@home_route.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    if request.method == "POST":
        email = request.form.get("email")
        flash("Se o e-mail existir, enviaremos instruções para redefinir a senha.", "info")
        return redirect(url_for("home.login_admin"))

    return render_template("esqueci_senha.html")

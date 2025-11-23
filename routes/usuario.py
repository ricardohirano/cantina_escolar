from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.usuario import criar_usuario, listar_usuarios, ativar_usuario, desativar_usuario

rota_usuario = Blueprint("usuario", __name__)

# Rota de criação de usuarios
@rota_usuario.route("/usuarios/novo", methods=["GET", "POST"])
def novo_usuario():
    if request.method == "POST":
        nome  = request.form.get("nome")
        email = request.form.get("email")
        confirma_email = request.form.get("confirma_email")
        senha = request.form.get("senha")

        if not (nome and email and confirma_email and senha):
            flash("Preencha todos os campos.", "warning")
            return render_template("usuario_form.html", usuario=None)

        if email != confirma_email:
            flash("Os e-mails não conferem.", "danger")
            return render_template("usuario_form.html", usuario=None)

        novo = criar_usuario(nome, email, senha)
        if not novo:
            flash("E-mail já cadastrado.", "danger")
            return render_template("usuario_form.html", usuario=None)

        flash("Cadastro criado! Aguarde ativação do administrador.", "success")
        return redirect(url_for("home.login_admin"))

    return render_template("usuario_form.html", usuario=None)

#Rota admin (ativar/desativar)
def exigir_admin():
    if session.get("tipo") != "admin":
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("home.login_admin"))

@rota_usuario.get("/usuarios")
def listar():
    if (resp := exigir_admin()):
        return resp
    usuarios = listar_usuarios()
    return render_template("usuarios_lista.html", usuarios=usuarios)

@rota_usuario.post("/usuarios/<int:usuario_id>/ativar")
def ativar(usuario_id):
    if (resp := exigir_admin()):
        return resp
    if ativar_usuario(usuario_id):
        flash("Usuário ativado e promovido a admin.", "success")
    else:
        flash("Usuário não encontrado.", "danger")
    return redirect(url_for("usuario.listar"))

@rota_usuario.post("/usuarios/<int:usuario_id>/desativar")
def desativar(usuario_id):
    if (resp := exigir_admin()):
        return resp
    if desativar_usuario(usuario_id):
        flash("Usuário desativado.", "warning")
    else:
        flash("Usuário não encontrado.", "danger")
    return redirect(url_for("usuario.listar"))

@rota_usuario.route("/usuarios/<int:usuario_id>/promover", methods=["POST"])
def promover(usuario_id):
    if (resp := exigir_admin()):
        return resp
    from database.usuario import promover_para_moderador
    if promover_para_moderador(usuario_id):
        flash("Usuário promovido a moderador.", "success")
    else:
        flash("Usuário não encontrado.", "danger")
    return redirect(url_for("usuario.listar"))
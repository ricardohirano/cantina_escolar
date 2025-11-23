import os
from flask import Flask, render_template
from routes.home import home_route
from routes.produto import produto_bp
from routes.cardapio import rota_cardapio
from routes.usuario import rota_usuario


def create_app():
    app = Flask(__name__)
    app.secret_key = "uma-chave-secreta-qualquer"

    # Recarga automática de templates (evita cache chato em dev)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True

    # Caminho de upload personalizado
    app.config["UPLOAD_FOLDER"] = os.path.join("static", "foto_prod")
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ===== REGISTRO DOS BLUEPRINTS =====
    app.register_blueprint(home_route)     # Login / Painel (/)
    app.register_blueprint(produto_bp)     # Produtos (/produtos)
    app.register_blueprint(rota_cardapio)  # Cardápio público (/cardapio)
    app.register_blueprint(rota_usuario)   # Usuários (/usuarios)

    # Rota teste opcional
    @app.get("/teste")
    def teste():
        return "<h2>Servidor Flask ativo!</h2>"

    # Mostrar todas as rotas no console (diagnóstico)
    with app.app_context():
        print("\n== ENDPOINTS CARREGADOS ==")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint:30s} -> {rule}")
        print("================================\n")

    return app


if __name__ == "__main__":
    app = create_app()
    # Roda na rede local para permitir acesso de outros dispositivos
    app.run(host="0.0.0.0", port=5000, debug=True)

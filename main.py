import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from routes.home import home_route
from routes.produto import produto_bp
from routes.cardapio import rota_cardapio
from routes.usuario import rota_usuario
from routes.api_cardapio import rota_api


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-key-insegura")

    # Libera a API para Netlify e Live Server (127.0.0.1:5500)
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "https://cantinasenairegistro.netlify.app",
                    "http://127.0.0.1:5500",
                ]
            }
        },
    )

    # Recarga automática de templates
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True

    # Pasta de upload das fotos (no painel)
    app.config["UPLOAD_FOLDER"] = os.path.join("static", "foto_prod")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ===== BLUEPRINTS =====
    app.register_blueprint(home_route)
    app.register_blueprint(produto_bp)
    app.register_blueprint(rota_cardapio)
    app.register_blueprint(rota_usuario)
    app.register_blueprint(rota_api)

    # (OPCIONAL) Servir os arquivos do deploy_netlify via Flask,
    # só para testar local em http://127.0.0.1:5000/deploy_netlify/cardapio.html
    @app.route("/deploy_netlify/<path:filename>")
    def netlify_static(filename):
        return send_from_directory("deploy_netlify", filename)

    print("\n=== ROTAS CARREGADAS ===")
    for r in app.url_map.iter_rules():
        print(r)
    print("=========================\n")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

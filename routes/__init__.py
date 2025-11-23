#dmdfskfdms# routes/__init__.py
from flask import Blueprint

# blueprint “produtos”
produto_bp = Blueprint("produto", __name__, url_prefix="/produtos")

# você pode importar as rotas aqui pra conectar:
from .produto import *  # noqa

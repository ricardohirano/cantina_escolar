# utils/imagem.py
import os, uuid
from PIL import Image
from werkzeug.utils import secure_filename

EXTENSOES_PERMITIDAS = {".jpg", ".jpeg", ".png", ".webp"}

def _ext_ok(nome):
    ext = os.path.splitext(nome)[1].lower()
    return ext in EXTENSOES_PERMITIDAS

def gerar_nome_unico(original, forcar_ext=None):
    base_seguro = secure_filename(os.path.splitext(original)[0]) or "img"
    ext = (forcar_ext or os.path.splitext(original)[1] or ".jpg").lower()
    if ext not in EXTENSOES_PERMITIDAS:
        ext = ".jpg"
    return f"{base_seguro}-{uuid.uuid4().hex}{ext}"

def salvar_redimensionada(stream_arquivo, caminho_destino, max_lado=800, formato="JPEG", qualidade=85):
    """
    - stream_arquivo: objeto file-like (ex.: request.files["foto"])
    - caminho_destino: caminho completo (ex.: static/foto_prod/abc.jpg)
    - max_lado: tamanho máximo de largura/altura (mantém proporção)
    - formato: "JPEG" ou "WEBP"
    """
    img = Image.open(stream_arquivo)

    # Converte para RGB se for PNG com transparência
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Redimensiona mantendo proporção
    img.thumbnail((max_lado, max_lado))  # in-place, respeita aspect ratio

    params = {}
    if formato.upper() == "JPEG":
        params["optimize"] = True
        params["quality"] = qualidade
        params["progressive"] = True
    elif formato.upper() == "WEBP":
        params["quality"] = qualidade
        params["method"] = 6  # melhor compressão

    # Garante diretório
    os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)

    img.save(caminho_destino, formato, **params)
    return True

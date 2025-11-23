import qrcode
import os

def gerar_qrcode(url: str, caminho_arquivo: str) -> str:

    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

    # cria o QR Code
    qr = qrcode.QRCode(
        version=1,  # tamanho automático
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    # adiciona os dados e gera a imagem
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # salva a imagem 
    img.save(caminho_arquivo)
    return caminho_arquivo

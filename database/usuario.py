# database/usuario.py
from werkzeug.security import generate_password_hash

USUARIOS = [
    {
        "id": 1,
        "nome": "Ricardo",
        "email": "ricardo@teste.com",
        "senha": "scrypt:32768:8:1$zH7cDAFaSrfHwnEi$256c638809b162d7290de7018e67a274ccdd2b0b9fe6676d6ca86bca7bb07e69ac0fe25b55f833d311b16a01808ade7b7ffa89ae902282f698f3d357612bace0",
        "tipo": "admin",
        "ativo": True
    },
    {
        "id": 2,
        "nome": "Hildo",
        "email": "hildo@teste.com",
        "senha": "scrypt:32768:8:1$zH7cDAFaSrfHwnEi$256c638809b162d7290de7018e67a274ccdd2b0b9fe6676d6ca86bca7bb07e69ac0fe25b55f833d311b16a01808ade7b7ffa89ae902282f698f3d357612bace0",
        "tipo": "admin",
        "ativo": True
    }
]

def buscar_usuario_por_email(usuario_email):
    for u in USUARIOS:
        if u.get("email") == usuario_email:
            return u
    return None

def buscar_usuario_por_id(usuario_id):
    for u in USUARIOS:
        if u.get("id") == usuario_id:
            return u
    return None

def proximo_id_usuario():
    if not USUARIOS:
        return 1
    return max(u["id"] for u in USUARIOS) + 1

def criar_usuario(nome, email, senha_plana):
   
    if buscar_usuario_por_email(email):
        return None

    existe_admin = any(u.get("ativo") and u.get("tipo") == "admin" for u in USUARIOS)

    if not existe_admin:
        tipo = "admin"
        ativo = True
    else:
        tipo = "pendente"
        ativo = False

    novo = {
        "id": proximo_id_usuario(),
        "nome": nome,
        "email": email,
        "senha": generate_password_hash(senha_plana),
        "tipo": tipo,
        "ativo": ativo
    }
    USUARIOS.append(novo)
    return novo


def promover_para_moderador(usuario_id):
    u = buscar_usuario_por_id(usuario_id)
    if not u:
        return False
    u["tipo"] = "moderador"
    u["ativo"] = True
    return True

# uso do admin

def listar_usuarios():
    return sorted(USUARIOS, key=lambda u: (not u.get("ativo", False), u.get("nome","")))

def ativar_usuario(usuario_id):
    u = buscar_usuario_por_id(usuario_id)
    if not u:
        return False
    u["ativo"] = True
    if u.get("tipo") == "pendente":
        u["tipo"] = "admin"  
    return True

def desativar_usuario(usuario_id):
    u = buscar_usuario_por_id(usuario_id)
    if not u:
        return False
    u["ativo"] = False
    return True

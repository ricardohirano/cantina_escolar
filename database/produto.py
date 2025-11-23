CATEGORIAS = ["Bebidas", "Sobremesas", "Salgados", "Refeicoes", "Sorvetes", "Outros"]

PRODUTOS = [
    {
        "id": 1,
        "nome": "Pão de Queijo",
        "preco": 6.50,
        "categoria": "Salgados",
        "foto_url": "pao_queijo.jpg",  
        "disponivel": True,
        "descricao": "Tradicional, quentinho e crocante por fora."
    },
    {
        "id": 2,
        "nome": "Suco Natural",
        "preco": 5.00,
        "categoria": "Bebidas",
        "foto_url": "suco_natural.jpg",
        "disponivel": True,
        "descricao": "Feito com frutas frescas e sem conservantes."
    },
    {
        "id": 3,
        "nome": "Brigadeiro",
        "preco": 3.00,
        "categoria": "Sobremesas",
        "foto_url": "brigadeiro.jpg",
        "disponivel": True,
        "descricao": "Clássico de chocolate com granulado."
    }
]


def proximo_id_produto():
    if not PRODUTOS:

        return 1
    return max(p.get("id", 0) for p in PRODUTOS) + 1


def listar_produtos():
    PRODUTOS.sort(key=lambda x: (x.get("categoria") or "Outros", x.get("nome") or ""))
    return PRODUTOS


def produto_por_id(produto_id):
    for p in PRODUTOS:
        if p.get("id") == produto_id:
            return p
    return None


def alternar_disponibilidade(produto_id):
    p = produto_por_id(produto_id)
    if not p:
        return False
    p["disponivel"] = not p.get("disponivel", True)
    return True


def remover_produto(produto_id):
    p = produto_por_id(produto_id)
    if not p:
        return False
    PRODUTOS.remove(p)
    return True

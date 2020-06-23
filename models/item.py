class Item:
    def __init__(self, Produtos, qtd_produto, id_pedido, id=None):
        self.id = id
        self.Produtos = Produtos
        self.qtd_produto = qtd_produto
        self.id_pedido = id_pedido

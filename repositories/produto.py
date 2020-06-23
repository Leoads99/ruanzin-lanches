from models.produto import Produto


class ProdutoRepository:
    def __init__(self, db):
        self.__db = db

    def get(self, id=None):
        cursor = self.__db.connection.cursor()
        if (id):
            sql_command = "SELECT id, nome, preco_unitario from produto WHERE id = %s"

            cursor.execute(sql_command, (id,))

            tupla = cursor.fetchone()

            clientes = Produto(tupla[1], tupla[2], id=tupla[0])
        else:
            sql_command = "SELECT id, nome, preco_unitario from produto"
            cursor.execute(sql_command)
            clientes = self.transform_produto(cursor.fetchall())

        return clientes

    def save(self, produto):
        cursor = self.__db.connection.cursor()

        if(produto.id):
            sql_command = "UPDATE produto SET nome=%s, preco_unitario=%s where id=%s"
            cursor.execute(sql_command, (produto.nome,
                                         produto.preco_unitario, produto.id))
        else:
            sql_command = "INSERT INTO produto(nome, preco_unitario) VALUES (%s, %s)"
            cursor.execute(sql_command, (produto.nome,
                                         produto.preco_unitario))

        self.__db.connection.commit()

        return produto

    def delete(self, id):
        cursor = self.__db.connection.cursor()
        sql_command = "DELETE FROM produto WHERE id = %s"
        cursor.execute(sql_command, (id,))

        self.__db.connection.commit()

    def transform_produto(self, produto):
        def create_produto_tuple(tupla):
            return Produto(tupla[1], tupla[2], id=tupla[0])
        return list(map(create_produto_tuple, produto))

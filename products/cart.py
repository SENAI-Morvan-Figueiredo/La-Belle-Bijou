from decimal import Decimal

class Cart:
    def __init__(self, request):
        self.session = request.session # salva a sessão do usuário
        cart = self.session.get("cart") # procura se já tem um carrinho na sessão
        if not cart:
            cart = self.session["cart"] = {} # se não tiver cria um dicionário vazio
        self.cart = cart # salva em self.cart

    def add(self, produto, quantidade=1, override=False):
        produto_id = str(produto.id) # transforma o id do produto em string (request.session só trabalha bem com chaves de texto)
        if produto_id not in self.cart: # se o produto não estiver no carrinho
            self.cart[produto_id] = { # adiciona as informações do produto
                "nome": produto.nome,
                "quantidade": 0,
                "preco": str(produto.preco),
                "imagem": produto.imagem_principal.url if produto.imagem_principal else "",
            }
        if override:
            self.cart[produto_id]["quantidade"] = quantidade
        else: # se o produto já estiver no carrinho adiciona 1 na quantidade
            self.cart[produto_id]["quantidade"] += quantidade
        print(self.session["cart"])
        self.save() # salva na sessão

    def remove(self, produto):
        produto_id = str(produto.id) # transforma o id do produto em string (request.session só trabalha bem com chaves de texto)
        if produto_id in self.cart:
            del self.cart[produto_id] # deleta o produto do carrinho
            self.save() # salva na sessão

    def save(self): # função para salvar alterações na sessão
        self.session["cart"] = self.cart # define o carrinho da sessão como sendo o carrinho atualizado
        self.session.modified = True # salva na sessão

    def clear(self): # função para limpar o carrinho
        self.session["cart"] = {} # define o carrinho da sessão como sendo vazio
        self.session.modified = True # salva na sessão

    def __iter__(self): # função padrão do python que define como um objeto será tratado em um loop
        for produto_id, item in self.cart.items(): # percorre cada produto no carrinho
            item = item.copy()  # faz uma cópia de cada informação dos produtos
            item["id"] = int(produto_id)
            item["preco"] = Decimal(item["preco"])
            item["total"] = item["preco"] * item["quantidade"] # faz o calculo do preço total daquele produto de acordo com a quantidade
            yield item

    def __len__(self): # função padrão do python chamada ao usar o comando .len
        return sum(item["quantidade"] for item in self.cart.values()) # faz a soma de todos os itens no carrinho

    def get_total_price(self): # função para calcular o valor total do pedido
        return sum(
            Decimal(item["preco"]) * item["quantidade"]
            for item in self.cart.values()
        )
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from services import (
    autenticar,
    listar_produtos,
    criar_produto,
    atualizar_produto,
    remover_produto,
    obter_produto,
    listar_clientes,
    criar_cliente,
    atualizar_cliente,
    remover_cliente,
    obter_cliente,
    obter_cliente_por_cpf,
    listar_pedidos_por_cliente,
    ItemCarrinho,
    calcular_resumo_carrinho,
    criar_venda,
    listar_vendas,
    estoque_baixo,
    relatorio_mensal_por_vendedor,
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

COR_MENU = "#0B1320"
COR_CARD = "#0F1B2D"
COR_BOTAO = "#1EC28B"
COR_HOVER = "#17A377"
COR_DESTAQUE = "#4FC3F7"

NOME_MERCADO = "Mercado TechPlus"
NOME_SISTEMA = "MercadoTech PDV"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{NOME_SISTEMA} — {NOME_MERCADO}")
        self.geometry("1420x820")
        self.minsize(1360, 780)

        self.usuario_logado = None
        self.carrinho = []
        self.cliente_selecionado = None
        self.ultima_busca_produtos_venda = []

        self.tela_login()

    # Limpa todos os widgets da janela principal.
    def limpar(self):
        for widget in self.winfo_children():
            widget.destroy()

    # Limpa apenas o conteudo central da tela principal.
    def limpar_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    # Converte texto monetario em numero decimal.
    def _parse_float(self, valor: str) -> float:
        valor = valor.strip().replace("R$", "").replace(" ", "").replace(",", ".")
        return float(valor)

    # Converte texto numerico em inteiro.
    def _parse_int(self, valor: str) -> int:
        return int(valor.strip())

    # Limpa os campos do formulario de produtos.
    def _limpar_form_produtos(self):
        self.p_id.delete(0, "end")
        self.p_nome.delete(0, "end")
        self.p_categoria.delete(0, "end")
        self.p_preco.delete(0, "end")
        self.p_qtd.delete(0, "end")
        self.p_cb.delete(0, "end")
        self.p_mari.set("0")
        self.p_data.delete(0, "end")
        self.p_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.p_nome.focus_set()

    # Limpa os campos do formulario de clientes.
    def _limpar_form_clientes(self):
        self.c_id.delete(0, "end")
        self.c_nome.delete(0, "end")
        self.c_cpf.delete(0, "end")
        self.c_tel.delete(0, "end")
        self.c_cidade.delete(0, "end")
        self.flag_fla.deselect()
        self.flag_op.deselect()
        self.flag_sousa.deselect()
        self.c_nome.focus_set()

    # Monta a tela de autenticacao do sistema.
    def tela_login(self):
        self.limpar()

        frame = ctk.CTkFrame(self, fg_color=COR_MENU)
        frame.pack(expand=True, fill="both")

        ctk.CTkLabel(
            frame,
            text=NOME_SISTEMA,
            font=("Arial", 30, "bold"),
            text_color=COR_DESTAQUE
        ).pack(pady=18)

        ctk.CTkLabel(
            frame,
            text=f"{NOME_MERCADO} • Parte 2",
            font=("Arial", 14),
            text_color="white"
        ).pack(pady=(0, 22))

        self.usuario_entry = ctk.CTkEntry(frame, placeholder_text="Usuario", width=280)
        self.usuario_entry.pack(pady=8)

        self.senha_entry = ctk.CTkEntry(frame, placeholder_text="Senha", show="*", width=280)
        self.senha_entry.pack(pady=8)

        ctk.CTkButton(
            frame,
            text="Entrar",
            fg_color=COR_BOTAO,
            hover_color=COR_HOVER,
            text_color="black",
            command=self._login,
            width=220
        ).pack(pady=16)

        ctk.CTkLabel(
            frame,
            text="Usuario padrao: admin | senha: 1234",
            font=("Arial", 12),
            text_color="#B0BEC5"
        ).pack(pady=10)

    # Valida o login e abre a tela principal.
    def _login(self):
        usuario = self.usuario_entry.get().strip()
        senha = self.senha_entry.get().strip()

        try:
            info = autenticar(usuario, senha)
            if not info:
                messagebox.showerror("Erro", "Usuario ou senha invalidos.")
                return

            self.usuario_logado = info
            self.tela_principal()

        except Exception as exc:
            messagebox.showerror("Erro", f"Falha ao conectar no banco: {exc}")

    # Monta a estrutura principal do sistema apos o login.
    def tela_principal(self):
        self.limpar()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        menu = ctk.CTkFrame(self, width=250, fg_color=COR_MENU, corner_radius=0)
        menu.grid(row=0, column=0, sticky="ns")
        menu.grid_propagate(False)

        ctk.CTkLabel(
            menu,
            text=NOME_SISTEMA,
            text_color=COR_DESTAQUE,
            font=("Arial", 18, "bold")
        ).pack(pady=(18, 6))

        ctk.CTkLabel(
            menu,
            text=f"Ola, {self.usuario_logado['nome']}",
            text_color="white",
            font=("Arial", 12)
        ).pack(pady=(0, 6))

        ctk.CTkLabel(
            menu,
            text=f"Perfil: {self.usuario_logado.get('perfil', 'N/A')}",
            text_color="#B0BEC5",
            font=("Arial", 11)
        ).pack(pady=(0, 18))

        btn_style = {
            "fg_color": COR_BOTAO,
            "hover_color": COR_HOVER,
            "text_color": "black",
            "width": 200
        }

        ctk.CTkButton(menu, text="Vendas", command=self.tela_vendas, **btn_style).pack(pady=8)
        ctk.CTkButton(menu, text="Produtos", command=self.tela_produtos, **btn_style).pack(pady=8)
        ctk.CTkButton(menu, text="Clientes", command=self.tela_clientes, **btn_style).pack(pady=8)
        ctk.CTkButton(menu, text="Consultas", command=self.tela_consultas, **btn_style).pack(pady=8)
        ctk.CTkButton(menu, text="Relatorios", command=self.tela_relatorios, **btn_style).pack(pady=8)

        ctk.CTkButton(
            menu,
            text="Sair",
            fg_color="#EF5350",
            hover_color="#D84343",
            text_color="white",
            command=self.tela_login,
            width=200
        ).pack(pady=26)

        self.conteudo = ctk.CTkFrame(self, fg_color=COR_CARD)
        self.conteudo.grid(row=0, column=1, sticky="nsew")

        self.tela_vendas()

    # Monta a tela de cadastro e manutencao de produtos.
    def tela_produtos(self):
        self.limpar_conteudo()

        ctk.CTkLabel(
            self.conteudo,
            text="Produtos",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(pady=14)

        form = ctk.CTkFrame(self.conteudo, fg_color=COR_MENU)
        form.pack(pady=10, padx=16, fill="x")

        self.p_id = ctk.CTkEntry(form, placeholder_text="ID", width=100)
        self.p_id.grid(row=0, column=0, padx=8, pady=8)

        self.p_nome = ctk.CTkEntry(form, placeholder_text="Nome", width=220)
        self.p_nome.grid(row=0, column=1, padx=8, pady=8)

        self.p_categoria = ctk.CTkEntry(form, placeholder_text="Categoria", width=180)
        self.p_categoria.grid(row=0, column=2, padx=8, pady=8)

        self.p_preco = ctk.CTkEntry(form, placeholder_text="Preco", width=120)
        self.p_preco.grid(row=0, column=3, padx=8, pady=8)

        self.p_qtd = ctk.CTkEntry(form, placeholder_text="Quantidade", width=120)
        self.p_qtd.grid(row=0, column=4, padx=8, pady=8)

        self.p_cb = ctk.CTkEntry(form, placeholder_text="Codigo de barras", width=220)
        self.p_cb.grid(row=1, column=1, padx=8, pady=8)

        self.p_mari = ctk.CTkOptionMenu(form, values=["0", "1"], width=120)
        self.p_mari.grid(row=1, column=2, padx=8, pady=8)
        self.p_mari.set("0")

        self.p_data = ctk.CTkEntry(form, placeholder_text="Data cadastro (YYYY-MM-DD)", width=200)
        self.p_data.grid(row=1, column=3, padx=8, pady=8)
        self.p_data.insert(0, datetime.now().strftime("%Y-%m-%d"))

        btns = ctk.CTkFrame(form, fg_color="transparent")
        btns.grid(row=1, column=4, padx=8, pady=8)

        ctk.CTkButton(
            btns,
            text="Salvar",
            fg_color=COR_BOTAO,
            hover_color=COR_HOVER,
            text_color="black",
            command=self._salvar_produto,
            width=140
        ).pack(pady=4)

        ctk.CTkButton(
            btns,
            text="Carregar",
            fg_color=COR_DESTAQUE,
            hover_color="#2DA7D7",
            text_color="black",
            command=self._carregar_produto,
            width=140
        ).pack(pady=4)

        ctk.CTkButton(
            btns,
            text="Excluir",
            fg_color="#FFA726",
            hover_color="#FB8C00",
            text_color="black",
            command=self._excluir_produto,
            width=140
        ).pack(pady=4)

        self.lista_produtos = ctk.CTkTextbox(self.conteudo, width=1050, height=500)
        self.lista_produtos.pack(pady=10, padx=16, fill="both", expand=True)

        self._atualizar_lista_produtos()

    # Salva um novo produto ou atualiza um existente.
    def _salvar_produto(self):
        try:
            dados = {
                "nome": self.p_nome.get().strip(),
                "categoria": self.p_categoria.get().strip(),
                "preco": self._parse_float(self.p_preco.get()),
                "quantidade": self._parse_int(self.p_qtd.get()),
                "codigo_barras": self.p_cb.get().strip() or None,
                "fabricado_em_mari": self.p_mari.get() == "1",
                "data_cadastro": self.p_data.get().strip(),
            }

            if not dados["nome"] or not dados["categoria"]:
                messagebox.showerror("Erro", "Nome e categoria sao obrigatorios.")
                return

            produto_id = self.p_id.get().strip()

            if produto_id:
                atualizar_produto(int(produto_id), dados)
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
            else:
                criar_produto(dados)
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.")

            self._atualizar_lista_produtos()
            self._limpar_form_produtos()

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Carrega os dados de um produto pelo ID informado.
    def _carregar_produto(self):
        try:
            produto_id = int(self.p_id.get().strip())
            produto = obter_produto(produto_id)

            if not produto:
                messagebox.showerror("Erro", "Produto nao encontrado.")
                return

            self.p_nome.delete(0, "end")
            self.p_nome.insert(0, produto["nome"])

            self.p_categoria.delete(0, "end")
            self.p_categoria.insert(0, produto["categoria"])

            self.p_preco.delete(0, "end")
            self.p_preco.insert(0, str(produto["preco"]))

            self.p_qtd.delete(0, "end")
            self.p_qtd.insert(0, str(produto["quantidade"]))

            self.p_cb.delete(0, "end")
            self.p_cb.insert(0, produto.get("codigo_barras") or "")

            self.p_mari.set("1" if int(produto["fabricado_em_mari"]) == 1 else "0")

            self.p_data.delete(0, "end")
            self.p_data.insert(0, str(produto["data_cadastro"]))

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Exclui um produto pelo ID informado.
    def _excluir_produto(self):
        try:
            produto_id = int(self.p_id.get().strip())
            remover_produto(produto_id)
            messagebox.showinfo("Sucesso", "Produto removido com sucesso.")
            self._atualizar_lista_produtos()
            self._limpar_form_produtos()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Atualiza a listagem de produtos na interface.
    def _atualizar_lista_produtos(self, filtros=None):
        produtos = listar_produtos(filtros or {})

        self.lista_produtos.configure(state="normal")
        self.lista_produtos.delete("1.0", "end")
        self.lista_produtos.insert("end", "ID | Nome | Categoria | Preco | Quantidade | Mari | Data\n")
        self.lista_produtos.insert("end", "-" * 115 + "\n")

        for produto in produtos:
            self.lista_produtos.insert(
                "end",
                f"{produto['id']} | {produto['nome']} | {produto['categoria']} | "
                f"R$ {float(produto['preco']):.2f} | {produto['quantidade']} | "
                f"{produto['fabricado_em_mari']} | {produto['data_cadastro']}\n"
            )

        self.lista_produtos.configure(state="disabled")

    # Monta a tela de cadastro e consulta de clientes.
    def tela_clientes(self):
        self.limpar_conteudo()

        ctk.CTkLabel(
            self.conteudo,
            text="Clientes",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(pady=14)

        form = ctk.CTkFrame(self.conteudo, fg_color=COR_MENU)
        form.pack(pady=10, padx=16, fill="x")

        self.c_id = ctk.CTkEntry(form, placeholder_text="ID", width=100)
        self.c_id.grid(row=0, column=0, padx=8, pady=8)

        self.c_nome = ctk.CTkEntry(form, placeholder_text="Nome", width=200)
        self.c_nome.grid(row=0, column=1, padx=8, pady=8)

        self.c_cpf = ctk.CTkEntry(form, placeholder_text="CPF", width=180)
        self.c_cpf.grid(row=0, column=2, padx=8, pady=8)

        self.c_tel = ctk.CTkEntry(form, placeholder_text="Telefone", width=160)
        self.c_tel.grid(row=0, column=3, padx=8, pady=8)

        self.c_cidade = ctk.CTkEntry(form, placeholder_text="Cidade", width=160)
        self.c_cidade.grid(row=0, column=4, padx=8, pady=8)

        flags = ctk.CTkFrame(form, fg_color="transparent")
        flags.grid(row=1, column=0, columnspan=5, padx=8, pady=8, sticky="w")

        self.flag_fla = ctk.CTkCheckBox(flags, text="Torce Flamengo")
        self.flag_fla.grid(row=0, column=0, padx=10)

        self.flag_op = ctk.CTkCheckBox(flags, text="Assiste One Piece")
        self.flag_op.grid(row=0, column=1, padx=10)

        self.flag_sousa = ctk.CTkCheckBox(flags, text="E de Sousa")
        self.flag_sousa.grid(row=0, column=2, padx=10)

        botoes = ctk.CTkFrame(form, fg_color="transparent")
        botoes.grid(row=0, column=5, rowspan=2, padx=8, pady=8)

        ctk.CTkButton(
            botoes,
            text="Salvar",
            fg_color=COR_BOTAO,
            hover_color=COR_HOVER,
            text_color="black",
            command=self._salvar_cliente,
            width=140
        ).pack(pady=4)

        ctk.CTkButton(
            botoes,
            text="Carregar",
            fg_color=COR_DESTAQUE,
            hover_color="#2DA7D7",
            text_color="black",
            command=self._carregar_cliente,
            width=140
        ).pack(pady=4)

        ctk.CTkButton(
            botoes,
            text="Excluir",
            fg_color="#FFA726",
            hover_color="#FB8C00",
            text_color="black",
            command=self._excluir_cliente,
            width=140
        ).pack(pady=4)

        busca = ctk.CTkFrame(self.conteudo, fg_color=COR_MENU)
        busca.pack(pady=8, padx=16, fill="x")

        self.busca_cliente = ctk.CTkEntry(busca, placeholder_text="Pesquisar cliente por nome ou CPF", width=300)
        self.busca_cliente.grid(row=0, column=0, padx=8, pady=8)

        ctk.CTkButton(
            busca,
            text="Pesquisar",
            fg_color=COR_BOTAO,
            hover_color=COR_HOVER,
            text_color="black",
            command=self._pesquisar_clientes,
            width=160
        ).grid(row=0, column=1, padx=8, pady=8)

        ctk.CTkButton(
            busca,
            text="Listar todos",
            fg_color=COR_DESTAQUE,
            hover_color="#2DA7D7",
            text_color="black",
            command=self._atualizar_lista_clientes,
            width=160
        ).grid(row=0, column=2, padx=8, pady=8)

        self.lista_clientes = ctk.CTkTextbox(self.conteudo, width=1050, height=280)
        self.lista_clientes.pack(pady=8, padx=16, fill="both", expand=True)

        consulta = ctk.CTkFrame(self.conteudo, fg_color=COR_MENU)
        consulta.pack(pady=8, padx=16, fill="x")

        self.consulta_cpf = ctk.CTkEntry(consulta, placeholder_text="CPF para consultar dados e pedidos", width=260)
        self.consulta_cpf.grid(row=0, column=0, padx=8, pady=8)

        ctk.CTkButton(
            consulta,
            text="Consultar cliente",
            fg_color=COR_BOTAO,
            hover_color=COR_HOVER,
            text_color="black",
            command=self._consultar_cliente_pedidos,
            width=180
        ).grid(row=0, column=1, padx=8, pady=8)

        self.box_pedidos_cliente = ctk.CTkTextbox(self.conteudo, width=1050, height=220)
        self.box_pedidos_cliente.pack(pady=8, padx=16, fill="both", expand=True)

        self._atualizar_lista_clientes()

    # Salva um novo cliente ou atualiza um existente.
    def _salvar_cliente(self):
        try:
            dados = {
                "nome": self.c_nome.get().strip(),
                "cpf": self.c_cpf.get().strip(),
                "telefone": self.c_tel.get().strip() or None,
                "cidade": self.c_cidade.get().strip() or None,
                "torce_flamengo": self.flag_fla.get() == 1,
                "assiste_one_piece": self.flag_op.get() == 1,
                "eh_de_sousa": self.flag_sousa.get() == 1,
            }

            if not dados["nome"] or not dados["cpf"]:
                messagebox.showerror("Erro", "Nome e CPF sao obrigatorios.")
                return

            cliente_id = self.c_id.get().strip()

            if cliente_id:
                atualizar_cliente(int(cliente_id), dados)
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso.")
            else:
                criar_cliente(dados)
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso.")

            self._atualizar_lista_clientes()
            self._limpar_form_clientes()

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Carrega os dados de um cliente pelo ID informado.
    def _carregar_cliente(self):
        try:
            cliente_id = int(self.c_id.get().strip())
            cliente = obter_cliente(cliente_id)

            if not cliente:
                messagebox.showerror("Erro", "Cliente nao encontrado.")
                return

            self.c_nome.delete(0, "end")
            self.c_nome.insert(0, cliente["nome"])

            self.c_cpf.delete(0, "end")
            self.c_cpf.insert(0, cliente["cpf"])

            self.c_tel.delete(0, "end")
            self.c_tel.insert(0, cliente["telefone"] or "")

            self.c_cidade.delete(0, "end")
            self.c_cidade.insert(0, cliente["cidade"] or "")

            if int(cliente["torce_flamengo"]) == 1:
                self.flag_fla.select()
            else:
                self.flag_fla.deselect()

            if int(cliente["assiste_one_piece"]) == 1:
                self.flag_op.select()
            else:
                self.flag_op.deselect()

            if int(cliente["eh_de_sousa"]) == 1:
                self.flag_sousa.select()
            else:
                self.flag_sousa.deselect()

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Exclui um cliente pelo ID informado.
    def _excluir_cliente(self):
        try:
            cliente_id = int(self.c_id.get().strip())
            remover_cliente(cliente_id)
            messagebox.showinfo("Sucesso", "Cliente removido com sucesso.")
            self._atualizar_lista_clientes()
            self._limpar_form_clientes()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Executa a pesquisa de clientes pelo termo informado.
    def _pesquisar_clientes(self):
        termo = self.busca_cliente.get().strip() or None
        self._atualizar_lista_clientes(termo)

    # Atualiza a listagem de clientes na interface.
    def _atualizar_lista_clientes(self, termo=None):
        clientes = listar_clientes(termo)

        self.lista_clientes.configure(state="normal")
        self.lista_clientes.delete("1.0", "end")
        self.lista_clientes.insert("end", "ID | Nome | CPF | Telefone | Cidade | Flamengo | One Piece | Sousa\n")
        self.lista_clientes.insert("end", "-" * 120 + "\n")

        for cliente in clientes:
            self.lista_clientes.insert(
                "end",
                f"{cliente['id']} | {cliente['nome']} | {cliente['cpf']} | {cliente['telefone'] or '-'} | "
                f"{cliente['cidade'] or '-'} | {cliente['torce_flamengo']} | "
                f"{cliente['assiste_one_piece']} | {cliente['eh_de_sousa']}\n"
            )

        self.lista_clientes.configure(state="disabled")

    # Exibe os dados e pedidos de um cliente consultado por CPF.
    def _consultar_cliente_pedidos(self):
        try:
            cpf = self.consulta_cpf.get().strip()
            if not cpf:
                messagebox.showerror("Erro", "Informe o CPF do cliente.")
                return

            cliente = obter_cliente_por_cpf(cpf)
            if not cliente:
                messagebox.showerror("Erro", "Cliente nao encontrado.")
                return

            pedidos = listar_pedidos_por_cliente(int(cliente["id"]))

            self.box_pedidos_cliente.configure(state="normal")
            self.box_pedidos_cliente.delete("1.0", "end")
            self.box_pedidos_cliente.insert(
                "end",
                f"Cliente: {cliente['nome']} | CPF: {cliente['cpf']} | Telefone: {cliente['telefone'] or '-'} | Cidade: {cliente['cidade'] or '-'}\n"
            )
            self.box_pedidos_cliente.insert("end", "-" * 130 + "\n")
            self.box_pedidos_cliente.insert("end", "Pedidos realizados:\n")

            if not pedidos:
                self.box_pedidos_cliente.insert("end", "(nenhum pedido encontrado)\n")
            else:
                for pedido in pedidos:
                    self.box_pedidos_cliente.insert(
                        "end",
                        f"Venda #{pedido['id']} | {pedido['data_hora']} | "
                        f"Forma: {pedido['forma_pagamento']} | Status: {pedido['status_pagamento']} | "
                        f"Subtotal: R$ {float(pedido['subtotal']):.2f} | "
                        f"Desconto: R$ {float(pedido['desconto']):.2f} | "
                        f"Total: R$ {float(pedido['total']):.2f} | "
                        f"Vendedor: {pedido['vendedor_nome']}\n"
                    )

            self.box_pedidos_cliente.configure(state="disabled")

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Monta a tela de filtros e consultas de produtos.
    def tela_consultas(self):
        self.limpar_conteudo()

        ctk.CTkLabel(
            self.conteudo,
            text="Consultas de Produtos",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(pady=14)

        filtros = ctk.CTkFrame(self.conteudo, fg_color=COR_MENU)
        filtros.pack(pady=10, padx=16, fill="x")

        self.f_nome = ctk.CTkEntry(filtros, placeholder_text="Nome contem", width=220)
        self.f_nome.grid(row=0, column=0, padx=8, pady=8)

        self.f_cat = ctk.CTkEntry(filtros, placeholder_text="Categoria", width=180)
        self.f_cat.grid(row=0, column=1, padx=8, pady=8)

        self.f_min = ctk.CTkEntry(filtros, placeholder_text="Preco minimo", width=120)
        self.f_min.grid(row=0, column=2, padx=8, pady=8)

        self.f_max = ctk.CTkEntry(filtros, placeholder_text="Preco maximo", width=120)
        self.f_max.grid(row=0, column=3, padx=8, pady=8)

        self.f_mari = ctk.CTkOptionMenu(filtros, values=["(qualquer)", "0", "1"], width=120)
        self.f_mari.grid(row=0, column=4, padx=8, pady=8)
        self.f_mari.set("(qualquer)")

        ctk.CTkButton(
            filtros,
            text="Aplicar filtros",
            fg_color=COR_BOTAO,
            hover_color=COR_HOVER,
            text_color="black",
            command=self._aplicar_filtros,
            width=150
        ).grid(row=0, column=5, padx=8, pady=8)

        ctk.CTkButton(
            filtros,
            text="Estoque baixo",
            fg_color=COR_DESTAQUE,
            hover_color="#2DA7D7",
            text_color="black",
            command=self._mostrar_estoque_baixo,
            width=160
        ).grid(row=0, column=6, padx=8, pady=8)

        self.lista_consultas = ctk.CTkTextbox(self.conteudo, width=1050, height=540)
        self.lista_consultas.pack(pady=10, padx=16, fill="both", expand=True)

        self._aplicar_filtros()

    # Aplica os filtros de consulta de produtos.
    def _aplicar_filtros(self):
        try:
            filtros = {}

            if self.f_nome.get().strip():
                filtros["nome"] = self.f_nome.get().strip()

            if self.f_cat.get().strip():
                filtros["categoria"] = self.f_cat.get().strip()

            if self.f_min.get().strip():
                filtros["preco_min"] = float(self.f_min.get().replace(",", "."))

            if self.f_max.get().strip():
                filtros["preco_max"] = float(self.f_max.get().replace(",", "."))

            if self.f_mari.get() in ("0", "1"):
                filtros["fabricado_em_mari"] = self.f_mari.get() == "1"

            produtos = listar_produtos(filtros)

            self.lista_consultas.configure(state="normal")
            self.lista_consultas.delete("1.0", "end")
            self.lista_consultas.insert("end", "ID | Nome | Categoria | Preco | Quantidade | Mari\n")
            self.lista_consultas.insert("end", "-" * 100 + "\n")

            if not produtos:
                self.lista_consultas.insert("end", "(sem resultados)\n")
            else:
                for produto in produtos:
                    self.lista_consultas.insert(
                        "end",
                        f"{produto['id']} | {produto['nome']} | {produto['categoria']} | "
                        f"R$ {float(produto['preco']):.2f} | {produto['quantidade']} | "
                        f"{produto['fabricado_em_mari']}\n"
                    )

            self.lista_consultas.configure(state="disabled")

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Exibe os produtos retornados pela view de estoque baixo.
    def _mostrar_estoque_baixo(self):
        try:
            produtos = estoque_baixo()

            self.lista_consultas.configure(state="normal")
            self.lista_consultas.delete("1.0", "end")
            self.lista_consultas.insert("end", "Produtos com estoque inferior a 5 unidades\n")
            self.lista_consultas.insert("end", "-" * 100 + "\n")

            if not produtos:
                self.lista_consultas.insert("end", "(nenhum produto com estoque baixo)\n")
            else:
                for produto in produtos:
                    self.lista_consultas.insert(
                        "end",
                        f"{produto['id']} | {produto['nome']} | {produto['categoria']} | "
                        f"R$ {float(produto['preco']):.2f} | Quantidade: {produto['quantidade']} | "
                        f"Mari: {produto['fabricado_em_mari']}\n"
                    )

            self.lista_consultas.configure(state="disabled")

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Monta a tela de vendas do sistema.
    def tela_vendas(self):
        self.limpar_conteudo()

        ctk.CTkLabel(
            self.conteudo,
            text="Vendas",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(pady=14)

        info = ctk.CTkFrame(self.conteudo, fg_color=COR_MENU)
        info.pack(pady=(0, 10), padx=16, fill="x")

        self.v_vendedor_lbl = ctk.CTkLabel(
            info,
            text=f"Vendedor responsavel: {self.usuario_logado['nome']} | Perfil: {self.usuario_logado.get('perfil', 'N/A')}",
            text_color="white",
            font=("Arial", 13, "bold")
        )
        self.v_vendedor_lbl.pack(anchor="w", padx=12, pady=10)

        top = ctk.CTkFrame(self.conteudo, fg_color=COR_MENU)
        top.pack(pady=10, padx=16, fill="x")

        self.v_cpf = ctk.CTkEntry(top, placeholder_text="CPF do cliente", width=220)
        self.v_cpf.grid(row=0, column=0, padx=8, pady=8)
        if self.cliente_selecionado:
            self.v_cpf.insert(0, self.cliente_selecionado["cpf"])

        ctk.CTkButton(
            top,
            text="Buscar cliente",
            fg_color=COR_DESTAQUE,
            hover_color="#2DA7D7",
            text_color="black",
            command=self._buscar_cliente,
            width=160
        ).grid(row=0, column=1, padx=8, pady=8)

        cliente_texto = "Cliente: nao selecionado"
        if self.cliente_selecionado:
            cliente_texto = f"Cliente: {self.cliente_selecionado['nome']} (ID={self.cliente_selecionado['id']})"

        self.v_cliente_lbl = ctk.CTkLabel(top, text=cliente_texto, text_color="white")
        self.v_cliente_lbl.grid(row=0, column=2, padx=8, pady=8, sticky="w")

        mid = ctk.CTkFrame(self.conteudo, fg_color=COR_MENU)
        mid.pack(pady=10, padx=16, fill="x")

        self.v_prod_id = ctk.CTkEntry(mid, placeholder_text="ID do produto", width=150)
        self.v_prod_id.grid(row=0, column=0, padx=8, pady=8)

        self.v_qtd = ctk.CTkEntry(mid, placeholder_text="Quantidade", width=150)
        self.v_qtd.grid(row=0, column=1, padx=8, pady=8)

        ctk.CTkButton(
            mid,
            text="Adicionar item",
            fg_color=COR_BOTAO,
            hover_color=COR_HOVER,
            text_color="black",
            command=self._add_item,
            width=180
        ).grid(row=0, column=2, padx=8, pady=8)

        self.v_item_remover = ctk.CTkEntry(mid, placeholder_text="Item para remover", width=150)
        self.v_item_remover.grid(row=0, column=3, padx=8, pady=8)

        ctk.CTkButton(
            mid,
            text="Remover item",
            fg_color="#FFA726",
            hover_color="#FB8C00",
            text_color="black",
            command=self._remover_item_por_indice,
            width=180
        ).grid(row=0, column=4, padx=8, pady=8)

        busca_prod = ctk.CTkFrame(self.conteudo, fg_color=COR_MENU)
        busca_prod.pack(pady=(0, 10), padx=16, fill="x")

        self.v_busca_prod = ctk.CTkEntry(busca_prod, placeholder_text="Buscar produto por nome", width=260)
        self.v_busca_prod.grid(row=0, column=0, padx=8, pady=8)

        ctk.CTkButton(
            busca_prod,
            text="Buscar produto",
            fg_color=COR_BOTAO,
            hover_color=COR_HOVER,
            text_color="black",
            command=self._buscar_produtos_venda,
            width=170
        ).grid(row=0, column=1, padx=8, pady=8)

        ctk.CTkButton(
            busca_prod,
            text="Listar alguns",
            fg_color=COR_DESTAQUE,
            hover_color="#2DA7D7",
            text_color="black",
            command=self._listar_produtos_rapido_venda,
            width=170
        ).grid(row=0, column=2, padx=8, pady=8)

        bottom_venda = ctk.CTkFrame(self.conteudo, fg_color=COR_MENU)
        bottom_venda.pack(pady=(0, 10), padx=16, fill="x")

        ctk.CTkLabel(bottom_venda, text="Forma de pagamento", text_color="white").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.v_forma = ctk.CTkOptionMenu(bottom_venda, values=["cartao", "boleto", "pix", "berries"], width=180)
        self.v_forma.grid(row=0, column=1, padx=8, pady=8)
        self.v_forma.set("pix")

        ctk.CTkLabel(bottom_venda, text="Status do pagamento", text_color="white").grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.v_status = ctk.CTkOptionMenu(bottom_venda, values=["pendente", "confirmado", "cancelado"], width=180)
        self.v_status.grid(row=0, column=3, padx=8, pady=8)
        self.v_status.set("pendente")

        ctk.CTkButton(
            bottom_venda,
            text="Finalizar venda",
            fg_color=COR_DESTAQUE,
            hover_color="#2DA7D7",
            text_color="black",
            command=self._finalizar_venda,
            width=180
        ).grid(row=0, column=4, padx=16, pady=8)

        area_venda = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        area_venda.pack(pady=10, padx=16, fill="both", expand=True)

        self.v_itens = ctk.CTkTextbox(area_venda, width=670, height=470)
        self.v_itens.pack(side="left", padx=(0, 10), fill="both", expand=True)

        self.v_produtos_apoio = ctk.CTkTextbox(area_venda, width=360, height=470)
        self.v_produtos_apoio.pack(side="left", fill="both")
        self._render_produtos_apoio()

        self._render_carrinho()

    # Busca e seleciona o cliente da venda pelo CPF informado.
    def _buscar_cliente(self):
        cpf = self.v_cpf.get().strip()

        if not cpf:
            messagebox.showerror("Erro", "Informe o CPF do cliente.")
            return

        cliente = obter_cliente_por_cpf(cpf)

        if not cliente:
            messagebox.showerror("Erro", "Cliente nao encontrado. Cadastre o cliente antes da venda.")
            return

        self.cliente_selecionado = cliente
        self.v_cliente_lbl.configure(text=f"Cliente: {cliente['nome']} (ID={cliente['id']})")
        self._render_carrinho()

    # Busca produtos por nome para apoio rapido na venda.
    def _buscar_produtos_venda(self):
        try:
            termo = self.v_busca_prod.get().strip()
            filtros = {}
            if termo:
                filtros["nome"] = termo
            self.ultima_busca_produtos_venda = listar_produtos(filtros)
            self._render_produtos_apoio()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Lista alguns produtos para apoio rapido na tela de vendas.
    def _listar_produtos_rapido_venda(self):
        try:
            self.ultima_busca_produtos_venda = listar_produtos()[:15]
            self._render_produtos_apoio()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Atualiza a area de apoio com produtos e IDs.
    def _render_produtos_apoio(self):
        if not hasattr(self, "v_produtos_apoio"):
            return

        self.v_produtos_apoio.configure(state="normal")
        self.v_produtos_apoio.delete("1.0", "end")
        self.v_produtos_apoio.insert("end", "Consulta rapida de produtos\n")
        self.v_produtos_apoio.insert("end", "-" * 45 + "\n")

        produtos = self.ultima_busca_produtos_venda if self.ultima_busca_produtos_venda else listar_produtos()[:15]

        if not produtos:
            self.v_produtos_apoio.insert("end", "(sem produtos encontrados)\n")
        else:
            for produto in produtos:
                self.v_produtos_apoio.insert(
                    "end",
                    f"ID {produto['id']} | {produto['nome']} | Estoque: {produto['quantidade']}\n"
                )

        self.v_produtos_apoio.configure(state="disabled")

    # Adiciona um item ao carrinho da venda.
    def _add_item(self):
        try:
            produto_id = int(self.v_prod_id.get().strip())
            quantidade = int(self.v_qtd.get().strip())

            if quantidade <= 0:
                raise ValueError("Quantidade invalida.")

            produto = obter_produto(produto_id)
            if not produto:
                raise ValueError("Produto nao encontrado.")

            self.carrinho.append(ItemCarrinho(produto_id=produto_id, quantidade=quantidade))
            self.v_prod_id.delete(0, "end")
            self.v_qtd.delete(0, "end")
            self._render_carrinho()

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Remove um item especifico do carrinho pelo numero exibido.
    def _remover_item_por_indice(self):
        try:
            if not self.carrinho:
                raise ValueError("Carrinho vazio.")

            indice_texto = self.v_item_remover.get().strip()
            if not indice_texto:
                raise ValueError("Informe o numero do item que deseja remover.")

            indice = int(indice_texto)

            if indice < 1 or indice > len(self.carrinho):
                raise ValueError("Item informado nao existe no carrinho.")

            self.carrinho.pop(indice - 1)
            self.v_item_remover.delete(0, "end")
            self._render_carrinho()

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Atualiza a exibicao do carrinho e do resumo da venda.
    def _render_carrinho(self):
        self.v_itens.configure(state="normal")
        self.v_itens.delete("1.0", "end")
        self.v_itens.insert("end", "Carrinho\n")
        self.v_itens.insert("end", "-" * 100 + "\n")

        if not self.carrinho:
            self.v_itens.insert("end", "(vazio)\n")
        else:
            for indice, item in enumerate(self.carrinho, start=1):
                produto = obter_produto(item.produto_id)
                nome_produto = produto["nome"] if produto else "Produto nao encontrado"
                self.v_itens.insert(
                    "end",
                    f"{indice}. ID {item.produto_id} - {nome_produto} | Quantidade: {item.quantidade}\n"
                )

        cliente_id = int(self.cliente_selecionado["id"]) if self.cliente_selecionado else None

        try:
            resumo = calcular_resumo_carrinho(cliente_id, self.carrinho)
            self.v_itens.insert("end", "\nResumo da venda\n")
            self.v_itens.insert("end", "-" * 100 + "\n")
            self.v_itens.insert("end", f"Vendedor: {self.usuario_logado['nome']}\n")
            self.v_itens.insert("end", f"Subtotal: R$ {resumo['subtotal']:.2f}\n")
            self.v_itens.insert("end", f"Desconto: R$ {resumo['desconto']:.2f}\n")
            self.v_itens.insert("end", f"Total: R$ {resumo['total']:.2f}\n")
        except Exception as exc:
            self.v_itens.insert("end", f"\nErro no resumo: {exc}\n")

        self.v_itens.configure(state="disabled")

    # Finaliza a venda com os dados informados na interface.
    def _finalizar_venda(self):
        if not self.cliente_selecionado:
            messagebox.showerror("Erro", "Selecione um cliente para concluir a venda.")
            return

        try:
            venda_id = criar_venda(
                cliente_id=int(self.cliente_selecionado["id"]),
                vendedor_id=int(self.usuario_logado["id"]),
                forma=self.v_forma.get(),
                status=self.v_status.get(),
                itens=self.carrinho,
            )
            messagebox.showinfo("Sucesso", f"Venda registrada com sucesso. ID={venda_id}")
            self.carrinho = []
            self.cliente_selecionado = None
            self.ultima_busca_produtos_venda = []
            self.tela_vendas()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Monta a tela de relatorios do sistema.
    def tela_relatorios(self):
        self.limpar_conteudo()

        ctk.CTkLabel(
            self.conteudo,
            text="Relatorios",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(pady=14)

        frame = ctk.CTkFrame(self.conteudo, fg_color=COR_MENU)
        frame.pack(pady=10, padx=16, fill="x")

        self.r_ano = ctk.CTkEntry(frame, placeholder_text="Ano", width=140)
        self.r_ano.grid(row=0, column=0, padx=8, pady=8)
        self.r_ano.insert(0, str(datetime.now().year))

        self.r_mes = ctk.CTkEntry(frame, placeholder_text="Mes", width=120)
        self.r_mes.grid(row=0, column=1, padx=8, pady=8)
        self.r_mes.insert(0, str(datetime.now().month))

        ctk.CTkButton(
            frame,
            text="Relatorio por vendedor",
            fg_color=COR_DESTAQUE,
            hover_color="#2DA7D7",
            text_color="black",
            command=self._relatorio_proc,
            width=240
        ).grid(row=0, column=2, padx=8, pady=8)

        ctk.CTkButton(
            frame,
            text="Listar vendas do mes",
            fg_color=COR_BOTAO,
            hover_color=COR_HOVER,
            text_color="black",
            command=self._listar_vendas_mes,
            width=220
        ).grid(row=0, column=3, padx=8, pady=8)

        self.r_box = ctk.CTkTextbox(self.conteudo, width=1050, height=560)
        self.r_box.pack(pady=10, padx=16, fill="both", expand=True)

    # Executa a procedure do relatorio mensal por vendedor.
    def _relatorio_proc(self):
        try:
            ano = int(self.r_ano.get().strip())
            mes = int(self.r_mes.get().strip())
            dados = relatorio_mensal_por_vendedor(ano, mes)

            self.r_box.configure(state="normal")
            self.r_box.delete("1.0", "end")
            self.r_box.insert("end", f"Relatorio mensal por vendedor — {ano}-{mes:02d}\n")
            self.r_box.insert("end", "-" * 115 + "\n")

            if not dados:
                self.r_box.insert("end", "(sem registros no periodo)\n")
            else:
                for linha in dados:
                    self.r_box.insert(
                        "end",
                        f"{linha['vendedor_nome']} | Vendas: {linha['qtd_vendas']} | "
                        f"Subtotal: R$ {float(linha['subtotal'] or 0):.2f} | "
                        f"Desconto: R$ {float(linha['desconto'] or 0):.2f} | "
                        f"Total: R$ {float(linha['total'] or 0):.2f}\n"
                    )

            self.r_box.configure(state="disabled")

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # Lista as vendas registradas no mes informado.
    def _listar_vendas_mes(self):
        try:
            ano = int(self.r_ano.get().strip())
            mes = int(self.r_mes.get().strip())
            vendas = listar_vendas(ano, mes)

            self.r_box.configure(state="normal")
            self.r_box.delete("1.0", "end")
            self.r_box.insert("end", f"Vendas do mes — {ano}-{mes:02d}\n")
            self.r_box.insert("end", "-" * 115 + "\n")

            if not vendas:
                self.r_box.insert("end", "(sem vendas no periodo)\n")
            else:
                for venda in vendas:
                    self.r_box.insert(
                        "end",
                        f"#{venda['id']} | {venda['data_hora']} | Cliente: {venda['cliente_nome']} | "
                        f"Vendedor: {venda['vendedor_nome']} | Forma: {venda['forma_pagamento']} | "
                        f"Status: {venda['status_pagamento']} | Total: R$ {float(venda['total']):.2f}\n"
                    )

            self.r_box.configure(state="disabled")

        except Exception as exc:
            messagebox.showerror("Erro", str(exc))


if __name__ == "__main__":
    App().mainloop()
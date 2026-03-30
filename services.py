from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple

from db import conectar, fetchall_dict, fetchone_dict

DESCONTO_PCT = 0.05
FORMAS_PAGAMENTO_VALIDAS = {"cartao", "boleto", "pix", "berries"}
STATUS_PAGAMENTO_VALIDOS = {"pendente", "confirmado", "cancelado"}


@dataclass
class ItemCarrinho:
    produto_id: int
    quantidade: int


def autenticar(usuario: str, senha: str) -> Optional[dict]:
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, usuario, nome, perfil FROM usuarios WHERE usuario=%s AND senha=%s",
            (usuario, senha),
        )
        return fetchone_dict(cur)


# ----------------- PRODUTOS -----------------
def listar_produtos(filtros: dict | None = None) -> list[dict]:
    filtros = filtros or {}
    where = []
    params = []

    if filtros.get("nome"):
        where.append("nome LIKE %s")
        params.append(f"%{filtros['nome']}%")

    if filtros.get("categoria"):
        where.append("categoria = %s")
        params.append(filtros["categoria"])

    if filtros.get("preco_min") is not None:
        where.append("preco >= %s")
        params.append(filtros["preco_min"])

    if filtros.get("preco_max") is not None:
        where.append("preco <= %s")
        params.append(filtros["preco_max"])

    if filtros.get("fabricado_em_mari") is not None:
        where.append("fabricado_em_mari = %s")
        params.append(1 if filtros["fabricado_em_mari"] else 0)

    sql = """
        SELECT id, nome, categoria, preco, quantidade, codigo_barras, fabricado_em_mari, data_cadastro
        FROM produtos
    """

    if where:
        sql += " WHERE " + " AND ".join(where)

    sql += " ORDER BY nome ASC"

    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        return fetchall_dict(cur)


def criar_produto(dados: dict) -> int:
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO produtos (nome, categoria, preco, quantidade, codigo_barras, fabricado_em_mari, data_cadastro)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                dados["nome"],
                dados["categoria"],
                dados["preco"],
                dados["quantidade"],
                dados.get("codigo_barras"),
                1 if dados.get("fabricado_em_mari") else 0,
                dados["data_cadastro"],
            ),
        )
        return int(cur.lastrowid)


def atualizar_produto(produto_id: int, dados: dict) -> None:
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE produtos
            SET nome=%s, categoria=%s, preco=%s, quantidade=%s, codigo_barras=%s, fabricado_em_mari=%s, data_cadastro=%s
            WHERE id=%s
            """,
            (
                dados["nome"],
                dados["categoria"],
                dados["preco"],
                dados["quantidade"],
                dados.get("codigo_barras"),
                1 if dados.get("fabricado_em_mari") else 0,
                dados["data_cadastro"],
                produto_id,
            ),
        )

        if cur.rowcount == 0:
            raise ValueError("Produto não encontrado.")


def remover_produto(produto_id: int) -> None:
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM produtos WHERE id=%s", (produto_id,))

        if cur.rowcount == 0:
            raise ValueError("Produto não encontrado.")


def obter_produto(produto_id: int) -> Optional[dict]:
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, nome, categoria, preco, quantidade, codigo_barras, fabricado_em_mari, data_cadastro
            FROM produtos
            WHERE id=%s
            """,
            (produto_id,),
        )
        return fetchone_dict(cur)


# ----------------- CLIENTES -----------------
def listar_clientes(termo: str | None = None) -> list[dict]:
    sql = """
        SELECT id, nome, cpf, telefone, cidade, torce_flamengo, assiste_one_piece, eh_de_sousa
        FROM clientes
    """
    params = []

    if termo:
        sql += " WHERE nome LIKE %s OR cpf LIKE %s"
        params = [f"%{termo}%", f"%{termo}%"]

    sql += " ORDER BY nome ASC"

    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        return fetchall_dict(cur)


def criar_cliente(dados: dict) -> int:
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO clientes (nome, cpf, telefone, cidade, torce_flamengo, assiste_one_piece, eh_de_sousa)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                dados["nome"],
                dados["cpf"],
                dados.get("telefone"),
                dados.get("cidade"),
                1 if dados.get("torce_flamengo") else 0,
                1 if dados.get("assiste_one_piece") else 0,
                1 if dados.get("eh_de_sousa") else 0,
            ),
        )
        return int(cur.lastrowid)


def atualizar_cliente(cliente_id: int, dados: dict) -> None:
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE clientes
            SET nome=%s, cpf=%s, telefone=%s, cidade=%s, torce_flamengo=%s, assiste_one_piece=%s, eh_de_sousa=%s
            WHERE id=%s
            """,
            (
                dados["nome"],
                dados["cpf"],
                dados.get("telefone"),
                dados.get("cidade"),
                1 if dados.get("torce_flamengo") else 0,
                1 if dados.get("assiste_one_piece") else 0,
                1 if dados.get("eh_de_sousa") else 0,
                cliente_id,
            ),
        )

        if cur.rowcount == 0:
            raise ValueError("Cliente não encontrado.")


def remover_cliente(cliente_id: int) -> None:
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes WHERE id=%s", (cliente_id,))

        if cur.rowcount == 0:
            raise ValueError("Cliente não encontrado.")


def obter_cliente(cliente_id: int) -> Optional[dict]:
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, nome, cpf, telefone, cidade, torce_flamengo, assiste_one_piece, eh_de_sousa
            FROM clientes
            WHERE id=%s
            """,
            (cliente_id,),
        )
        return fetchone_dict(cur)


def obter_cliente_por_cpf(cpf: str) -> Optional[dict]:
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, nome, cpf, telefone, cidade, torce_flamengo, assiste_one_piece, eh_de_sousa
            FROM clientes
            WHERE cpf=%s
            """,
            (cpf,),
        )
        return fetchone_dict(cur)


def listar_pedidos_por_cliente(cliente_id: int) -> list[dict]:
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                v.id,
                v.data_hora,
                v.subtotal,
                v.desconto,
                v.total,
                v.forma_pagamento,
                v.status_pagamento,
                u.nome AS vendedor_nome
            FROM vendas v
            JOIN usuarios u ON u.id = v.vendedor_id
            WHERE v.cliente_id = %s
            ORDER BY v.data_hora DESC
            """,
            (cliente_id,),
        )
        return fetchall_dict(cur)


# ----------------- VENDAS -----------------
def calcular_resumo_carrinho(cliente_id: int | None, itens: List[ItemCarrinho]) -> dict:
    if not itens:
        return {"subtotal": 0.0, "desconto": 0.0, "total": 0.0}

    with conectar() as conn:
        cur = conn.cursor()

        subtotal = 0.0
        for item in itens:
            cur.execute("SELECT preco FROM produtos WHERE id=%s", (item.produto_id,))
            row = cur.fetchone()
            if not row:
                raise ValueError(f"Produto {item.produto_id} não encontrado.")
            preco = float(row[0])
            if item.quantidade <= 0:
                raise ValueError("Quantidade inválida.")
            subtotal += preco * item.quantidade

        desconto = 0.0
        if cliente_id is not None:
            cur.execute(
                """
                SELECT torce_flamengo, assiste_one_piece, eh_de_sousa
                FROM clientes
                WHERE id=%s
                """,
                (cliente_id,),
            )
            cli = cur.fetchone()
            if cli and (int(cli[0]) == 1 or int(cli[1]) == 1 or int(cli[2]) == 1):
                desconto = round(subtotal * DESCONTO_PCT, 2)

        total = round(subtotal - desconto, 2)

        return {
            "subtotal": round(subtotal, 2),
            "desconto": desconto,
            "total": total,
        }


def criar_venda(cliente_id: int, vendedor_id: int, forma: str, status: str, itens: List[ItemCarrinho]) -> int:
    if not itens:
        raise ValueError("Carrinho vazio.")

    if forma not in FORMAS_PAGAMENTO_VALIDAS:
        raise ValueError("Forma de pagamento inválida.")

    if status not in STATUS_PAGAMENTO_VALIDOS:
        raise ValueError("Status de pagamento inválido.")

    with conectar() as conn:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT torce_flamengo, assiste_one_piece, eh_de_sousa
            FROM clientes
            WHERE id=%s
            """,
            (cliente_id,),
        )
        cli = cur.fetchone()

        if not cli:
            raise ValueError("Cliente não encontrado.")

        subtotal = 0.0
        produtos_cache: Dict[int, Tuple[float, int]] = {}

        for item in itens:
            cur.execute("SELECT preco, quantidade FROM produtos WHERE id=%s FOR UPDATE", (item.produto_id,))
            row = cur.fetchone()

            if not row:
                raise ValueError(f"Produto {item.produto_id} não encontrado.")

            preco, estoque = float(row[0]), int(row[1])

            if item.quantidade <= 0:
                raise ValueError("Quantidade inválida.")

            if estoque < item.quantidade:
                raise ValueError(
                    f"Sem estoque suficiente para o produto {item.produto_id}. Disponível: {estoque}."
                )

            subtotal += preco * item.quantidade
            produtos_cache[item.produto_id] = (preco, estoque)

        desconto = 0.0
        if int(cli[0]) == 1 or int(cli[1]) == 1 or int(cli[2]) == 1:
            desconto = round(subtotal * DESCONTO_PCT, 2)

        total = round(subtotal - desconto, 2)

        cur.execute(
            """
            INSERT INTO vendas (cliente_id, vendedor_id, subtotal, desconto, total, forma_pagamento, status_pagamento)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (cliente_id, vendedor_id, subtotal, desconto, total, forma, status),
        )
        venda_id = int(cur.lastrowid)

        for item in itens:
            preco = produtos_cache[item.produto_id][0]
            total_item = round(preco * item.quantidade, 2)

            cur.execute(
                """
                INSERT INTO venda_itens (venda_id, produto_id, quantidade, preco_unitario, total_item)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (venda_id, item.produto_id, item.quantidade, preco, total_item),
            )

            cur.execute(
                "UPDATE produtos SET quantidade = quantidade - %s WHERE id=%s",
                (item.quantidade, item.produto_id),
            )

        return venda_id


def listar_vendas(ano: int | None = None, mes: int | None = None) -> list[dict]:
    where = []
    params = []

    if ano is not None:
        where.append("YEAR(v.data_hora) = %s")
        params.append(ano)

    if mes is not None:
        where.append("MONTH(v.data_hora) = %s")
        params.append(mes)

    sql = """
        SELECT
            v.id,
            v.data_hora,
            v.total,
            v.subtotal,
            v.desconto,
            v.forma_pagamento,
            v.status_pagamento,
            c.nome AS cliente_nome,
            u.nome AS vendedor_nome
        FROM vendas v
        JOIN clientes c ON c.id = v.cliente_id
        JOIN usuarios u ON u.id = v.vendedor_id
    """

    if where:
        sql += " WHERE " + " AND ".join(where)

    sql += " ORDER BY v.data_hora DESC"

    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        return fetchall_dict(cur)


def detalhar_venda(venda_id: int) -> dict:
    with conectar() as conn:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                v.id,
                v.data_hora,
                v.subtotal,
                v.desconto,
                v.total,
                v.forma_pagamento,
                v.status_pagamento,
                c.nome AS cliente_nome,
                c.cpf AS cliente_cpf,
                u.nome AS vendedor_nome
            FROM vendas v
            JOIN clientes c ON c.id = v.cliente_id
            JOIN usuarios u ON u.id = v.vendedor_id
            WHERE v.id = %s
            """,
            (venda_id,),
        )
        venda = fetchone_dict(cur)

        if not venda:
            raise ValueError("Venda não encontrada.")

        cur.execute(
            """
            SELECT
                vi.produto_id,
                p.nome AS produto_nome,
                vi.quantidade,
                vi.preco_unitario,
                vi.total_item
            FROM venda_itens vi
            JOIN produtos p ON p.id = vi.produto_id
            WHERE vi.venda_id = %s
            ORDER BY p.nome ASC
            """,
            (venda_id,),
        )
        itens = fetchall_dict(cur)

        venda["itens"] = itens
        return venda


def estoque_baixo() -> list[dict]:
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vw_estoque_baixo")
        return fetchall_dict(cur)


def relatorio_mensal_por_vendedor(ano: int, mes: int) -> list[dict]:
    with conectar() as conn:
        cur = conn.cursor()
        cur.callproc("sp_relatorio_vendas_vendedor", (ano, mes))
        results = []

        for result in cur.stored_results():
            results = fetchall_dict(result)

        return results
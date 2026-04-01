from dataclasses import dataclass
from typing import Optional


# Representa um produto cadastrado no sistema.
@dataclass
class Produto:
    id: Optional[int]
    nome: str
    categoria: str
    preco: float
    quantidade: int
    codigo_barras: Optional[str] = None
    fabricado_em_mari: int = 0
    data_cadastro: str = "2026-01-01"


# Representa um cliente do sistema.
@dataclass
class Cliente:
    id: Optional[int]
    nome: str
    cpf: str
    telefone: Optional[str] = None
    cidade: Optional[str] = None
    torce_flamengo: int = 0
    assiste_one_piece: int = 0
    eh_de_sousa: int = 0


# Representa um usuario do sistema (admin ou vendedor).
@dataclass
class Usuario:
    id: Optional[int]
    usuario: str
    senha: str
    nome: str
    perfil: str = "VENDEDOR"


# Representa uma venda realizada no sistema.
@dataclass
class Venda:
    id: Optional[int]
    cliente_id: int
    vendedor_id: int
    subtotal: float
    desconto: float
    total: float
    forma_pagamento: str
    status_pagamento: str


# Representa um item pertencente a uma venda.
@dataclass
class VendaItem:
    id: Optional[int]
    venda_id: int
    produto_id: int
    quantidade: int
    preco_unitario: float
    total_item: float
# MercadoTech PDV — Parte 2

Sistema de vendas com interface gráfica em Python utilizando CustomTkinter e banco de dados MySQL.

## Objetivo

Este projeto estende o CRUD inicial para um sistema de vendas completo, contemplando cadastro de produtos e clientes, realização de vendas, consultas, controle de estoque e relatórios.

## Requisitos da Parte 2 atendidos

- Cadastro e manutenção de produtos
- Cadastro e manutenção de clientes
- Venda associada a cliente e vendedor
- Venda com um ou mais itens
- Forma de pagamento com status
- Bloqueio de venda sem estoque disponível
- Desconto automático para clientes que:
  - torcem Flamengo
  - assistem One Piece
  - são de Sousa
- Consulta de produtos por:
  - nome
  - faixa de preço
  - categoria
  - fabricado em Mari
- Consulta de produtos com estoque baixo por view
- Relatório mensal de vendas por vendedor por stored procedure
- Índices e integridade referencial no banco
- Interface gráfica pronta para uso

## Tecnologias

- Python
- CustomTkinter
- MySQL
- mysql-connector-python

## Estrutura dos arquivos

- `app.py`: interface gráfica
- `services.py`: regras de negócio
- `db.py`: conexão e utilitários do banco
- `schema.sql`: criação do banco, tabelas, view e procedure
- `init_db.py`: execução automática do schema
- `models.py`: modelagem das entidades
- `config.py`: configurações de conexão
- `requirements.txt`: dependências do projeto

## Regras de negócio implementadas

### Desconto
O sistema aplica 5% de desconto quando o cliente atende a pelo menos um dos critérios definidos na especificação.

### Estoque
A venda não é concluída quando algum item solicitado possui quantidade insuficiente em estoque.

### Relatórios
O relatório mensal por vendedor é emitido por stored procedure, consolidando quantidade de vendas e valores do período.

## Banco de dados

O projeto possui:

- chaves estrangeiras
- índices
- view `vw_estoque_baixo`
- stored procedure `sp_relatorio_vendas_vendedor`

## Como executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
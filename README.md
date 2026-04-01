# MercadoTech PDV - Parte 2

Sistema de vendas desenvolvido em Python com interface grafica em CustomTkinter e banco de dados MySQL.

---

## 1. Objetivo

Este projeto foi desenvolvido para atender a Parte 2 da disciplina de Banco de Dados, ampliando um sistema CRUD para um sistema completo de vendas.

O sistema permite o cadastro e gerenciamento de produtos e clientes, a realizacao de vendas com multiplos itens, o controle de estoque, consultas com filtros e a geracao de relatorios mensais por vendedor.

---

## 2. Funcionalidades

- Cadastro, edicao e remocao de produtos
- Cadastro, edicao e remocao de clientes
- Listagem de produtos e clientes
- Consulta de cliente por CPF
- Visualizacao do historico de pedidos do cliente
- Realizacao de vendas com um ou mais itens
- Associacao da venda a cliente e vendedor
- Controle de estoque durante a venda
- Aplicacao automatica de desconto
- Consulta de produtos por nome
- Consulta de produtos por categoria
- Consulta de produtos por faixa de preco
- Consulta de produtos fabricados em Mari
- Consulta de produtos com estoque baixo
- Relatorio mensal de vendas por vendedor

---

## 3. Requisitos da Parte 2 atendidos

- Sistema com multiplas entidades e relacionamentos
- Cliente associado a varias compras
- Venda composta por um ou mais itens
- Venda associada a vendedor
- Venda com forma de pagamento e status
- Validacao de estoque antes da conclusao da venda
- Consulta de produtos com filtros
- Consulta de estoque baixo por view
- Relatorio mensal por vendedor
- Uso de view
- Uso de stored procedure
- Uso de indices
- Uso de integridade referencial
- Interface grafica pronta para uso

---

## 4. Tecnologias utilizadas

- Python
- CustomTkinter
- MySQL
- mysql-connector-python

---

## 5. Estrutura do projeto

- `app.py`: interface grafica do sistema
- `services.py`: regras de negocio
- `db.py`: conexao com o banco de dados
- `schema.sql`: estrutura do banco, tabelas, view e procedure
- `init_db.py`: criacao automatica do banco
- `models.py`: modelagem das entidades
- `config.py`: configuracao de acesso ao banco
- `requirements.txt`: dependencias do projeto

---

## 6. Regras de negocio

### 6.1 Desconto
O sistema aplica 5% de desconto quando o cliente atende a pelo menos um dos criterios abaixo:

- torce Flamengo
- assiste One Piece
- e de Sousa

### 6.2 Controle de estoque
A venda nao e concluida quando a quantidade solicitada excede o estoque disponivel.

### 6.3 Relatorios
O relatorio mensal de vendas por vendedor e gerado por stored procedure no banco de dados.

### 6.4 Vendedor da venda
Toda venda registrada no sistema fica associada ao usuario logado, que representa o vendedor responsavel pela operacao.

---

## 7. Banco de dados

O sistema utiliza MySQL com os seguintes recursos:

- tabelas relacionais com chaves estrangeiras
- indices para otimizacao de consultas
- view `vw_estoque_baixo`
- stored procedure `sp_relatorio_vendas_vendedor`

As principais entidades do sistema sao:

- `usuarios`
- `clientes`
- `produtos`
- `vendas`
- `venda_itens`

---

## 8. Pre-requisitos

Antes de executar o projeto, e necessario ter instalado:

- Python 3
- MySQL Server
- pip

---

## 9. Instalacao e execucao

### 9.1 Instalar dependencias

Execute no terminal:

```bash
pip install -r requirements.txt

---

9.2 Configurar o banco de dados

Edite o arquivo config.py com os dados do seu ambiente:
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "1234"
DB_NAME = "mercadotech_db"

---

9.3 Criar o banco e a estrutura

Execute no terminal:

python init_db.py

---

9.4 Executar o sistema

Execute no terminal:

python app.py

---

10. Usuarios para acesso

O sistema possui os seguintes usuarios para teste e demonstracao:

Usuario: admin | Senha: 1234
Usuario: vendedor1 | Senha: 1234
Usuario: vendedor2 | Senha: 1234

---

11. Observacoes importantes
- O arquivo schema.sql recria completamente o banco de dados.
- Ao executar init_db.py, os dados anteriores podem ser apagados.
- Recomenda-se executar o sistema com o MySQL ativo e configurado corretamente.
- Para fins de apresentacao, o sistema permite demonstrar vendas associadas a diferentes vendedores por meio dos usuarios cadastrados.

---

12. Aderencia a especificacao

O projeto foi desenvolvido de acordo com os requisitos da Parte 2, contemplando:

- modulo de vendas completo
- relacionamento entre entidades
- validacao de estoque
- regras de desconto
- consultas com filtros
- uso de view e stored procedure
- relatorio mensal por vendedor
- interface grafica funcional

---

13. Fluxo basico de uso

Uma sequencia recomendada para utilizar o sistema e:

- realizar login
- cadastrar ou consultar produtos
- cadastrar ou consultar clientes
- iniciar uma venda
- informar o CPF do cliente
- adicionar um ou mais itens ao carrinho
- selecionar forma e status de pagamento
- finalizar a venda
- consultar relatorios ou historico de pedidos
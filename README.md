# MercadoTech PDV — Parte 2

Sistema de vendas desenvolvido em Python com interface gráfica (CustomTkinter) e banco de dados MySQL.

---

## 1. Objetivo

Este projeto foi desenvolvido para atender à Parte 2 da disciplina de Banco de Dados, estendendo um sistema CRUD para um sistema completo de vendas.

O sistema contempla cadastro e gerenciamento de produtos e clientes, realização de vendas com múltiplos itens, controle de estoque, consultas com filtros e geração de relatórios mensais por vendedor.

---

## 2. Funcionalidades

- Cadastro, edição e remoção de produtos
- Cadastro, edição e remoção de clientes
- Listagem de produtos e clientes
- Consulta de cliente por CPF
- Visualização do histórico de pedidos do cliente
- Realização de vendas com um ou mais itens
- Associação da venda a cliente e vendedor
- Controle de estoque durante a venda
- Aplicação automática de desconto
- Consulta de produtos por:
  - nome
  - categoria
  - faixa de preço
  - fabricação em Mari
- Consulta de produtos com estoque baixo
- Relatório mensal de vendas por vendedor

---

## 3. Requisitos da Parte 2 atendidos

- Sistema com múltiplas entidades e relacionamentos
- Cliente associado a várias compras
- Venda composta por um ou mais itens
- Venda associada a vendedor
- Venda com forma de pagamento e status
- Validação de estoque antes da venda
- Consulta de produtos com filtros
- Consulta de estoque baixo por view
- Relatório mensal por vendedor
- Uso de view
- Uso de stored procedure
- Uso de índices
- Uso de integridade referencial
- Interface gráfica pronta para uso

---

## 4. Tecnologias utilizadas

- Python
- CustomTkinter
- MySQL
- mysql-connector-python

---

## 5. Estrutura do projeto

- `app.py`: interface gráfica do sistema
- `services.py`: regras de negócio
- `db.py`: conexão com o banco
- `schema.sql`: estrutura do banco (tabelas, view e procedure)
- `init_db.py`: criação automática do banco
- `models.py`: modelagem das entidades
- `config.py`: configurações de conexão
- `requirements.txt`: dependências do projeto

---

## 6. Regras de negócio

### 6.1 Desconto
O sistema aplica 5% de desconto quando o cliente atende a pelo menos um dos critérios:

- torce Flamengo
- assiste One Piece
- é de Sousa

### 6.2 Controle de estoque
A venda não é concluída quando a quantidade solicitada excede o estoque disponível.

### 6.3 Relatórios
O relatório mensal de vendas por vendedor é gerado por stored procedure no banco de dados.

---

## 7. Banco de dados

O sistema utiliza MySQL com os seguintes recursos:

- tabelas relacionais com chaves estrangeiras
- índices para otimização de consultas
- view `vw_estoque_baixo`
- stored procedure `sp_relatorio_vendas_vendedor`

---

## 8. Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- Python 3
- MySQL Server
- pip

---

## 9. Instalação e execução

### 9.1 Instalar dependências

Execute no terminal:

```bash
pip install -r requirements.txt

---

9.2 Configurar o banco de dados

Edite o arquivo config.py com suas credenciais:

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "1234"
DB_NAME = "mercadotech_db"

---

9.3 Criar o banco e estrutura

Execute:

python init_db.py

---

9.4 Executar o sistema

Execute:

python app.py

--- 

10. Login padrão:

 Usuário: admin
 Senha: 1234

---

11. Observações importantes:

O arquivo schema.sql recria completamente o banco de dados.
Ao executar init_db.py, todos os dados anteriores podem ser apagados.
Recomenda-se executar o sistema com o MySQL ativo e configurado corretamente.

---

12. Aderência à especificação

O projeto foi desenvolvido seguindo os requisitos da Parte 2, incluindo:

módulo de vendas completo
relacionamento entre entidades
validação de estoque
regras de desconto
consultas com filtros
uso de view e stored procedure
relatório mensal por vendedor
interface gráfica funcional


---


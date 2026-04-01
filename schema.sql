-- Schema do sistema de vendas MercadoTech PDV

-- Remove o banco existente para recriacao completa
DROP DATABASE IF EXISTS mercadotech_db;

-- Cria o banco de dados com suporte a UTF-8
CREATE DATABASE mercadotech_db
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

-- Seleciona o banco para uso
USE mercadotech_db;

-- Tabela de usuarios do sistema
CREATE TABLE usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario VARCHAR(60) NOT NULL UNIQUE,
  senha VARCHAR(120) NOT NULL,
  nome VARCHAR(120) NOT NULL,
  perfil ENUM('ADMIN', 'VENDEDOR') NOT NULL DEFAULT 'VENDEDOR',
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tabela de clientes cadastrados no sistema
CREATE TABLE clientes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  cpf VARCHAR(14) NOT NULL UNIQUE,
  telefone VARCHAR(30),
  cidade VARCHAR(80),
  torce_flamengo TINYINT(1) NOT NULL DEFAULT 0,
  assiste_one_piece TINYINT(1) NOT NULL DEFAULT 0,
  eh_de_sousa TINYINT(1) NOT NULL DEFAULT 0,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_clientes_nome (nome)
) ENGINE=InnoDB;

-- Tabela de produtos disponiveis para venda
CREATE TABLE produtos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(140) NOT NULL UNIQUE,
  categoria VARCHAR(80) NOT NULL,
  preco DECIMAL(10,2) NOT NULL CHECK (preco >= 0),
  quantidade INT NOT NULL CHECK (quantidade >= 0),
  codigo_barras VARCHAR(40),
  fabricado_em_mari TINYINT(1) NOT NULL DEFAULT 0,
  data_cadastro DATE NOT NULL DEFAULT (CURRENT_DATE),
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_prod_nome (nome),
  INDEX idx_prod_categoria (categoria),
  INDEX idx_prod_preco (preco),
  INDEX idx_prod_mari (fabricado_em_mari),
  INDEX idx_prod_qtd (quantidade)
) ENGINE=InnoDB;

-- Tabela de vendas realizadas no sistema
CREATE TABLE vendas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cliente_id INT NOT NULL,
  vendedor_id INT NOT NULL,
  data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  subtotal DECIMAL(10,2) NOT NULL DEFAULT 0,
  desconto DECIMAL(10,2) NOT NULL DEFAULT 0,
  total DECIMAL(10,2) NOT NULL DEFAULT 0,
  forma_pagamento ENUM('cartao', 'boleto', 'pix', 'berries') NOT NULL,
  status_pagamento ENUM('pendente', 'confirmado', 'cancelado') NOT NULL DEFAULT 'pendente',
  CONSTRAINT fk_vendas_cliente FOREIGN KEY (cliente_id)
    REFERENCES clientes(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  CONSTRAINT fk_vendas_vendedor FOREIGN KEY (vendedor_id)
    REFERENCES usuarios(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  INDEX idx_vendas_data (data_hora),
  INDEX idx_vendas_vendedor (vendedor_id),
  INDEX idx_vendas_cliente (cliente_id)
) ENGINE=InnoDB;

-- Tabela de itens que compoem cada venda
CREATE TABLE venda_itens (
  id INT AUTO_INCREMENT PRIMARY KEY,
  venda_id INT NOT NULL,
  produto_id INT NOT NULL,
  quantidade INT NOT NULL CHECK (quantidade > 0),
  preco_unitario DECIMAL(10,2) NOT NULL CHECK (preco_unitario >= 0),
  total_item DECIMAL(10,2) NOT NULL CHECK (total_item >= 0),
  CONSTRAINT fk_itens_venda FOREIGN KEY (venda_id)
    REFERENCES vendas(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT fk_itens_produto FOREIGN KEY (produto_id)
    REFERENCES produtos(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  INDEX idx_itens_venda (venda_id),
  INDEX idx_itens_prod (produto_id)
) ENGINE=InnoDB;

-- Remove a view existente para recriacao
DROP VIEW IF EXISTS vw_estoque_baixo;

-- View que lista produtos com estoque inferior a 5 unidades
CREATE VIEW vw_estoque_baixo AS
SELECT
  id,
  nome,
  categoria,
  preco,
  quantidade,
  fabricado_em_mari
FROM produtos
WHERE quantidade < 5
ORDER BY quantidade ASC, nome ASC;

-- Remove a procedure existente para recriacao
DROP PROCEDURE IF EXISTS sp_relatorio_vendas_vendedor;

-- Define delimitador para criacao da procedure
DELIMITER $$

-- Procedure que gera relatorio mensal de vendas por vendedor
CREATE PROCEDURE sp_relatorio_vendas_vendedor(
  IN p_ano INT,
  IN p_mes INT
)
BEGIN
  SELECT
    u.id AS vendedor_id,
    u.nome AS vendedor_nome,
    COUNT(v.id) AS qtd_vendas,
    COALESCE(SUM(v.subtotal), 0) AS subtotal,
    COALESCE(SUM(v.desconto), 0) AS desconto,
    COALESCE(SUM(v.total), 0) AS total
  FROM usuarios u
  LEFT JOIN vendas v
    ON u.id = v.vendedor_id
   AND YEAR(v.data_hora) = p_ano
   AND MONTH(v.data_hora) = p_mes
  WHERE u.perfil IN ('ADMIN', 'VENDEDOR')
  GROUP BY u.id, u.nome
  ORDER BY total DESC, vendedor_nome ASC;
END$$

-- Restaura o delimitador padrao
DELIMITER ;

-- Insere usuario administrador padrao no sistema
INSERT INTO usuarios (usuario, senha, nome, perfil)
VALUES ('admin', '1234', 'Administrador', 'ADMIN');

-- Insere usuarios vendedores para teste e apresentacao
INSERT INTO usuarios (usuario, senha, nome, perfil)
VALUES
  ('vendedor1', '1234', 'Vendedor 1', 'VENDEDOR'),
  ('vendedor2', '1234', 'Vendedor 2', 'VENDEDOR');
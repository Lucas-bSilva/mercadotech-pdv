from __future__ import annotations

from pathlib import Path
import mysql.connector

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD

SCHEMA_FILE = Path(__file__).with_name("schema.sql")


# Executa o arquivo schema.sql no servidor MySQL.
def executar_schema():
    sql = SCHEMA_FILE.read_text(encoding="utf-8")

    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        autocommit=True,
    )
    cur = conn.cursor()

    delimiter = ";"
    buffer = []
    statements = []

    for line in sql.splitlines():
        stripped = line.strip()

        if not stripped or stripped.startswith("--"):
            continue

        if stripped.upper().startswith("DELIMITER "):
            if buffer:
                statements.append(("\n".join(buffer), delimiter))
                buffer = []
            delimiter = stripped.split()[1]
            continue

        buffer.append(line)

        if stripped.endswith(delimiter):
            statements.append(("\n".join(buffer), delimiter))
            buffer = []

    if buffer:
        statements.append(("\n".join(buffer), delimiter))

    for statement, current_delimiter in statements:
        statement = statement.strip()
        if statement.endswith(current_delimiter):
            statement = statement[:-len(current_delimiter)]
        if statement:
            cur.execute(statement)

    cur.close()
    conn.close()


# Inicializa o banco de dados a partir do schema.
if __name__ == "__main__":
    executar_schema()
    print("Banco, tabelas, view e procedure criados com sucesso.")
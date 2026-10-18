"""
Acesso ao banco SQLite do laboratório.

Aqui ficam só funções simples com SQL puro (sem ORM):
criar a tabela, inserir dados iniciais e fazer o CRUD de demandas.
"""

import os
import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path

# No Docker o banco fica no volume /data (veja o docker-compose.yml).
# Fora do Docker dá para trocar o caminho com a variável DB_PATH.
DB_PATH = Path(os.getenv("DB_PATH", "/data/lab.db"))

COLUMNS = "id, title, category, description, status, owner, created_at"


def get_connection():
    """Abre uma conexão com o banco. Cada linha volta como dicionário."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Cria a tabela demands e insere 3 registros se ela estiver vazia."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with closing(get_connection()) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS demands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL,
                owner TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        total = connection.execute("SELECT COUNT(*) FROM demands").fetchone()[0]

        if total == 0:
            initial_demands = [
                (
                    "Organizar evento comunitário",
                    "Comunidade",
                    "Planejar local, divulgação e equipe de apoio",
                    "pendente",
                    "Marina",
                    "2026-04-11",
                ),
                (
                    "Cadastrar voluntários",
                    "ONG",
                    "Registrar nome, contato e área de interesse",
                    "em andamento",
                    "Carlos",
                    "2026-04-11",
                ),
                (
                    "Atualizar agenda escolar",
                    "Educação",
                    "Publicar calendário com atividades do mês",
                    "concluída",
                    "Luciana",
                    "2026-04-11",
                ),
            ]
            connection.executemany(
                """
                INSERT INTO demands (title, category, description, status, owner, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                initial_demands,
            )

        connection.commit()


def list_demands():
    """Retorna todas as demandas, da mais antiga para a mais nova."""
    with closing(get_connection()) as connection:
        rows = connection.execute(
            f"SELECT {COLUMNS} FROM demands ORDER BY id"
        ).fetchall()
    return [dict(row) for row in rows]


def get_demand_by_id(demand_id):
    """Retorna uma demanda pelo id, ou None se ela não existir."""
    with closing(get_connection()) as connection:
        row = connection.execute(
            f"SELECT {COLUMNS} FROM demands WHERE id = ?",
            (demand_id,),
        ).fetchone()
    return dict(row) if row else None


def create_demand(title, category, description, status, owner, created_at=None):
    """Insere uma nova demanda e retorna o registro criado."""
    if not created_at:
        created_at = date.today().isoformat()

    with closing(get_connection()) as connection:
        cursor = connection.execute(
            """
            INSERT INTO demands (title, category, description, status, owner, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, category, description, status, owner, created_at),
        )
        connection.commit()
        new_id = cursor.lastrowid

    return get_demand_by_id(new_id)


def update_demand(demand_id, title, category, description, status, owner, created_at):
    """Atualiza todos os campos de uma demanda e retorna o registro novo."""
    with closing(get_connection()) as connection:
        connection.execute(
            """
            UPDATE demands
            SET title = ?, category = ?, description = ?, status = ?, owner = ?, created_at = ?
            WHERE id = ?
            """,
            (title, category, description, status, owner, created_at, demand_id),
        )
        connection.commit()

    return get_demand_by_id(demand_id)


def delete_demand(demand_id):
    """Exclui uma demanda. Retorna True se alguma linha foi apagada."""
    with closing(get_connection()) as connection:
        cursor = connection.execute(
            "DELETE FROM demands WHERE id = ?",
            (demand_id,),
        )
        connection.commit()
        return cursor.rowcount > 0


def get_summary():
    """Conta quantas demandas existem no total e em cada status."""
    with closing(get_connection()) as connection:
        rows = connection.execute(
            "SELECT status, COUNT(*) AS quantidade FROM demands GROUP BY status"
        ).fetchall()

    # Ex.: {"pendente": 1, "em andamento": 1, "concluída": 1}
    by_status = {row["status"]: row["quantidade"] for row in rows}

    return {
        "total": sum(by_status.values()),
        "pending": by_status.get("pendente", 0),
        "in_progress": by_status.get("em andamento", 0),
        "done": by_status.get("concluída", 0),
    }

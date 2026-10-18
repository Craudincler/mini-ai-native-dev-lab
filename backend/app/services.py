from app.database import get_summary, list_demands

VALID_STATUS = ["pendente", "em andamento", "concluída"]


def normalize_status(status: str) -> str:
    """Padroniza o status; se vier um valor desconhecido, usa 'pendente'."""
    value = status.strip().lower()
    if value not in VALID_STATUS:
        return "pendente"
    return value


def build_summary():
    return get_summary()


def list_all_demands():
    return list_demands()

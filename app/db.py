import psycopg

from app.config import get_settings

settings = get_settings()

conninfo = f"dbname={settings.db_name} user={settings.db_user} password={settings.db_password} host={settings.db_host}"


def get_conn():
    return psycopg.connect(conninfo=conninfo)

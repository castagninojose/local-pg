"""Project configurations.
"""

from typing import Dict

from decouple import AutoConfig

from localpg.constants import LOG_DIR, PARENT_LOGGER, PG_PORT_DEFAULT, REPO_ROOT

config = AutoConfig(search_path=REPO_ROOT)

COMPOSE_PROJECT_NAME = config("COMPOSE_PROJECT_NAME", default="localpg", cast=str)


PG_CFG = {
    "dialect": config("POSTGRES_DIALECT", default="postgres", cast=str),
    "driver": config("POSTGRES_DRIVER", default="psycopg2", cast=str),
    "username": config("POSTGRES_USER", default="pg-loader", cast=str),
    "password": config("POSTGRES_PASSWORD", default="pg-loader", cast=str),
    "host": config("POSTGRES_HOST", default="postgres-db", cast=str),
    "port": PG_PORT_DEFAULT,
    "database": config("POSTGRES_DB", default="db", cast=str),
    "db_type": config("POSTGRES_DB_TYPE", default="postgres", cast=str),
}


DEFAULT_LOGGER_CONFIG = {"level": "DEBUG", "handlers": ["console", "file"]}

GENERAL_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s-%(name)s-%(levelname)s: %(message)s"}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": str(LOG_DIR),
            "maxBytes": 20 * 1024 ** 2,  # 20 Mb
            "backupCount": 9,
            "encoding": "utf8",
        },
    },
    "loggers": {
        PARENT_LOGGER: {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}


def get_uri_db_pg(pg_cfg: Dict[str, str]) -> str:
    """Build SQLAlchemy URI

    Parameters
    ----------
    pg_cfg : dict
        Postgres credentials.
        It has the following keys:
            - dialect
            - driver
            - username
            - password
            - host
            - port
            - database
            - db_type

    Returns
    -------
    uri_db : str
        Connection string of SqlAlchemy

    """
    uri_db = f"{pg_cfg['dialect']}://{pg_cfg['username']}:{pg_cfg['password']}@{pg_cfg['host']}:{pg_cfg['port']}/{pg_cfg['database']}"  # noqa: E501
    return uri_db

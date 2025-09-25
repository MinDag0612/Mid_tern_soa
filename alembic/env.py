from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Alembic Config object, provides access to values within alembic.ini
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# No SQLAlchemy models metadata; migrations use imperative style
TARGET_METADATA = None


load_dotenv()


def _build_database_url() -> str:
    host = os.getenv("DB_HOST", "mysql")
    port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "TuitionDB")
    username = os.getenv("DB_USER", "sa")
    password = os.getenv("DB_PASSWORD", "12345")
    charset = os.getenv("DB_CHARSET", "utf8mb4")

    auth_part = username
    if password:
        auth_part = f"{username}:{password}"

    return (
        f"mysql+pymysql://{auth_part}@{host}:{port}/{db_name}"
        f"?charset={charset}"
    )


def run_migrations_offline() -> None:
    url = _build_database_url()
    context.configure(
        url=url,
        target_metadata=TARGET_METADATA,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(_build_database_url(), future=True)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=TARGET_METADATA,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

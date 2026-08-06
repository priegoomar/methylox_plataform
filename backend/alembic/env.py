from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.database import Base
from app import models


# Alembic Config object
config = context.config


# Configuración de logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Metadata para detectar modelos
target_metadata = Base.metadata


# Leer DATABASE_URL desde Render
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception(
        "DATABASE_URL environment variable is missing"
    )


# Reemplazar URL de alembic.ini
config.set_main_option(
    "sqlalchemy.url",
    DATABASE_URL
)


# ==========================================
# MIGRACIONES OFFLINE
# ==========================================

def run_migrations_offline():
    url = config.get_main_option(
        "sqlalchemy.url"
    )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
    )

    with context.begin_transaction():
        context.run_migrations()


# ==========================================
# MIGRACIONES ONLINE
# ==========================================

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ==========================================
# EXECUTION
# ==========================================

if context.is_offline_mode():
    run_migrations_offline()

else:
    run_migrations_online()

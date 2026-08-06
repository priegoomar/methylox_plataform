from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.database import Base
from app import models

# ==========================================
# ALEMBIC CONFIGURATION
# ==========================================
config = context.config

# Configuración de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de SQLAlchemy para autogenerar migraciones
target_metadata = Base.metadata

# ==========================================
# DATABASE URL FROM RENDER
# ==========================================
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise Exception("DATABASE_URL is not configured")

# Render entrega postgresql://
# SQLAlchemy necesita el driver psycopg2
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# ==========================================
# OFFLINE MIGRATIONS
# ==========================================
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# ==========================================
# ONLINE MIGRATIONS
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
# EXECUTE
# ==========================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

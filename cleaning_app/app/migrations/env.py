import os
import sys

from sqlalchemy import create_engine

from alembic import context


myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../../")

config = context.config

from core.db import BaseMeta, DATABASE_URL  # noqa: E402

target_metadata = BaseMeta.metadata

import app.users.models  # noqa: E402, F401
import app.apartments.models  # noqa: E402, F401
import app.tasks.models  # noqa: E402, F401


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

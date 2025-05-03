from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import sys
import os

# Добавляем путь к src в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Импортируем ваши модели
from db.models import UserModel
from db.session import async_session_maker

config = context.config
fileConfig(config.config_file_name)

target_metadata = UserModel.metadata

def run_migrations_online():
    connectable = async_session_maker.bind

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_schemas=True
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()

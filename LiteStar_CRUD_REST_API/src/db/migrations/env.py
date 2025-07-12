from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from db.models import Base
from lib.settings import settings

target_metadata = Base.metadata

def run_migrations_online():
    connectable = create_async_engine(str(settings.DATABASE_URL))

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()

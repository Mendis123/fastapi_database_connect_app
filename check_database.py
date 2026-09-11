from sqlalchemy import create_engine, text
from config import settings

engine = create_engine(settings.database_url)

with engine.connect() as connection:
    connection.execute(text('SELECT 1'))

print('database connection successful')

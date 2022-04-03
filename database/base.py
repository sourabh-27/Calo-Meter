# Import all the models, so that Base has them before being
# imported by Alembic
from .base_class import Base  # noqa
import os

def get_url():
    from dotenv import load_dotenv

    load_dotenv()
    user = os.getenv("MYSQL_USERNAME")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST")
    db = os.getenv("MYSQL_DBNAME")
    return f"mysql://{user}:{password}@{host}/{db}"
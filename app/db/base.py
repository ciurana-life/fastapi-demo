# Import all the models, so that Base has them before being
# imported by Alembic


from app.db.base_class import Base  # noqa: <Error>, isort: skip
from app.users.models import User  # noqa: <Error>, isort: skip

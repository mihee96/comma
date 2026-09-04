# Alembic autogenerate 와 create_all 이 모든 모델을 인식하도록 한 곳에서 import 합니다.
from app.db.base_class import Base  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.village import Village  # noqa: F401
from app.models.reservation import Reservation  # noqa: F401
from app.models.review import Review  # noqa: F401
from app.models.subscription import Subscription  # noqa: F401

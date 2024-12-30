import pytest
from sqlalchemy import create_engine

from core.config import settings
from core.models import Base
from main import main_app
from fastapi.testclient import TestClient
import core.models.base
from secure import create_jwt
from tests.schemas import RequestDTO


@pytest.fixture(scope="session",autouse=True)
def setup_db():
    engine = create_engine(str(settings.db.sync_url))
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.fixture(scope="session")
def client():

    with TestClient(main_app) as client:
        yield client


@pytest.fixture(scope="session")
def data_for_test(request):
    user_id=request.param.id
    if type(user_id) == int:
        token = create_jwt(user_id)
    else:
        token = user_id
    return RequestDTO(token=token,data=request.param.data)

def idfn(val):
    return "id " + str(val.id) + " status code " + str(val.data.status_code)
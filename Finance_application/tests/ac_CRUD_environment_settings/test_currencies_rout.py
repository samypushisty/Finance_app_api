import time
import pytest
import json

from core.redis_db.redis_helper import redis_client
from tests.ac_CRUD_environment_settings.datafortest import DataForTestCurrencies
from tests.conftest import idfn
from tests.schemas import DataDTO, DataForFixture
data_test = DataForTestCurrencies()

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.input)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=data_test.wrong_currency)),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data=data_test.input))],
                         indirect=True, scope="function", ids=idfn)
def test_get(client,data_for_test):
    response = client.get("/api/v1/environment_settings/currencies", params={"token": data_for_test.token, "name":data_for_test.data.data["name"]})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code == data_for_test.data.status_code
    if response.status_code == 200:
        assert answer["detail"]["price"] == float(redis_client.get(data_test.input["name"]))

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200)),
                          DataForFixture(id="www",data=DataDTO(status_code=401))],
                         indirect=True, scope="function", ids=idfn)
def test_get_all(client,data_for_test):
    response = client.get("/api/v1/environment_settings/currencies/all", params={"token": data_for_test.token})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code ==data_for_test.data.status_code
    if response.status_code == 200:
            assert answer["detail"]["currencies"] == redis_client.keys('*')

import time

import pytest
import json

from secure.jwt_functions import validation
from tests.ab_settings.datafortest import DataForTestSettings
from tests.conftest import idfn
from tests.schemas import DataDTO, DataForFixture
testdata = DataForTestSettings()

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=testdata.new)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=testdata.new_wrong)),
                          DataForFixture(id=9999,data=DataDTO(status_code=404,data=testdata.new)),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data=testdata.new))],
                         indirect=True, scope="function", ids=idfn)
def test_settings_patch(client,data_for_test):
    response = client.patch("/api/v1/settings",json=data_for_test.data.data, params={"token": data_for_test.token})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code == data_for_test.data.status_code

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=testdata.new)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=200,data=testdata.old)),
                          DataForFixture(id=9999,data=DataDTO(status_code=404)),
                          DataForFixture(id="www",data=DataDTO(status_code=401))],
                         indirect=True, scope="function", ids=idfn)
def test_settings_get(client,data_for_test):
    response = client.get("/api/v1/settings", params={"token": data_for_test.token})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code == data_for_test.data.status_code
    if response.status_code == 200:
        data = data_for_test.data.data
        data["chat_id"] = validation(data_for_test.token).id
        assert answer["detail"] == data_for_test.data.data




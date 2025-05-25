import time
import pytest
import json

from tests.ac_CRUD_environment_settings.datafortest import DataForTestUserCategories
from tests.conftest import idfn
from tests.schemas import DataDTO, DataForFixture
data_test = DataForTestUserCategories()

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.input)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.input)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.input)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.input)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.input)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=data_test.wrong_limit)),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data=data_test.input))],
                         indirect=True, scope="function", ids=idfn)
def test_post(client,data_for_test):
    response = client.post("/api/v1/environment_settings/category",json=data_for_test.data.data, params={"token": data_for_test.token})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code == data_for_test.data.status_code

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404)),
                          DataForFixture(id="www",data=DataDTO(status_code=401))],
                         indirect=True, scope="function", ids=idfn)
def test_get_all(client,data_for_test):
    response = client.get("/api/v1/environment_settings/category/all", params={"token": data_for_test.token})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code ==data_for_test.data.status_code
    if response.status_code == 200:
        data = data_test.for_test
        for i in range(5):
            data["table_id"] = i+1
            assert answer["detail"]["categories"][i] == data

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.new_id_2)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.new_id_4)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=data_test.new_wrong_limit)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404,data=data_test.new_wrong_id)),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data=data_test.new_wrong_limit))],
                         indirect=True, scope="function", ids=idfn)
def test_patch(client,data_for_test):
    response = client.patch("/api/v1/environment_settings/category",json=data_for_test.data.data, params={"token": data_for_test.token})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code == data_for_test.data.status_code

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data={"table_id": 1})),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404,data={"table_id": 1})),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data={"table_id": 1}))],
                         indirect=True, scope="function", ids=idfn)
def test_delete(client,data_for_test):
    response = client.delete("/api/v1/environment_settings/category", params={"token": data_for_test.token, "table_id": data_for_test.data.data["table_id"]})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code == data_for_test.data.status_code

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data={"table_id": 3})),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404,data={"table_id": 3})),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data={"table_id": 3}))],
                         indirect=True, scope="function", ids=idfn)
def test_get(client,data_for_test):
    response = client.get("/api/v1/environment_settings/category", params={"token": data_for_test.token, "table_id": data_for_test.data.data["table_id"]})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code == data_for_test.data.status_code
    if response.status_code == 200:
        data = data_test.for_test
        data["table_id"] = 3
        assert answer["detail"] == data

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404)),
                          DataForFixture(id="www",data=DataDTO(status_code=401))],
                         indirect=True, scope="function", ids=idfn)
def test_get_all_patch(client,data_for_test):
    response = client.get("/api/v1/environment_settings/category/all", params={"token": data_for_test.token})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code ==data_for_test.data.status_code
    if response.status_code == 200:
        for i in range(4):
            if i % 2:
                data = data_test.for_test
            else:
                data = data_test.for_test_patch
            data["table_id"] = i+2
            assert answer["detail"]["categories"][i] == data
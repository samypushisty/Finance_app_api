import time
import pytest
import json

from tests.ac_CRUD_environment_settings.datafortest import DataForTestUserEnvironment
from tests.conftest import idfn
from tests.schemas import DataDTO, DataForFixture
data_test = DataForTestUserEnvironment()

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.data_param)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.data_param)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.data_param)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.data_param)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.data_param)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=data_test.wrong_data_param)),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data=data_test.data_param))],
                         indirect=True, scope="function", ids=idfn)
def test_post_user_category_post(client,data_for_test):
    response = client.post("/api/v1/category",json=data_for_test.data.data, params={"token": data_for_test.token})
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
def test_settings_get_all(client,data_for_test):
    response = client.get("/api/v1/category/all", params={"token": data_for_test.token})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code ==data_for_test.data.status_code
    if response.status_code == 200:
        data = data_test.data_param_for_test
        for i in range(5):
            data["category_id"] = i+1
            assert answer["detail"]["categories"][i] == data

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.new_data_param_2)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.new_data_param_4)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=data_test.new_wrong_data_param)),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data=data_test.new_wrong_data_param))],
                         indirect=True, scope="function", ids=idfn)
def test_user_category_patch(client,data_for_test):
    response = client.patch("/api/v1/category",json=data_for_test.data.data, params={"token": data_for_test.token})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code == data_for_test.data.status_code

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data={"category_id": 1})),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404,data={"category_id": 1})),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data={"category_id": 1}))],
                         indirect=True, scope="function", ids=idfn)
def test_user_category_delete(client,data_for_test):
    response = client.delete("/api/v1/category", params={"token": data_for_test.token, "category_id": data_for_test.data.data["category_id"]})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code == data_for_test.data.status_code

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data={"category_id": 3})),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404,data={"category_id": 3})),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data={"category_id": 3}))],
                         indirect=True, scope="function", ids=idfn)
def test_user_category_get(client,data_for_test):
    response = client.get("/api/v1/category", params={"token": data_for_test.token, "category_id": data_for_test.data.data["category_id"]})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code == data_for_test.data.status_code
    if response.status_code == 200:
        data = data_test.data_param_for_test
        data["category_id"] = 3
        assert answer["detail"] == data

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404)),
                          DataForFixture(id="www",data=DataDTO(status_code=401))],
                         indirect=True, scope="function", ids=idfn)
def test_settings_get_all_patch(client,data_for_test):
    response = client.get("/api/v1/category/all", params={"token": data_for_test.token})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code ==data_for_test.data.status_code
    if response.status_code == 200:
        for i in range(4):
            if i % 2:
                data = data_test.data_param_for_test
            else:
                data = data_test.data_param_for_test_patch
            data["category_id"] = i+2
            assert answer["detail"]["categories"][i] == data
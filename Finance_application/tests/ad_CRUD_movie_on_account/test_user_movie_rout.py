import time
from decimal import Decimal, ROUND_HALF_UP

import pytest
import json
from core.redis_db.redis_helper import redis_client
from tests.ad_CRUD_movie_on_account.datafortest import DataForTestMovieOnAccount
from tests.conftest import idfn
from tests.schemas import DataDTO, DataForFixture
data_test = DataForTestMovieOnAccount()

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.input_e2_c2)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.input_e3_c3)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.input_o2_c2)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.input_o3_c3)),
                          DataForFixture(id=9999999999, data=DataDTO(status_code=200, data=data_test.input_e3_c3_byn)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.input_o3_c3_byn)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=data_test.wrong_currency)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=data_test.wrong_type_o)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=data_test.wrong_cash_id)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=data_test.wrong_category_id)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=data_test.wrong_type_e)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=data_test.wrong_not_type)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=data_test.wrong_all_type)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404,data=data_test.input_wrong_user_o)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404,data=data_test.input_wrong_user_e)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=403,data=data_test.input_wrong_balance_0)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=403,data=data_test.input_wrong_balance_0_currency)),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data=data_test.input_e2_c2))],
                         indirect=True, scope="function", ids=idfn)
def test_post(client,data_for_test):
    response = client.post("/api/v1/movies",json=data_for_test.data.data, params={"token": data_for_test.token})
    answer = json.loads(response.text)
    assert response.status_code == data_for_test.data.status_code

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200, data={"page": 1})),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=404, data={"page": 2})),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=422, data={"page": 0})),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404, data={"page": 1})),
                          DataForFixture(id="www",data=DataDTO(status_code=401, data={"page": 1}))],
                         indirect=True, scope="function", ids=idfn)
def test_get_all(client,data_for_test):
    response = client.get("/api/v1/movies/all", params={"page":data_for_test.data.data["page"],"token": data_for_test.token})
    answer = json.loads(response.text)
    assert response.status_code == data_for_test.data.status_code
    if response.status_code == 200:
        data = data_test.for_test
        for i in range(6):
            assert answer["detail"]["movies"][i] == data[i]
        assert len(answer["detail"]["movies"]) == len(data)

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200)), ],
                         indirect=True, scope="function", ids=idfn)
def test_balance(client,data_for_test):
    response = client.get("/api/v1/total_balance", params={"token": data_for_test.token})
    answer = json.loads(response.text)
    response = client.get("/api/v1/total_balance", params={"token": data_for_test.token,"currency":"USD"})
    answer_balance_currency = json.loads(response.text)
    response = client.get("/api/v1/environment_settings/cash_accounts", params={"token": data_for_test.token, "table_id":2})
    answer_cash_account = json.loads(response.text)
    response = client.get("/api/v1/environment_settings/type_of_earnings", params={"token": data_for_test.token, "table_id":2})
    answer_earnings = json.loads(response.text)
    response = client.get("/api/v1/environment_settings/category", params={"token": data_for_test.token, "table_id":2})
    answer_outlays = json.loads(response.text)

    price_base = Decimal(redis_client.get("BYN"))
    price_convert = Decimal(redis_client.get("USD"))

    assert answer["detail"]["balance"] == str((Decimal("1800.00") / price_convert * price_base+Decimal("900.00")).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))
    assert answer_balance_currency["detail"]["balance"] == str((Decimal("900.00") / price_base * price_convert+Decimal("1800.00")).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))
    assert answer_cash_account["detail"]["balance"] == str((Decimal("900.00") / price_convert * price_base).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))
    assert answer_earnings["detail"]["balance"] == str((Decimal("1000.00") / price_convert * price_base).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))
    assert answer_outlays["detail"]["balance"] == str((Decimal("-100") / price_convert * price_base).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data={"table_id": 3})),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404,data={"table_id": 3})),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data={"table_id": 3}))],
                         indirect=True, scope="function", ids=idfn)
def test_get(client,data_for_test):
    response = client.get("/api/v1/movies", params={"token": data_for_test.token, "table_id": data_for_test.data.data["table_id"]})
    answer = json.loads(response.text)
    assert response.status_code == data_for_test.data.status_code
    if response.status_code == 200:
        data = data_test.for_test[2]
        data["table_id"] = 3
        assert answer["detail"] == data


@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.new_id_1)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.new_id_2)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.new_id_3)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=200,data=data_test.new_id_4)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404,data=data_test.new_wrong_id)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404,data=data_test.new_wrong_id)),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=403,data=data_test.new_wrong_balance_0)),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=422,data=data_test.new_wrong_currency)),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data=data_test.new_wrong_id))],
                         indirect=True, scope="function", ids=idfn)
def test_patch(client,data_for_test):
    response = client.patch("/api/v1/movies",json=data_for_test.data.data, params={"token": data_for_test.token})
    answer = json.loads(response.text)
    print(answer)
    assert response.status_code == data_for_test.data.status_code

@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200)), ],
                         indirect=True, scope="function", ids=idfn)
def test_patch_balance_1(client,data_for_test):
    response = client.get("/api/v1/total_balance", params={"token": data_for_test.token})
    answer = json.loads(response.text)
    response = client.get("/api/v1/total_balance", params={"token": data_for_test.token, "currency": "USD"})
    answer_balance_currency = json.loads(response.text)
    response = client.get("/api/v1/environment_settings/cash_accounts",
                          params={"token": data_for_test.token, "table_id": 2})
    answer_cash_account = json.loads(response.text)
    response = client.get("/api/v1/environment_settings/type_of_earnings",
                          params={"token": data_for_test.token, "table_id": 2})
    answer_earnings = json.loads(response.text)
    response = client.get("/api/v1/environment_settings/category", params={"token": data_for_test.token, "table_id": 2})
    answer_outlays = json.loads(response.text)

    price_base = Decimal(redis_client.get("BYN"))
    price_convert = Decimal(redis_client.get("USD"))

    assert answer["detail"]["balance"] == str(
        (Decimal("2800.00") / price_convert * price_base).quantize(Decimal("0.00"),
                                                                                       rounding=ROUND_HALF_UP))
    assert answer_cash_account["detail"]["balance"] == str(
        (Decimal("1000.00") / price_convert * price_base).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))
    assert answer_earnings["detail"]["balance"] == str(
        (Decimal("1200.00") / price_convert * price_base).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))
    assert answer_outlays["detail"]["balance"] == str(
        (Decimal("-200") / price_convert * price_base).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))



@pytest.mark.parametrize("data_for_test",
                         [DataForFixture(id=9999999999,data=DataDTO(status_code=200,data={"table_id": 4})),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=403,data={"table_id": 1})),
                          DataForFixture(id=9999999999,data=DataDTO(status_code=404,data={"table_id": 4})),
                          DataForFixture(id=1234567897,data=DataDTO(status_code=404,data={"table_id": 1})),
                          DataForFixture(id="www",data=DataDTO(status_code=401,data={"table_id": 1}))],
                         indirect=True, scope="function", ids=idfn)
def test_delete(client,data_for_test):
    response = client.delete("/api/v1/movies", params={"token": data_for_test.token, "table_id": data_for_test.data.data["table_id"]})
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
def test_get_all_patch(client,data_for_test):
    response = client.get("/api/v1/movies/all", params={"page":1,"token": data_for_test.token})
    answer = json.loads(response.text)
    print(answer)
    print(data_for_test.data.status_code)
    print(time.time())
    assert response.status_code == data_for_test.data.status_code
    if response.status_code == 200:
        data = data_test.for_test_patch
        for i in range(5):
            assert answer["detail"]["movies"][i] == data[i]
        assert len(answer["detail"]["movies"]) == len(data)

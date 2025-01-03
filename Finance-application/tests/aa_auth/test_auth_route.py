import pytest
import json


@pytest.mark.parametrize("data,code",
                         [({"chat_id": 1234567897}, 200),({"chat_id": 9999999999}, 200), ({"chat_id": 1234}, 422)])
def test_auth(client,data,code):
    response = client.post("/api/v1/auth", json=data)
    answer = json.loads(response.text)
    print(answer["detail"])
    assert response.status_code == code
    if response.status_code == 200:
        answer = json.loads(response.text)
        assert len(answer["detail"]["jwt"].split(".")) == 3



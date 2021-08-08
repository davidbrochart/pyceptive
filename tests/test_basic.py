from datetime import datetime
from typing import List, Optional
from pyceptive import ObserverModel


class User(ObserverModel):
    id: int
    name = "John Doe"
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    "id": "123",
    "signup_ts": "2019-06-01 12:22",
    "friends": [1, 2, "3"],
}


def test_basic():
    user = User(**external_data)
    changes = []

    @user.on_change("id", "friends")
    def action():
        changes.append(user.copy())

    assert len(changes) == 0
    assert user.id == 123
    assert user.friends == [1, 2, 3]
    user.id = 1
    assert len(changes) == 1
    assert changes[-1].id == 1
    user.friends = [4]
    assert len(changes) == 2
    assert changes[-1].friends == [4]


from pylage.ENGINE.runtime.session_store import InMemorySessionStore


def test_session_store_put_and_get():
    store = InMemorySessionStore(ttl=300)
    session = object()

    store.put("token", session)

    assert store.get("token") is session


def test_session_store_get_refreshes_ttl():
    now = [100.0]

    def clock():
        return now[0]

    store = InMemorySessionStore(ttl=10, clock=clock)
    session = object()

    store.put("token", session)
    now[0] = 109.0

    assert store.get("token") is session

    now[0] = 118.0
    assert store.get("token") is session


def test_session_store_expired_entry_is_not_returned():
    now = [100.0]

    def clock():
        return now[0]

    store = InMemorySessionStore(ttl=10, clock=clock)
    session = object()

    store.put("token", session)
    now[0] = 110.0

    assert store.get("token") is None


def test_session_store_remove():
    store = InMemorySessionStore(ttl=300)
    session = object()

    store.put("token", session)

    assert store.remove("token") is session
    assert store.get("token") is None
    assert store.remove("token") is None


def test_session_store_evict_expired():
    now = [100.0]

    def clock():
        return now[0]

    store = InMemorySessionStore(ttl=10, clock=clock)
    active = object()
    expired = object()

    store.put("active", active)
    store.put("expired", expired)
    now[0] = 109.0
    assert store.get("active") is active
    now[0] = 110.0

    assert store.evict_expired() == [("expired", expired)]
    assert store.get("expired") is None
    assert store.get("active") is active


def test_session_store_clear_returns_entries():
    store = InMemorySessionStore(ttl=300)
    first = object()
    second = object()

    store.put("first", first)
    store.put("second", second)

    assert set(store.clear()) == {("first", first), ("second", second)}
    assert store.get("first") is None
    assert store.get("second") is None


def test_session_store_rejects_invalid_ttl():
    try:
        InMemorySessionStore(ttl=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for non-positive TTL")

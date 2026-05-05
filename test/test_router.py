import pytest

from game.core.router import Router


@pytest.fixture
def router():
    return Router()


def test_router_dispatch(capsys, router):
    event_type = int

    def handle(event: event_type):
        print(f"Received event: {event}")

    router.register(event_type, handle)
    router.dispatch(5)
    captured = capsys.readouterr()
    assert "Received event: 5" in captured.out


def test_router_priority(capsys, router):
    event_type = int

    def handle_first(event: event_type):
        print(f"First handler received: {event}")

    def handle_snd(event: event_type):
        print(f"Second handler received: {event}")

    router.register(event_type, handle_first)
    router.register(event_type, handle_snd)
    router.dispatch(5)
    captured = capsys.readouterr()
    assert captured.out == "First handler received: 5\nSecond handler received: 5\n"

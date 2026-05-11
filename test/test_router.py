import pytest

from game.core.router import Router


@pytest.fixture
def router():
    return Router()


def test_router_dispatch(capsys, router):
    def handle(event: int):
        print(f"Received event: {event}")

    router.register(int, handle)
    router.dispatch(5)
    captured = capsys.readouterr()
    assert "Received event: 5" in captured.out


def test_router_priority(capsys, router):
    def handle_first(event: int):
        print(f"First handler received: {event}")

    def handle_snd(event: int):
        print(f"Second handler received: {event}")

    router.register(int, handle_first)
    router.register(int, handle_snd)
    router.dispatch(5)
    captured = capsys.readouterr()
    assert captured.out == "First handler received: 5\nSecond handler received: 5\n"

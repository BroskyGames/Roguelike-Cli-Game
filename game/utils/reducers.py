from typing import Any, Protocol, overload


class ReducerFn[V, A](Protocol):
    @overload
    def __call__(self, __value: V, __acc: A) -> A: ...

    @overload
    def __call__(self, __value: V, __acc: Any) -> A: ...


class Reducer[A, V]:
    def __init__(
        self,
        function: ReducerFn[V, A],
        initial: A | None = None,
    ):
        self.function = function
        self.acc: A | None = initial

    def __call__(self, value: V):
        self.acc = self.function(value, self.acc)

    def get_acc(self) -> A:
        assert self.acc is not None, "Accumulator is not initialized"
        return self.acc


@overload
def combine_reducers[T1, V](
    r1: Reducer[T1, V],
    /,
) -> Reducer[tuple[T1], V]: ...


@overload
def combine_reducers[T1, T2, V](
    r1: Reducer[T1, V],
    r2: Reducer[T2, V],
    /,
) -> Reducer[tuple[T1, T2], V]: ...


@overload
def combine_reducers[T1, T2, T3, V](
    r1: Reducer[T1, V],
    r2: Reducer[T2, V],
    r3: Reducer[T3, V],
    /,
) -> Reducer[tuple[T1, T2, T3], V]: ...


@overload
def combine_reducers[T1, T2, T3, T4, V](
    r1: Reducer[T1, V],
    r2: Reducer[T2, V],
    r3: Reducer[T3, V],
    r4: Reducer[T4, V],
    /,
) -> Reducer[tuple[T1, T2, T3, T4], V]: ...


@overload
def combine_reducers[T1, T2, T3, T4, T5, V](
    r1: Reducer[T1, V],
    r2: Reducer[T2, V],
    r3: Reducer[T3, V],
    r4: Reducer[T4, V],
    r5: Reducer[T5, V],
    /,
) -> Reducer[tuple[T1, T2, T3, T4, T5], V]: ...


def combine_reducers[V](
    *reducers: Reducer[Any, V],
) -> Reducer[tuple[Any, ...], V]:
    def combined_function(value: V, _: Any) -> tuple[Any]:
        acc = []
        for reducer in reducers:
            reducer(value)
            acc.append(reducer.acc)
        return tuple(acc)

    return Reducer(combined_function, None)


if __name__ == "__main__":

    def test(reducer: Reducer[Any, int]) -> Any:
        for i in range(10):
            reducer(i)
        return reducer.acc

    def add(x: int, acc: int):
        return acc + x

    def add_twice(x: int, acc: int):
        return acc + x * 2

    def last(x: int, _: Any):
        return x

    a = combine_reducers(
        Reducer(add, 0),
        Reducer(add, 1),
        Reducer(add_twice, 1),
        Reducer(last, None),
    )

    print(test(a))

from typing import Any, Callable, TypeVar, overload


class Reducer[T, V]:
    def __init__(self, function: Callable[[V, T | None], T], initial: T | None):
        self.function = function
        self.acc: T | None = initial
    def __call__(self, value: V):
        self.acc = self.function(value, self.acc)

@overload
def combine_reducers[T1, V](
    r1: Reducer[T1, V],
) -> Reducer[tuple[T1], V]: ...

@overload
def combine_reducers[T1, T2, V](
    r1: Reducer[T1, V],
    r2: Reducer[T2, V],
) -> Reducer[tuple[T1, T2], V]: ...

@overload
def combine_reducers[T1, T2, T3, V](
    r1: Reducer[T1, V],
    r2: Reducer[T2, V],
    r3: Reducer[T3, V],
) -> Reducer[tuple[T1, T2, T3], V]: ...

@overload
def combine_reducers[T1, T2, T3, T4, V](
    r1: Reducer[T1, V],
    r2: Reducer[T2, V],
    r3: Reducer[T3, V],
    r4: Reducer[T4, V],
) -> Reducer[tuple[T1, T2, T3, T4], V]: ...

@overload
def combine_reducers[T1, T2, T3, T4, T5, V](
    r1: Reducer[T1, V],
    r2: Reducer[T2, V],
    r3: Reducer[T3, V],
    r4: Reducer[T4, V],
    r5: Reducer[T5, V],
) -> Reducer[tuple[T1, T2, T3, T4, T5], V]: ...

def combine_reducers[V](*reducers: Reducer[Any, V]) -> Reducer[tuple[Any, ...], V]:
    def combined_function(value: V, _: None) -> tuple[Any]:
        acc = []
        for reducer in reducers:
            reducer(value)
            acc.append(reducer.acc)
        return tuple(acc)

    return Reducer(combined_function, None)


if __name__ == '__main__':
    def test(reducer: Reducer[Any, int]) -> Any:
        for i in range(10):
            reducer(i)
        return reducer.acc

    def add(x: int, acc: int):
        return acc + x

    def add_twice(x: int, acc: int):
        return acc + x*2

    print(test(combine_reducers(Reducer(add, 0), Reducer(add, 1), Reducer(add_twice, 1))))
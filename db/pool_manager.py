from typing import TypeVar, Generic


T = TypeVar("T")


class ReusablePool(Generic[T]):
    def __init__(self, size: int) -> None:
        if size <= 0:
            raise ValueError("'size' should be greater than zero")
        self.size: int = size
        self.free: list[T] = []
        self.in_use: list[T] = []

        for _ in range(size):
            self.free.append(T())

    def acquire(self) -> T:
        if len(self.free) <= 0:
            raise Exception("No more objects are available")

        obj = self.free[0]
        self.free.remove(obj)
        self.in_use.append(obj)
        return obj

    def release(self, obj: T) -> None:
        self.in_use.remove(obj)
        self.free.append(obj)


class PoolManager:
    def __init__(self, pool: ReusablePool):
        self.pool = pool

    def __enter__(self) -> T:
        self.obj = self.pool.acquire()
        return self.obj

    def __exit__(self, type, value, traceback):
        self.pool.release(self.obj)

from collections import deque
from typing import Any


class Stack:
    """Стек (LIFO) на основе списка."""

    def __init__(self) -> None:
        self._data: list[Any] = []

    def push(self, item: Any) -> None:
        """Добавить элемент на вершину стека."""
        self._data.append(item)

    def pop(self) -> Any:
        """Снять и вернуть верхний элемент стека.
        Выбрасывает IndexError, если стек пуст.
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Any | None:
        """Вернуть верхний элемент без удаления.
        Возвращает None, если стек пуст.
        """
        return self._data[-1] if self._data else None

    def is_empty(self) -> bool:
        """Проверить, пуст ли стек."""
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data})"


class Queue:
    """Очередь (FIFO) на основе collections.deque."""

    def __init__(self) -> None:
        self._data: deque[Any] = deque()

    def enqueue(self, item: Any) -> None:
        """Добавить элемент в конец очереди."""
        self._data.append(item)

    def dequeue(self) -> Any:
        """Извлечь и вернуть первый элемент очереди.
        Выбрасывает IndexError, если очередь пуста.
        """
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()

    def peek(self) -> Any | None:
        """Вернуть первый элемент без удаления.
        Возвращает None, если очередь пуста.
        """
        return self._data[0] if self._data else None

    def is_empty(self) -> bool:
        """Проверить, пуста ли очередь."""
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Queue({list(self._data)})"

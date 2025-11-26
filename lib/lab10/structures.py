from collections import deque
from typing import Any, Optional

class Stack:
    """Стек (LIFO) на основе list."""
    
    def __init__(self):
        self._data: list[Any] = []

    def push(self, item: Any) -> None:
        """Добавить элемент на вершину стека."""
        self._data.append(item)

    def pop(self) -> Any:
        """Снять и вернуть верхний элемент стека."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Optional[Any]:
        """Вернуть верхний элемент без удаления. None, если стек пуст."""
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self) -> bool:
        """Проверить, пуст ли стек."""
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data})"


class Queue:
    """Очередь (FIFO) на основе collections.deque."""
    
    def __init__(self):
        self._data: deque[Any] = deque()

    def enqueue(self, item: Any) -> None:
        """Добавить элемент в конец очереди."""
        self._data.append(item)

    def dequeue(self) -> Any:
        """Взять и вернуть первый элемент очереди."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()

    def peek(self) -> Optional[Any]:
        """Вернуть первый элемент без удаления. None, если очередь пуста."""
        if self.is_empty():
            return None
        return self._data[0]

    def is_empty(self) -> bool:
        """Проверить, пуста ли очередь."""
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Queue({list(self._data)})"
    
if __name__ == "__main__":
    print("🔍 Тестирование Stack:")
    s = Stack()
    s.push(10)
    s.push(20)
    print(f"  peek: {s.peek()}")        # 20
    print(f"  pop: {s.pop()}")          # 20
    print(f"  pop: {s.pop()}")          # 10
    print(f"  пустой: {s.is_empty()}")  # True

    print("\n🔍 Тестирование Queue:")
    q = Queue()
    q.enqueue("A")
    q.enqueue("B")
    print(f"  peek: {q.peek()}")        # A
    print(f"  dequeue: {q.dequeue()}")  # A
    print(f"  dequeue: {q.dequeue()}")  # B
    print(f"  пустая: {q.is_empty()}")  # True
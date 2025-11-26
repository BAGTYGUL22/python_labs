from typing import Any, Optional, Iterator

class Node:
    """Узел односвязного списка."""
    
    __slots__ = ('value', 'next')
    
    def __init__(self, value: Any, next: Optional['Node'] = None):
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.value})"


class SinglyLinkedList:
    """Односвязный список."""
    
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None  # для O(1) append
        self._size: int = 0

    def append(self, value: Any) -> None:
        """Добавить элемент в конец списка за O(1)."""
        new_node = Node(value)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def prepend(self, value: Any) -> None:
        """Добавить элемент в начало списка за O(1)."""
        new_node = Node(value, self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self._size += 1

    def insert(self, idx: int, value: Any) -> None:
        """Вставить элемент по индексу. Поддерживает вставку в конец."""
        if idx < 0 or idx > self._size:
            raise IndexError("list index out of range")
        
        if idx == 0:
            self.prepend(value)
        elif idx == self._size:
            self.append(value)
        else:
            # Идём до предыдущего узла
            current = self.head
            for _ in range(idx - 1):
                assert current is not None
                current = current.next
            new_node = Node(value, current.next)
            current.next = new_node
            self._size += 1

    def remove(self, value: Any) -> None:
        """Удалить первое вхождение значения. Если не найдено — ничего не делает."""
        if self.head is None:
            return
        
        # Удаление из головы
        if self.head.value == value:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self._size -= 1
            return
        
        # Поиск предыдущего узла
        current = self.head
        while current.next is not None and current.next.value != value:
            current = current.next
        
        if current.next is not None:
            # Нашли — удаляем
            current.next = current.next.next
            if current.next is None:
                self.tail = current
            self._size -= 1

    def __iter__(self) -> Iterator[Any]:
        """Итерация по значениям списка."""
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"SinglyLinkedList({list(self)})"

    def __str__(self) -> str:
        """Красивый вывод: [A] -> [B] -> [C] -> None"""
        if self.head is None:
            return "None"
        parts = []
        current = self.head
        while current:
            parts.append(f"[{current.value}]")
            current = current.next
        return " -> ".join(parts) + " -> None"


if __name__ == "__main__":
    print(" Тестирование SinglyLinkedList:")
    ll = SinglyLinkedList()
    ll.append("X")
    ll.append("Y")
    ll.prepend("START")
    ll.insert(2, "MIDDLE")
    print(f"  Список: {ll}")           # [START] -> [X] -> [MIDDLE] -> [Y] -> None
    print(f"  Длина: {len(ll)}")       # 4
    print(f"  Как список: {list(ll)}") # ['START', 'X', 'MIDDLE', 'Y']

    ll.remove("MIDDLE")
    print(f"  После удаления 'MIDDLE': {ll}")  # [START] -> [X] -> [Y] -> None
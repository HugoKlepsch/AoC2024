import dataclasses
import typing


@dataclasses.dataclass
class Node:
    data: typing.Any
    next: typing.Optional[typing.Self]
    prev: typing.Optional[typing.Self]


@dataclasses.dataclass
class DoublyLinkedList:
    head: typing.Optional[Node] = None
    tail: typing.Optional[Node] = None
    size: int = 0

    def append(self, data: typing.Any):
        """Add a new node at the end of the list"""

        # Increment list size
        self.size += 1

        # Check if the list is empty and create a new node with default data
        if not self.head:
            self.head = Node(data, None, None)
            self.tail = self.head
            return

        # Create a new node for appending
        new_node = Node(data, None, self.tail)
        self.tail.next = new_node
        self.tail = new_node
        return

    def prepend(self, data: typing.Any):
        """Add a new node at the beginning of the list"""

        # Increment list size
        self.size += 1

        # Check if the list is empty and create a new node with default data
        if not self.head:
            self.head = Node(data, None, None)
            self.tail = self.head
            return

        # Create a new node for appending
        new_node = Node(data, self.head, None)
        self.head.prev = new_node
        self.head = new_node
        return

    def insert_before(self, data: typing.Any, index: int):
        assert 0 <= index < self.size
        current_node: typing.Optional[Node] = self.head
        i = 0
        while current_node:
            if i == index:
                previous_node = current_node.prev
                after_node = current_node
                new_node = Node(data, previous_node, after_node)
                previous_node.next = new_node
                after_node.prev = new_node
                self.size += 1
                return
            current_node = current_node.next
            i += 1

    def remove(self, index: int):
        assert 0 <= index < self.size
        current_node: typing.Optional[Node] = self.head
        i = 0
        while current_node:
            if i == index:
                previous_node = current_node.prev
                after_node = current_node.next
                previous_node.next = after_node
                after_node.prev = previous_node
                self.size -= 1
                return
            current_node = current_node.next
            i += 1

    def insert_before_node(self, data: typing.Any, n: Node):
        new_node = Node(data, n, n.prev)
        if n.prev is not None:
            n.prev.next = new_node
        n.prev = new_node
        if self.head == n:
            self.head = new_node
        self.size += 1

    def remove_node(self, n: Node) -> typing.Any:
        if n.prev is not None:
            n.prev.next = n.next
        if n.next is not None:
            n.next.prev = n.prev
        if self.head == n:
            self.head = n.next
        if self.tail == n:
            self.tail = n.prev
        self.size -= 1
        return n.data

    def iterator(self) -> typing.Iterator[Node]:
        current_node: typing.Optional[Node] = self.head
        while current_node:
            yield current_node
            current_node = current_node.next

    def reverse_iterator(self) -> typing.Iterator[Node]:
        current_node: typing.Optional[Node] = self.tail
        while current_node:
            yield current_node
            current_node = current_node.prev

    def get_size(self):
        """Return the number of elements in the list"""
        return self.size

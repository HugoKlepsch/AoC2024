import timeit
import dataclasses
import typing


@dataclasses.dataclass
class Block:
    file_id: typing.Optional[int]
    file_part: typing.Optional[int]

    def is_empty(self) -> bool:
        return self.file_id is None


def p1():
    blocks: typing.List[Block] = read_parse()
    free_stack = []
    for i, block in enumerate(blocks):
        if block.is_empty():
            free_stack.append(i)  # AKA "Push"
    score = 0
    for block_i in range(len(blocks) - 1, -1, -1):
        block = blocks[block_i]
        if block.is_empty():
            continue
        free_i = free_stack.pop(0)
        if free_i > block_i:
            break
        blocks[free_i] = block
        blocks[block_i] = Block(None, None)

    output = ''
    for block_i in range(len(blocks)):
        block = blocks[block_i]
        file_id = block.file_id
        if block.is_empty():
            file_id = '.'
        else:
            score += block.file_id * block_i
        output += str(file_id)
    print(output)

    print(score)


@dataclasses.dataclass
class Span:
    start: int
    end: int  # One past the end
    file_id: typing.Optional[int]

    @property
    def length(self) -> int:
        return self.end - self.start

    def is_empty(self) -> bool:
        return self.file_id is None


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


def print_spans(spans: DoublyLinkedList):
    print('-------------------------')
    output = ''
    for node in spans.iterator():
        span: Span = node.data
        print(f'Span: {span}, is empty: {span.is_empty()}, length: {span.length}')
        if span.is_empty():
            output += '.' * span.length
        else:
            output += str(span.file_id) * span.length
    print(output)
    print('-------------------------')


def p2():
    blocks: typing.List[Block] = read_parse()

    spans: DoublyLinkedList = DoublyLinkedList()  # DLL of Node
    cur_span = Span(0, 0, 0)  # Assumption: There is always a file_id 0
    for i in range(1, len(blocks)):
        block = blocks[i]
        prev_block = blocks[i-1]
        if block.file_id != prev_block.file_id:
            # End current span and start new span
            cur_span.end = i
            spans.append(cur_span)
            cur_span = Span(i, 0, block.file_id)
    cur_span.end = len(blocks)
    spans.append(cur_span)

    current_node: typing.Optional[Node] = spans.tail
    while current_node is not None:
        span: Span = current_node.data
        if span.is_empty():
            current_node = current_node.prev
            continue
        free_node = spans.head
        while free_node is not None and free_node != current_node:
            free_span: Span = free_node.data
            if free_span.is_empty() and free_span.length >= span.length:
                if free_span.length == span.length:
                    # Case: exact length match
                    # Completely replace free span with used span, mark old used as free
                    free_span.file_id = span.file_id
                    span.file_id = None
                    break
                elif free_span.length > span.length:
                    # Case: More than enough space to move the span
                    # Shrink the free span to the right, and move span to the empty left space
                    old_len = span.length
                    old_file = span.file_id
                    new_start = free_span.start
                    new_end = new_start + old_len
                    new_span = Span(new_start, new_end, old_file)
                    free_span.start += span.length
                    spans.insert_before_node(new_span, free_node)
                    span.file_id = None
                    break
            free_node = free_node.next
        current_node = current_node.prev

    score = 0
    output = ''
    block_id = 0
    for node in spans.iterator():
        span: Span = node.data
        if span.is_empty():
            output += '.' * span.length
            block_id += span.length
        else:
            output += str(span.file_id) * span.length
            for i in range(span.length):
                score += span.file_id * block_id
                block_id += 1

    print(output)
    print(score)


def read_parse():
    with open('input') as f:
        data = f.read()
    blocks: typing.List[Block] = []
    data = data.strip()
    file_id = 0
    block_id = 0
    def next_or_none(i: typing.Iterable[typing.Any]):
        for e in i:
            yield e
        while True:
            yield None
    d_iter = next_or_none(data)
    c = next(d_iter)
    while c is not None:
        file_len = int(c)
        for file_part in range(file_len):
            blocks.append(Block(file_id, file_part))
            block_id += 1
        file_id += 1

        empty_char = next(d_iter)
        if empty_char is None:
            break
        empty_len = int(empty_char)
        for empty_part in range(empty_len):
            blocks.append(Block(None, None))
            block_id += 1

        c = next(d_iter)

    return blocks


if __name__ == '__main__':
    print(f'p1: {timeit.timeit(p1, number=1)}')
    print(f'p2: {timeit.timeit(p2, number=1)}')

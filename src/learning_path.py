from typing import TypeVar, Generic

import yaml
from pathlib import Path


T = TypeVar("T")


class Node(Generic[T]):

    TESTS_ROOT = Path(".") / 'tests'
    ABSOLUTE_ROOT = Path(".") / 'exercises'

    def __init__(self, base_path: str, filename: str, mode: str, hint: str):
        self.file_path = self.ABSOLUTE_ROOT / base_path / filename
        self.file_name = filename
        self.mode = mode
        self.hint = hint
        self.test_file_name = self.TESTS_ROOT / base_path / f"test_{filename}"
        self.next_node: T = None

    def set_next_node(self, node: T):
        self.next_node = node


class LearningPath:

    def __init__(self, raw):
        self.head = None
        self.lessons = {}

        prev = None
        for section, exercises in raw.items():
            for exercise_data in exercises.values():
                node = Node(section, **exercise_data)
                if self.head is None:
                    self.head = node
                if prev is not None:
                    prev.set_next_node(node)
                prev = node
                self.lessons[exercise_data['filename']] = node

    def __repr__(self):
        node: Node = self.head
        nodes: list[str] = []
        while node is not None:
            nodes.append(node.file_name)
            node: Node = node.next_node
        nodes.append("None")
        return " -> ".join(nodes)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next_node


def load_learning_path_from_file(filename: str | Path = "learning_path.yaml") -> LearningPath:
    with open(filename) as _file:
        return LearningPath(yaml.safe_load(_file))


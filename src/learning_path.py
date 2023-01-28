import subprocess
from enum import Enum
from typing import TypeVar, Generic

import yaml
from pathlib import Path

T = TypeVar("T")


class BasePath(Enum):
    TEST = Path(".") / 'tests'
    EXERCISE = Path(".") / 'exercises'


class Mode(Enum):
    TEST = 'pytest'
    RUN = 'python'


class Node(Generic[T]):

    def __init__(self, section: str, filename: str, mode: str, hint: str):
        self._section = section
        self._file_name = filename
        self._file_path = BasePath.EXERCISE.value / self._section / self._file_name
        self.mode: Mode = Mode(mode)
        self.hint = hint
        self.check_command: str = self._make_check_command()
        self.next_node: T = None

    @property
    def file_path(self):
        return self._file_path

    def _make_check_command(self) -> str:
        file_to_execute = self.file_path
        if self.mode == Mode.TEST:
            file_to_execute = BasePath.TEST.value / self._section / f"test_{self._file_name}"
        return f"{self.mode.value} {file_to_execute}"

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
            nodes.append(node._file_name)
            node: Node = node.next_node
        nodes.append("None")
        return " -> ".join(nodes)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next_node

    def find_first_lesson(self) -> (int, int):
        for index, node in enumerate(self.lessons.values()):
            result = subprocess.run(node.check_command, shell=True, capture_output=True)
            if result.returncode != 0:
                break
        else:
            index = len(self.lessons)
        return index, len(self.lessons)

    @classmethod
    def from_file(cls, filename: str | Path = "learning_path.yaml") -> 'LearningPath':
        with open(filename) as _file:
            return cls(yaml.safe_load(_file))

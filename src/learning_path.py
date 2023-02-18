import subprocess
from enum import Enum

from typing import Dict, Optional

import yaml
from pathlib import Path


class BasePath(Enum):
    TEST = Path(".") / 'tests'
    EXERCISE = Path(".") / 'exercises'


Mode = {
    "TEST": 'pytest',
    "RUN": 'python'
}


class Node:

    def __init__(self, section: str, filename: str, mode: str, hint: str):
        self._section = section
        self._file_name = filename
        self._file_path: Path = BasePath.EXERCISE.value / self._section / self._file_name
        self.mode: str = Mode[mode]
        self.hint = hint
        self.check_command: str = self._make_check_command()
        self.next_node = None

    @property
    def file_path(self) -> Path:
        return self._file_path

    def _make_check_command(self) -> str:
        file_to_execute = self.file_path
        if self.mode == Mode["TEST"]:
            file_to_execute = BasePath.TEST.value / self._section / f"test_{self._file_name}"
        return f"{self.mode} {file_to_execute}"

    def set_next_node(self, node: 'Node') -> None:
        self.next_node = node


class LearningPath:

    def __init__(self, raw: Dict[str, dict]) -> None:
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

    @property
    def total_lessons(self) -> int:
        return len(self.lessons)

    def __repr__(self) -> str:
        node: Node = self.head
        nodes: list[str] = []
        while node is not None:
            nodes.append(node.file_path.name)
            node: Node = node.next_node
        nodes.append("None")
        return " -> ".join(nodes)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next_node

    def find_first_lesson(self) -> (int, Optional[Node]):
        for index, node in enumerate(self.lessons.values()):
            result = subprocess.run(node.check_command, shell=True) #, capture_output=True)
            if result.returncode != 0:
                break
        else:
            index = len(self.lessons)
            node = None
        return index, node

    @classmethod
    def from_file(cls, filename: Path) -> 'LearningPath':
        with filename.absolute().open() as _file:
            return cls(yaml.safe_load(_file))

import os
import subprocess

from pbar import progress_bar

from learning_path import LearningPath, Node
from printer import Printer


class ExerciseHandler:

    def __init__(self, learning_path: LearningPath, printer: Printer) -> None:
        self._learning_path = learning_path
        self._progress_bar = None
        self._printer = printer

    def start(self):
        self._printer.start()
        start_index, start_node = self._learning_path.find_first_lesson()
        self._progress_bar = progress_bar(
            self._learning_path.total_lessons,
            start_index
        )
        if start_node is not None:
            self._printer.next_stage(start_node)
        else:
            self.finish()

    def finish(self):
        self._printer.finish()
        exit(0)

    def _handle_next_node(self, next_node: Node) -> None:
        self._progress_bar.update(1)
        self._progress_bar.display()
        self._printer.next_stage(next_node)

    def _handle_success(self, node: Node):
        if node.next_node is not None:
            self._handle_next_node(node.next_node)
        else:
            self.finish()

    def _handle_retry(self, node):
        self._printer.retry(node)
        self._progress_bar.display()

    def _handle(self, return_code: int, node: Node):
        if return_code == 0:
            self._handle_success(node)
        else:
            self._handle_retry(node)

    def handle(self, event):
        base_path, filename = os.path.split(event.src_path)
        node: Node = self._learning_path.lessons[filename]
        result = subprocess.run(node.check_command, shell=True)
        self._handle(result.returncode, node)

from handler import ExerciseHandler
from learning_path import LearningPath
from printer import Printer
from watcher import Watcher, EventHandler


def main():
    directory = '../exercises'
    learning_path = LearningPath.from_file('learning_path.yaml')
    exercise_handler = ExerciseHandler(
        learning_path=learning_path,
        printer=Printer()
    )
    handler = EventHandler(exercise_handler)
    w = Watcher(directory, handler)
    w.run()

import time
from datetime import datetime, timedelta

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from .handler import ExerciseHandler


class Watcher:
    def __init__(self, _directory, event_handler: 'EventHandler') -> None:
        self.observer = Observer()
        self.directory = _directory
        self.event_handler = event_handler

    def run(self) -> None:
        self.observer.schedule(self.event_handler, self.directory, recursive=True)
        self.observer.start()
        self.event_handler.exercise_handler.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Stop. Exiting...")
        finally:
            self.observer.join()


class EventHandler(FileSystemEventHandler):

    def __init__(self, exercise_handler: ExerciseHandler) -> None:
        self.last_modified = datetime.now()
        self.exercise_handler = exercise_handler

    def on_modified(self, event: FileModifiedEvent) -> None:
        if (datetime.now() - self.last_modified < timedelta(seconds=2)) or event.is_directory:
            return
        else:
            self.last_modified = datetime.now()

        if event.src_path.endswith('.py'):
            self.exercise_handler.handle(event)

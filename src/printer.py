import pyfiglet

from learning_path import Node


class Printer:
    def __init__(self, font: str = 'slant') -> None:
        self.figlet = pyfiglet.Figlet(font=font)

    def start(self) -> None:
        print(self.figlet.renderText('Welcome to pylings'))

    def finish(self) -> None:
        print(self.figlet.renderText('Congrats! You have just finished pylings'))

    @staticmethod
    def next_stage(next_node: Node) -> None:
        print(f"\nGo to the next stage: {next_node.file_path}")

    @staticmethod
    def retry(node: Node) -> None:
        print("There is still something missing here. Try again.\n")
        print(f"Here is a hint: {node.hint}")

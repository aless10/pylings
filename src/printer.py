import pyfiglet


class Printer:
    def __init__(self, font: str = 'slant') -> None:
        self.figlet = pyfiglet.Figlet(font=font)

    def start(self):
        print(self.figlet.renderText('Welcome to pythonlings'))

    def finish(self):
        print(self.figlet.renderText('Congrats! You have just finished pythonlings'))

    @staticmethod
    def next_stage(next_node):
        print(f"\nGo to the next stage: {next_node.next_node.file_path}")

    @staticmethod
    def retry(node):
        print("There is still something missing here. Try again.\n")
        print(f"Here is a hint: {node.hint}")

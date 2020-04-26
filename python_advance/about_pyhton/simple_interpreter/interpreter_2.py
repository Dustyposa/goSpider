from typing import Any


class Interpreter:
    def __init__(self):
        self.stack = []
        self.environment = {}

    def STORE_NAME(self, name) -> None:
        val = self.stack.pop()
        self.environment[name] = val

    def LOAD_NAME(self, name) -> None:
        val = self.environment[name]
        self.stack.append(val)

    def parse_argument(self, instruction, argument, what_to_execute) -> Any:
        """解析每条指令的实际参数"""
        numbers = ["LOAD_VALUE"]
        names = ["LOAD_NAME", "STORE_NAME"]
        if instruction in numbers:
            argument = what_to_execute["numbers"][argument]
        elif instruction in names:
            argument = what_to_execute["names"][argument]

        return argument

    def LOAD_VALUE(self, val) -> None:
        self.stack.append(val)

    def PRINT_ANSWER(self) -> None:
        answer = self.stack.pop()
        print(answer)

    def ADD_TWO_VALUES(self) -> None:
        total = self.stack.pop() + self.stack.pop()
        self.stack.append(total)

    def run_code(self, what_to_execute) -> None:
        instructions = what_to_execute["instructions"]
        for each_step in instructions:
            step_name, argument = each_step
            argument = self.parse_argument(step_name, argument, what_to_execute)
            bytes_method = getattr(self, step_name)
            if argument is None:
                bytes_method()
            else:
                bytes_method(argument)


if __name__ == '__main__':
    what_to_execute = {
        "instructions": [("LOAD_VALUE", 0),
                         ("STORE_NAME", 0),
                         ("LOAD_VALUE", 1),
                         ("STORE_NAME", 1),
                         ("LOAD_NAME", 0),
                         ("LOAD_NAME", 1),
                         ("ADD_TWO_VALUES", None),
                         ("PRINT_ANSWER", None)],
        "numbers": [1, 2],
        "names": ["a", "b"]}
    Interpreter().run_code(what_to_execute)

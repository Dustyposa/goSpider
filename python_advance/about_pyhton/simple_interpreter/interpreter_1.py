class Interpreter:
    def __init__(self):
        self.stack = []

    def LOAD_VALUE(self, val) -> None:
        self.stack.append(val)

    def PRINT_ANSWER(self) -> None:
        answer = self.stack.pop()
        print(answer)

    def ADD_TWO_VALUES(self) -> None:
        total = self.stack.pop() + self.stack.pop()
        self.stack.append(total)

    def run_code(self, what_to_execute) -> None:
        instructions, numbers = what_to_execute["instructions"], what_to_execute["numbers"]
        for each_step in instructions:
            step_name, argument = each_step
            if step_name == "LOAD_VALUE":
                getattr(self, step_name)(numbers[argument])
            elif step_name == "ADD_TWO_VALUES":
                getattr(self, step_name)()
            elif step_name == "PRINT_ANSWER":
                getattr(self, step_name)()


if __name__ == '__main__':
    # what_to_execute = {
    #     "instructions": [("LOAD_VALUE", 0),  # the first number
    #                      ("LOAD_VALUE", 1),  # the second number
    #                      ("ADD_TWO_VALUES", None),
    #                      ("PRINT_ANSWER", None)],
    #     "numbers": [7, 5]
    # }
    what_to_execute = {
        "instructions": [("LOAD_VALUE", 0),
                         ("LOAD_VALUE", 1),
                         ("ADD_TWO_VALUES", None),
                         ("LOAD_VALUE", 2),
                         ("ADD_TWO_VALUES", None),
                         ("PRINT_ANSWER", None)],
        "numbers": [7, 5, 8]}
    Interpreter().run_code(what_to_execute)

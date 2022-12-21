from collections import deque

from helpers import get_data


def get_result(operand_1: int, operand_2: int, operator: str):
    match operator:
        case '+':
            return operand_1 + operand_2
        case '-':
            return operand_1 - operand_2
        case '*':
            return operand_1 * operand_2
        case '/':
            return operand_1 / operand_2


def day_21():
    # data = get_data(21, "example")
    data = get_data(21)

    values = dict()
    calculations = deque()
    for line in data:
        name, says = line.strip().split(": ")
        if " " in says:
            operand_1, operator, operand_2 = says.split(" ")
            calculations.append(dict(operand_1=operand_1,
                                     operand_2=operand_2,
                                     operator=operator,
                                     value=name
                                     ))
        else:
            values[name] = int(says)

    while calculations:
        calc = next(c for c in calculations if c["operand_1"] in values and c["operand_2"] in values)
        calculations.remove(calc)

        values[calc["value"]] = get_result(values[calc["operand_1"]], values[calc["operand_2"]], calc["operator"])

    print("Part 1:", values["root"])


if __name__ == "__main__":
    day_21()

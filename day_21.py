from collections import deque

from helpers import get_data
from sympy.parsing.sympy_parser import parse_expr
from sympy import solve


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
    data = get_data(21, "example")
    # data = get_data(21)

    values = dict()
    values_2 = dict()
    calculations = deque()
    calculations_2 = dict()
    for line in data:
        name, says = line.strip().split(": ")
        if " " in says:
            operand_1, operator, operand_2 = says.split(" ")
            calculations.append(dict(operand_1=operand_1,
                                     operand_2=operand_2,
                                     operator=operator,
                                     value=name
                                     ))
            calculations_2[name] = says if name != "root" else says.replace("+", "=")
        else:
            values[name] = int(says)
            if name != "humn":
                values_2[name] = int(says)

    while calculations:
        calc = next(c for c in calculations if c["operand_1"] in values and c["operand_2"] in values)
        calculations.remove(calc)

        values[calc["value"]] = get_result(values[calc["operand_1"]], values[calc["operand_2"]], calc["operator"])

    print("Part 1:", values["root"])

    root = calculations_2["root"]
    del calculations_2["root"]

    o = root
    while calculations_2 or values_2:
        parts = o.split(" ")
        new = []
        for part in parts:
            if part in calculations_2:
                new.append(f" ( {calculations_2[part]} ) ")
                del calculations_2[part]
            elif part in values_2:
                new.append(str(values_2[part]))
                del values_2[part]
            else:
                new.append(part)
        o = " ".join(new)

    left, right = o.split(" = ")
    result_left = parse_expr(left)
    result_right = parse_expr(right)

    result = solve(parse_expr(f"{result_left} - {result_right}"))[0]

    print("Part 2:", result)


if __name__ == "__main__":
    day_21()

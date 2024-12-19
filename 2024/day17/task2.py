from dataclasses import dataclass
from enum import Enum
import re
from time import time
from typing import Optional, Union, Callable


from utils.file_utils import load_file, chunk_input


class Register(Enum):
    A = 0
    B = 1
    C = 2


Value = Union[str, int]


@dataclass
class State:

    ip: int
    registers: dict[Register, Value]
    outputs: list[int]
    expected_outputs: int


def eval_combo(operand: int, state: State) -> Value:
    assert 0 <= operand < 7, f"Invalid operand: {operand}"

    if operand <= 3:
        return operand

    if operand == 4:
        return state.registers[Register.A]

    if operand == 5:
        return state.registers[Register.B]

    if operand == 6:
        return state.registers[Register.C]

    raise ValueError(f"Invalid operand: {operand}")


def maybe_eval(lhs: Value, rhs: Value,
               stringify: Callable[[Value, Value], str],
               operator: Callable[[int, int], int]) -> Value:
    if isinstance(lhs, str) or isinstance(rhs, str):
        return stringify(lhs, rhs)
    return operator(lhs, rhs)


def div(operand: int, state: State, output_reg: Register) -> State:

    lhs = state.registers[Register.A]
    rhs = eval_combo(operand, state)

    state.registers[output_reg] = maybe_eval(
        lhs,
        rhs,
        lambda l, r: f"({l} >> {r})",
        lambda l, r: l >> r
    )

    state.ip += 2
    return state


def b_xor_lit(operand: int, state: State) -> State:

    lhs = state.registers[Register.B]
    rhs = operand

    state.registers[Register.B] = maybe_eval(
        lhs,
        rhs,
        lambda l, r: f"({l} ^ {r})",
        lambda l, r: l ^ r
    )

    state.ip += 2
    return state


def b_mod(operand: int, state: State) -> State:

    state.registers[Register.B] = maybe_eval(
        eval_combo(operand, state),
        8,
        lambda l, r: f"({l} % {r})",
        lambda l, r: l % r
    )

    state.ip += 2
    return state


def jump_not_zero(operand: int, state: State) -> State:
    if len(state.outputs) == state.expected_outputs:
        state.ip += 2
        return state

    print(f"Not enough outputs, jumping: {len(state.outputs)}, {
          state.expected_outputs}, {state.outputs}")
    state.ip = operand
    return state


def b_xor_c(_: int, state: State) -> State:

    state.registers[Register.B] = maybe_eval(
        state.registers[Register.B],
        state.registers[Register.C],
        lambda l, r: f"({l} ^ {r})",
        lambda l, r: l ^ r
    )

    state.ip += 2
    return state


def out(operand: int, state: State) -> State:

    state.outputs.append(
        maybe_eval(
            eval_combo(operand, state),
            8,
            lambda l, r: f"({l} % {r})",
            lambda l, r: l % r
        )
    )

    state.ip += 2
    return state


def run_program(state: State, program: list[int]) -> State:

    while state.ip < len(program):
        opcode = program[state.ip]
        operand = program[state.ip + 1]

        if opcode == 0:
            state = div(operand, state, Register.A)
        elif opcode == 1:
            state = b_xor_lit(operand, state)
        elif opcode == 2:
            state = b_mod(operand, state)
        elif opcode == 3:
            state = jump_not_zero(operand, state)
        elif opcode == 4:
            state = b_xor_c(operand, state)
        elif opcode == 5:
            state = out(operand, state)
        elif opcode == 6:
            state = div(operand, state, Register.B)
        elif opcode == 7:
            state = div(operand, state, Register.C)
        else:
            raise ValueError(f"Invalid opcode: {opcode}")

    return state


def self_replicate(filename_str: str) -> int:

    content = load_file(filename_str)

    register_inputs, program_inputs = chunk_input(content, "")

    assert len(register_inputs) == 3
    assert len(program_inputs) == 1

    program = list(map(int, re.findall(r'\d+', program_inputs[0])))
    state = State(
        ip=0,
        registers={
            Register.A: 'A',  # int(re.findall(r'\d+', register_inputs[0])[0]),
            Register.B: int(re.findall(r'\d+', register_inputs[1])[0]),
            Register.C: int(re.findall(r'\d+', register_inputs[2])[0])
        },
        outputs=[],
        expected_outputs=len(program)
    )

    state = run_program(state, program)

    print(state.outputs)

    # return ",".join(map(str, state.outputs))


if __name__ == "__main__":

    test_res = self_replicate("data2_test.txt")
    # assert test_res == "4,6,3,5,6,3,5,2,1,0", f"Test failed: {test_res}"
    # start = time()
    print(self_replicate("data1_real.txt"))
    # print("Execution time:", time() - start)

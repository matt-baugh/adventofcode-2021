from abc import ABC, abstractmethod
from pathlib import Path
from typing import Literal, Optional, Union

from tqdm import tqdm


from utils.file_utils import parse_file_lines

PRINT = False
LOW = 0
HIGH = 1


class Module(ABC):
    def __init__(self, name: str, dest_mods: list[str]):
        self.name = name
        self.dest_mods = dest_mods

    @abstractmethod
    def process_pulse(self, pulse_level: int, pulse_from: str) -> Optional[tuple[int, list[str]]]:
        pass


class FlipFlop(Module):
    def __init__(self, name: str, dest_mods: list[str]):
        super().__init__(name, dest_mods)
        self.on = False

    def process_pulse(self, pulse_level: int, pulse_from: str) -> Optional[tuple[int, list[str]]]:
        if pulse_level == 1:
            return None

        assert pulse_level == 0, f'Invalid pulse level: {pulse_level}'
        self.on = not self.on
        return (int(self.on), self.dest_mods)


class Conjunction(Module):
    def __init__(self, name: str, dest_mods: list[str]):
        super().__init__(name, dest_mods)
        self.memory: dict[str, int] = {}

    def process_pulse(self, pulse_level: int, pulse_from: str) -> Optional[tuple[int, list[str]]]:

        assert pulse_from in self.memory, f'Unexpected pulse from: {pulse_from} to {self.name}'
        self.memory[pulse_from] = pulse_level

        if all(self.memory.values()):
            return (LOW, self.dest_mods)
        else:
            return (HIGH, self.dest_mods)

    def add_input_module(self, mod_name: str):
        self.memory[mod_name] = 0


class Broadcast(Module):
    def __init__(self, name: str, dest_mods: list[str]):
        super().__init__(name, dest_mods)
        assert self.name == 'broadcaster'

    def process_pulse(self, pulse_level: int, pulse_from: str) -> Optional[tuple[int, list[str]]]:
        return (pulse_level, self.dest_mods)


def calc_pulses(filename: str, num_presses: int) -> int:

    raw_input = parse_file_lines(Path(__file__).parent / filename, ' -> ')

    module_map: dict[str, Module] = {}
    conj_modules: set[str] = set()

    for m_id, m_to in raw_input:
        dest_modules = m_to.split(', ')
        if m_id == 'broadcaster':
            module_map[m_id] = Broadcast(m_id, dest_modules)
            continue

        module_op = m_id[0]
        module_name = m_id[1:]
        if module_op == '%':
            module_map[module_name] = FlipFlop(module_name, dest_modules)
        elif module_op == '&':
            module_map[module_name] = Conjunction(module_name, dest_modules)
            conj_modules.add(module_name)
        else:
            raise ValueError(
                f'Invalid module operation: {module_op} from "{m_id} -> {m_to}"')

    for mod_name, mod_obj in module_map.items():
        for c_to in conj_modules & set(mod_obj.dest_mods):
            module_map[c_to].add_input_module(mod_name)

    num_high = 0
    num_low = 0
    for i in tqdm(range(num_presses)):
        curr_pulses = [(LOW, 'broadcaster', 'button')]
        num_low += 1

        while len(curr_pulses) > 0:
            new_pulses = []
            for pulse_level, pulse_to, pulse_from in curr_pulses:

                if pulse_level == LOW and pulse_to == 'rx':
                    print(f'Low pulse from {pulse_from} to {pulse_to} at {i}')
                    return i

                if pulse_to not in module_map:
                    continue
                pulse_output = module_map[pulse_to].process_pulse(
                    pulse_level, pulse_from)
                if pulse_output is None:
                    continue

                pulse_level, pulse_dests = pulse_output
                if pulse_level == LOW:
                    num_low += len(pulse_dests)
                elif pulse_level == HIGH:
                    num_high += len(pulse_dests)
                else:
                    raise ValueError(f'Invalid pulse level: {pulse_level}')

                new_pulses.extend([(pulse_level, pulse_dest, pulse_to)
                                   for pulse_dest in pulse_dests])

            curr_pulses = new_pulses

        if PRINT:
            print(f'After button {i} - Low: {num_low}, High: {num_high}')

    return num_high * num_low


if __name__ == "__main__":
    test_sol = calc_pulses("data1_test.txt", 1000)
    print(test_sol)
    assert test_sol == 32000000
    test_sol2 = calc_pulses("data1_test2.txt", 1000)
    print(test_sol2)
    assert test_sol2 == 11687500
    real_sol = calc_pulses("data1_real.txt", 1000)
    print(real_sol)
    assert real_sol == 794930686
    real_sol = calc_pulses("data1_real.txt", 1000000000000000)
    print(real_sol)

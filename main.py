import math
from abc import ABC
from dataclasses import dataclass
from typing import Sequence

from utils import store_to_file, introduce_gaussian_error, plot


def r_from_angle(angle: float):
    return [
        [math.cos(angle), math.sin(angle), 0],
        [-math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ]


@dataclass(frozen=True, slots=True)
class Position:
    x: float
    y: float
    t: float

    @classmethod
    def from_string(cls, string: str):
        return cls(*map(float, string.split(' ')))

    def __str__(self):
        return f'x={self.x}; y={self.y}; t={self.t};'


class Positions(list[Position]):
    @classmethod
    def from_file(cls, file_path: str):
        with open(file_path) as file:
            return cls(Position.from_string(line) for line in file)

    def plot(self, title='Positions'):
        x_values = tuple(pos.x for pos in self)
        y_values = tuple(pos.y for pos in self)
        plot(x_values, y_values, title=title)


@dataclass
class Vector(ABC):
    x: float
    y: float

    @property
    def modulus(self):
        return (self.x ** 2 + (self.y ** 2)) ** 0.5

    @property
    def angle(self):
        return math.atan2(self.y, self.x)


@dataclass
class PositionsVector(Vector):
    delta_t: float

    @classmethod
    def from_positions(cls, pos1: Position, pos2: Position):
        return cls(pos2.x - pos1.x, pos2.y - pos1.y, pos2.t - pos1.t)


class PositionsVectors(list[PositionsVector]):
    @classmethod
    def from_positions(cls, positions: Sequence[Position]):
        return cls(PositionsVector.from_positions(p1, p2) for p1, p2 in zip(positions, positions[1:]))


class Speed(Vector):
    @classmethod
    def from_positions(cls, pos1: Position, pos2: Position):
        return cls((pos2.x - pos1.x) / (delta_t := pos2.t - pos1.t), (pos2.y - pos1.y) / delta_t)


class Speeds(list[Speed]):
    @classmethod
    def from_positions(cls, positions: Sequence[Position]):
        return cls(Speed.from_positions(p1, p2) for p1, p2 in zip(positions, positions[1:]))


class AngularSpeed(float):
    @classmethod
    def from_positions(cls, p1: Position, p2: Position, p3: Position):
        pv1 = PositionsVector.from_positions(p1, p2)
        pv2 = PositionsVector.from_positions(p2, p3)
        return cls((pv2.angle - pv1.angle) / pv1.delta_t)


class AngularSpeeds(list[AngularSpeed]):
    @classmethod
    def from_positions(cls, positions: Positions):
        return cls(AngularSpeed.from_positions(p1, p2, p3)
                   for p1, p2, p3 in zip(positions, positions[1:], positions[2:]))


@dataclass(eq=False)
class PositionsEstimation:
    name: str
    initial_pos: Position
    initial_angle: float
    linear_speeds: Sequence[float]
    angular_speeds: Sequence[float]
    t_values: Sequence[float]

    def __post_init__(self):
        self.positions = self._estimate_positions()

    def _estimate_positions(self):
        positions, pos, angle = [self.initial_pos], self.initial_pos, self.initial_angle
        for linear_speed, angular_speed, t in zip(self.linear_speeds, list(self.angular_speeds)+[0], self.t_values[1:]):
            x = linear_speed * math.cos(angle) * (delta_t := t - pos.t) + pos.x
            y = linear_speed * math.sin(angle) * delta_t + pos.y
            pos = Position(x, y, t)
            positions.append(pos)
            angle += angular_speed * delta_t
        return Positions(positions)

    @staticmethod
    def _error(actual: Position, expected: Position) -> float:
        return ((actual.x - expected.x) ** 2 + ((actual.y - expected.y) ** 2)) ** 0.5

    def errors(self, expected: Sequence[Position]):
        return [self._error(expected_pos, actual_pos) for expected_pos, actual_pos in zip(expected, self.positions)]


if __name__ == '__main__':
    positions = Positions.from_file('Path_SRA2223.txt')
    positions.plot()

    speeds = Speeds.from_positions(positions)
    linear_speeds = tuple(speed.modulus for speed in speeds)
    angular_speeds = AngularSpeeds.from_positions(positions)

    store_to_file(linear_speeds, 'linear_speeds.txt')
    store_to_file(angular_speeds, 'angular_speeds.txt')

    args = {
        'initial_pos': positions[0],
        'initial_angle': PositionsVector.from_positions(positions[0], positions[1]).angle,
        'linear_speeds': linear_speeds,
        'angular_speeds': angular_speeds,
        't_values': tuple(p.t for p in positions)
    }

    estimation1 = PositionsEstimation(**args, name='with no artificial error')

    args['linear_speeds'] = introduce_gaussian_error(linear_speeds)
    estimation2 = PositionsEstimation(**args, name='with linear speed error')

    args['angular_speeds'] = introduce_gaussian_error(angular_speeds)
    estimation3 = PositionsEstimation(**args, name='with both errors')

    args['linear_speeds'] = linear_speeds
    estimation4 = PositionsEstimation(**args, name='with angular speed error')

    for estimation in (estimation1, estimation2, estimation4, estimation3):
        error_title = f'Error {estimation.name}'
        error_sequence = estimation.errors(positions)
        print(f'{error_title:-^60}')
        print('Max error:', max(error_sequence))
        print('Average error:', sum(error_sequence) / len(error_sequence))
        print('-' * 60 + '\n')
        estimation.positions.plot(title=f'Estimated positions {estimation.name}')
        lines = tuple(f'{pos} error={error};' for pos, error in zip(estimation.positions, error_sequence))
        store_to_file(lines, f'estimated_positions_{'_'.join(estimation.name.split(' '))}.txt')
        plot(tuple(p.t for p in positions), error_sequence, title=error_title, x_label='Time', y_label='Error')


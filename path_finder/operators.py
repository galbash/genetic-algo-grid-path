import abc
import random
from typing import Sequence, Tuple

from path_finder.chromosome import Chromosome
from path_finder.direction import random_direction


class Operator(abc.ABC):
    pass


class ProbabilityOperator(Operator):
    def __init__(self, probability: float):
        self.probability = probability

    @property
    def test_probability(self) -> bool:
        return random.random() < self.probability


class Cross(ProbabilityOperator):
    @abc.abstractmethod
    def __call__(
        self, parent1: Chromosome, parent2: Chromosome
    ) -> Tuple[
        Chromosome, Chromosome,
    ]:
        raise NotImplementedError()


class PathFinderCross(Cross):
    DEFAULT_PROBABILITY = 0.85

    def __init__(self, probability=DEFAULT_PROBABILITY):
        super().__init__(probability)

    def __call__(
        self, parent1: Chromosome, parent2: Chromosome
    ) -> Tuple[
        Chromosome, Chromosome,
    ]:
        if not self.test_probability:
            return (
                parent1,
                parent2,
            )

        first_point = random.randrange(
            0, len(parent1) + 1
        )  # we can take the entire chromosome
        second_point = random.randrange(
            0, len(parent2) + 1
        )  # we can take the entire chromosome
        return (
            parent1[:first_point] + parent2[second_point:],
            parent2[:second_point] + parent1[first_point:],
        )


class Choose(Operator):
    @abc.abstractmethod
    def __call__(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        raise NotImplementedError()


class PathFinderChoose(Choose):
    def __call__(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        return random.choice([parent1, parent2])


class Mutation(ProbabilityOperator):
    def __init__(self, min_dist, probability: float):
        super().__init__(probability / min_dist)

    @abc.abstractmethod
    def __call__(self, chrom: Chromosome) -> Chromosome:
        raise NotImplementedError()


class SwitchMutation(Mutation):
    DEFAULT_PROBABILITY = 0.1

    def __init__(self, min_dist, probability=DEFAULT_PROBABILITY):
        super().__init__(min_dist, probability)

    def __call__(self, chrom: Chromosome) -> Chromosome:
        return [random_direction() if self.test_probability else d for d in chrom]


class AddMutation(Mutation):
    DEFAULT_PROBABILITY = 0.05

    def __init__(self, min_dist, probability=DEFAULT_PROBABILITY):
        super().__init__(min_dist, probability)

    def __call__(self, chrom: Chromosome) -> Chromosome:
        new_chrom = []
        self._possibly_append_direction(new_chrom)

        for direction in chrom:
            new_chrom.append(direction)
            self._possibly_append_direction(new_chrom)

        return new_chrom

    def _possibly_append_direction(self, new_chrom):
        if self.test_probability:
            new_chrom.append(random_direction())


class RemoveMutation(Mutation):
    DEFAULT_PROBABILITY = 0.05

    def __init__(self, min_dist, probability=DEFAULT_PROBABILITY):
        super().__init__(min_dist, probability)

    def __call__(self, chrom: Chromosome) -> Chromosome:
        return [
            d
            for d in chrom
            if not self.test_probability  # keep on most cases, filter only if test_probability = True
        ]


class PathFinderOperationSequence:
    def __init__(self, cross: Cross, choose: Choose, mutations: Sequence[Mutation]):
        self.cross = cross
        self.choose = choose
        self.mutations = mutations

    def __call__(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        chrom = self.choose(*self.cross(parent1, parent2))
        for mutation in self.mutations:
            chrom = mutation(chrom)

        return chrom

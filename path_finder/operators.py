"""
Different genetic operjators the algorithm utilizes
"""
import abc
import random
from typing import Sequence, Tuple

from path_finder.chromosome import Chromosome
from path_finder.direction import random_direction


class Operator(abc.ABC):
    """
    A basic operator interface
    """

    pass


class ProbabilityOperator(Operator):
    """
    An operator that has a probability to operate
    """

    def __init__(self, probability: float):
        """
        :param probability: a float in the range [0, 1]
        """
        self.probability = probability

    @property
    def test_probability(self) -> bool:
        """
        :return: True if the test was true, false otherwise. probability
            of truth value is determined at init
        """
        return random.random() < self.probability


class Cross(ProbabilityOperator):
    """
    Mixes two chromosomes
    """

    @abc.abstractmethod
    def __call__(
        self, parent1: Chromosome, parent2: Chromosome
    ) -> Tuple[
        Chromosome, Chromosome,
    ]:
        """
        :param parent1: the first chromosome to use
        :param parent2: the second chromosome to use
        :return: 2 child chromosomes which are the result of the mix
        """
        raise NotImplementedError()


class PathFinderCross(Cross):
    """
    see Cross
    """

    DEFAULT_PROBABILITY = 1  # we already use elitism

    def __init__(self, probability=DEFAULT_PROBABILITY):
        """
        See ProbabilityOperator.__init__
        """
        super().__init__(probability)

    def __call__(
        self, parent1: Chromosome, parent2: Chromosome
    ) -> Tuple[
        Chromosome, Chromosome,
    ]:
        """
        see Cross.__call__
        """
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
    """
    An operator that chooses one of two chromosomes
    """

    @abc.abstractmethod
    def __call__(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        """
        :param parent1: The first chromosome
        :param parent2: The second chromosome
        :return: one of the chromosomes which was selected
        """
        raise NotImplementedError()


class PathFinderChoose(Choose):
    """
    See Choose
    """

    def __call__(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        """
        See Choose.__call__
        """
        return random.choice([parent1, parent2])


class Mutation(ProbabilityOperator):
    """
    An operator that performes a mutation on the chromosome
    """

    def __init__(self, min_dist, probability: float):
        """
        :param min_dist: minimum distance from source to target in the environment.
            used to tune the probability
        :param probability: see ProbabilityOperator.__init__
        """
        super().__init__(probability / min_dist)

    @abc.abstractmethod
    def __call__(self, chrom: Chromosome) -> Chromosome:
        """
        :param chrom: The chromosome to mutate
        :return: The chromosome after the mutation
        """
        raise NotImplementedError()


class SwitchMutation(Mutation):
    """
    A mutation that switches random genes (directions) in the chromosome
    """

    DEFAULT_PROBABILITY = 0.1

    def __init__(self, min_dist, probability=DEFAULT_PROBABILITY):
        """
        See Mutation.__init__
        """
        super().__init__(min_dist, probability)

    def __call__(self, chrom: Chromosome) -> Chromosome:
        """
        See Mutation.__call__
        """
        return [random_direction() if self.test_probability else d for d in chrom]


class AddMutation(Mutation):
    """
    A mutation that adds random genes (directions) in the chromosome at random locations
    """

    DEFAULT_PROBABILITY = 0.05

    def __init__(self, min_dist, probability=DEFAULT_PROBABILITY):
        """
        See Mutation.__init__
        """
        super().__init__(min_dist, probability)

    def __call__(self, chrom: Chromosome) -> Chromosome:
        """
        See Mutation.__call__
        """
        new_chrom = []
        self._possibly_append_direction(new_chrom)

        for direction in chrom:
            new_chrom.append(direction)
            self._possibly_append_direction(new_chrom)

        return new_chrom

    def _possibly_append_direction(self, new_chrom) -> None:
        """
        Adds a direction to the chromosome with the mutation probability
        :param new_chrom: the chromosome to add the direction to
        """
        if self.test_probability:
            new_chrom.append(random_direction())


class RemoveMutation(Mutation):
    """
    A mutation that removes random genes (directions) in the chromosome from random locations
    """

    DEFAULT_PROBABILITY = 0.05

    def __init__(self, min_dist, probability=DEFAULT_PROBABILITY):
        """
        See Mutation.__init__
        """
        super().__init__(min_dist, probability)

    def __call__(self, chrom: Chromosome) -> Chromosome:
        """
        See Mutation.__call__
        """
        return [
            d
            for d in chrom
            if not self.test_probability  # keep on most cases, filter only if test_probability = True
        ]


class RemovePairMutation(Mutation):
    """
    A mutation that removes random pairs of genes (directions) in the chromosome from random locations
    """

    DEFAULT_PROBABILITY = 0.05

    def __init__(self, min_dist, probability=DEFAULT_PROBABILITY):
        """
        See Mutation.__init__
        """
        super().__init__(min_dist // 2, probability)

    def __call__(self, chrom: Chromosome) -> Chromosome:
        """
        See Mutation.__call__
        """
        it = iter(chrom)
        return sum(
            (
                [d1, d2] if d2 else [d1]
                for d1, d2 in zip(it, it)
                if not self.test_probability  # keep on most cases, filter only if test_probability = True
            ),
            [],
        )


class PathFinderOperationSequence:
    """
    A sequence of genetic operations used by the algorithm
    """

    def __init__(self, cross: Cross, choose: Choose, mutations: Sequence[Mutation]):
        """
        :param cross: The Cross step to use
        :param choose: The Choose step to use
        :param mutations: A list of Mutations to apply
        """
        self.cross = cross
        self.choose = choose
        self.mutations = mutations

    def __call__(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        """
        :param parent1: The first chromosome used for breeding
        :param parent2: The second chromosome used for breeding
        :return: The chromosome resulting from the genetic operations
        """
        chrom = self.choose(*self.cross(parent1, parent2))
        for mutation in self.mutations:
            chrom = mutation(chrom)

        return chrom

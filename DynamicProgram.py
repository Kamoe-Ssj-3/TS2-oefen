from ProjectPlanning import ProjectPlanning
from itertools import chain, combinations
import time


class DynamicProgram(ProjectPlanning):
    def __init__(self, filepath):
        """
        Constructor that initializes the DynamicProgram class by inheriting from ProjectPlanning.

        Args:
            filepath (str): Path to the text file containing project planning data.
        """
        super().__init__(filepath)
        self.memo = {}
        self.subsets_considered = 0

    def _q_s(self, S):
        """
        Calculate q(S), the total time required to process jobs in the complement of S.

        Args:
            S (set): The set of projects S.

        Returns:
            int: The total processing time of the complement of S.
        """
        return sum(self.processing_times[i] for i in range(self.nProjects) if i not in S)

    def _f(self, S):
        """
        Recursive function to compute the value of f(S) using memoization.

        Args:
            S (frozenset): The current set of projects to schedule.

        Returns:
            float: The minimum objective value for the given set S.
        """
        if S in self.memo:
            return self.memo[S]

        if not S:
            return 0  # Base case: f(\emptyset) = 0

        q_S = self._q_s(S)
        min_value = float('inf')

        for i in S:
            S_minus_i = frozenset(S - {i})
            delay = max((q_S + self.processing_times[i]) - self.due_dates[i], 0)
            min_value = min(min_value, delay + self._f(S_minus_i))

        self.memo[S] = min_value
        self.subsets_considered += 1
        return min_value

    def solve(self):
        """
        Solves the project planning problem using the dynamic programming approach.
        Prints computation time and the number of subsets considered.
        """
        start_time = time.time()
        time_limit = 5 * 60  # 5 minutes in seconds
        full_set = frozenset(range(self.nProjects))

        try:
            result = self._f(full_set)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if elapsed_time > time_limit:
                raise TimeoutError("Solution exceeded time limit.")

            print(f"Optimal objective value: {result}")
            print(f"Computation time: {elapsed_time:.2f} seconds")
            print(f"Number of subsets considered: {self.subsets_considered}")

        except TimeoutError as e:
            print(str(e))
            print(f"Computation time: {elapsed_time:.2f} seconds")
            print(f"Number of subsets considered: {self.subsets_considered}")
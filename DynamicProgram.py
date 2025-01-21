from ProjectPlanning import ProjectPlanning
from itertools import chain, combinations
import time


class DynamicProgram(ProjectPlanning):
    def __init__(self, filepath):
        """
        Constructor that initializes the dynamic programming solution by inheriting from ProjectPlanning.

        Args:
            filepath (str): Path to the text file containing project planning data.
        """
        super().__init__(filepath)

    def solve(self):
        """
        Solves the project planning problem using dynamic programming.

        Returns:
            float: The optimal objective value.
        """
        n = self.nProjects
        p = self.processing_times
        d = self.due_dates

        # DP table to store f(S) for all subsets S
        dp = {}
        dp[frozenset()] = 0  # Base case: f(∅) = 0

        # Iterate over all subsets of {1, ..., n}
        for size in range(1, n + 1):
            for S in combinations(range(n), size):
                S = frozenset(S)
                S_complement = frozenset(range(n)) - S

                # Calculate q_S
                q_S = sum(p[i] for i in S_complement)

                # Recurrence relation
                dp[S] = float('inf')
                for i in S:
                    f_S_minus_i = dp[S - frozenset([i])]
                    delay = max(q_S + p[i] - d[i], 0)
                    dp[S] = min(dp[S], delay + f_S_minus_i)

        # Return the objective value for the full set
        return dp[frozenset(range(n))]
from ProjectPlanning import ProjectPlanning
from gurobipy import Model, GRB, quicksum

class MIP(ProjectPlanning):
    def __init__(self, filepath):
        """
        Constructor that initializes the MIP model by inheriting from ProjectPlanning.

        Args:
            filepath (str): Path to the text file containing project planning data.
        """
        super().__init__(filepath)
        self.model = self._create_model()

    def _create_model(self):
        """
        Creates the Gurobi model for the project planning problem.

        Returns:
            gurobipy.Model: The Gurobi optimization model.
        """
        # Create a new model
        model = Model("ProjectPlanningMIP")

        n = self.nProjects
        p = self.processing_times
        d = self.due_dates

        # Decision variables
        C = model.addVars(n, vtype=GRB.CONTINUOUS, name="C")  # Completion time
        D = model.addVars(n, vtype=GRB.CONTINUOUS, name="D")  # Delay
        X = model.addVars(n, n, vtype=GRB.BINARY, name="X")   # Execution order

        # Objective: Minimize total delay
        model.setObjective(quicksum(D[i] for i in range(n)), GRB.MINIMIZE)

        # Constraints
        M = sum(p) + max(d)  # Big-M constant

        # Constraint (1): X_ij + X_ji = 1 for all i != j
        for i in range(n):
            for j in range(n):
                if i != j:
                    model.addConstr(X[i, j] + X[j, i] == 1, name=f"X_symmetry_{i}_{j}")

        # Constraint (2): C[j] >= C[i] + p[j] - M * (1 - X[i, j]) for all i != j
        for i in range(n):
            for j in range(n):
                if i != j:
                    model.addConstr(C[j] >= C[i] + p[j] - M * (1 - X[i, j]), name=f"C_order_{i}_{j}")

        # Constraint (3): C[i] >= p[i] for all i
        for i in range(n):
            model.addConstr(C[i] >= p[i], name=f"C_processing_{i}")

        # Constraint (4): D[i] >= C[i] - d[i] for all i
        for i in range(n):
            model.addConstr(D[i] >= C[i] - d[i], name=f"D_delay_{i}")

        # Constraint (5): C[i], D[i] >= 0 for all i
        for i in range(n):
            model.addConstr(C[i] >= 0, name=f"C_nonnegative_{i}")
            model.addConstr(D[i] >= 0, name=f"D_nonnegative_{i}")

        return model

    def solve(self):
        """
        Solves the project planning problem using the Gurobi model.
        """
        self.model.optimize()
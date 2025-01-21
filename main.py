from DynamicProgram import DynamicProgram
from MIP import MIP
from ProjectPlanning import ProjectPlanning

# Example usage:

if __name__ == "__main__":
    # mip = MIP('projects_1_10.txt')
    # mip.solve()
    # print(mip)
    dp = DynamicProgram('projects_1_40.txt')
    print(dp.solve())
class ProjectPlanning:
    def __init__(self, filepath):
        """
        Constructor that initializes the project planning instance from a given text file.

        Args:
            filepath (str): Path to the text file containing project planning data.
        """
        self.nTeams = 0
        self.nProjects = 0
        self.processing_times = []  # List to store processing times for each project
        self.due_dates = []  # List to store due dates for each project

        # Read data from the text file
        self._parse_file(filepath)

    def _parse_file(self, filepath):
        """
        Parses the input file and sets instance variables.

        Args:
            filepath (str): Path to the text file containing project planning data.
        """
        with open(filepath, 'r') as file:
            lines = file.readlines()

        # Parse nTeams
        self.nTeams = int(lines[1].strip())

        # Parse nProjects
        self.nProjects = int(lines[3].strip())

        # Parse project properties
        for line in lines[5:]:
            _, processing_time, due_date = map(int, line.split())
            self.processing_times.append(processing_time)
            self.due_dates.append(due_date)

    def __str__(self):
        """
        Returns a string representation of the ProjectPlanning instance.

        Returns:
            str: String representation of the instance.
        """
        return (f"Teams: {self.nTeams}\n"
                f"Projects: {self.nProjects}\n"
                f"Processing Times: {self.processing_times}\n"
                f"Due Dates: {self.due_dates}")

# Example usage:
# Assuming the text file is named 'project_data.txt' and located in the same directory


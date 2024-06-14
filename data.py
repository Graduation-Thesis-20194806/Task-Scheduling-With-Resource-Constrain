import csv
from datetime import datetime

class Task:
    def __init__(self, task_id, task_type, priority, effort, dependencies, earliest_start, latest_end):
        self.task_id = task_id
        self.task_type = task_type
        self.priority = priority
        self.effort = effort
        self.dependencies = dependencies
        self.earliest_start = earliest_start
        self.latest_end = latest_end

class Node:
    def __init__(self, id, competency, index):
        self.id = id
        self.competency = competency
        self.index = index

def read_tasks_from_csv(filename):
    tasks = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            task_id = int(row['task_id'])
            task_type = row['task_type']
            priority = int(row['priority'])
            effort = int(row['effort'])
            dependencies = list(map(int, row['dependencies'].split(','))) if row['dependencies'] else []
            earliest_start = datetime.strptime(row['earliest_start'])

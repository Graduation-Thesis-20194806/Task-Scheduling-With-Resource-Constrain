import random
import csv
from datetime import datetime, timedelta


class Task:
    def __init__(self, task_id, task_type, priority, effort, dependencies, earliest_start, latest_end):
        self.task_id = task_id
        self.task_type = task_type
        self.priority = priority
        self.effort = effort
        self.dependencies = dependencies
        self.earliest_start = earliest_start
        self.latest_end = latest_end


def generate_tasks(num_tasks, project_start_date, project_duration_days):
    task_types = ['Design', 'Dev', 'Test']
    tasks = []

    def random_date(start, end):
        if end <= start:
            return start
        return start + timedelta(days=random.randint(0, (end - start).days))

    project_end_date = project_start_date + timedelta(days=project_duration_days)

    dev_tasks = []
    test_tasks = []
    design_tasks = []

    for i in range(1, num_tasks + 1):
        # Ensure task counts follow the required relationship
        if len(dev_tasks) <= len(test_tasks) or len(test_tasks) <= len(design_tasks):
            task_type = 'Dev' if len(dev_tasks) <= len(test_tasks) else 'Test'
            task_type = 'Test' if len(test_tasks) <= len(design_tasks) else task_type
        else:
            task_type = random.choice(task_types)

        priority = random.randint(1, 5)
        effort = random.randint(1, 24)

        dependencies = []
        if task_type == 'Test':
            dependent_tasks = [t for t in tasks if t.task_type == 'Dev']
        elif task_type == 'Dev':
            dependent_tasks = [t for t in tasks if t.task_type == 'Design']
        else:
            dependent_tasks = []

        if dependent_tasks:
            dependencies = random.sample(dependent_tasks, k=random.randint(0, len(dependent_tasks)))

        if dependencies:
            earliest_start = max(d.latest_end for d in dependencies)
        else:
            earliest_start = random_date(project_start_date, project_end_date - timedelta(days=effort))

        latest_end = random_date(earliest_start + timedelta(hours=effort), project_end_date)

        if dependencies:
            latest_end = max(latest_end, max(d.latest_end for d in dependencies))

        task = Task(i, task_type, priority, effort, [d.task_id for d in dependencies], earliest_start, latest_end)
        tasks.append(task)

        if task_type == 'Dev':
            dev_tasks.append(task)
        elif task_type == 'Test':
            test_tasks.append(task)
        elif task_type == 'Design':
            design_tasks.append(task)

    return tasks


def write_tasks_to_csv(tasks, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["task_id", "task_type", "priority", "effort", "dependencies", "earliest_start", "latest_end"])
        for task in tasks:
            writer.writerow([
                task.task_id,
                task.task_type,
                task.priority,
                task.effort,
                ','.join(map(str, task.dependencies)),
                task.earliest_start.strftime('%Y-%m-%d %H:%M:%S'),
                task.latest_end.strftime('%Y-%m-%d %H:%M:%S')
            ])


# Define project parameters
num_tasks = 600
project_start_date = datetime(2024, 7, 1)
project_duration_days = 400

# Generate tasks
tasks = generate_tasks(num_tasks, project_start_date, project_duration_days)

# Write tasks to CSV
csv_filename = 'dataset/project_tasks600_2.csv'
write_tasks_to_csv(tasks, csv_filename)

print(f'Tasks have been written to {csv_filename}')

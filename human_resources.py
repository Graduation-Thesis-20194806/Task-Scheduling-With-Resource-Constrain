import csv
import random
import uuid

# Define the levels and their respective competency ranges
levels = {
    'Developer': {
        'Intern Developer': (0, 0.2),
        'Fresher Developer': (0.1, 0.4),
        'Junior Developer': (0.3, 0.5),
        'Middle-Level Developer': (0.4, 0.6),
        'Senior Developer': (0.5, 0.8),
        'Lead Developer or Architect': 1
    },
    'Designer': {
        'Intern': (0, 0.2),
        'Fresher': (0.1, 0.5),
        'Junior': (0.5, 0.8),
        'Senior': 1
    },
    'Tester': {
        'Fresher': (0.3, 0.5),
        'Junior': (0.5, 0.8),
        'Senior': 1
    }
}


def generate_competency(level_range):
    if isinstance(level_range, tuple):
        return round(random.uniform(level_range[0], level_range[1]), 2)
    return level_range


def generate_employee(emp_type):
    levels_for_type = list(levels[emp_type].keys())
    level = random.choice(levels_for_type)
    competency = generate_competency(levels[emp_type][level])
    return {
        'id': str(uuid.uuid4()),
        'type': emp_type,
        'level': level,
        'competency': competency
    }


def ensure_middle_level_employees():
    employees = []
    for emp_type in levels.keys():
        middle_level = 'Middle-Level Developer' if emp_type == 'Developer' else 'Senior'
        competency = generate_competency(levels[emp_type][middle_level])
        employees.append({
            'id': str(uuid.uuid4()),
            'type': emp_type,
            'level': middle_level,
            'competency': competency
        })
    return employees


def generate_dataset(num_employees):
    # Initialize employee counts
    dev_count = 0
    tester_count = 0
    designer_count = 0

    dataset = ensure_middle_level_employees()

    # Adjust counts for the initial middle-level employees
    for emp in dataset:
        if emp['type'] == 'Developer':
            dev_count += 1
        elif emp['type'] == 'Tester':
            tester_count += 1
        elif emp['type'] == 'Designer':
            designer_count += 1

    remaining_employees = num_employees - len(dataset)

    while remaining_employees > 0:
        emp_type = random.choice(['Developer', 'Tester', 'Designer'])

        if emp_type == 'Developer':
            dev_count += 1
        elif emp_type == 'Tester':
            if tester_count >= dev_count - 1:  # Ensure testers are less than developers
                continue
            tester_count += 1
        elif emp_type == 'Designer':
            if designer_count >= tester_count:  # Ensure designers are less than or equal to testers
                continue
            designer_count += 1

        dataset.append(generate_employee(emp_type))
        remaining_employees -= 1

    return dataset


def save_to_csv(filename, dataset):
    keys = dataset[0].keys()
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(dataset)


# Input for number of employees
num_employees = int(input("Enter the number of employees: "))

# Generate dataset and save to CSV
dataset = generate_dataset(num_employees)
save_to_csv('dataset/employees_dataset.csv', dataset)
print(f"Dataset of {num_employees} employees saved to 'employees_dataset.csv'.")

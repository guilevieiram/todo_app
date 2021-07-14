import pandas as pd

# Data
CSV_DATA_FILE = 'data.csv'
# Tasks
TASK_ATTRIBUTES = ['description', 'done']
STANDARD_TASK = {'description': '', 'done': False}

class TaskManager():

    def __init__(self):
        self.tasks: pd.DataFrame = pd.read_csv(CSV_DATA_FILE)

    def add_task(self, description: str) -> None:
        if not description == '':
            task = STANDARD_TASK
            task['description'] = description
            task_df = pd.DataFrame([task])
            self.tasks = pd.concat([task_df, self.tasks], ignore_index=True)

    def validate_task(self, task_id: int = None, description: str = None) -> None:
        if description is not None:
            task_id = self.get_id(description=description)

        self.tasks.at[task_id, 'done'] = not self.tasks.at[task_id, 'done']

    def show_tasks(self, done: bool = True, undone: bool = True):
        print(self.tasks)

    def get_id(self, description: str) -> int:
        return self.tasks[self.tasks['description'] == description].index[0]

    def get_tasks(self) -> dict:
        return self.tasks.to_dict(orient='list')

    def save_tasks(self) -> None:
        self.tasks.to_csv(CSV_DATA_FILE, index=False)

    def delete_task(self, description: str) -> None:
        task_id = self.get_id(description)
        self.tasks = self.tasks.drop([task_id])

    def clear_tasks(self) -> None:
        self.tasks = pd.DataFrame(columns=TASK_ATTRIBUTES)

    def set_all_tasks(self, state: bool) -> None:
        self.tasks['done'] = state


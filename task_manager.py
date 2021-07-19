import psycopg2
import pandas as pd
from abc import ABC, abstractmethod

# Data
TABLE_NAME = 'tasks'
CSV_DATA_FILE = 'data.csv'
POSTGRESQL_CONFIG = {
        'user': '',
        'password': '',
        'host': '',
        'port': ,
        'database': 
        }



# Tasks
TASK_ATTRIBUTES = ['description', 'done']
STANDARD_TASK = {'description': '', 'done': False}

class TaskManager(ABC):

    @abstractmethod
    def add_task(self, description: str) -> None:
        pass
    
    @abstractmethod
    def validate_task(self, description: str) -> None:
        pass
    
    @abstractmethod
    def show_tasks(self, done: bool = True, undone: bool = True):
        pass
    
    @abstractmethod
    def get_tasks(self) -> dict:
        pass
    
    @abstractmethod
    def save_tasks(self) -> None:
        pass
    
    @abstractmethod
    def delete_task(self, description: str) -> None:
        pass
    
    @abstractmethod
    def clear_tasks(self) -> None:
        pass
    
    @abstractmethod
    def set_all_tasks(self, state: bool) -> None:
        pass

class TaskManagerCloud(TaskManager):

    def __init__(self):
        self.configurations = POSTGRESQL_CONFIG
        self.table_name = TABLE_NAME
        self.connection: psycopg2.connect
        self.connect_to_db()
        self.create_table()

    def add_task(self, description: str) -> None:
        if not description == '':
            task = STANDARD_TASK
            task['description'] = description

            cursor = self.connection.cursor()
            sql = f"INSERT INTO {self.table_name} VALUES ('{task['description']}', {task['done']})"
            cursor.execute(sql)
            self.connection.commit()

    def validate_task(self, description: str) -> None:
        cursor = self.connection.cursor()
        sql = f"UPDATE {self.table_name} SET done = NOT done WHERE description = '{description}'"
        cursor.execute(sql)
        self.connection.commit()

    def show_tasks(self):
        cursor = self.connection.cursor()
        sql = f"SELECT * FROM {self.table_name}"
        cursor.execute(sql)
        print(cursor.fetchall())

    def get_tasks(self) -> dict:
        cursor = self.connection.cursor()
        sql = f"SELECT description, done FROM {self.table_name}"
        cursor.execute(sql)
        list_of_attributes = cursor.fetchall()
        return {
        'description': [element[0] for element in list_of_attributes][::-1],
        'done': [element[1] for element in list_of_attributes][::-1]
        }

    def save_tasks(self) -> None:
        self.connection.commit()
        self.close_connection_to_db()

    def delete_task(self, description: str) -> None:
        cursor = self.connection.cursor()
        sql = f"DELETE FROM {self.table_name} WHERE description = '{description}'"
        cursor.execute(sql)
        self.connection.commit()

    def clear_tasks(self) -> None:
        cursor = self.connection.cursor()
        sql = f"DELETE FROM {self.table_name}"
        cursor.execute(sql)
        self.connection.commit()

    def set_all_tasks(self, state: bool) -> None:
        cursor = self.connection.cursor()
        sql = f"UPDATE {self.table_name} SET done = {state}"
        cursor.execute(sql)
        self.connection.commit()

    # Cloud methods
    def create_table(self) -> None:
        cursor = self.connection.cursor()

        sql = f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
            description VARCHAR (100) UNIQUE NOT NULL, 
            done BOOLEAN NOT NULL
            )'''
        cursor.execute(sql)
        self.connection.commit()

    def connect_to_db(self) -> None:
        self.connection = psycopg2.connect(
            database=self.configurations['database'],
            user=self.configurations['user'],
            password=self.configurations['password'],
            host=self.configurations['host'],
            port=self.configurations['port']
        )

        self.connection.commit()

    def close_connection_to_db(self) -> None:   
        self.connection.close()

class TaskManagerLocal(TaskManager):

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


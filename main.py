from kivymd.app import MDApp

from screen import Screen
from task_manager import TaskManagerCloud, TaskManagerLocal, TaskManager

## CONSTANTS

# Colors
PRIMARY_COLOR = 'BlueGray'
SECONDARY_COLOR = 'Pink'


class ToDoApp(MDApp):

    def __init__(self):
        super().__init__()

        self.task_manager: TaskManager = TaskManagerLocal()
        self.screen: Screen

    def build(self):
        self.theme_cls.primary_palette = PRIMARY_COLOR
        self.theme_cls.accent_palette = SECONDARY_COLOR
        self.screen: Screen = self.initialize_screen()  
        self.make_task_list()
        return self.screen.get_screen()

    def initialize_screen(self) -> Screen:  
        screen = Screen()     
        screen.initilize_widgets(
            add_task_function=self.add_task,
            validate_task_function=self.validate_task,
            delete_task_function=self.delete_task,
            clear_tasks_function=self.clear_tasks,
            menu_functions_list=self.make_menu_function_list()
            )
        return screen

    def make_task_list(self) -> None:
        tasks = self.task_manager.get_tasks()
        self.screen.reset_task_list(tasks=tasks)

    def add_task(self, description: str) -> None:
        self.task_manager.add_task(description=description)
        self.make_task_list()
   
    def validate_task(self, description: str) -> None:
        self.task_manager.validate_task(description=description)
        self.make_task_list()

    def delete_task(self, description:str) -> None:
        self.task_manager.delete_task(description=description)
        self.make_task_list()

    def clear_tasks(self) -> None:
        self.task_manager.clear_tasks()
        self.make_task_list()

    def set_all_tasks(self, state: bool) -> None:
        self.task_manager.set_all_tasks(state=state)
        self.make_task_list()

    def change_to_local_db(self) -> None:
        self.task_manager.save_tasks()
        self.task_manager = TaskManagerLocal()
        self.make_task_list()

    def change_to_cloud_db(self) -> None:
        self.task_manager.save_tasks()
        self.task_manager = TaskManagerCloud()
        self.make_task_list()

    def make_menu_function_list(self) -> None:
        return [
        {'name': 'Clear', 'function': self.clear_tasks},
        {'name': 'Do all', 'function': lambda : self.set_all_tasks(state=True)},
        {'name': 'Undo all', 'function': lambda : self.set_all_tasks(state=False)},
        {'name': 'Local data', 'function': lambda : self.change_to_local_db()},
        {'name': 'Cloud data', 'function': lambda : self.change_to_cloud_db()}
        ]

    def exit_and_save(self) -> None:
        self.task_manager.save_tasks()

    # dev tools
    def show_tasks(self) -> None:
        self.task_manager.show_tasks()

def main() -> None:
    app = ToDoApp()
    app.run()
    app.exit_and_save()

if __name__ == '__main__':
    main()
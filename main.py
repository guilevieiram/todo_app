'''
TODO:

make task verification action
implement deleting button
implement deleting action
save and load old tasks (pickle?)
test
export to android
'''


from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.list import MDList, OneLineIconListItem,IconLeftWidget
from kivy.uix.scrollview import ScrollView

import pandas as pd

## CONSTANTS

# Toolbar
TOOLBAR_TITLE = 'To-do:'
TOOLBAR_POSITION = {'top': 1}

# Logo
LOGO_SOURCE = 'cat.png'
LOGO_POSITION = {'center_x': .08, 'center_y': 0.8}
LOGO_SIZE = {'width': 50, 'height': 100}

# Input
INPUT_TEXT = ""
INPUT_HALIGN = "center"
INPUT_SIZE = (.6,1)
INPUT_POSITION = {'center_x': .5, 'center_y': .8}
INPUT_FONT_SIZE = 20

# Add task button
ADD_TASK_BUTTON_TEXT = 'Add'
ADD_TASK_BUTTON_FONT_SIZE = 14
ADD_TASK_BUTTON_POSITION = {'center_x': .9, 'center_y': 0.8}

# Task list
TASK_LIST_POSITION = {'center_x': .5, 'center_y': 0.25}

# Tasks
TASK_ATTRIBUTES = ['description', 'done']
STANDARD_TASK = {'description': '', 'done': False}

# Checkbox
BLANK_CHECKBOX = 'checkbox-blank-outline'
FIILED_CHECKBOX = 'check-box-outline'

# Color
PRIMARY_COLOR = 'Pink'
SECONDARY_COLOR = 'Pink'

# Data
CSV_DATA_FILE = 'data.csv'

class ItemList(ScrollView):
    def __init__(self, position: dict, validate_task_function):
        super().__init__()
        self.pos_hint = position
        self.validate_task_function = validate_task_function
        self.create_list()

    def add_item(self, text: str, icon: str = 'language-python') -> None:
        item = OneLineIconListItem(text=text)
        icon = IconLeftWidget(icon=icon)
        item.add_widget(icon)

        icon.on_press = lambda : self.validate_task_function(description=text)
        item.on_press = lambda : self.validate_task_function(description=text)

        self.list.add_widget(item)


    def create_list(self) -> None:
        self.list = MDList()

    def update_list(self) -> None:
        self.add_widget(self.list)

    def delete_list(self):
        self.remove_widget(self.list)

class Screen():

    def __init__(self, add_task_function, validate_task_function, theme):
        self.screen: MDScreen = MDScreen()
        self.theme = theme
        self.toolbar: MDToolbar = self.create_toolbar()
        self.logo: Image = self.create_logo()
        self.input: MDTextField = self.create_input_field()
        self.add_task_button = self.create_add_task_button(function=add_task_function)
        self.task_list = self.create_task_list(validate_task_function=validate_task_function)

        self.add_widgets()

    def create_toolbar(self) -> MDToolbar:
        return MDToolbar(
            title=TOOLBAR_TITLE,
            pos_hint=TOOLBAR_POSITION
            )

    def create_logo(self) -> Image:
        return Image(
            source = LOGO_SOURCE,
            pos_hint = LOGO_POSITION,
            width=LOGO_SIZE['height'],
            height=LOGO_SIZE['width']
            )

    def create_input_field(self) -> MDTextField:
        return MDTextField(
            text=INPUT_TEXT, 
            halign=INPUT_HALIGN,
            size_hint=INPUT_SIZE,
            pos_hint=INPUT_POSITION,
            font_size=INPUT_FONT_SIZE
            )

    def create_add_task_button(self, function) -> MDFillRoundFlatButton:
        return MDFillRoundFlatButton(
            text=ADD_TASK_BUTTON_TEXT, 
            font_size=ADD_TASK_BUTTON_FONT_SIZE, 
            pos_hint=ADD_TASK_BUTTON_POSITION,
            on_press=lambda x: self.add_task_action(
                add_task_function=function)
            )

    def create_task_list(self, validate_task_function) -> ItemList:
        return ItemList(
            position=TASK_LIST_POSITION, 
            validate_task_function=validate_task_function
            )

    def add_widgets(self) -> None:
        self.screen.add_widget(self.toolbar)
        self.screen.add_widget(self.logo)
        self.screen.add_widget(self.input)
        self.screen.add_widget(self.add_task_button)
        self.screen.add_widget(self.task_list)

    def get_screen(self) -> MDScreen:
        return self.screen

    def add_task_action(self, add_task_function) -> None:
        add_task_function(self.input.text)
        self.input.text = ''

    def add_task_list(self, tasks: dict) -> None:
        descriptions = tasks['description']
        done_tags = tasks['done']

        icons = []
        for done_tag in done_tags:
            if done_tag: icons.append(FIILED_CHECKBOX)
            else: icons.append(BLANK_CHECKBOX) 

        self.task_list.create_list()
        for description, icon in zip(descriptions, icons):
            self.task_list.add_item(text=description, icon=icon)
        self.task_list.update_list()

    def delete_task_list(self) -> None:
        self.task_list.delete_list()

    def reset_task_list(self, tasks: dict) -> None:
        self.delete_task_list()
        self.add_task_list(tasks=tasks)

class TaskManager():

    def __init__(self):
        self.tasks: pd.DataFrame = pd.read_csv(CSV_DATA_FILE)

    def add_task(self, description: str) -> None:
        task = STANDARD_TASK
        task['description'] = description
        task_df = pd.DataFrame([task])
        self.tasks = pd.concat([task_df, self.tasks], ignore_index=True)

    def validate_task(self, id: int = None, description: str = None) -> None:
        if description is not None:
            id = self.get_id(description=description)

        self.tasks.at[id, 'done'] = not self.tasks.at[id, 'done']

    def show_tasks(self, done: bool = True, undone: bool = True):
        print(self.tasks)

    def get_id(self, description: str) -> int:
        return self.tasks[self.tasks['description'] == description].index[0]

    def get_tasks(self) -> dict:
        return self.tasks.to_dict(orient='list')

    def save_tasks(self) -> None:
        self.tasks.to_csv(CSV_DATA_FILE, index=False)

class ToDoApp(MDApp):

    def __init__(self):
        super().__init__()
        self.task_manager: TaskManager = TaskManager()
        self.screen: Screen

    def build(self):
        self.theme_cls.primary_palette = PRIMARY_COLOR
        self.theme_cls.accent_palette = SECONDARY_COLOR

        self.screen: Screen = Screen(theme=self.theme_cls,
                                    add_task_function=self.add_task,
                                    validate_task_function=self.validate_task
                                    )

        self.make_task_list()

        return self.screen.get_screen()

    def make_task_list(self) -> None:
        tasks = self.task_manager.get_tasks()
        self.screen.reset_task_list(tasks=tasks)

    def add_task(self, description: str) -> None:
        self.task_manager.add_task(description=description)
        self.make_task_list()
   
    def validate_task(self, description: str = None, id: int = None) -> None:
        self.task_manager.validate_task(description=description, id=id)
        self.make_task_list()

    def exit_and_save(self) -> None:
        self.task_manager.save_tasks()

    # dev tools
    def show_tasks(self) -> None:
        self.task_manager.show_tasks()


if __name__ == '__main__':
    app = ToDoApp()
    app.run()

    app.exit_and_save()



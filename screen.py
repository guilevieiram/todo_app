from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFillRoundFlatButton, MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.list import MDList, OneLineAvatarIconListItem,IconLeftWidget, IconRightWidget
from kivy.uix.scrollview import ScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

# Logo
LOGO_SOURCE = 'graphics/cat.png'
LOGO_POSITION = {'center_x': .1, 'center_y': 0.8}
LOGO_SIZE = {'width': 50, 'height': 50}

# Toolbar
TOOLBAR_TITLE = 'To-dos'
TOOLBAR_POSITION = {'top': 1}

# Input
INPUT_TEXT = ""
INPUT_TEXT_COLOR = [0,0,0,1]
INPUT_HINT_TEXT = "Add a new task"
INPUT_HALIGN = "left"
INPUT_SIZE = (.6,1)
INPUT_POSITION = {'center_x': .5, 'center_y': .8}
INPUT_FONT_SIZE = 20

# Add task button
ADD_TASK_BUTTON_ICON = 'plus-thick'
ADD_TASK_BUTTON_FONT_SIZE = 14
ADD_TASK_BUTTON_POSITION = {'center_x': .9, 'center_y': 0.8}

# Task list
TASK_LIST_POSITION = {'center_x': .5, 'center_y': 0.2}

# Checkbox
BLANK_CHECKBOX = 'checkbox-blank-outline'
FIILED_CHECKBOX = 'check-box-outline'

# Delete 
DELETE_ICON = 'trash-can-outline'
MENU = 'menu'

# Cat
CAT_TASK = 'Feed the cat'
CAT = 'cat'

# Data settings
CLOUD = 1
CLOUD_ICON = 'cloud'
LOCAL = 0
LOCAL_ICON = 'home'


class ItemList(ScrollView):

    def __init__(self, position: dict, **kwargs):
        super().__init__()

        self.pos_hint = position
        self.validate_task_function = kwargs['validate_task_function']
        self.delete_task_function = kwargs['delete_task_function']

        self.create_list()

    def add_item(self, text: str, box_icon: str, delete_icon: str) -> None:

        item = OneLineAvatarIconListItem(text=text)
        box_icon = IconLeftWidget(icon=box_icon)
        delete_icon = IconRightWidget(icon=delete_icon)

        item.add_widget(box_icon)
        item.add_widget(delete_icon)

        delete_icon.on_press = lambda: self.delete_task_function(description=text)
        box_icon.on_press = lambda: self.validate_task_function(description=text)
        item.on_press = lambda: self.validate_task_function(description=text)

        self.list.add_widget(item)

    def create_list(self) -> None:
        self.list = MDList()

    def update_list(self) -> None:
        self.add_widget(self.list)

    def delete_list(self):
        self.remove_widget(self.list)

    def clear_list(self) -> None:
        self.delete_list()
        self.update_list()

class Screen():

    def __init__(self):
        self.screen: MDScreen = MDScreen()

        # Screen Widgets
        self.menu: MDDropdownMenu 
        self.toolbar: MDToolbar 
        self.logo: Image 
        self.input: MDTextField
        self.add_task_button: MDFillRoundFlatButton
        self.task_list: ItemList

    # Returning the MDScreen object
    def get_screen(self) -> MDScreen:
        return self.screen

    # Making the widgets
    def initilize_widgets(self, **kwargs):
        self.add_task_function = kwargs['add_task_function']
        self.validate_task_function = kwargs['validate_task_function']
        self.delete_task_function = kwargs['delete_task_function']
        self.clear_tasks_function = kwargs['clear_tasks_function']
        self.menu_functions_list = kwargs['menu_functions_list']
        self.change_db_function = kwargs['change_db_function']

        self.data_type = kwargs['data_type']

        self.create_widgets()

    def create_widgets(self) -> None:
        self.toolbar = self.create_toolbar()
        self.logo = self.create_logo()
        self.input = self.create_input_field()
        self.add_task_button = self.create_add_task_button()
        self.task_list = self.create_task_list()
        self.menu  = self.create_menu()

        self.add_widgets()

    def add_widgets(self) -> None:
        self.screen.add_widget(self.toolbar)
        self.screen.add_widget(self.logo)
        self.screen.add_widget(self.input)
        self.screen.add_widget(self.add_task_button)
        self.screen.add_widget(self.task_list)

    def create_toolbar(self) -> MDToolbar:

        def menu_callback(button):
            self.menu.caller = button
            self.menu.open()

        toolbar =  MDToolbar(
            title=TOOLBAR_TITLE,
            pos_hint=TOOLBAR_POSITION,
            )
        
        toolbar.left_action_items = [[MENU, lambda x: menu_callback(x)]]
        toolbar.right_action_items = [
            [LOCAL_ICON if self.data_type == LOCAL else CLOUD_ICON, lambda x: self.change_db_action()],
            [CAT, lambda x: self.add_task_function(CAT_TASK)]
            ]
        return toolbar

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
            hint_text=INPUT_HINT_TEXT,
            on_text_validate=lambda x: self.add_task_action(),
            text_color=INPUT_TEXT_COLOR,
            halign=INPUT_HALIGN,
            size_hint=INPUT_SIZE,
            pos_hint=INPUT_POSITION,
            font_size=INPUT_FONT_SIZE
            )

    def create_add_task_button(self) -> MDFillRoundFlatButton:
        return MDFloatingActionButton(
            icon = ADD_TASK_BUTTON_ICON,   
            font_size=ADD_TASK_BUTTON_FONT_SIZE, 
            pos_hint=ADD_TASK_BUTTON_POSITION,
            on_press=lambda x: self.add_task_action()
            )

    def create_task_list(self) -> ItemList:
        return ItemList(
            position=TASK_LIST_POSITION, 
            validate_task_function=self.validate_task_function,
            delete_task_function=self.delete_task_function
            )

    def create_menu(self) -> MDDropdownMenu:

        def run_and_dismiss(function):
            function()
            self.menu.dismiss()

        self.menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": menu_function["name"],
                "height": dp(56),
                "on_release": lambda func=menu_function["function"]: run_and_dismiss(func),
             } for menu_function in self.menu_functions_list
        ]

        return MDDropdownMenu(
            items=self.menu_items,
            width_mult=5,
        )

    # Screen <-> TaskList interface
    def add_task_action(self) -> None:
        self.add_task_function(self.input.text)
        self.input.text = ''

    def add_task_list(self, tasks: dict) -> None:
        descriptions = tasks['description']
        done_tags = tasks['done']
        icons = [FIILED_CHECKBOX if done_tag else BLANK_CHECKBOX for done_tag in done_tags]

        self.task_list.create_list()

        for description, icon in zip(descriptions, icons):
            self.task_list.add_item(text=description, box_icon=icon, delete_icon=DELETE_ICON)

        self.task_list.update_list()

    def change_db_action(self) -> None:

        self.data_type = self.change_db_function()
        self.update_toolbar()
        
    def update_toolbar(self) -> None:
        self.screen.remove_widget(self.toolbar)
        self.toolbar = self.create_toolbar()
        self.screen.add_widget(self.toolbar)

    def delete_task_list(self) -> None:
        self.task_list.delete_list()

    def reset_task_list(self, tasks: dict) -> None:
        self.delete_task_list()
        self.add_task_list(tasks=tasks)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
from datetime import datetime

class Task:
    def __init__(self, description, due_date):
        self.description = description
        self.due_date = due_date
        self.status = "Incomplete"

class ToDoListManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.tasks = []

        with self.canvas.before:
            Color(*get_color_from_hex('#F0F0F0'))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.add_widget(Label(text='To-Do List Manager', font_size=24, size_hint_y=None, height=50))

        input_layout = GridLayout(cols=3, spacing=10, size_hint_y=None, height=40)
        self.description_input = TextInput(hint_text='Enter task description', multiline=False)
        self.due_date_input = TextInput(hint_text='Due date (YYYY-MM-DD)', multiline=False)
        self.add_button = Button(text='Add Task', background_color=get_color_from_hex('#4CAF50'))
        self.add_button.bind(on_press=self.add_task)

        input_layout.add_widget(self.description_input)
        input_layout.add_widget(self.due_date_input)
        input_layout.add_widget(self.add_button)

        self.add_widget(input_layout)

        self.task_layout = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.task_layout.bind(minimum_height=self.task_layout.setter('height'))

        task_scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.7))
        task_scroll.add_widget(self.task_layout)
        self.add_widget(task_scroll)

        action_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.complete_button = Button(text='Mark Complete', background_color=get_color_from_hex('#2196F3'))
        self.complete_button.bind(on_press=self.mark_complete)
        self.remove_button = Button(text='Remove Task', background_color=get_color_from_hex('#F44336'))
        self.remove_button.bind(on_press=self.remove_task)

        action_layout.add_widget(self.complete_button)
        action_layout.add_widget(self.remove_button)

        self.add_widget(action_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def add_task(self, instance):
        description = self.description_input.text
        due_date = self.due_date_input.text
        if description and due_date:
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
                task = Task(description, due_date)
                self.tasks.append(task)
                self.update_task_list()
                self.description_input.text = ''
                self.due_date_input.text = ''
            except ValueError:
                self.show_error("Invalid date format. Please use YYYY-MM-DD.")
        else:
            self.show_error("Please enter both description and due date.")

    def update_task_list(self):
        self.task_layout.clear_widgets()
        for index, task in enumerate(self.tasks):
            task_str = f"{task.description} (Due: {task.due_date}) - {task.status}"
            task_button = Button(text=task_str, size_hint_y=None, height=40)
            task_button.background_color = get_color_from_hex('#81C784') if task.status == "Complete" else get_color_from_hex('#FFFFFF')
            task_button.color = get_color_from_hex('#000000')
            task_button.bind(on_press=lambda x, idx=index: self.select_task(idx))
            self.task_layout.add_widget(task_button)

    def select_task(self, index):
        for i, child in enumerate(self.task_layout.children):
            if i == index:
                child.background_color = get_color_from_hex('#BBDEFB')
            elif self.tasks[i].status == "Complete":
                child.background_color = get_color_from_hex('#81C784')
            else:
                child.background_color = get_color_from_hex('#FFFFFF')

    def mark_complete(self, instance):
        selected = next((i for i, child in enumerate(self.task_layout.children) if child.background_color == get_color_from_hex('#BBDEFB')), None)
        if selected is not None:
            self.tasks[selected].status = "Complete"
            self.update_task_list()
        else:
            self.show_error("Please select a task to mark as complete.")

    def remove_task(self, instance):
        selected = next((i for i, child in enumerate(self.task_layout.children) if child.background_color == get_color_from_hex('#BBDEFB')), None)
        if selected is not None:
            del self.tasks[selected]
            self.update_task_list()
        else:
            self.show_error("Please select a task to remove.")

    def show_error(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(300, 150))
        popup.open()

class ToDoApp(App):
    def build(self):
        return ToDoListManager()

if __name__ == '__main__':
    ToDoApp().run()
	
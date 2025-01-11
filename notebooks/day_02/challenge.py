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
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.dropdown import DropDown
from datetime import datetime
from kivy.clock import Clock
from kivy.metrics import dp
import json
from kivy.uix.modalview import ModalView

class Task:
    def __init__(self, description, due_date, category, priority):
        self.description = description
        self.due_date = due_date
        self.category = category
        self.priority = priority
        self.status = "Incomplete"

    def to_dict(self):
        return {
            'description': self.description,
            'due_date': self.due_date,
            'category': self.category,
            'priority': self.priority,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data['description'], data['due_date'], data['category'], data['priority'])
        task.status = data['status']
        return task

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = [0, 0, 0, 0]
        self.color = get_color_from_hex('#FFFFFF')
        self.outline_color = get_color_from_hex('#000000')
        self.outline_width = 1
        self.bind(size=self.update_canvas, pos=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*get_color_from_hex('#4CAF50'))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[5])
            Color(*self.outline_color)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 5), width=self.outline_width)

class ToDoListManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(5)
        self.tasks = []

        with self.canvas.before:
            Color(*get_color_from_hex('#E0E0E0'))
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        title_layout = BoxLayout(size_hint_y=None, height=dp(60))
        title = Label(text='[b]TaskSphere[/b]', font_size=dp(28), markup=True, color=get_color_from_hex('#333333'))
        title_layout.add_widget(title)
        self.add_widget(title_layout)

        button_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
        self.add_button = RoundedButton(text='Add Task', size_hint=(None, None), size=(dp(80), dp(40)))
        self.add_button.bind(on_press=self.show_add_task_popup)
        button_layout.add_widget(self.add_button)

        self.sort_button = RoundedButton(text='Sort Tasks', size_hint=(None, None), size=(dp(80), dp(40)))
        self.sort_button.bind(on_press=self.show_sort_popup)
        button_layout.add_widget(self.sort_button)

        self.export_button = RoundedButton(text='Export Tasks', size_hint=(None, None), size=(dp(80), dp(40)))
        self.export_button.bind(on_press=self.export_tasks)
        button_layout.add_widget(self.export_button)

        self.add_widget(button_layout)

        self.search_input = TextInput(hint_text='Search tasks', multiline=False, size_hint_y=None, height=dp(40))
        self.search_input.bind(text=self.filter_tasks)
        self.add_widget(self.search_input)

        self.task_layout = GridLayout(cols=1, spacing=dp(2), size_hint_y=None)
        self.task_layout.bind(minimum_height=self.task_layout.setter('height'))

        task_scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        task_scroll.add_widget(self.task_layout)
        self.add_widget(task_scroll)

        action_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
        self.complete_button = RoundedButton(text='Complete', size_hint=(None, None), size=(dp(80), dp(40)))
        self.complete_button.bind(on_press=self.mark_complete)
        self.remove_button = RoundedButton(text='Remove', size_hint=(None, None), size=(dp(80), dp(40)))
        self.remove_button.background_color = get_color_from_hex('#F44336')
        self.remove_button.bind(on_press=self.remove_task)
        self.view_button = RoundedButton(text='View', size_hint=(None, None), size=(dp(80), dp(40)))
        self.view_button.background_color = get_color_from_hex('#2196F3')
        self.view_button.bind(on_press=self.view_task)

        action_layout.add_widget(self.complete_button)
        action_layout.add_widget(self.remove_button)
        action_layout.add_widget(self.view_button)

        self.add_widget(action_layout)

        self.load_tasks()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def show_add_task_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.description_input = TextInput(hint_text='Enter task description', multiline=False)
        content.add_widget(self.description_input)
        
        add_button = RoundedButton(text='Next', size_hint_y=None, height=dp(40))
        add_button.bind(on_press=self.show_date_popup)
        content.add_widget(add_button)
        
        self.add_popup = Popup(title='Add Task', content=content, size_hint=(0.9, 0.4))
        self.add_popup.open()

    def show_date_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.due_date_input = TextInput(hint_text='Due date (YYYY-MM-DD)', multiline=False)
        content.add_widget(self.due_date_input)
        
        add_button = RoundedButton(text='Next', size_hint_y=None, height=dp(40))
        add_button.bind(on_press=self.show_category_popup)
        content.add_widget(add_button)
        
        self.date_popup = Popup(title='Set Due Date', content=content, size_hint=(0.9, 0.4))
        self.add_popup.dismiss()
        self.date_popup.open()

    def show_category_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        categories = ['Work', 'Personal', 'Shopping', 'Other']
        for category in categories:
            btn = RoundedButton(text=category, size_hint_y=None, height=dp(40))
            btn.bind(on_press=lambda x, cat=category: self.set_category(cat))
            content.add_widget(btn)
        
        self.category_popup = Popup(title='Select Category', content=content, size_hint=(0.9, 0.6))
        self.date_popup.dismiss()
        self.category_popup.open()

    def set_category(self, category):
        self.selected_category = category
        self.show_priority_popup()

    def show_priority_popup(self):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        priorities = ['Low', 'Medium', 'High']
        for priority in priorities:
            btn = RoundedButton(text=priority, size_hint_y=None, height=dp(40))
            btn.bind(on_press=lambda x, pri=priority: self.add_task(pri))
            content.add_widget(btn)
        
        self.priority_popup = Popup(title='Select Priority', content=content, size_hint=(0.9, 0.5))
        self.category_popup.dismiss()
        self.priority_popup.open()

    def add_task(self, priority):
        description = self.description_input.text
        due_date = self.due_date_input.text
        category = self.selected_category
        
        if description and due_date:
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
                task = Task(description, due_date, category, priority)
                self.tasks.append(task)
                self.update_task_list()
                self.priority_popup.dismiss()
                self.save_tasks()
            except ValueError:
                self.show_error("Invalid date format. Please use YYYY-MM-DD.")
        else:
            self.show_error("Please fill in all fields.")

    def update_task_list(self):
        self.task_layout.clear_widgets()
        for index, task in enumerate(self.tasks):
            task_str = f"{task.description[:20]}... ({task.due_date})"
            task_button = RoundedButton(text=task_str, size_hint_y=None, height=dp(40))
            task_button.background_color = self.get_task_color(task)
            task_button.color = get_color_from_hex('#000000')
            task_button.bind(on_press=lambda x, idx=index: self.select_task(idx))
            self.task_layout.add_widget(task_button)

    def get_task_color(self, task):
        if task.status == "Complete":
            return get_color_from_hex('#81C784')
        elif task.priority == "High":
            return get_color_from_hex('#FFCDD2')
        elif task.priority == "Medium":
            return get_color_from_hex('#FFF9C4')
        else:
            return get_color_from_hex('#FFFFFF')

    def select_task(self, index):
        for i, child in enumerate(self.task_layout.children):
            if i == len(self.tasks) - 1 - index:
                child.background_color = get_color_from_hex('#BBDEFB')
            else:
                child.background_color = self.get_task_color(self.tasks[len(self.tasks) - 1 - i])

    def mark_complete(self, instance):
        selected = next((i for i, child in enumerate(self.task_layout.children) if child.background_color == get_color_from_hex('#BBDEFB')), None)
        if selected is not None:
            self.tasks[len(self.tasks) - 1 - selected].status = "Complete"
            self.update_task_list()
            self.save_tasks()
        else:
            self.show_error("Please select a task to mark as complete.")

    def remove_task(self, instance):
        selected = next((i for i, child in enumerate(self.task_layout.children) if child.background_color == get_color_from_hex('#BBDEFB')), None)
        if selected is not None:
            del self.tasks[len(self.tasks) - 1 - selected]
            self.update_task_list()
            self.save_tasks()
        else:
            self.show_error("Please select a task to remove.")

    def view_task(self, instance):
        selected = next((i for i, child in enumerate(self.task_layout.children) if child.background_color == get_color_from_hex('#BBDEFB')), None)
        if selected is not None:
            task = self.tasks[len(self.tasks) - 1 - selected]
            content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
            content.add_widget(Label(text=f"Description: {task.description}"))
            content.add_widget(Label(text=f"Due Date: {task.due_date}"))
            content.add_widget(Label(text=f"Category: {task.category}"))
            content.add_widget(Label(text=f"Priority: {task.priority}"))
            content.add_widget(Label(text=f"Status: {task.status}"))
            
            edit_button = RoundedButton(text='Edit Task', size_hint_y=None, height=dp(40))
            edit_button.bind(on_press=lambda x: self.edit_task(task))
            content.add_widget(edit_button)
            
            view = ModalView(size_hint=(0.9, 0.6))
            view.add_widget(content)
            view.open()
        else:
            self.show_error("Please select a task to view.")

    def edit_task(self, task):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        description_input = TextInput(text=task.description, multiline=False)
        content.add_widget(description_input)
        due_date_input = TextInput(text=task.due_date, multiline=False)
        content.add_widget(due_date_input)
        category_input = TextInput(text=task.category, multiline=False)
        content.add_widget(category_input)
        priority_input = TextInput(text=task.priority, multiline=False)
        content.add_widget(priority_input)
        
        save_button = RoundedButton(text='Save Changes', size_hint_y=None, height=dp(40))
        save_button.bind(on_press=lambda x: self.save_task_changes(task, description_input.text, due_date_input.text, category_input.text, priority_input.text))
        content.add_widget(save_button)
        
        edit_popup = Popup(title='Edit Task', content=content, size_hint=(0.9, 0.6))
        edit_popup.open()

    def save_task_changes(self, task, description, due_date, category, priority):
        task.description = description
        task.due_date = due_date
        task.category = category
        task.priority = priority
        self.update_task_list()
        self.save_tasks()
        self.show_error("Task updated successfully!")

    def show_error(self, message):
        popup = Popup(title='Message', content=Label(text=message), size_hint=(0.9, 0.3))
        popup.open()

    def filter_tasks(self, instance, value):
        filtered_tasks = [task for task in self.tasks if value.lower() in task.description.lower()]
        self.task_layout.clear_widgets()
        for index, task in enumerate(filtered_tasks):
            task_str = f"{task.description[:20]}... ({task.due_date})"
            task_button = RoundedButton(text=task_str, size_hint_y=None, height=dp(40))
            task_button.background_color = self.get_task_color(task)
            task_button.color = get_color_from_hex('#000000')
            task_button.bind(on_press=lambda x, idx=index: self.select_task(self.tasks.index(filtered_tasks[idx])))
            self.task_layout.add_widget(task_button)

    def save_tasks(self):
        with open('tasks.json', 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as f:
                self.tasks = [Task.from_dict(task_dict) for task_dict in json.load(f)]
            self.update_task_list()
        except FileNotFoundError:
            pass

    def show_sort_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        sort_options = ['Due Date', 'Priority', 'Category']
        for option in sort_options:
            btn = RoundedButton(text=f'Sort by {option}', size_hint_y=None, height=dp(40))
            btn.bind(on_press=lambda x, opt=option: self.sort_tasks(opt))
            content.add_widget(btn)
        
        sort_popup = Popup(title='Sort Tasks', content=content, size_hint=(0.9, 0.6))
        sort_popup.open()

    def sort_tasks(self, criteria):
        if criteria == 'Due Date':
            self.tasks.sort(key=lambda x: x.due_date)
        elif criteria == 'Priority':
            priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
            self.tasks.sort(key=lambda x: priority_order[x.priority])
        elif criteria == 'Category':
            self.tasks.sort(key=lambda x: x.category)
        self.update_task_list()

    def export_tasks(self, instance):
        with open('exported_tasks.txt', 'w') as f:
            for task in self.tasks:
                f.write(f"Description: {task.description}\n")
                f.write(f"Due Date: {task.due_date}\n")
                f.write(f"Category: {task.category}\n")
                f.write(f"Priority: {task.priority}\n")
                f.write(f"Status: {task.status}\n")
                f.write("\n")
        self.show_error("Tasks exported to 'exported_tasks.txt'")

class ToDoApp(App):
    def build(self):
        return ToDoListManager()

if __name__ == '__main__':
    ToDoApp().run()
	
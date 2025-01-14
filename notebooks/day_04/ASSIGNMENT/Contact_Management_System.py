import csv
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle

class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

class ContactManager:
    def __init__(self, filename):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    self.contacts.append(Contact(*row))
        except FileNotFoundError:
            pass

    def save_contacts(self):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Phone', 'Email'])
            for contact in self.contacts:
                writer.writerow([contact.name, contact.phone, contact.email])

    def add_contact(self, name, phone, email):
        new_contact = Contact(name, phone, email)
        self.contacts.append(new_contact)
        self.save_contacts()
        return True

    def search_contact(self, name):
        return [contact for contact in self.contacts if name.lower() in contact.name.lower()]

    def update_contact(self, old_name, name, phone, email):
        for contact in self.contacts:
            if contact.name.lower() == old_name.lower():
                contact.name = name
                contact.phone = phone
                contact.email = email
                self.save_contacts()
                return True
        return False

    def delete_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                self.contacts.remove(contact)
                self.save_contacts()
                return True
        return False

    def export_json(self, json_filename):
        data = [vars(contact) for contact in self.contacts]
        with open(json_filename, 'w') as file:
            json.dump(data, file, indent=4)

    def import_json(self, json_filename):
        try:
            with open(json_filename, 'r') as file:
                data = json.load(file)
            self.contacts = [Contact(**contact_data) for contact_data in data]
            self.save_contacts()
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False

class MenuButton(Button):
    pass

class ContactCard(BoxLayout):
    def __init__(self, contact, select_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 5]
        self.size_hint_y = None
        self.height = 100
        self.contact = contact

        with self.canvas.before:
            Color(*get_color_from_hex('#E0E0E0'))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        name_label = Label(text=contact.name, font_size=18, color=get_color_from_hex('#333333'), halign='left', valign='middle')
        name_label.bind(size=name_label.setter('text_size'))
        self.add_widget(name_label)

        details_layout = BoxLayout(orientation='horizontal')
        details_layout.add_widget(Label(text=contact.phone, font_size=14, color=get_color_from_hex('#666666')))
        details_layout.add_widget(Label(text=contact.email, font_size=14, color=get_color_from_hex('#666666')))
        self.add_widget(details_layout)

        select_button = Button(text="Select", size_hint=(None, None), size=(100, 40), 
                               background_color=get_color_from_hex('#4CAF50'))
        select_button.bind(on_press=lambda x: select_callback(contact))
        self.add_widget(select_button)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class ContactListScreen(Screen):
    def __init__(self, contact_manager, **kwargs):
        super().__init__(**kwargs)
        self.contact_manager = contact_manager
        self.layout = FloatLayout()

        with self.canvas.before:
            Color(*get_color_from_hex('#F5F5F5'))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.contacts_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.contacts_layout.bind(minimum_height=self.contacts_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.8))
        scroll_view.add_widget(self.contacts_layout)
        self.layout.add_widget(scroll_view)

        menu_button = Button(text='☰', size_hint=(None, None), size=(60, 60), 
                             pos_hint={'top': 1, 'left': 1}, font_size=30)
        menu_button.bind(on_press=self.toggle_menu)
        self.layout.add_widget(menu_button)

        self.menu_layout = BoxLayout(orientation='vertical', size_hint=(None, 1), width=200, 
                                     pos_hint={'x': -1, 'top': 1})
        self.menu_layout.add_widget(MenuButton(text='Add Contact', on_press=self.switch_to_add))
        self.menu_layout.add_widget(MenuButton(text='Search', on_press=self.switch_to_search))
        self.menu_layout.add_widget(MenuButton(text='Export', on_press=self.export_contacts))
        self.menu_layout.add_widget(MenuButton(text='Import', on_press=self.import_contacts))
        self.layout.add_widget(self.menu_layout)

        self.add_widget(self.layout)
        self.load_contacts()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def load_contacts(self):
        self.contacts_layout.clear_widgets()
        for contact in self.contact_manager.contacts:
            self.contacts_layout.add_widget(ContactCard(contact, self.select_contact))

    def select_contact(self, contact):
        app = App.get_running_app()
        app.root.get_screen('edit').load_contact(contact)
        app.root.current = 'edit'

    def toggle_menu(self, instance):
        target_x = 0 if self.menu_layout.pos_hint['x'] < 0 else -1
        self.menu_layout.pos_hint = {'x': target_x, 'top': 1}

    def switch_to_add(self, instance):
        self.manager.current = 'add'

    def switch_to_search(self, instance):
        self.manager.current = 'search'

    def export_contacts(self, instance):
        self.contact_manager.export_json('contacts_export.json')
        self.show_popup("Success", "Contacts exported to contacts_export.json")

    def import_contacts(self, instance):
        if self.contact_manager.import_json('contacts_export.json'):
            self.load_contacts()
            self.show_popup("Success", "Contacts imported from contacts_export.json")
        else:
            self.show_popup("Error", "Failed to import contacts. Please check the file format.")

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(300, 200))
        popup.open()

class AddContactScreen(Screen):
    def __init__(self, contact_manager, **kwargs):
        super().__init__(**kwargs)
        self.contact_manager = contact_manager
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.name_input = TextInput(hint_text='Name', multiline=False)
        self.phone_input = TextInput(hint_text='Phone', multiline=False)
        self.email_input = TextInput(hint_text='Email', multiline=False)

        layout.add_widget(self.name_input)
        layout.add_widget(self.phone_input)
        layout.add_widget(self.email_input)

        add_button = Button(text="Add Contact", size_hint_y=None, height=50, 
                            background_color=get_color_from_hex('#4CAF50'))
        add_button.bind(on_press=self.add_contact)
        layout.add_widget(add_button)

        back_button = Button(text="Back", size_hint_y=None, height=50, 
                             background_color=get_color_from_hex('#2196F3'))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def add_contact(self, instance):
        name = self.name_input.text
        phone = self.phone_input.text
        email = self.email_input.text
        if name and phone and email:
            if self.contact_manager.add_contact(name, phone, email):
                self.clear_inputs()
                self.show_popup("Success", "Contact added successfully!")
                app = App.get_running_app()
                app.root.get_screen('list').load_contacts()
        else:
            self.show_popup("Error", "Please fill all fields!")

    def clear_inputs(self):
        self.name_input.text = ''
        self.phone_input.text = ''
        self.email_input.text = ''

    def go_back(self, instance):
        self.manager.current = 'list'

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(300, 200))
        popup.open()

class EditContactScreen(Screen):
    def __init__(self, contact_manager, **kwargs):
        super().__init__(**kwargs)
        self.contact_manager = contact_manager
        self.contact = None
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.name_input = TextInput(hint_text='Name', multiline=False)
        self.phone_input = TextInput(hint_text='Phone', multiline=False)
        self.email_input = TextInput(hint_text='Email', multiline=False)

        layout.add_widget(self.name_input)
        layout.add_widget(self.phone_input)
        layout.add_widget(self.email_input)

        update_button = Button(text="Update Contact", size_hint_y=None, height=50, 
                               background_color=get_color_from_hex('#4CAF50'))
        update_button.bind(on_press=self.update_contact)
        layout.add_widget(update_button)

        delete_button = Button(text="Delete Contact", size_hint_y=None, height=50, 
                               background_color=get_color_from_hex('#F44336'))
        delete_button.bind(on_press=self.delete_contact)
        layout.add_widget(delete_button)

        back_button = Button(text="Back", size_hint_y=None, height=50, 
                             background_color=get_color_from_hex('#2196F3'))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def load_contact(self, contact):
        self.contact = contact
        self.name_input.text = contact.name
        self.phone_input.text = contact.phone
        self.email_input.text = contact.email

    def update_contact(self, instance):
        if self.contact:
            name = self.name_input.text
            phone = self.phone_input.text
            email = self.email_input.text
            if name and phone and email:
                if self.contact_manager.update_contact(self.contact.name, name, phone, email):
                    self.show_popup("Success", "Contact updated successfully!")
                    app = App.get_running_app()
                    app.root.get_screen('list').load_contacts()
                    self.go_back(None)
                else:
                    self.show_popup("Error", "Failed to update contact!")
            else:
                self.show_popup("Error", "Please fill all fields!")

    def delete_contact(self, instance):
        if self.contact:
            if self.contact_manager.delete_contact(self.contact.name):
                self.show_popup("Success", "Contact deleted successfully!")
                app = App.get_running_app()
                app.root.get_screen('list').load_contacts()
                self.go_back(None)
            else:
                self.show_popup("Error", "Failed to delete contact!")

    def go_back(self, instance):
        self.manager.current = 'list'

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(300, 200))
        popup.open()

class SearchScreen(Screen):
    def __init__(self, contact_manager, **kwargs):
        super().__init__(**kwargs)
        self.contact_manager = contact_manager
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.search_input = TextInput(hint_text='Search by name', multiline=False)
        layout.add_widget(self.search_input)

        search_button = Button(text="Search", size_hint_y=None, height=50, 
                               background_color=get_color_from_hex('#4CAF50'))
        search_button.bind(on_press=self.search_contacts)
        layout.add_widget(search_button)

        self.results_layout = BoxLayout(orientation='vertical', spacing=10)
        layout.add_widget(self.results_layout)

        back_button = Button(text="Back", size_hint_y=None, height=50, 
                             background_color=get_color_from_hex('#2196F3'))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def search_contacts(self, instance):
        name = self.search_input.text
        if name:
            results = self.contact_manager.search_contact(name)
            self.results_layout.clear_widgets()
            for contact in results:
                self.results_layout.add_widget(ContactCard(contact, self.select_contact))
        else:
            self.show_popup("Error", "Please enter a name to search!")

    def select_contact(self, contact):
        app = App.get_running_app()
        app.root.get_screen('edit').load_contact(contact)
        app.root.current = 'edit'

    def go_back(self, instance):
        self.manager.current = 'list'

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(300, 200))
        popup.open()

class ContactManagerApp(App):
    def build(self):
        self.title = 'Contact Management System'
        self.contact_manager = ContactManager('contacts.csv')
        sm = ScreenManager()
        sm.add_widget(ContactListScreen(name='list', contact_manager=self.contact_manager))
        sm.add_widget(AddContactScreen(name='add', contact_manager=self.contact_manager))
        sm.add_widget(EditContactScreen(name='edit', contact_manager=self.contact_manager))
        sm.add_widget(SearchScreen(name='search', contact_manager=self.contact_manager))
        return sm

if __name__ == '__main__':
    ContactManagerApp().run()

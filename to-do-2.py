from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
import random
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("todolist/firebase_config.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://to-do-list-a6fe0-default-rtdb.firebaseio.com/'
})


# Build Dashboard Screen
def build_dashboard_screen(sm):
    screen = Screen(name='dashboard')
    layout = FloatLayout()

    # App Title
    title_label = Label(text="[color=00ff00][b]TO-DO LIST APP[/b][/color]", markup=True, font_size=24,
                        size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'top': 1})
    layout.add_widget(title_label)

    # Date and Day
    today = datetime.now()
    date_text = today.strftime("%A, %d %B %Y")
    date_label = Label(text=f"[b]{date_text}[/b]", markup=True,
                       size_hint=(1, 0.05), pos_hint={'center_x': 0.5, 'top': 0.93},
                       color=(1, 1, 0, 1))
    layout.add_widget(date_label)

    # Task Table
    table = GridLayout(cols=4, spacing=5, size_hint_y=None, padding=10)
    table.bind(minimum_height=table.setter('height'))

    scroll = ScrollView(size_hint=(1, 0.65), pos_hint={'x': 0, 'y': 0.2})
    scroll.add_widget(table)
    layout.add_widget(scroll)

    

    # Add Task Button
    add_btn = Button(text='Add Task',
                     size_hint=(0.3, 0.1),
                     pos_hint={'center_x': 0.5, 'y': 0.05})

    def switch_to_add_task(instance):
        sm.current = 'add_task'

    add_btn.bind(on_press=switch_to_add_task)
    layout.add_widget(add_btn)

    
    screen.add_widget(layout)
    return screen

# Build Add Task Screen
def build_add_task_screen(sm):
    screen = Screen(name='add_task')
    layout = FloatLayout()

    # Title
    title = Label(text="[color=00ff00][b]ADD NEW TASK[/b][/color]", markup=True, font_size=24,
                  size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'top': 1})
    layout.add_widget(title)

    # Input fields
    obj_label = Label(text="Objective", size_hint=(0.3, 0.08), pos_hint={'x': 0.05, 'top': 0.85})
    layout.add_widget(obj_label)
    obj_input = TextInput(size_hint=(0.6, 0.08), pos_hint={'x': 0.35, 'top': 0.85})
    layout.add_widget(obj_input)

    deadline_label = Label(text="Deadline", size_hint=(0.3, 0.08), pos_hint={'x': 0.05, 'top': 0.7})
    layout.add_widget(deadline_label)
    deadline_input = TextInput(size_hint=(0.6, 0.08), pos_hint={'x': 0.35, 'top': 0.7})
    layout.add_widget(deadline_input)

    priority_label = Label(text="Priority", size_hint=(0.3, 0.08), pos_hint={'x': 0.05, 'top': 0.55})
    layout.add_widget(priority_label)
    priority_input = Spinner(
        text='Select Priority',
        values=('High', 'Medium', 'Low'),
        size_hint=(0.6, 0.08),
        pos_hint={'x': 0.35, 'top': 0.55}
    )
    layout.add_widget(priority_input)

    # Save Task Button
    add_btn = Button(text="Save Task",
                     size_hint=(0.3, 0.1),
                     pos_hint={'center_x': 0.7, 'y': 0.05})
    
        # Back Button
    back_btn = Button(text="Back",
                      size_hint=(0.3, 0.1),
                      pos_hint={'x': 0.2, 'y': 0.05})

    def go_back(instance):
        sm.current = 'dashboard'

    back_btn.bind(on_press=go_back)
    layout.add_widget(back_btn)


    def save_task(instance):
        objective = obj_input.text.strip()
        deadline = deadline_input.text.strip()
        priority = priority_input.text.strip()

        if objective:
            task_data = {
                'objective': objective,
                'deadline': deadline,
                'priority': priority,
                'done': False  # default value
            }
            task_id = f"task_{random.randint(1000, 9999)}"
            db.reference(f"tasks/{task_id}").set(task_data)

            obj_input.text = ""
            deadline_input.text = ""
            priority_input.text = ""

            

    add_btn.bind(on_press=save_task)
    layout.add_widget(add_btn)

    screen.add_widget(layout)
    return screen

# Build App
def build():
    sm = ScreenManager()
    sm.add_widget(build_dashboard_screen(sm))
    sm.add_widget(build_add_task_screen(sm))
    return sm

class MyApp(App):
    def build(self):
        return build()

if __name__ == "__main__":
    MyApp().run()

# calculate user expense
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView

import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import firebase_admin
from firebase_admin import credentials, db

signedin_user=""
signedin_name=""

sm = ScreenManager()
sm.transition = SlideTransition()

# --- Color Theme ---
Window.clearcolor = (0.01, 0.09, 0.17, 1)  # Dark Navy Blue

PRIMARY_COLOR = (0.2, 0.6, 0.8, 1)  # Teal Blue
SECONDARY_COLOR = (0.1, 0.4, 0.6, 1)
TEXT_COLOR = (1, 1, 1, 1)
BUTTON_TEXT_COLOR = (1, 1, 1, 1)

cred = credentials.Certificate("fireabase_config.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://splitwise-cf423-default-rtdb.firebaseio.com/'
})


email_input_signup=None
password_input=None
name_input=None
user_data = {
    "otp": "",
    "email":"",
    "password":"",
    "name":""
}

# --- Popup ---
def show_popup(title, message):
    popup = Popup(title=title, content=Label(text=message, color=TEXT_COLOR),
                  size_hint=(None, None), size=(300, 200),
                  background_color=SECONDARY_COLOR)
    popup.open()

# --- Navigation ---
def go_to_signup(instance):
    sm.transition.direction = 'left'
    sm.current = 'signup'

def go_to_login(instance):
    sm.transition.direction = 'right'
    sm.current = 'login'

def go_to_dashboard(instance):
    sm.transition.direction = 'right'
    sm.current = 'dashboard'

#write into the database
def write_email_and_password(user_id, email, password, name):
    # If user_id is None, generate a new one; otherwise, use the provided user_id
   
    if user_id is None:
        user_id = random.randint(1, 9999)
        
    ref = db.reference(f'users/{user_id}')
    ref.set({
        'name': name,
        'email': email,
        'password': password  
    })
    print(f"User '{user_id}' added successfully.")


# --- Send OTP Email ---
def send_otp(instance):
    global email_input_signup
    email = email_input_signup.text.strip()
    if not email:
        show_popup("Error", "Please enter a valid email.")
        return

    otp = str(random.randint(100000, 999999))
    user_data["otp"] = otp
    user_data["email"] = email

    sender_email = "curriculumfiles@schooli.online"
    sender_password = "lcfbcqncjhzbwawq"  #App Password
    subject = "Your OTP Code"
    body = f"Your One-Time Password (OTP) is: {otp}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        show_popup("Success", f"OTP sent to {email}")
    except Exception as e:
        show_popup("Error", f"Failed to send email")

def verify_otp(instance):
    global otp_input_signup, password_input_signup
    entered_otp = otp_input_signup.text.strip()
    if entered_otp == user_data["otp"]:
        show_popup("Success", "OTP verified! You are signed up.")
        user_data["name"] = name_input_signup.text.strip()
        user_data["password"] = password_input_signup.text.strip()
        user_data["email"] = email_input_signup.text.strip()
        email = user_data["email"]
        password = user_data["password"]
        name = user_data["name"]
        write_email_and_password(None, email, password, name)
    
   
    else:
        show_popup("Error", "Invalid OTP. Please try again.")

# ----SCREEN TEMPLATES----
# --- Login Screen ---
def build_login_screen():
    global email_input,password_input
    layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
    layout.add_widget(Label(text='[b]SmartSplit App[/b]', markup=True, font_size=36,
                            size_hint=(1, None), height=60, color="yellow"))

    float_layout = FloatLayout(size_hint=(1, 1))

    email_input = TextInput(hint_text='Email', multiline=False,
                            size_hint=(0.6, None), height=50,
                            pos_hint={'center_x': 0.5, 'center_y': 0.7},
                            background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    password_input = TextInput(hint_text='Password', password=True, multiline=False,
                               size_hint=(0.6, None), height=50,
                               pos_hint={'center_x': 0.5, 'center_y': 0.55},
                               background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    submit_btn = Button(text='Login', size_hint=(0.4, None), height=50,
                        pos_hint={'center_x': 0.5, 'center_y': 0.4},
                        background_color=PRIMARY_COLOR, color=BUTTON_TEXT_COLOR)
    

    float_layout.add_widget(email_input)
    float_layout.add_widget(password_input)
    float_layout.add_widget(submit_btn)

    layout.add_widget(float_layout)

    switch_btn = Button(text='New User? Go to Signup', size_hint=(1, None), height=50,
                        background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR,on_press=go_to_signup)

    layout.add_widget(switch_btn)

    return layout

# --- Signup Screen ---
def build_signup_screen():
    global email_input_signup, otp_input_signup, password_input_signup, name_input_signup

    layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
    layout.add_widget(Label(text='[b]SIGN UP[/b]', markup=True, font_size=36,
                            size_hint=(1, None), height=60, color=TEXT_COLOR))

    float_layout = FloatLayout(size_hint=(1, 1))

    name_input_signup = TextInput(hint_text='Name', multiline=False,
                           size_hint=(0.6, None), height=50,
                           pos_hint={'center_x': 0.5, 'center_y': 0.85},
                           background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    email_input_signup = TextInput(hint_text='Email', multiline=False,
                                   size_hint=(0.6, None), height=50,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.70},
                                   background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    password_input_signup = TextInput(hint_text='Password', password=True, multiline=False,
                               size_hint=(0.6, None), height=50,
                               pos_hint={'center_x': 0.5, 'center_y': 0.55},
                               background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    generate_otp_btn = Button(text='Generate OTP', size_hint=(0.4, None), height=40,
                              pos_hint={'center_x': 0.5, 'center_y': 0.40},
                              background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR)
    generate_otp_btn.bind(on_press=send_otp)

    otp_input_signup = TextInput(hint_text='Enter OTP', multiline=False,
                                 size_hint=(0.6, None), height=50,
                                 pos_hint={'center_x': 0.5, 'center_y': 0.25},
                                 background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    verify_btn = Button(text='Verify OTP', size_hint=(0.4, None), height=50,
                        pos_hint={'center_x': 0.5, 'center_y': 0.10},
                        background_color=PRIMARY_COLOR, color=BUTTON_TEXT_COLOR,on_press=verify_otp)


    float_layout.add_widget(name_input_signup)
    float_layout.add_widget(email_input_signup)
    float_layout.add_widget(password_input_signup)
    float_layout.add_widget(generate_otp_btn)
    float_layout.add_widget(otp_input_signup)
    float_layout.add_widget(verify_btn)

    layout.add_widget(float_layout)

    switch_btn = Button(text='Already a user? Go to Login', size_hint=(1, None), height=50,
                        background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR,on_press=go_to_login)
    
    layout.add_widget(switch_btn)

    return layout

#-----Dashboard-----

def build_dashboard_screen():
    
    global owe_amount_label, other_owe_amount_label

    layout = FloatLayout(size_hint=(1, 1))

    # Welcome label
    welcome_label = Label(
        text=f'[b]WELCOME {signedin_name.upper()}![/b]',
        markup=True,
        font_size=28,
        size_hint=(None, None), size=(300, 30),
        pos_hint={'center_x': 0.5, 'top': 0.95},
        color="yellow"
    )
    layout.add_widget(welcome_label)

    # Info bar container
    info_float = FloatLayout(size_hint=(None, None), size=(650, 90),
                             pos_hint={'center_x': 0.5, 'top': 0.88})



    # Horizontal box for balances and refresh
    info_box = BoxLayout(orientation='horizontal',
                         spacing=30,
                         size_hint=(None, None),
                         size=(600, 60),
                         pos_hint={'center_x': 0.5, 'center_y': 0.5})

    # YOU OWE section
    owe_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(120, 60))
    owe_label = Label(text='[b]YOU OWE[/b]', markup=True, font_size=18,
                      color="yellow", size_hint=(1, 0.4))
    owe_amount_label = Label(text=str(0), font_size=24,
                             color=TEXT_COLOR, size_hint=(1, 0.6))
    owe_box.add_widget(owe_label)
    owe_box.add_widget(owe_amount_label)

    # OTHERS OWE YOU section
    other_owe_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(160, 60))
    other_owe_label = Label(text='[b]OTHERS OWE YOU[/b]', markup=True,
                            font_size=18, color="yellow", size_hint=(1, 0.4))
    other_owe_amount_label = Label(text=str(0), font_size=24,
                                   color=TEXT_COLOR, size_hint=(1, 0.6))
    other_owe_box.add_widget(other_owe_label)
    other_owe_box.add_widget(other_owe_amount_label)

   
    refresh_btn = Button(
        text='Refresh',
        size_hint=(None, None), size=(100, 40),
        background_color=SECONDARY_COLOR,
        color=(1, 1, 1, 1),
        font_size=16,
       
    )

    # Add all to the info box
    info_box.add_widget(owe_box)
    info_box.add_widget(other_owe_box)
    info_box.add_widget(refresh_btn)

    info_float.add_widget(info_box)
    layout.add_widget(info_float)

    # Group members
    group =["member1", "member2", "member3"]  # Placeholder for group members
    num_members = len(group)
    cols = 3 + num_members

    # Table
    table = GridLayout(cols=cols, size_hint_y=None, spacing=5, padding=5)
   # table.bind(minimum_height=table.setter('height'))

    # Add header row
    headers = ['DESCRIPTION', 'PAID BY', 'AMOUNT'] + group
    for col in headers:
        table.add_widget(Label(text=f"[b]{col}[/b]", markup=True,
                            color="yellow", size_hint_y=None, height=40))

   
    # Buttons at bottom
    btn_layout = BoxLayout(
        orientation='horizontal',
        size_hint=(1, None), height=60, spacing=20, padding=[0, 0, 0, 10]
    )
    add_expense_btn = Button(
        text='Add Expense',
        size_hint=(0.5, 1),
        background_color=SECONDARY_COLOR,
        color=(1, 1, 1, 1),
        
    )
    add_group_members_btn = Button(
        text='Add Group Members',
        size_hint=(0.5, 1),
        background_color=SECONDARY_COLOR,
        color=(1, 1, 1, 1),
       
    )
    btn_layout.add_widget(add_expense_btn)
    btn_layout.add_widget(add_group_members_btn)
    layout.add_widget(btn_layout)

    return layout


def build_add_group_screen():
        global member_name_input, member_email_input, contact_input
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        layout.add_widget(Label(
            text='[b]ADD GROUP MEMBER[/b]', markup=True, font_size=36,
            size_hint=(1, None), height=60, color="yellow"
        ))

        float_layout = FloatLayout(size_hint=(1, 1))

        # Name
        name_label = Label(text='Name:', size_hint=(None, None), size=(100, 40),
                        pos_hint={'center_x': 0.2, 'center_y': 0.75}, color=TEXT_COLOR)
        member_name_input = TextInput(size_hint=(0.6, None), height=50,
                                    pos_hint={'center_x': 0.6, 'center_y': 0.75},
                                    background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

        # Email
        email_label = Label(text='Email:', size_hint=(None, None), size=(100, 40),
                            pos_hint={'center_x': 0.2, 'center_y': 0.6}, color=TEXT_COLOR)
        member_email_input = TextInput(size_hint=(0.6, None), height=50,
                                    pos_hint={'center_x': 0.6, 'center_y': 0.6},
                                    background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

        # Contact
        contact_label = Label(text='Contact (optional):', size_hint=(None, None), size=(150, 40),
                            pos_hint={'center_x': 0.2, 'center_y': 0.45}, color=TEXT_COLOR)
        contact_input = TextInput(size_hint=(0.6, None), height=50,
                                pos_hint={'center_x': 0.6, 'center_y': 0.45},
                                background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

        # Buttons
        add_btn = Button(text='Add Member', size_hint=(0.4, None), height=50,
                        pos_hint={'center_x': 0.5, 'center_y': 0.3},
                        background_color=PRIMARY_COLOR, color=BUTTON_TEXT_COLOR,
                       )

        back_btn = Button(text='Back to Dashboard', size_hint=(1, None), height=50,
                        pos_hint={'center_x': 0.5, 'center_y': 0.15},
                        background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR,
                       )

        # Add to layout
        float_layout.add_widget(name_label)
        float_layout.add_widget(member_name_input)
        float_layout.add_widget(email_label)
        float_layout.add_widget(member_email_input)
        float_layout.add_widget(contact_label)
        float_layout.add_widget(contact_input)
        float_layout.add_widget(add_btn)
        float_layout.add_widget(back_btn)

        layout.add_widget(float_layout)
        return layout

#
def build_add_expense_screen():
    global who_paid_spinner, description_input, amount_input
    layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

    layout.add_widget(Label(
        text='[b]ADD EXPENSE[/b]', markup=True, font_size=36,
        size_hint=(1, None), height=60, color="yellow"
    ))

    float_layout = FloatLayout(size_hint=(1, 1))

    # Who Paid
    who_paid_label = Label(text='Who Paid:', size_hint=(None, None), size=(120, 40),
                           pos_hint={'center_x': 0.18, 'center_y': 0.75}, color=TEXT_COLOR)
    
    # who_paid_input = TextInput(size_hint=(0.6, None), height=50,
    #                            pos_hint={'center_x': 0.6, 'center_y': 0.75},
    #                            background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
    group=["meber1", "member2", "member3"]  # Placeholder for group members
    who_paid_spinner= Spinner(
        text='Group Members',
        values=group,
        size_hint=(0.5, None), size=(180, 50),
        pos_hint={'x': 0.3, 'center_y': 0.75},
        background_color="white",
        color=TEXT_COLOR,
        font_size=16,
    )
    # Description
    description_label = Label(text='Description:', size_hint=(None, None), size=(120, 40),
                              pos_hint={'center_x': 0.18, 'center_y': 0.6}, color=TEXT_COLOR)
    description_input = TextInput(size_hint=(0.6, None), height=50,
                                  pos_hint={'center_x': 0.6, 'center_y': 0.6},
                                  background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    # Amount
    amount_label = Label(text='Amount:', size_hint=(None, None), size=(120, 40),
                         pos_hint={'center_x': 0.18, 'center_y': 0.45}, color=TEXT_COLOR)
    amount_input = TextInput(size_hint=(0.6, None), height=50,
                             pos_hint={'center_x': 0.6, 'center_y': 0.45},
                             background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    # Buttons
    add_btn = Button(text='Add', size_hint=(0.4, None), height=50,
                     pos_hint={'center_x': 0.5, 'center_y': 0.28},
                     background_color=PRIMARY_COLOR, color=BUTTON_TEXT_COLOR,
                     )

    back_btn = Button(
        text='Back to Dashboard',
        size_hint=(1, None), height=50,
        pos_hint={'center_x': 0.5, 'center_y': 0.14},
        background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR
    )

    # Call add_expense when the button is pressed, then go to dashboard
   
    # Add widgets
    float_layout.add_widget(who_paid_label)
    float_layout.add_widget(who_paid_spinner)
    float_layout.add_widget(description_label)
    float_layout.add_widget(description_input)
    float_layout.add_widget(amount_label)
    float_layout.add_widget(amount_input)
    float_layout.add_widget(add_btn)
    float_layout.add_widget(back_btn)

    layout.add_widget(float_layout)

    return layout

# --- Screens ---


signup_screen = Screen(name='signup')
signup_screen.add_widget(build_signup_screen())

login_screen = Screen(name='login')
login_screen.add_widget(build_login_screen())


dashboard_screen = Screen(name='dashboard')
dashboard_screen.add_widget(build_dashboard_screen())

sm.add_widget(login_screen)
sm.add_widget(signup_screen)
sm.add_widget(dashboard_screen)
class MyApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyApp().run()


































































































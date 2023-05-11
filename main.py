import glob

import plyer
import pyrebase
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
from kivymd.uix.toolbar import MDTopAppBar
from plyer import filechooser
from kivy.lang import Builder
from Converter import ImageConverter, PDFConverter
import os, shutil

screen_helper = """
#:import Label kivy.uix.label.Label
#:import Image kivy.uix.image.Image
#:import Button kivy.uix.button.Button
ScreenManager:
    LoginPage:
    FirstPage:
    SecondPage:
    ThirdPage:
    PrinterPage:
    SignupPage:
<LoginPage>:
    name: 'Login'
    MDTopAppBar:
        title:"Image to STL"
        pos_hint:{"top":1}
    MDFloatLayout:
        MDLabel:
            text:"fill email and password for log In"
            pos_hint:{"center_x":0.8,"center_y":0.8}
            theme_text_color: "Custom"
            text_color: (200, 140, 140)
            font_size:"25"
        MDFloatLayout:
            size_hint:.85,.08
            pos_hint:{"center_x":.5,"center_y":.6}    
            canvas:
                Color:
                    rgb:(238/255, 238/255, 238/255, 1)
                RoundedRectangle:
                    size:self.size
                    pos:self.pos
                    radius:[25]
            TextInput:
                id:email
                hint_text: "Email"
                size_hint:1,None
                pos_hint:{"center_x":.5,"center_y":.5}
                height: self.minimum_height
                multiline:False
                cursor_color: 3/255,93/255, 93/255, 1
                cursor_width:"2sp"
                foreground_color:3/255, 93/255, 93/255, 1
                background_color:0,0,0,0
                padding:15
                font_size:"18sp"  
        MDFloatLayout:
            size_hint:.85,.08
            pos_hint:{"center_x":.5,"center_y":.475}    
            canvas:
                Color:
                    rgb:(238/255, 238/255, 238/255, 1)
                RoundedRectangle:
                    size:self.size
                    pos:self.pos
                    radius:[25]
            TextInput:
                id:password
                hint_text: "Password"
                password:True
                size_hint:1,None
                pos_hint:{"center_x":.5,"center_y":.5}
                height: self.minimum_height
                multiline:False
                cursor_color: 3/255, 93/255, 93/255, 1
                cursor_width:"2sp"
                foreground_color:3/255, 93/255, 93/255, 1
                background_color:0,0,0,0
                padding:15
                font_size:"18sp"
        MDTextButton:
            text:"sign up"
            font_size: "19sp"
            theme_text_color: "Custom"
            text_color: 200, 140, 140
            pos_hint:{"center_x":.5,"center_y":.21}
            on_release:root.manager.current = 'Signup'
        Button:
            text: "LOG IN"
            font_size: "20sp"
            size_hint:.5,.08
            pos_hint:{"center_x":.5,"center_y":.12}
            background_color: 0,0,0,0
            on_release:app.login(email.text,password.text)
            canvas.before:
                Color:
                    rgb: (0/255, 150/255, 136/255)
                RoundedRectangle:
                    size: self.size
                    pos:self.pos
                    radius:[23]
<SignupPage>:
    name: 'Signup'
    MDTopAppBar:
        title:"Image to STL"
        pos_hint:{"top":1}
    MDFloatLayout:
        MDLabel:
            text:"fill your data to signup"
            pos_hint:{"center_x":0.835,"center_y":0.8}
            theme_text_color: "Custom"
            text_color: (200, 140, 140)
            font_size:"25"
        MDFloatLayout:
            size_hint:.85,.08
            pos_hint:{"center_x":.5,"center_y":.6}    
            canvas:
                Color:
                    rgb:(238/255, 238/255, 238/255, 1)
                RoundedRectangle:
                    size:self.size
                    pos:self.pos
                    radius:[25]
            TextInput:
                id:email
                hint_text: "Email"
                size_hint:1,None
                pos_hint:{"center_x":.5,"center_y":.5}
                height: self.minimum_height
                multiline:False
                cursor_color: 0/255,150/255, 136/255, 1
                cursor_width:"2sp"
                foreground_color:0/255, 150/255, 136/255, 1
                background_color:0,0,0,0
                padding:15
                font_size:"18sp"  
        MDFloatLayout:
            size_hint:.85,.08
            pos_hint:{"center_x":.5,"center_y":.475}    
            canvas:
                Color:
                    rgb:(238/255, 238/255, 238/255, 1)
                RoundedRectangle:
                    size:self.size
                    pos:self.pos
                    radius:[25]
            TextInput:
                id:password
                hint_text: "Password"
                password:True
                size_hint:1,None
                pos_hint:{"center_x":.5,"center_y":.5}
                height: self.minimum_height
                multiline:False
                cursor_color: 96/255,74/255, 215/255, 1
                cursor_width:"2sp"
                foreground_color:96/255, 74/255, 215/255, 1
                background_color:0,0,0,0
                padding:15
                font_size:"18sp"
        Button:
            text: "Sign Up"
            font_size: "20sp"
            size_hint:.35,.08
            pos_hint:{"center_x":.725,"center_y":.18}
            background_color:0,0,0,0
            on_release:app.signup(email.text,password.text);root.manager.current = 'Login'
            canvas.before:
                Color:
                    rgb: 0/255, 150/255, 136/255, 1
                RoundedRectangle:
                    size: self.size
                    pos:self.pos
                    radius:[23]
        Button:
            text: "Back"
            font_size: "20sp"
            size_hint:.35,.08
            pos_hint:{"center_x":.275,"center_y":.18}
            background_color:0,0,0,0
            on_release:root.manager.current = 'Login'
            canvas.before:
                Color:
                    rgb: 0/255, 150/255, 136/255, 1
                RoundedRectangle:
                    size: self.size
                    pos:self.pos
                    radius:[23]
    

<PrinterPage>:
    name: 'printer'
    MDTopAppBar:
        title:"Image to STL"
        pos_hint:{"top":1}
    MDLabel:
        text:" jjjj"
        pos_hint:{"center_x":0.75,"center_y":0.8}
        theme_text_color: "Custom"
        text_color: 200, 140, 140
        font_size:"25"
<FirstPage>:
    name: 'First'
    MDBottomNavigation:
        MDBottomNavigationItem:
            name: "screen1"
            text: "Converting"
            icon: "convert"
            MDTopAppBar:
                title:"Image to STL"
                pos_hint:{"top":1}
            MDLabel:
                text:"upload photo to convert to stl file"
                pos_hint:{"center_x":0.75,"center_y":0.8}
                theme_text_color: "Custom"
                text_color: 200, 140, 140
                font_size:"25"  
            Button:
                id: abc
                background_normal: 'upload_b.png'
                pos_hint: {'center_x':0.5,'center_y':0.5}
                size_hint: .3, .3
                on_press:app.file_chooser();self.background_normal=app.imagepdf;root.manager.screens[2].ids.img.source = app.imagepdf
            MDRectangleFlatButton:
                text: 'Convert'
                font_size:20
                pos_hint: {'center_x':0.5,'center_y':0.2}
                on_press:
                    app.btnfunc();
                    if '.pdf' in app.imagePath: root.manager.current = 'Third';

        MDBottomNavigationItem:
            name: "screen2"
            text: "Chat"
            icon: "chat"
            MDTopAppBar:
                title:"Image to STL"
                pos_hint:{"top":1}
            MDLabel:
                text:"the chat with the printer owner"
                pos_hint:{"center_x":0.75,"center_y":0.8}
                theme_text_color: "Custom"
                text_color: 200, 140, 140
                font_size:"25"
        MDBottomNavigationItem:
            name: "screen3"
            text: "History"
            icon: "history"
            MDTopAppBar:
                title:"Image to STL"
                pos_hint:{"top":1}
            MDLabel:
                text:"the stl files you have converted"
                pos_hint:{"center_x":0.75,"center_y":0.8}
                theme_text_color: "Custom"
                text_color: 200, 140, 140
                font_size:"25"
        MDBottomNavigationItem:
            name: "screen4"
            text: "LogOut"
            icon: "logout"
            on_enter: root.manager.current = 'Login';

<SecondPage>:
    name: 'Second'
    MDTopAppBar:
        title:"The Stl File"
        pos_hint:{"top":1}
    Image:
        id:img
        source: ''
        pos_hint: {'center_x':0.5,'center_y':0.65}
        size_hint: .4, .4
    MDRectangleFlatButton:
        text: 'Download the stl file'
        font_size:20
        pos_hint: {'center_x':0.5,'center_y':0.3}
        on_press:
            app.directory_chooser();
            if app.temp!='true':print(app.temp)
            else:root.manager.current = 'First'
    MDRectangleFlatButton:
        text: 'Back'
        font_size:20
        pos_hint: {'center_x':0.25,'center_y':0.1}
        on_press: root.manager.current = 'First'
    MDRectangleFlatButton:
        text: 'send'
        font_size:20
        pos_hint: {'center_x':0.75,'center_y':0.1}
        on_press: app.send();root.manager.current = 'First'
<ThirdPage>:
    name: 'Third'
    BoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title:"choose image to convert it"
            pos_hint:{"top":1}
        ScrollView:
            size: self.size
            GridLayout:
                id: wall
                cols: 2
                row_force_default: True
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 200
                top: self.height
                spacing: "40dp"
                padding: "70dp"
"""

class FirstPage(Screen):
    pass
class SecondPage(Screen):
    pass
class PrinterPage(Screen):
    pass
class ThirdPage(Screen):
    pass
class LoginPage(Screen):
    pass

class SignupPage(Screen):
    pass
# Create the screen manager
sm = ScreenManager()
sm.add_widget(FirstPage(name='First'))
sm.add_widget(SecondPage(name='Second'))
sm.add_widget(ThirdPage(name='Third'))
sm.add_widget(FirstPage(name='Login'))
sm.add_widget(PrinterPage(name='printer'))
sm.add_widget(FirstPage(name='Signup'))
class MyApp(MDApp):
    screen = Screen()
    config={
        "apiKey": "AIzaSyDqyR1lzvY-SzZ6-30yL7LQZ5IrmcEsRQQ",
        "authDomain": "dvis-ff74a.firebaseapp.com",
        "databaseURL": "https://dvis-ff74a-default-rtdb.firebaseio.com",
        "projectId": "dvis-ff74a",
        "storageBucket": "dvis-ff74a.appspot.com",
        "messagingSenderId": "282026381544",
        "appId": "1:282026381544:web:173ef9fd4c7fef4a43795d",
        "measurementId": "G-0B9MLSDQ33",
        "serviceAccount": "dvis-ff74a-firebase-adminsdk-31g83-5cae6c3910.json",
        "databaseURL": "https://dvis-ff74a-default-rtdb.firebaseio.com/"
    }
    firebase=pyrebase.initialize_app(config)
    '''
    data={
        'Email':'areenaldda@gmail.com',
        'Password':'Aa212654'
    }
    firebase.post('https://dvis-ff74a-default-rtdb.firebaseio.com/Users',data)

    
    #Get Data
    
    result=firebase.get('https://dvis-ff74a-default-rtdb.firebaseio.com/Users','')
    for i in result.keys():
        print(result[i]['Email'])
    '''


    def build(self):
        self.imagePath = ''
        self.imagepdf = ''
        self.user=''
        self.temp = ''
        self.DestDir = os.getcwd()
        self.images=[]
        self.theme_cls.primary_palette = "Teal"
        self.toolbar = MDTopAppBar(title="Image to STL")
        self.toolbar.pos_hint = {"top": 1}
        self.screen.add_widget(self.toolbar)
        screen = Builder.load_string(screen_helper)
        return screen
    def btnfunc(self):

        self.root.screens[2].ids.img.source = self.imagepdf
        print("button is pressed!!")
        print(self.imagePath)
        directory = self.DestDir + f'/images/'  # directory name
        if '.pdf' in self.imagePath and self.imagePath != '':
            self.images=PDFConverter(self.imagePath, self.DestDir)
            for i, image_path in enumerate(self.images):
                button = Button(background_normal=image_path)
                button.bind(on_press=lambda button, i=i: self.xxx(i))
                self.root.screens[3].ids.wall.add_widget(button)
            print('+++++++++',self.imagePath)

        elif self.imagePath != '':
            ImageConverter(self.imagePath, self.DestDir)
            self.root.current = 'Second'

    def file_chooser(self):
        file = filechooser.open_file()
        self.imagePath = file[0]
        if '.pdf' in self.imagePath and self.imagePath != '':
            self.imagepdf = 'PDF.svg'
        else:
            self.imagepdf = self.imagePath

    def directory_chooser(self):
        file = filechooser.open_file(file_name="surface.stl")
        directoryPath = file[0]
        finalPath = self.DestDir + f'/stlFiles/surface.stl'
        popup = Popup(title='Error message!!',
                      content=MDLabel(text='you must write the name of the file with suffix .stl'
                                      , halign='center'),
                      size_hint=(None, None), size=(450, 150), background='white', title_color='black')
        if '.' not in directoryPath:
            directoryPath += '.stl'
        print(directoryPath)
        if '.stl' in directoryPath:
            self.temp = 'true'
        else:
            self.temp = 'false'
        if self.temp == 'true':
            os.replace(finalPath, directoryPath)
        else:
            popup.open()
    def xxx(self, index):
        print("Sel:", self.DestDir,self.images[index])
        self.imagePath=os.path.join(self.DestDir,self.images[index])
        print('xxxxxxx',self.imagePath)
        self.root.screens[1].ids.abc.background_normal = self.images[index]
        self.imagepdf=self.images[index]
        self.root.screens[3].ids.wall.clear_widgets()
        self.root.current = 'First'
    def signup(self,mail,pas):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://dvis-ff74a-default-rtdb.firebaseio.com', None)
        data = {
            'Email': mail,
            'Password': pas,
            'user': 0
        }
        firebase.post('https://dvis-ff74a-default-rtdb.firebaseio.com/Users', data)
    def login(self,mail,pas):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://dvis-ff74a-default-rtdb.firebaseio.com', None)
        result = firebase.get('https://dvis-ff74a-default-rtdb.firebaseio.com/Users', '')
        for i in result.keys():
            if result[i]['Email']==mail:
                if result[i]['Password']==pas:
                    if result[i]['user']==0:
                        self.user=mail
                        print(self.user+" Logged In!")
                        self.root.current = 'First'
                    else:
                        self.root.current = 'printer'

    def send(self):
        plyer.notification.notify(title="My App",message="TTTTT")
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://dvis-ff74a-default-rtdb.firebaseio.com', None)
        storage=firebase.storage()
        imgg="test.png"
        storage.child(imgg).put(imgg)
        data = {
            'file': self.imagePath,
            'send': self.user,
            'IsDone': 1,
            'time': " "
        }
        firebase.post('https://dvis-ff74a-default-rtdb.firebaseio.com/Prints', data)


if __name__ == '__main__':
    MyApp().run()
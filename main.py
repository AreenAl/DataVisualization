import glob
import plyer
from firebase import firebase
from firebase_admin import credentials, initialize_app, storage
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage, Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton, MDTextButton, MDRectangleFlatButton
from kivymd.uix.toolbar import MDTopAppBar
from plyer import filechooser
from kivy.lang import Builder
from Converter import ImageConverter, PDFConverter
import os, shutil
from kivy.utils import get_color_from_hex


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
    MDFloatLayout:
        MDLabel:
            text:"data for print"
            pos_hint:{"center_x":0.835,"center_y":0.86}
            theme_text_color: "Custom"
            text_color: (200, 140, 140)
            font_size:"25"
    ScrollView:
        size: self.size
        pos_hint:{"center_y":.31}
        top: 20
        id:kk



                
            
<FirstPage>:
    name: 'First'
    MDBottomNavigation:
        id:bottom_navigation
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
            ScrollView:
                size: self.size
                GridLayout:
                    id: amma
                    cols: 2
                    row_force_default: True
                    size_hint_y: None
                    height: self.minimum_height
                    row_default_height: 200
                    top: self.height
                    spacing: "40dp"
                    padding: "70dp"
            
                
        MDBottomNavigationItem:
            name: "screen3"
            text: "History"
            icon: "history"
            MDTopAppBar:
                title:"Image to STL"
                pos_hint:{"top":1}
            MDLabel:
                text:"the images you have converted"
                pos_hint:{"center_x":0.75,"center_y":0.8}
                theme_text_color: "Custom"
                text_color: 200, 140, 140
                font_size:"25"
            ScrollView:
                size: self.size
                pos_hint:{"center_y":.22}
                top: 20
                id:scroll
                
        MDBottomNavigationItem:
            name: "screen4"
            text: "LogOut"
            icon: "logout"
            on_enter: root.manager.current = 'Login'

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
    cred = credentials.Certificate("dvis-ff74a-firebase-adminsdk-31g83-5cae6c3910.json")
    initialize_app(cred, {'storageBucket': 'dvis-ff74a.appspot.com',
                          'databaseURL': "https://dvis-ff74a-default-rtdb.firebaseio.com/"
                          })
    '''
    cred_obj = firebase_admin.credentials.Certificate("dvis-ff74a-firebase-adminsdk-31g83-5cae6c3910.json")
    default_app = firebase_admin.initialize_app(cred_obj, {
        'databaseURL': "https://dvis-ff74a-default-rtdb.firebaseio.com/"
    })'''
    '''
    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://dvis-ff74a-default-rtdb.firebaseio.com', None)
    data = {
        'Email': "areenal",
        'Password': "12345",
        'user': 1
    }
    firebase.post('https://dvis-ff74a-default-rtdb.firebaseio.com/Users', data)
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
        self.history=[]
        self.async_images=[]
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
        prints = firebase.get('https://dvis-ff74a-default-rtdb.firebaseio.com/Prints', '')
        chats = firebase.get('https://dvis-ff74a-default-rtdb.firebaseio.com/Chats', '')

        for i in result.keys():
            if result[i]['Email']== mail:
                if result[i]['Password']==pas:
                    if result[i]['user']==0:
                        self.user=mail
                        print(self.user+" Logged In!")
                        grid = GridLayout(cols=2, size_hint_y=None)
                        grid.row_force_default = True
                        grid.row_default_height = 200
                        for b in prints.keys():
                            if prints[b]['send'] == self.user:
                                self.history.append(prints[b]['file'])
                        for i, a in enumerate(self.history):
                            image = AsyncImage(source=a)
                            #image.bind(on_touch_down=self.mess(i))
                            image.bind(on_touch_down=self.on_async_image_press)
                            self.async_images.append(image)
                            '''image = Button(text=" ",background_normal=prints[b]['file'], height=200)
                            image.bind(on_press=lambda x, i=i: self.mess(i))
                            '''
                            grid.add_widget(image)
                            grid.bind(minimum_height=grid.setter('height'))
                        # create the input text field
                        # add the grid and input text field to the list view layout
                        self.root.screens[1].ids.scroll.add_widget(grid)
                        self.root.current = 'First'
                        for a in chats.keys():
                            if chats[a]['username']==self.user:
                                title_label = MDLabel(text=chats[a]['message'], font_size="100", halign='center')
                                self.root.screens[1].ids.amma.add_widget(title_label)

                    else:
                        grid = GridLayout(cols=3)
                        grid.row_force_default = True
                        grid.row_default_height = 200

                        # set the height of the grid to be the sum of its children
                        for c in prints.keys():
                            if prints[c]['IsDone']==1:
                                title_label = MDLabel(text=prints[c]['send'], font_size="50", halign='center')
                                usern = prints[c]['send']
                                # create the image for the item
                                image = AsyncImage(source=prints[c]['file'])
                                # mess = Button(background_normal='mes.png',size_hint= {.54, .5},height=10)
                                mess = MDRectangleFlatButton(text='Send', pos_hint={"center_y": 0.055})
                                mess.bind(on_press=lambda x: self.mess(usern))
                                #mess.bind(on_press=lambda a: prints[c]['IsDone']=0)

                                # add the label and image to the grid
                                grid.add_widget(mess)
                                grid.add_widget(title_label)
                                grid.add_widget(image)
                                grid.bind(minimum_height=grid.setter('height'))

                            '''a=result[i]['file']
                            bb=MDLabel(text=result[i]['send'], x='0.2')
                            xx=AsyncImage(source=a)
                            #self.root.screens[4].ids.ll.add_widget(xx)'''

                        # create the input text field
                        # add the grid and input text field to the list view layout
                        self.root.screens[4].ids.kk.add_widget(grid)
                        #self.root.screens[4].ids.kk.add_widget(input_text)
                        self.root.current = 'printer'

    def on_async_image_press(self, instance, touch):
        for i, async_image in enumerate(self.async_images):
            if async_image.collide_point(*touch.pos):
                # Perform actions when the AsyncImage is pressed
                print(self.history[i])

                import requests
                img_data = requests.get(self.history[i]).content
                with open('image_name.jpg', 'wb') as handler:
                    handler.write(img_data)
                self.root.screens[1].ids.abc.background_normal = 'image_name.jpg'
                self.imagePath = 'image_name.jpg'
                self.imagepdf = 'image_name.jpg'

                self.root.screens[1].ids.bottom_navigation.switch_tab("screen1")

    def send(self):
        from firebase import firebase
        bucket = storage.bucket()
        fileName = self.imagePath
        blob = bucket.blob(fileName)
        blob.upload_from_filename(fileName)
        # Opt : if you want to                                       make public access from the URL
        blob.make_public()
        print("your file url", blob.public_url)
        data = {
            'file': blob.public_url,
            'send': self.user,
            'IsDone': 1,
            'time': " "
        }
        firebase = firebase.FirebaseApplication('https://diatrack-48525.firebaseio.com/', authentication=None)
        firebase.post('https://dvis-ff74a-default-rtdb.firebaseio.com/Prints', data)
    def mess(self,username):
        #plyer.notification.notify(title="My App",message="TTTTT")

        send=MDFlatButton(text="Send")
        close=MDFlatButton(text="Close")
        self.set_button_background_color(send, (0, 0.5, 0.5, 1))  # Teal color
        self.set_button_background_color(close, (0, 0.5, 0.5, 1))  # Red color

        text_input = TextInput(hint_text="Enter your message", multiline=False)
        button_layout = BoxLayout(orientation='horizontal',size_hint_x=None, width=470, spacing=70)
        button_layout.add_widget(Widget(size_hint_x=1))
        button_layout.add_widget(send)
        button_layout.add_widget(close)

        content_layout = BoxLayout(orientation='vertical')
        content_layout.add_widget(text_input)
        content_layout.add_widget(button_layout)

        self.dialog=Popup(title="Write Message  "
                                "               ",
                          size_hint=(0.9, 0.65),
                          auto_dismiss=False,
                          content=content_layout,
                          background_color=get_color_from_hex("#CCCCCC"))  # Set the background color here        )
        send.bind(on_release=lambda btn: self.send(btn, text_input.text,username))
        close.bind(on_release=self.dialog.dismiss)
        self.dialog.open()

    def send(self,obj,text,user):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://dvis-ff74a-default-rtdb.firebaseio.com', None)
        data = {
            'username': user,
            'message': text
        }
        firebase.post('https://dvis-ff74a-default-rtdb.firebaseio.com/Chats', data)
        self.dialog.dismiss()

    def set_button_background_color(self,button, color):
        button.background_color = color

        def set_button_canvas_size(instance, value):
            button.canvas.before.clear()
            with button.canvas.before:
                from kivy.graphics import Color
                Color(*button.background_color)
                from kivy.graphics import Rectangle
                Rectangle(pos=button.pos, size=button.size)

        button.bind(pos=set_button_canvas_size, size=set_button_canvas_size)


if __name__ == '__main__':
    MyApp().run()
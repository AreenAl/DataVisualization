from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.image import Image, AsyncImage
from kivymd.uix.button import MDFlatButton,MDFillRoundFlatButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from plyer import filechooser
from kivy.lang import Builder
from Converter import ImageConverter
import os

screen_helper = """
ScreenManager:
    FirstPage:
    SecondPage:
<FirstPage>:
    name: 'First'
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
        background_normal: 'upload_b.png'
        pos_hint: {'center_x':0.5,'center_y':0.5}
        size_hint: .3, .3
        on_press: app.file_chooser()
    MDRectangleFlatButton:
        text: 'Convert'
        pos_hint: {'center_x':0.5,'center_y':0.2}
        on_press: app.btnfunc();root.manager.current = 'Second'
<SecondPage>:
    name: 'Second'
    MDTopAppBar:
        title:"The Stl File"
        pos_hint:{"top":1}
    Button:
        background_normal: 'upload_b.png'
        pos_hint: {'center_x':0.5,'center_y':0.65}
        size_hint: .3, .3
    MDRectangleFlatButton:
        text: 'Download'
        pos_hint: {'center_x':0.35,'center_y':0.4}
    MDRectangleFlatButton:
        text: 'Show'
        pos_hint: {'center_x':0.65,'center_y':0.4}
    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'First'

"""

class FirstPage(Screen):
    pass
class SecondPage(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(FirstPage(name='First'))
sm.add_widget(SecondPage(name='Second'))


class MyApp(MDApp):
    screen = Screen()
    def btnfunc(self):
        print("button is pressed!!")
        if self.imagePath != '':
            ImageConverter(self.imagePath,self.DestDir)
    def build(self):
        self.imagePath = ''
        self.DestDir = os.getcwd()
        self.theme_cls.primary_palette="Teal"
        self.toolbar=MDTopAppBar(title="Image to STL")
        self.toolbar.pos_hint={"top":1}
        self.screen.add_widget(self.toolbar)
        screen = Builder.load_string(screen_helper)
        return screen
    def file_chooser(self):

        file=filechooser.open_file()
        print(file[0])
        self.imagePath = file[0]

if __name__ == '__main__':
    MyApp().run()
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
class MyApp(MDApp):
    screen = Screen()
    def btnfunc(self, obj):
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
        self.screen.add_widget(MDLabel(
            text="upload photo to convert to stl file",
            pos_hint={"center_x":0.51,"center_y":0.8},
            theme_text_color= "Custom",
            text_color="slategrey",
            font_style="H5",
        ))
        self.screen.add_widget(Button(
            background_normal= 'upload_b.png',
            size_hint=(.3, .3),
            pos_hint={"x": 0.35, "y": 0.4},
            on_release=self.file_chooser,

        ))
        self.screen.add_widget(MDFillRoundFlatButton(
            text="CONVERT",
            font_size=20,
            pos_hint={"center_x":0.5,"center_y":0.25},
            on_release=self.btnfunc,
        ))
        return self.screen
    def file_chooser(self,obj):

        file=filechooser.open_file()
        print(file[0])
        self.imagePath = file[0]

if __name__ == '__main__':
    MyApp().run()
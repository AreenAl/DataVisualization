from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
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
    FirstPage:
    SecondPage:
    ThirdPage:
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
        id: abc
        background_normal: 'upload_b.png'
        pos_hint: {'center_x':0.5,'center_y':0.5}
        size_hint: .3, .3
        on_press: app.file_chooser();self.background_normal=app.imagepdf;root.manager.screens[1].ids.img.source = app.imagepdf
    MDRectangleFlatButton:
        text: 'Convert'
        font_size:20
        pos_hint: {'center_x':0.5,'center_y':0.2}
        on_press: app.btnfunc();root.manager.screens[1].ids.img.source = app.imagepdf
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
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'First'
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
                cols: 2
                row_force_default: True
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 200
                top: self.height
                spacing: "40dp"
                padding: "70dp"
                on_kv_post:
                    [self.add_widget(Button(background_normal=image_path,on_press=lambda button, i=i: app.xxx(i))) for i, image_path in enumerate(app.images)]

"""
class FirstPage(Screen):
    pass
class SecondPage(Screen):
    pass
class ThirdPage(Screen):
    pass
# Create the screen manager
sm = ScreenManager()
sm.add_widget(FirstPage(name='First'))
sm.add_widget(SecondPage(name='Second'))
sm.add_widget(ThirdPage(name='Third'))

class MyApp(MDApp):
    screen = Screen()
    def btnfunc(self):
        print("button is pressed!!")
        print(self.imagePath)
        if '.pdf' in self.imagePath and self.imagePath != '':
            PDFConverter(self.imagePath, self.DestDir)
            self.root.current = 'Third'
        elif self.imagePath != '':
            ImageConverter(self.imagePath, self.DestDir)
            self.root.current = 'Second'

    def build(self):
        self.imagePath = ''
        self.imagepdf = ''
        self.temp = ''
        self.DestDir = os.getcwd()
        self.theme_cls.primary_palette = "Teal"
        self.toolbar = MDTopAppBar(title="Image to STL")
        self.toolbar.pos_hint = {"top": 1}
        self.screen.add_widget(self.toolbar)
        self.images = os.listdir('images')
        for i in range(len(self.images)):
            temp = self.images[i]
            self.images[i] = 'images/' + temp
        screen = Builder.load_string(screen_helper)
        return screen

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
        print("Selected button index:", index)
        self.imagePath=os.path.join(self.DestDir,self.images[index])
        self.root.screens[0].ids.abc.background_normal = self.images[index]
        self.imagepdf=self.images[index]
        print("Directory Path:", os.path.join(self.DestDir,self.images[index]))
        self.root.current = 'First'

if __name__ == '__main__':
    MyApp().run()

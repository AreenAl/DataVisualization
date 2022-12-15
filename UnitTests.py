import os
from kivy.tests.common import GraphicUnitTest
from kivy.base import EventLoop
from main import MyApp
from Converter import ImageConverter


class MyTestCase(GraphicUnitTest):

    def test_build(self):
        window = MyApp()
        window.run()
        self.assertNotEqual(window, None)

    def test_size(self):
        window = MyApp()
        window.run()
        self.assertEqual(window.screen.width, 100)
        self.assertEqual(window.screen.height, 100)

    def test_converter(self):
        window = MyApp()
        window.build()
        ImageConverter(window.DestDir + "/test_pic.png", window.DestDir)
        self.assertEqual(os.path.exists(window.DestDir + "/stlFiles/surface.stl"), True)

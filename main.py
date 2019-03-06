from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty, NumericProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.listview import ListView
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.checkbox import CheckBox 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
import matplotlib
matplotlib.use("module://kivy.garden.matplotlib.backend_kivy")
from kivy.garden.matplotlib import FigureCanvasKivyAgg
import pandas as pd
import os

Window.clearcolor = (1,1,1,1)

class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, root, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(root, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, root, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_press(self):
        popup = TextInputPopup(self)
        popup.open()

    def update_changes(self, txt):
        self.text = txt

class Menu(BoxLayout):
    manager = ObjectProperty(None)
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def save(self, path, filename, data, size):
        with open(os.path.join(path, filename), 'w') as stream:
            for row in [data[i:i+size] for i in range(0, len(data), size)]:
                stream.write(','.join([str(item) for item in row])+'\n')
        self.dismiss_popup()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_load(self):
        content = LoadDialog(cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    
    def load(self):
        self.dismiss_popup()
        
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)

class EditData(Screen):
    data_items = ListProperty([])
    data_labels = ListProperty([])
    data_size = NumericProperty(0)

    def show_data(self, path, filename):
        self.data_items.clear()
        self.data_labels.clear()
        df = pd.read_csv(filename[0])
        self.data_items.extend(list(df.columns.values))
        for row in df.iterrows():
            index, data = row
            self.data_items.extend(data.tolist())
            self.data_size = len(data)

class LoadData(Screen):
    data_items = ListProperty([])
    data_labels = ListProperty([])
    data_size = NumericProperty(0)

    def show_data(self, path, filename):
        self.data_items.clear()
        self.data_labels.clear()
        df = pd.read_csv(filename[0])
        self.data_items.extend(list(df.columns.values))
        for row in df.iterrows():
            index, data = row
            self.data_items.extend(data.tolist())
            self.data_size = len(data)

class Help(Screen):
    pass

class Manager(ScreenManager):
    loadData = ObjectProperty(None)
    editData = ObjectProperty(None)
    helpScreen = ObjectProperty(None)

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MainApp(App):

    def build(self):
        return Menu()


if __name__ == '__main__':
   MainApp().run()


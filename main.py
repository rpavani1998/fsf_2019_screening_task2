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
from kivy.uix.dropdown import DropDown
import matplotlib
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from matplotlib.figure import Figure
import matplotlib as mpl
from kivy_matplotlib import MatplotFigure, MatplotNavToolbar
import matplotlib.pyplot as plt
import numpy as np
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


class AddData(Popup):
    pass

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
        # print(txt, self.index)
        # LoadData().change_data(txt, self.index)
        # EditData().change_data(txt, self.index)
        self.text = txt


class MultiSelectSpinner(Button):
    """Widget allowing to select multiple text options."""

    dropdown = ObjectProperty(None)
    """(internal) DropDown used with MultiSelectSpinner."""

    values = ListProperty([])
    """Values to choose from."""

    selected_values = ListProperty([])
    """List of values selected by the user."""

    def __init__(self, **kwargs):
        self.bind(dropdown=self.update_dropdown)
        self.bind(values=self.update_dropdown)
        super(MultiSelectSpinner, self).__init__(**kwargs)
        self.bind(on_release=self.toggle_dropdown)

    def toggle_dropdown(self, *args):
        if self.dropdown.parent:
            self.dropdown.dismiss()
        else:
            self.dropdown.open(self)

    def update_dropdown(self, *args):
        if not self.dropdown:
            self.dropdown = DropDown()
        values = self.values
        if values:
            if self.dropdown.children:
                self.dropdown.clear_widgets()
            for value in values:
                b = Factory.MultiSelectOption(text=value)
                b.bind(state=self.select_value)
                self.dropdown.add_widget(b)

    def select_value(self, instance, value):
        if value == 'down':
            if instance.text not in self.selected_values:
                self.selected_values.append(instance.text)
        else:
            if instance.text in self.selected_values:
                self.selected_values.remove(instance.text)

    def on_selected_values(self, instance, value):
        if value:
            self.text = ', '.join(value)
        else:
            self.text = ''

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

    
    def add_data(self):
        popup = AddData()
        popup.open()
    
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

    def update_data(self, text):
        for line in text.split('\n'):
            self.data_items.extend(line.split(','))

    # def change_data(self, text, index):
    #     print(self.data_items, self.data_items[index])
    #     self.data_items[index] = text

class PlotData(Screen):
    data_items = ListProperty([])
    data_labels = ListProperty([])
    data_size = NumericProperty(0)
    file_name = ''
    fig = None

    def load_data(self, path, filename):
        self.file_name = filename[0]
        self.data_items.clear()
        self.data_labels.clear()
        df = pd.read_csv(filename[0])
        self.data_labels.extend(list(df.columns.values))
        self.data_items.extend(list(df.columns.values))
        for row in df.iterrows():
            index, data = row
            self.data_items.extend(data.tolist())
            self.data_size = len(data)

    def update_data(self, text):
        for line in text.split('\n'):
            self.data_items.extend(line.split(','))

    def plot(self, plot, columns):
        fig = None
        columns = [ col.strip() for col in columns.split(',')]
        df = pd.read_csv(self.file_name)
        print(df)
        fig = mpl.figure.Figure(figsize=(2, 2))
        plt = fig.gca()
        if plot == 'Plot scatter points':
            x = df[columns[0]].values
            y = df[columns[1]].values
            plt.scatter(x, y, alpha=0.5)
        elif plot == 'Plot scatter points with smooth lines':
            x = df[columns[0]].values
            y = df[columns[1]].values
            plt.scatter(x, y, alpha=0.5)
            plt.plot(np.linspace(0, 1, 10), np.power(np.linspace(0, 1, 10), 2), c= "red", marker='.', linestyle=':')
        elif plot == 'Plot lines':
            x = df[columns[0]].values
            y = df[columns[1]].values
            plt.plot(x,y)
        # MatplotFigure (Kivy widget)
        self.fig = fig
        fig_kivy = MatplotFigure(fig)
        runTouchApp(fig_kivy)

    def save_png(self):
        self.fig.savefig('path/to/save/image/to.png') 


class LoadData(Screen):
    data_items = ListProperty([])
    data_labels = ListProperty([])
    data_size = NumericProperty(0)

    def show_data(self, path, filename):
        self.data_items.clear()
        self.data_labels.clear()
        df = pd.read_csv(filename[0])
        self.data_labels.extend(list(df.columns.values))
        self.data_items.extend(list(df.columns.values))
        for row in df.iterrows():
            index, data = row
            self.data_items.extend(data.tolist())
            self.data_size = len(data)

    def update_data(self, text):
        for line in text.split('\n'):
            self.data_items.extend(line.split(','))

    
    # def show_plot(self):
    #     content = PlotData()
    #     # print(self.data_items, self.data_labels, self.data_size)
    #     content.set_data(self.data_items, self.data_labels)
    # def change_data(self, text, index):
    #     print(self.data_items, self.data_items[index])
    #     self.data_items[index] = text

class Help(Screen):
    pass

class Manager(ScreenManager):
    loadData = ObjectProperty(None)
    plotData = ObjectProperty(None)
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


# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.recycleview.views import RecycleDataViewBehavior
# from kivy.uix.button import Button
# from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty, NumericProperty
# from kivy.uix.recyclegridlayout import RecycleGridLayout
# from kivy.uix.behaviors import FocusBehavior
# from kivy.uix.recycleview.layout import LayoutSelectionBehavior
# from kivy.uix.popup import Popup
# from kivy.uix.floatlayout import FloatLayout
# from kivy.factory import Factory
# import pandas as pd

# class TextInputPopup(Popup):
#     obj = ObjectProperty(None)
#     obj_text = StringProperty("")

#     def __init__(self, obj, **kwargs):
#         super(TextInputPopup, self).__init__(**kwargs)
#         self.obj = obj
#         self.obj_text = obj.text


# class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
#                                   RecycleGridLayout):
#     ''' Adds selection and focus behaviour to the view. '''


# class SelectableButton(RecycleDataViewBehavior, Button):
#     ''' Add selection support to the Button '''
#     index = None
#     selected = BooleanProperty(False)
#     selectable = BooleanProperty(True)

#     def refresh_view_attrs(self, rv, index, data):
#         ''' Catch and handle the view changes '''
#         self.index = index
#         return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

#     def on_touch_down(self, touch):
#         ''' Add selection on touch down '''
#         if super(SelectableButton, self).on_touch_down(touch):
#             return True
#         if self.collide_point(*touch.pos) and self.selectable:
#             return self.parent.select_with_touch(self.index, touch)

#     def apply_selection(self, rv, index, is_selected):
#         ''' Respond to the selection of items in the view. '''
#         self.selected = is_selected

#     def on_press(self):
#         popup = TextInputPopup(self)
#         popup.open()

#     def update_changes(self, txt):
#         self.text = txt

# class LoadDialog(FloatLayout):
#     load = ObjectProperty(None)
#     cancel = ObjectProperty(None)

# class RV(BoxLayout):
#     data_items = ListProperty([])
#     loadfile = ObjectProperty(None)
#     text_input = ObjectProperty(None)
#     data_labels = ListProperty([])
#     data_size = NumericProperty(0)

#     def dismiss_popup(self):
#         self._popup.dismiss()

#     def show_load(self):
#         content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
#         self._popup = Popup(title="Load file", content=content,
#                             size_hint=(0.9, 0.9))
#         self._popup.open()

#     def load(self, path, filename):
#         self.data_items.clear()
#         self.data_labels.clear()
#         print(path, filename)
#         df = pd.read_csv(filename[0])
#         self.data_labels.extend(list(df.columns.values))
#         for row in df.iterrows():
#             index, data = row
#             self.data_items.extend(data.tolist())
#             self.data_size = len(data)
#         self.dismiss_popup()

#     def load_sample(self, path, filename):
#         df = pd.read_csv(filename[0])
#         self.data_labels =list(df.columns.values)
#         for row in df.iterrows():
#             index, data = row
#             self.data_items.extend(data.tolist())
#             self.data_size = len(data)
    
        
#     def __init__(self, **kwargs):
#         super(RV, self).__init__(**kwargs)
#         self.load_sample('/Users/pavanirajula/Desktop',['/Users/pavanirajula/Desktop/C2ImportGroupsSample.csv'])


# class EditorApp(App):
#     title = "Kivy App"

#     def build(self):
#         return RV()

# Factory.register('LoadDialog', cls=LoadDialog)

# if __name__ == "__main__":
#     EditorApp().run()

# # from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
# # from kivy.app import App
# # from kivy.uix.boxlayout import BoxLayout
# # import matplotlib.pyplot as plt

# # plt.plot([1, 23, 2, 4])
# # plt.ylabel('some numbers')

# # class MyTestApp(App):

# #     def build(self):
# #         box = BoxLayout()
# #         box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
# #         return box

# # MyTestApp().run()


# #:import Label kivy.uix.label.Label
# <SelectableButton>:
#     # Draw a background to indicate selection
#     canvas.before:
#         Color:
#             rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
#         Rectangle:
#             pos: self.pos
#             size: self.size

# <RV>:
#     orientation: 'vertical'
#     ActionBar:
#         pos_hint: {'top':1}
#         ActionView:
#             use_separator: True
#             ActionPrevious:
#                 title: 'Example App'
#                 with_previous: False
#             ActionGroup:
#                 text: 'File'
#                 mode: 'spinner'
#                 ActionButton:
#                     text: 'Load'
#                     on_release: root.show_load()
#                 ActionButton:
#                     text:'Add Data'
#                 ActionButton:
#                     text:'Save as png'  
#             ActionGroup:
#                 text: 'Edit'
#                 mode: 'spinner'
#                 ActionButton:
#                     text:'Edit data'
#             ScrollView:
#                 size_hint: 1.0,0.7
#                 size: (500, 500)
#                 BoxLayout:
#                     orientation: "vertical"
#                     GridLayout:
#                         size_hint: 1, 0.7
#                         size_hint_y: None
#                         height: 25
#                         cols: root.data_size
#                         on_parent:
#                             print(root.data_items, root.data_labels, root.data_size)
#                             for i in root.data_labels:txt = "{0}".format(i); self.add_widget(Label(text = txt))
#                     BoxLayout:
#                         RecycleView:
#                             viewclass: 'SelectableButton'
#                             data: [{'text': str(x)} for x in root.data_items]
#                             SelectableRecycleGridLayout:
#                                 default_size: None, dp(26)
#                                 default_size_hint: 1, None
#                                 size_hint_y: None
#                                 cols: root.data_size
#                                 height: self.minimum_height
#                                 orientation: 'vertical'
#                                 multiselect: True
#                                 touch_multiselect: True

# <LoadDialog>:
#     BoxLayout:
#         size: root.size
#         pos: root.pos
#         orientation: "vertical"
#         FileChooserIconView:
#             id: filechooser
#             filters: ['*.csv']
#         BoxLayout:
#             size_hint_y: None
#             height: 30
#             Button:
#                 text: "Cancel"
#                 on_release: root.cancel()

#             Button:
#                 text: "Load"
#                 on_release: root.load(filechooser.path, filechooser.selection)

# <SelectableButton>:
#     # Draw a background to indicate selection
#     canvas.before:
#         Color:
#             rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
#         Rectangle:
#             pos: self.pos
#             size: self.size


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


class MainApp(App):

    def build(self):
        return Menu()


if __name__ == '__main__':
   MainApp().run()


import kivy
kivy.require('2.1.0')

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime

class ListItemsWithCheckbox(TwoLineAvatarIconListItem):
    """Custom list item"""
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def mark(self, check, the_list_item):
        """Mark the task as complete or incomplete"""
        if check.active == True:
            the_list_item.text = '[s]'+the_list_item.text+'[/s]'
        else:
            pass

    def delete_item(self, the_list_item):
        """Delete the task"""
        self.parent.remove_widget(the_list_item)

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Custom left container"""

class DialogContent(MDBoxLayout):
    """Opens a dialog box that gets the notes from the user"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%A %D %B %Y'))

    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        """This function gets the date from the date picker and converts
        it to a more friendly form then changes label on the dialog to that"""
        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

class MainApp(MDApp):
    task_list_dialog = None
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Note",
                type="custom",
                content_cls=DialogContent(),
            )

        self.task_list_dialog.open()

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date):
        """Add note to the list of notes"""
        print(task.text, task_date)
        self.root.ids['container'].add_widget(ListItemsWithCheckbox(text='[b]'+task.text+'[/b]', secondary_text=task_date))
        task.text = ""

if __name__ == "__main__":
    app = MainApp()
    app.run()

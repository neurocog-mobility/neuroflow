import traitlets
from ipywidgets import widgets
from tkinter import Tk, filedialog
from pathlib import Path

class SelectFolderButton(widgets.Button):
    """A folder widget that leverages tkinter.filedialog."""

    def __init__(self, details = None):
        super(SelectFolderButton, self).__init__()
        # Add the selected_files trait
        self.add_traits(files=traitlets.traitlets.List())
        # Create the button.
        self.details = details
        if details:
            self.description = f"Select Folder: {details}"
        else:
            self.description = "Select Folder"
        self.icon = "square-o"
        self.style.button_color = "orange"
        self.rootdir = Path.home()
        self.layout = widgets.Layout(width='auto', height='40px')
        self.folder = None
        # Set on click behavior.
        self.on_click(self.select_folder)

    @staticmethod
    def select_folder(b):
        """Generate instance of tkinter.filedialog.

        Parameters
        ----------
        b : obj:
            An instance of ipywidgets.widgets.Button 
        """
        with widgets.Output():
            try:
                # Create Tk root
                root = Tk()
                # Hide the main window
                root.withdraw()
                # Raise the root to the top of all windows.
                root.call('wm', 'attributes', '.', '-topmost', True)
                # Folder be set to b.value
                b.folder = filedialog.askdirectory(
                    initialdir=b.rootdir
                )

                if b.details:
                    b.description = f"{b.details} folder: {Path(b.folder)}"
                else:
                    b.description = f"Folder selected: {Path(b.folder)}"
                b.icon = "check-square-o"
                b.style.button_color = "lightgreen"
            except:
                pass
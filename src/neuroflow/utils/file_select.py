#%%
import traitlets
from ipywidgets import widgets
from tkinter import Tk, filedialog
from pathlib import Path

class SelectFilesButton(widgets.Button):
    """A file widget that leverages tkinter.filedialog."""

    def __init__(self, filetypes=(("All files", "*"),)):
        super(SelectFilesButton, self).__init__()
        # Add the selected_files trait
        self.add_traits(files=traitlets.traitlets.List())
        # Create the button.
        self.description = "Select Files"
        self.icon = "square-o"
        self.style.button_color = "orange"
        self.layout = widgets.Layout(width='auto', height='40px')
        # Set root directory
        # self.rootdir = os.path.realpath(
        #      '/home/abdulzaf/Documents/data/neurocog-lab/test-data/bittium'
        # )
        self.rootdir = Path.home()
        self.filetypes = filetypes
        # self.out = out
        # Set on click behavior.
        self.on_click(self.select_files)

    @staticmethod
    def select_files(b):
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
                # List of selected fileswill be set to b.value
                b.file = filedialog.askopenfilename(
                     multiple=False,
                     initialdir=b.rootdir,
                     filetypes=b.filetypes
                )

                b.description = f"File selected: {Path(b.file[0]).stem}{Path(b.file[0]).suffix}"
                b.icon = "check-square-o"
                b.style.button_color = "lightgreen"
            except:
                pass

# out = widgets.Output()
# raw = SelectFilesButton()
# widgets.VBox([raw, out])


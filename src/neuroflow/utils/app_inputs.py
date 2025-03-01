import ipywidgets as widgets
from IPython.display import display, HTML
from neuroflow.definitions import _define_data_catalog
from neuroflow.pipeline_registry import _get_pipeline_registry
from neuroflow.catalog.inputs.input_registry import _get_input_registry
from neuroflow.catalog.outputs.output_registry import _register_outputs
from neuroflow.catalog.inputs.intermediate_registry import _register_intermed
from neuroflow.utils.collect import _collect
from neuroflow.utils.utils import _format_text
from neuroflow.utils.setup import update_data_catalog
from IPython import get_ipython
import os
import traitlets
from ipywidgets import widgets
from tkinter import Tk, filedialog
from pathlib import Path
import yaml
import shutil

class SelectFilesButton(widgets.Button):
    """A file widget that leverages tkinter.filedialog."""

    def __init__(self, filetypes=(("All files", "*"), ), details = None):
        super(SelectFilesButton, self).__init__()
        # Add the selected_files trait
        self.add_traits(files=traitlets.traitlets.List())
        # Create the button.
        self.details = details
        if details:
            self.description = f"Select file: {details}"
        else:
            self.description = "Select file"
        self.icon = "square-o"
        self.style.button_color = "orange"
        self.layout = widgets.Layout(width='auto', height='40px')
        self.rootdir = Path("/home/abdulzaf/Documents/data/neurocog-lab/test-data/naps-multi") #Path.home()
        self.filetypes = filetypes
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

                if b.details:
                    b.description = f"{b.details} file: {Path(b.file[0]).stem}{Path(b.file[0]).suffix}"
                else:
                    b.description = f"File selected: {Path(b.file[0]).stem}{Path(b.file[0]).suffix}"
                b.icon = "check-square-o"
                b.style.button_color = "lightgreen"
            except:
                pass

class SelectFolderButton(widgets.Button):
    """A folder widget that leverages tkinter.filedialog."""

    def __init__(self, details = None):
        super(SelectFolderButton, self).__init__()
        # Add the selected_files trait
        self.add_traits(files=traitlets.traitlets.List())
        # Create the button.
        self.details = details
        if details:
            self.description = f"Select folder: {details}"
        else:
            self.description = "Select folder"
        self.icon = "square-o"
        self.style.button_color = "orange"
        self.rootdir = Path("/home/abdulzaf/Documents/data/neurocog-lab/test-data/naps-multi") #Path.home()
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

def _collect_inputs(input_registry, project_root):
    for ikey, imeta in input_registry.items():
        if imeta["requires_input"]:
            source_dir = imeta["catalog"]["path"]
            target_dir = os.path.join(project_root, "data")
            sub_dir = imeta["modality"]
            filepattern = imeta["filepattern"]
    
            _collect(source_dir, target_dir, sub_dir, filepattern)
            # update path in catalog
            input_registry[ikey]["catalog"]["path"] = os.path.join(target_dir, "raw", sub_dir)

    return input_registry

def on_inputs_registered(btn, output,
                         input_buttons, input_registry,
                         project_root, neuroflow_root,
                         pipeline_name):
    # complete input catalogs
    for i, (ikey, imeta) in enumerate(input_registry.items()):
        if imeta["requires_input"]:
            if imeta["pathtype"] == "file":
                input_registry[ikey]["catalog"]["filepath"] = input_buttons[ikey].file
            elif imeta["pathtype"] == "directory":
                input_registry[ikey]["catalog"]["path"] = input_buttons[ikey].folder

    try:
        # collect files
        input_registry = _collect_inputs(input_registry, project_root)

        # create intermediate and output registrys
        output_registry = _register_outputs(pipeline_name, project_root)
        inter_registry = _register_intermed(pipeline_name)

        # create data catalog
        catalog_data = _define_data_catalog(input_registry, inter_registry, output_registry)

        # write local catalog to project
        config_path = os.path.join(project_root, "catalogs", pipeline_name)
        os.makedirs(config_path, exist_ok=True)

        catalog_path = os.path.join(config_path, "catalog.yml")
        
        with open(catalog_path, 'w') as catalogfile:
            yaml.dump(catalog_data, catalogfile, default_flow_style=False)

        # write neuroflow catalog
        update_data_catalog(neuroflow_root, catalog_data)

        # set input_registry variable
        get_ipython().user_ns["input_registry"] = input_registry
        get_ipython().user_ns["inter_registry"] = inter_registry
        get_ipython().user_ns["output_registry"] = output_registry

        # update UI
        btn.description = "Inputs registered"
        btn.button_style = "success"
        btn.icon = "check-square-o"
        btn.button_style = "success"
        with output:
            print("All files successfully transferred.")
    except Exception as e:
        with output:
            print(f"Error occurred: {e}")


def app_register_inputs(pipeline_name, project_root, neuroflow_root):
    pipe_dict = _get_pipeline_registry()
    pipe_info = pipe_dict[pipeline_name]

    # create header
    print(f"Setting input catalog for: {_format_text(pipeline_name, bold=True)}")
    print(pipe_info["description"], end="\n")

    # input registration
    input_registry = _get_input_registry(pipeline_name)
    dict_btns = {}
    for i, (ikey, imeta) in enumerate(input_registry.items()):
        if imeta["requires_input"]:
            if imeta["pathtype"] == "file":
                btn = SelectFilesButton()
                dict_btns[ikey] = btn
            if imeta["pathtype"] == "directory":
                btn = SelectFolderButton(details = ikey)
                dict_btns[ikey] = btn
    
    for bkey, btn in dict_btns.items():
        display(btn)

    btn_register_inputs = widgets.Button(
        icon = "square-o",
        button_style = "info",
        layout = widgets.Layout(width='auto', height='40px'),
        description = "Register inputs"
    )
    output = widgets.Output()
    btn_register_inputs.on_click(lambda b: on_inputs_registered(
        b, output,
        dict_btns, input_registry,
        project_root, neuroflow_root,
        pipeline_name
    ))

    display(HTML("<br>"))
    display(btn_register_inputs)
    display(output)


def register_data_catalog(project_root, neuroflow_root, pipeline_name):
    # check if catalog exists in project
    config_path = os.path.join(project_root, "catalogs", pipeline_name)
    catalog_path = os.path.join(config_path, "catalog.yml")

    if Path(catalog_path).is_file():
        print(f"A data catalog for the {pipeline_name} pipeline already exists.")
        is_overwrite = input("Would you like to overwrite the data catalog? (y/n) [n]: ") or "n"
    else:
        is_overwrite = "y"

    if is_overwrite == "y":
        app_register_inputs(pipeline_name, project_root, neuroflow_root)
    else:
        # copy local catalog to neuroflow
        shutil.copyfile(
            os.path.join(config_path, "catalog.yml"),
            os.path.join(neuroflow_root, "conf", "base", "catalog.yml")
        )
        get_ipython().run_line_magic("reload_kedro", f"{neuroflow_root}")
        print("Reloaded data catalog.")

    
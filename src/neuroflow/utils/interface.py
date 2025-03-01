import ipywidgets as widgets
from IPython.display import display
from neuroflow.pipeline_registry import _get_pipeline_registry
from neuroflow.utils.setup import initialize_catalogs
from neuroflow.catalog.inputs.input_registry import _get_input_registry
from neuroflow.catalog.inputs.intermediate_registry import _get_inter_registry
from neuroflow.catalog.parameters.param_registry import _get_param_registry
from neuroflow.catalog.outputs.output_registry import _get_output_registry
from neuroflow.utils.folder_select import SelectFolderButton
from neuroflow.utils.file_select import SelectFilesButton
from neuroflow.utils.utils import _format_text
from IPython import get_ipython

def on_button_click(b, blist):
        for b, btn in enumerate(blist):
            print(b)
            print(btn.folder)

def on_inputs_registered(input_buttons, input_registry):
    # complete input catalogs
    for i, (ikey, imeta) in enumerate(input_registry.items()):
        if imeta["requires_input"]:
            if imeta["pathtype"] == "file":
                input_registry[ikey]["catalog"]["filepath"] = input_buttons[ikey].file
            elif imeta["pathtype"] == "directory":
                input_registry[ikey]["catalog"]["path"] = input_buttons[ikey].folder

    get_ipython().user_ns["input_registry"] = input_registry


def on_pipeline_selected(btn, output, pipeline_name, project_root, neuroflow_root):
    pipe_dict = _get_pipeline_registry()
    pipe_info = pipe_dict[pipeline_name]
    with output:
        output.clear_output()
        # create header
        print(f"Setting catalog for: {_format_text(pipeline_name, bold=True)}")
        print(pipe_info["description"])

        # input registration
        input_registry = _get_input_registry(pipeline_name)
        dict_btns = {}
        for i, (ikey, imeta) in enumerate(input_registry.items()):
            if imeta["requires_input"]:
                if imeta["pathtype"] == "file":
                    btn = SelectFilesButton()
                    dict_btns[ikey] = btn
                if imeta["pathtype"] == "directory":
                    btn = SelectFolderButton()
                    dict_btns[ikey] = btn
        
        for bkey, btn in dict_btns.items():
            display(btn)

        btn_register_inputs = widgets.Button(
            description = "Register inputs"
        )
        output_params = widgets.Output()
        btn_register_inputs.on_click(lambda b: on_inputs_registered(
            b, output_params, pipeline_name,
            project_root, neuroflow_root,
            dict_btns, input_registry
        ))

        display(btn_register_inputs)
        display(output_params)

def set_pipeline(btn, pipeline_name):
    btn.description = f"Selected: {pipeline_name}"
    btn.icon = "check-square-o"
    btn.button_style = "success"
    get_ipython().user_ns["pipeline_name"] = pipeline_name


def app_select_pipeline():
    pipe_dict = _get_pipeline_registry()
    pipes = list(pipe_dict.keys())
    dropdown = widgets.Dropdown(
        options=pipes,
        description='Select a pipeline:',
        disabled=False,
        value = pipes[0],
        layout = widgets.Layout(width='auto'),
        style = {'description_width': 'auto'}
    )
    btn_go = widgets.Button(
        icon = "square-o",
        button_style = "info",
        layout = widgets.Layout(width='auto', height='40px'),
        description = "Set pipeline"
    )

    output = widgets.Output()

    btn_go.on_click(lambda b: set_pipeline(b, dropdown.value)
    )

    display(dropdown)
    display(btn_go)
    display(output)
import ipywidgets as widgets
from IPython.display import display
from neuroflow.pipeline_registry import _get_pipeline_registry
from IPython import get_ipython
from neuroflow.utils.utils import _format_text


def set_pipeline(btn, pipeline_name):
    btn.description = f"Selected: {pipeline_name}"
    btn.icon = "check-square-o"
    btn.button_style = "success"
    get_ipython().user_ns["pipeline_name"] = pipeline_name

def on_dropdown_change(dropdown, output, pipe_dict):
    if dropdown['type'] == 'change' and dropdown['name'] == 'value':
        with output:
            output.clear_output()
            pipeline = pipe_dict[dropdown['new']]
            print(_format_text(pipeline["description"], underline=True))
            print(_format_text("\tInputs: ", bold=True), pipeline["input"])
            print(_format_text("\tParameters: ", bold=True), pipeline["params"])
            print(_format_text("\tOutputs: ", bold=True), pipeline["output"])
            print("")

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
    with output:
        pipeline = pipe_dict[pipes[0]]
        print(_format_text(pipeline["description"], underline=True))
        print(_format_text("\tInputs: ", bold=True), pipeline["input"])
        print(_format_text("\tParameters: ", bold=True), pipeline["params"])
        print(_format_text("\tOutputs: ", bold=True), pipeline["output"])
        print("")

    dropdown.observe(lambda dd: on_dropdown_change(dd, output, pipe_dict))
    btn_go.on_click(lambda b: set_pipeline(b, dropdown.value)
    )

    display(dropdown)
    display(output)
    display(btn_go)
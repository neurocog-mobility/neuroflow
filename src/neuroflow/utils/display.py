from neuroflow.pipeline_registry import _get_pipeline_registry
from neuroflow.utils.utils import _format_text

def display_pipelines():
    """
    
    :meta private:

    Display all registered pipelines.
    """
    pipeline_registry = _get_pipeline_registry()
    
    print(_format_text("\nRegistered pipelines:\n", bold=True))
    for pipename, pipeline in pipeline_registry.items():
        print(_format_text(f"{pipename} : ", bold=True, underline=True, color='blue'), end="")
        print(_format_text(pipeline["description"], underline=True))
        print(_format_text("\tInputs: ", bold=True), pipeline["input"])
        print(_format_text("\tParameters: ", bold=True), pipeline["params"])
        print(_format_text("\tOutputs: ", bold=True), pipeline["output"])
        print("")
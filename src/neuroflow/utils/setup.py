import os
import yaml
import click

from IPython import get_ipython
from neuroflow.utils.create_experiment import _create_experiment
from neuroflow.utils.collect import _copy_notebook_templates
from neuroflow.definitions import define_catalog
from neuroflow.input_registry import register_inputs
from neuroflow.output_registry import register_outputs
from neuroflow.param_registry import register_params
from neuroflow.utils.utils import _format_text
from neuroflow.pipeline_registry import get_pipeline_registry
import numpy as np
from IPython.display import clear_output
import shutil

ipython = get_ipython()

def initialize_catalogs(pipeline_name, project_root, neuroflow_root):
    config_path = os.path.join(project_root, "catalogs", pipeline_name)

    if os.path.exists(config_path):
        print(f"A data catalog for the {pipeline_name} pipeline already exists.")
        is_overwrite = input("Would you like to overwrite the catalogs? (y/n) [n]: ") or "n"
    else:
        is_overwrite = "y"

    if is_overwrite == "y":
        generate_catalogs(pipeline_name, project_root, neuroflow_root)
    else:
        # copy local catalog to neuroflow
        shutil.copyfile(
            os.path.join(config_path, "catalog.yml"),
            os.path.join(neuroflow_root, "conf", "base", "catalog.yml")
        )
        shutil.copyfile(
            os.path.join(config_path, "parameters.yml"),
            os.path.join(neuroflow_root, "conf", "base", "parameters.yml")
        )
        ipython.run_line_magic("reload_kedro", f"{neuroflow_root}")
        print("Reloaded config files.")



def generate_catalogs(pipeline_name, project_root, neuroflow_root):
    clear_output(wait=False)
    print(_format_text("\n~~~ Generating data registry ~~~", bold=True, underline=True))
    input_registry = register_inputs(pipeline_name, project_root)
    output_registry = register_outputs(pipeline_name, project_root)
    
    clear_output(wait=False)
    param_registry = register_params(pipeline_name, input_registry)
    
    clear_output(wait=False)
    print(_format_text("\n~~~ Creating catalogs ~~~", bold=True, underline=True))
    catalog_data, catalog_params = define_catalog(input_registry, output_registry, param_registry)

    # write local project catalog
    config_path = os.path.join(project_root, "catalogs", pipeline_name)
    os.makedirs(config_path, exist_ok=True)

    catalog_path = os.path.join(config_path, "catalog.yml")
    parameters_path = os.path.join(config_path, "parameters.yml")
    
    with open(catalog_path, 'w') as catalogfile:
        yaml.dump(catalog_data, catalogfile, default_flow_style=False)
    with open(parameters_path, 'w') as parametersfile:
        yaml.dump(catalog_params, parametersfile, default_flow_style=False)
    
    # write neuroflow catalog
    update_catalog(neuroflow_root, catalog_data, catalog_params)


def update_catalog(neuroflow_path, dict_catalog, dict_parameters):
    config_path = os.path.join(neuroflow_path, "conf", "base")

    catalog_path = os.path.join(config_path, "catalog.yml")
    parameters_path = os.path.join(config_path, "parameters.yml")
    
    with open(catalog_path, 'w') as catalogfile:
        yaml.dump(dict_catalog, catalogfile, default_flow_style=False)
    
    with open(parameters_path, 'w') as parametersfile:
        yaml.dump(dict_parameters, parametersfile, default_flow_style=False)
    
    ipython.run_line_magic("reload_kedro", f"{neuroflow_path}")
    print("Updated config files.")


def initialize_neuroflow(neuroflow_path):
    """
    """ 
    # RESET+UPDATE CATALOG & PARAMETERS
    pipeline_registry = get_pipeline_registry()

    inputs = []
    outputs = []
    params = []
    for key, val in pipeline_registry.items():
        inputs += val["input"]
        params += val["params"]
        outputs += val["output"]

    inputs = list(np.unique(inputs))
    params = list(np.unique(params))
    outputs = list(np.unique(outputs))

    catalog_data = {str(key): {"type": "pandas.CSVDataset", "filepath": ""} for key in inputs + outputs}
    catalog_params = {str(key): "placeholder" for key in params}
    print(catalog_data, catalog_params)
    update_catalog(neuroflow_path, catalog_data, catalog_params)

    print("-----------------------------------")
    print("-----------------------------------")
    print("Neuroflow loaded successfully.")
    print("-----------------------------------")
    print("-----------------------------------")


@click.group(name="Neuroflow")
def project_group() -> None:  # pragma: no cover
    pass


@project_group.command()  # 'create' subcommand
@click.option('--create', '-cr', help='Create a new NeuroFlow project in the given directory. Example: neuroflow --create [DIRECTORY] where [DIRECTORY] is the project directory')
def _main(create):
    """Create a new project."""
    print(f"-> Creating project: {create}")

    _create_experiment(create)
    _copy_notebook_templates(create)


if __name__ == "__main__":
    _main()
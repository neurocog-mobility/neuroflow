import os
import yaml
import click

from IPython import get_ipython
from neuroflow.utils.create_experiment import _create_experiment
from neuroflow.utils.collect import _copy_notebook_templates
from neuroflow.definitions import _define_catalog
from neuroflow.catalog.inputs.input_registry import _register_inputs, _get_input_registry
from neuroflow.catalog.inputs.intermediate_registry import _register_intermed, _get_inter_registry
from neuroflow.catalog.outputs.output_registry import _register_outputs, _get_output_registry
from neuroflow.catalog.parameters.param_registry import _register_params, _get_param_registry
from neuroflow.utils.utils import _format_text
import numpy as np
from IPython.display import clear_output
import shutil

ipython = get_ipython()

def initialize_catalogs(pipeline_name, project_root, neuroflow_root):
    """
    
    :meta private:
    
    """
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
    """
    
    :meta private:
    
    """
    clear_output(wait=False)
    input_registry = _register_inputs(pipeline_name, project_root)
    output_registry = _register_outputs(pipeline_name, project_root)
    inter_registry = _register_intermed(pipeline_name)
    
    clear_output(wait=False)
    param_registry = _register_params(pipeline_name, input_registry)
    
    clear_output(wait=False)
    print(_format_text("\n~~~ Creating catalogs ~~~", bold=True, underline=True))
    catalog_data, catalog_params = _define_catalog(input_registry, inter_registry, output_registry, param_registry)

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
    """
    
    :meta private:
    
    """
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

    :meta private:

    """ 
    # RESET+UPDATE CATALOG & PARAMETERS
    inputs = _get_input_registry()
    outputs = _get_output_registry()
    intermeds = _get_inter_registry()
    params = _get_param_registry()

    catalog_inputs = {str(key): info["catalog"] for key, info in inputs.items()}
    catalog_outputs = {str(key): info["catalog"] for key, info in outputs.items()}
    catalog_intermed = {str(key): info["catalog"] for key, info in intermeds.items()}
    catalog_data = {**catalog_inputs, **catalog_outputs, **catalog_intermed}
    catalog_params = {str(key): info["catalog"] for key, info in params.items()}
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

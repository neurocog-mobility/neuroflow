from neuroflow.catalog.parameters.param_registry import _register_params
from neuroflow.definitions import _define_parameter_catalog
from neuroflow.utils.setup import update_parameter_catalog
from IPython import get_ipython
import os
import yaml
import shutil
from pathlib import Path

def app_register_params(project_root, neuroflow_root, pipeline_name):
    param_registry = _register_params(pipeline_name, neuroflow_root)

    # create parameter catalog
    catalog_params = _define_parameter_catalog(param_registry)

    # write local catalog to project
    config_path = os.path.join(project_root, "catalogs", pipeline_name)
    os.makedirs(config_path, exist_ok=True)

    catalog_path = os.path.join(config_path, "parameters.yml")
    
    with open(catalog_path, 'w') as catalogfile:
        yaml.dump(catalog_params, catalogfile, default_flow_style=False)

    # write neuroflow catalog
    update_parameter_catalog(neuroflow_root, catalog_params)

    get_ipython().user_ns["param_registry"] = param_registry


def register_params(project_root, neuroflow_root, pipeline_name):
    # check if catalog exists in project
    config_path = os.path.join(project_root, "catalogs", pipeline_name)
    param_path = os.path.join(config_path, "parameters.yml")

    if Path(param_path).is_file():
        print(f"A parameter catalog for the {pipeline_name} pipeline already exists.")
        is_overwrite = input("Would you like to overwrite the parameter catalog? (y/n) [n]: ") or "n"
    else:
        is_overwrite = "y"

    if is_overwrite == "y":
        app_register_params(project_root, neuroflow_root, pipeline_name)
    else:
        # copy local catalog to neuroflow
        shutil.copyfile(
            os.path.join(config_path, "parameters.yml"),
            os.path.join(neuroflow_root, "conf", "base", "parameters.yml")
        )
        get_ipython().run_line_magic("reload_kedro", f"{neuroflow_root}")
        print("Reloaded parameter catalog.")
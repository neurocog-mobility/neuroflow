def _define_filepattern():
    return {
        "site": "[site]",
        "subject": "[subject]",
        "session": "[session]",
        "trial": "[trial]",
        "sensor": "[sensor]",
    }


def _define_catalog(input_registry, inter_registry, output_registry, param_registry):
    catalog_inputs = {}
    for key, value in input_registry.items():
        catalog_inputs[key] = value["catalog"]
    catalog_inter = {}
    for key, value in inter_registry.items():
        catalog_inter[key] = value["catalog"]
    catalog_outputs = {}
    for key, value in output_registry.items():
        catalog_outputs[key] = value["catalog"]
    catalog_data = {**catalog_inputs, **catalog_inter, **catalog_outputs}
    
    catalog_params = {}
    for key, value in param_registry.items():
        catalog_params[key] = value["catalog"]

    return catalog_data, catalog_params


def _define_data_catalog(input_registry, inter_registry, output_registry):
    catalog_inputs = {}
    for key, value in input_registry.items():
        catalog_inputs[key] = value["catalog"]
    catalog_inter = {}
    for key, value in inter_registry.items():
        catalog_inter[key] = value["catalog"]
    catalog_outputs = {}
    for key, value in output_registry.items():
        catalog_outputs[key] = value["catalog"]
    catalog_data = {**catalog_inputs, **catalog_inter, **catalog_outputs}

    return catalog_data


def _define_parameter_catalog(param_registry):
    catalog_params = {}
    for key, value in param_registry.items():
        catalog_params[key] = value["catalog"]

    return catalog_params

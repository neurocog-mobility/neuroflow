def define_filepattern():
    return {
        "site": "[site]",
        "subject": "[subject]",
        "session": "[session]",
        "trial": "[trial]",
        "sensor": "[sensor]",
    }


def define_catalog(input_registry, output_registry, param_registry):
    catalog_inputs = {}
    for key, value in input_registry.items():
        catalog_inputs[key] = value["catalog"]
    catalog_outputs = {}
    for key, value in output_registry.items():
        catalog_outputs[key] = value["catalog"]
    catalog_data = {**catalog_inputs, **catalog_outputs}
    
    catalog_params = {}
    for key, value in param_registry.items():
        catalog_params[key] = value["catalog"]

    return catalog_data, catalog_params
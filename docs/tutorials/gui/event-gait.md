# ```gait```

The ```gait``` command allows you to run gait event detectors (see [available gait modules](../../analysis.md#gait) for details).

In the GUI, selecting the ```gait``` command in the left-hand panel produces this screen:

![event-gait-gui](static/event-gait.png)

Here:

-  ```file_data```: Launches a file browser where you should select a standardized NeuroFlow .CSV file to run gait event detection on.
- ```detector```: Select the detector from the dropdown.
- ```detector_params```: Enter any custom parameters (see the parameters listed under each [detector](../../analysis.md#gait) for reference) as a dictionary-like string ({"parameter_one": value_one, "parameter_two": value_two, ...})
    - For example:

![detector-params](static/detector-params.png)

- ```savefile```: Browse/enter the filepath for the exported .CSV file. If left blank, the exported .CSV file will be automatically named and placed in the same folder as the source file.

## Example

Download the sample standardized Axivity .CSV data here: [data-gait.zip](static/data-gait.zip)

In the GUI window:

1. Under ```file_data``` select the extracted *sub-01_ses-01_neuroflow-axivity.csv* file.
3. Select *nimbalwear-ankles* from the ```detector``` dropdown.
5. Set ```savefile``` or leave blank for default export path.
6. Click ```Run``` in the right-hand panel to export a .CSV file with gait data appended to the source data.

!!! note "Tip"
    Try re-running the above steps but with a different ```detector``` or with custom ```detector_params``` (e.g. {"pushoff_threshold": 0.95}). Use the [```validate```](event-validate.md) command to inspect differences in the event detection.
# Tutorials

This section provides hands-on, step-by-step guides to help you learn how to use NeuroFlow in your own projects.

These tutorials cover the various functions within the GUI, each with sample data provided.

Beyond the functions built in to the GUI, you can always create custom analysis scripts incorporating the data loaders, event detectors, or feature extraction modules by using:
```
from neuroflow import ...
```
See the [API reference](../api.md) for more details.


## NeuroFlow GUI
### Pre-process
- [```convert```](gui/pre-convert.md): Convert raw files to a standardized .CSV
- [```sync```](gui/pre-sync.md): Use event sync timestamps to split continuous data recordings.
- [```window```](gui/pre-window.md): Use a reference timestamp to extract windows of data.
### Event detection
- [```gait```](gui/event-gait.md): Run gait event detectors.
- [```ecg```](gui/event-ecg.md): Run ECG event detectors.
- [```validate```](gui/event-validate.md): Launch the data validation interface.
### Feature extraction
- [```metrics```](gui/feature-metrics.md): Produce summary metrics.
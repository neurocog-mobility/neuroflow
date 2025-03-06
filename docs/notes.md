1. Run: rm ./source/*
2. Run: sphinx-apidoc --module-first --no-headings --no-toc -d 1 -o source ../src/neuroflow
3. Run: make clean && make html



#### SETUP
1. Python
    1. Download [COMPLETE]
    2. Install [COMPLETE]

2. NeuroFlow
    1. Download [COMPLETE]
    2. Install
        - navigate to root folder
        - open in terminal
        - "pip -vvv install -e ." (wait, it could take long for fresh Python installation)
        - test "python -m neuroflow --help"
    3. Complete setup
        1. Create NeuroFlow kernel: "kedro jupyter notebook"
        2. [OPTIONAL] Associate .ipynb files with Jupyter
            - "pip install nbopen"
            - "python -m nbopen.install_win"
            * otherwise give instructions for how to run Jupyter notebooks: "jupyter notebook neuroflow_template.ipynb"
            
1. Go to git/downloads
2. download for your system
3. Install with administrator privileges
4. Leave defaults, install and exit


TUTORIAL:

1. Download and extract data (note folder location)
2. Open a terminal in the location you want your project folder to be created.
3. Enter command: python -m neuroflow --create tutorial_pipeline
4. Success message then close terminal.
5. Open the created project folder.
6. Open the neuroflow_project.ipynb file.
7. POINT TO JUPYTER HELP FOR BASICS

1. Run the "Load" cell by selecting the cell and pressing Ctrl-Enter. Wait for loaded successfully prompt.
2. Run the "Select pipeline" cell. Wait until an "Open Kedro-Viz" link appears.
    3 parts:
    1. Select a processing pipeline from the dropdown
    2. Use Kedro Viz link to view an interactive map of each processing pipeline --> SEPARATE PAGE FOR HOW TO USE
    3. Select "Process step data" from the dropdown and click the "Set pipeline" button

3. Run "Data" cell
    1. For each required input dataset, click the "Select folder" button and select the folder that contains all the files for that dataset.
    2. Once all the folders are selected (i.e. green), click the "register inputs" button. Wait for success.

    Explain what happens at the end in terms of data collection.

4. Run "Parameters" cell
The program will now prompt you for setting the values of each listed parameter (in this case...)
Parameters can be:
    1. filepatterns: what the different parts in the filename correspond to (e.g. trial, subject, ...)
    2. parameter-value pairs: values to be set for a specific parameter (e.g. filter frequency, step length, ...)

Setting filepatterns:
The filepattern key gives 5 possible information types to be extracted from the filename (0: misc refers to anything other than options 1-5)
1. Set the filepattern for the Axivity dataset. An example filename from the data is displayed as: ____
2. The program will prompt you for the key corresponding to the highlighted information in the filename: NAPS
Sicne this is just a project name, we can enter 0 (for "miscellaneous") into the prompt and hit Enter
3. The next bit of filename information is now prompted: UW
This corresponds to the site, so we'll enter 1 into the prompt.
4. Continuing through the rest of the filename:
001: This is the subject code, so enter 2
Visit#01: This is the visit number, so enter 3
AXV6: This is the capture device, so enter 0
leftankle: This is the sensor location, so enter 5

The list of parameters now shows green for axivitiy and now highlights synx_filepattern.
Similar to above ...

The last parameter should now be highlighted (step parameters)
This is of the "parameter-value" format, and the default values are displayed for review.
To accept the default values, you can enter y into the prompt.
If you choose to override the default values, the program will prompt you to enter new values for each parameter.

You should now get a "Paramter registration successful".

Run pipeline cell, and watch progress. Will show # of tasks completed and a "Pipeline execution completed successfully" when fully done.

To see the pipeline outputs, go back to your project folder. Under data/processed you should now have "output_axivity_stepdata" and "output_axivity_stepplots"
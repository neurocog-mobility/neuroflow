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

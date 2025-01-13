from neuroflow.utils import create_experiment, collect
import os

def main():
    experiment_dir = "~/Documents/data/neurocog-lab/neuroflow-test"
    create_experiment._create_experiment(experiment_dir)
    collect._collect("~/Documents/data/neurocog-lab/fogcoa_mock/axivity_data",
                     experiment_dir,
                     "*ankle*.cwa",
                     "axivity",
                     expand=True)

if __name__ == "__main__":
    main()


#%%
# from neuroflow.pipelines.pipes.pipeline
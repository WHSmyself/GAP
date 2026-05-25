# -*- coding: utf-8 -*-
"""
Visible Optuna tuning entry point for the compiled GxE model.

Run this file directly after editing DEFAULT_ARGS below:
    python tune_params.py

The best hyperparameters will be written to best_params.json by default. Use the
saved JSON in run_train.py through --load_params best_params.json.
"""
import sys

DEFAULT_ARGS = {
    # Data directory. Graph raw files are expected under <root>/raw/.
    "--root": "/root/autodl-tmp/GAT/Maize/data/",
    "--env_file": "/root/autodl-tmp/GAT/Maize/data/raw/env.txt",
    "--pheno_file": "/root/autodl-tmp/GAT/Maize/data/raw/pheno.txt",

    # Graph raw file names.
    "--a_file": "Maize_A.txt",
    "--edge_attr_file": "Maize_edge_attributes.txt",
    "--node_attr_file": "Maize_node_attributes.txt",
    "--sample_id_file": "sample_id.txt",
    "--node_per_graph": "2473",
    "--processed_file": "data.pt",
    "--force_reprocess": True,

    # Prediction task used for tuning.
    "--trait": "Yield",
    "--split_mode": "env",
    "--test_env": "DEH1_2016",

    # Basic runtime settings for tuning.
    "--batch_size": "128",
    "--k_folds": "10",
    "--seed": "123",

    # Optuna settings.
    "--optuna": True,
    "--tune_only": True,
    "--optuna_trials": "50",
    "--optuna_epochs": "20",
    "--optuna_out": "best_params.json",
}

def dict_to_argv(arg_dict):
    argv = []
    for key, value in arg_dict.items():
        if isinstance(value, bool):
            if value:
                argv.append(key)
        elif value is None:
            continue
        else:
            argv.extend([key, str(value)])
    return argv

def main():
    import train_test
    default_argv = dict_to_argv(DEFAULT_ARGS)
    user_argv = sys.argv[1:]
    sys.argv = [sys.argv[0]] + default_argv + user_argv
    print("[INFO] Running Optuna tuning with arguments:")
    print(" ".join(sys.argv))
    train_test.main()

if __name__ == "__main__":
    main()

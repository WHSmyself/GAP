# G×E Graph Neural Network Model User Guide

This repository provides a compiled Linux release of a G×E graph neural network model for phenotype prediction.  
The model integrates genotype graph information and environment features to predict target traits such as yield.

---

## 1. Quick installation

This release was prepared for **Linux x86_64** with **Python 3.11** compiled extension modules.  
The compiled files should look like:

```text
data_loader.cpython-311-x86_64-linux-gnu.so
model.cpython-311-x86_64-linux-gnu.so
train_test.cpython-311-x86_64-linux-gnu.so
utils.cpython-311-x86_64-linux-gnu.so
```

The `cpython-311` part means that the modules should be used with Python 3.11.

### Recommended installation with conda

```bash
conda env create -f environment.yml
conda activate gap
python check_env.py
```

### Alternative installation with pip

```bash
conda create -n gap python=3.11 pip -y
conda activate gap
pip install -r requirements.txt
python check_env.py
```

If `check_env.py` finishes with:

```text
Compiled modules import OK.
```

the environment and compiled modules are ready to use.

---

## 2. Recommended folder structure

A typical release folder should be organized as follows:

```text
GAP/
├── environment.yml
├── requirements.txt
├── check_env.py
├── README.md
├── run_train.py
├── tune_params.py
├── data_loader.cpython-311-x86_64-linux-gnu.so
├── model.cpython-311-x86_64-linux-gnu.so
├── train_test.cpython-311-x86_64-linux-gnu.so
├── utils.cpython-311-x86_64-linux-gnu.so
└── data/
    ├── raw/
    │   ├── Maize_A.txt
    │   ├── Maize_edge_attributes.txt
    │   ├── Maize_node_attributes.txt
    │   ├── sample_id.txt
    │   ├── env.txt
    │   └── pheno.txt
    └── processed/
```

If the `processed/` folder does not exist, create it:

```bash
mkdir -p /path/to/data/processed
```

The model uses six main input files:

```text
Maize_A.txt
Maize_edge_attributes.txt
Maize_node_attributes.txt
sample_id.txt
env.txt
pheno.txt
```

---

## 3. Genotype graph files

### 3.1 `Maize_A.txt`

This file defines edges between SNP or marker nodes.

Example:

```text
1 2
1 5
2 10
3 12
```

Requirements:

```text
No header
Two columns
Whitespace-separated
Node indices start from 1
The maximum node index must be no larger than node_per_graph
```

---

### 3.2 `Maize_edge_attributes.txt`

This file stores edge attributes, such as LD values.

Example:

```text
0.82
0.64
0.91
0.55
```

Requirements:

```text
No header
One or more numeric columns
The number of rows must match Maize_A.txt
The row order must match Maize_A.txt
```

---

### 3.3 `Maize_node_attributes.txt`

This file stores node features for all genotype samples.

If there are:

```text
N samples
M nodes per sample graph
F node features
```

then `Maize_node_attributes.txt` must have:

```text
N × M rows
F columns
```

The row order should be:

```text
sample_1_node_1
sample_1_node_2
...
sample_1_node_M
sample_2_node_1
...
sample_N_node_M
```

Typical node features include:

```text
normalized SNP position
chromosome one-hot encoding
genotype value
other marker-level features
```

All values must be numeric. No header is needed.

---

### 3.4 `sample_id.txt`

This file stores sample IDs.

Example:

```text
Hybrid_001
Hybrid_002
Hybrid_003
```

Requirements:

```text
One sample ID per line
No header
The order must match the sample blocks in Maize_node_attributes.txt
Sample IDs must match the Sample column in pheno.txt
```

---

## 4. Preparing genotype graph input

Users should convert raw genotype data into four graph input files:

```text
Maize_A.txt
Maize_edge_attributes.txt
Maize_node_attributes.txt
sample_id.txt
```

A typical workflow is:

```text
1. Use SNP annotation data to assign each SNP a node index.
2. Use LD or another marker relationship to construct graph edges.
3. Save edge pairs as Maize_A.txt.
4. Save edge weights or LD values as Maize_edge_attributes.txt.
5. Build node-level features, such as genomic position and chromosome encoding.
6. Add genotype values as sample-specific node features.
7. Stack all samples in the same order as sample_id.txt.
8. Save the final node-feature matrix as Maize_node_attributes.txt.
```

Important distinction:

```text
number of samples:
  number of genotype lines or hybrids

node_per_graph:
  number of SNP or marker nodes in each sample graph
```

---

## 5. Environment feature file: `env.txt`

The model requires one row per environment.

Example:

```text
Env GDD_1_1 GDD_7_1 PTI_10_5 VPD_30_20
DEH1_2015 6.23 7.11 105.42 1.21
DEH2_2015 5.91 6.88 98.75 1.10
```

Requirements:

```text
Must contain an Env column
One row per environment
All feature columns should be numeric
Env values must match the Env column in pheno.txt
```

### Preparing `env.txt` from daily environmental data

If users start from daily environmental data, they should first aggregate daily records into environment-level features.

Daily environmental data usually contains:

```text
Env
Date
daily temperature variables
daily precipitation variables
daily humidity variables
other daily environmental or crop-weather variables
```

Example:

```text
Env       Date      RH2M    T2M_MAX   T2M_MIN   PRECTOTCORR
DEH1_2015 20150415  75.00   16.03     9.23      0.28
DEH1_2015 20150416  75.00   19.06     7.72      0.01
DEH1_2015 20150417  88.94   22.12     11.17     3.04
```

Recommended workflow:

```text
1. Match each environment with its growth-period start date, such as planting date.
2. Extract daily environmental records within the target growth period, such as the first 100 days after planting.
3. Calculate daily environmental or crop-weather indicators.
4. Use sliding windows to aggregate daily indicators into fixed-length environment-level features.
5. Save the final table as env.txt.
```

The final `env.txt` must be:

```text
Env feature_1 feature_2 feature_3 ...
```

The sliding-window step converts daily time-series environmental data into fixed-length features that can be used by the model.

---

## 6. Phenotype file: `pheno.txt`

The phenotype file stores phenotype records.

Example:

```text
Sample Env Yield PH
Hybrid_001 DEH1_2016 8.52 185.3
Hybrid_002 DEH1_2016 7.91 178.4
Hybrid_001 DEH2_2016 8.10 182.7
```

Requirements:

```text
Must contain a Sample column
Must contain an Env column
Must contain the target trait column, such as Yield
Sample values must match sample_id.txt
Env values must match env.txt
```

Rows with missing target trait, unmatched sample ID, or unmatched environment ID will be removed automatically.

---

## 7. Running the model

### 7.1 One-command run

If default paths and parameters in `run_train.py` are already correct:

```bash
python run_train.py
```

### 7.2 Full command example

```bash
python run_train.py \
  --root /root/autodl-tmp/GAT_Maize/data/ \
  --env_file /root/autodl-tmp/GAT_Maize/data/raw/env.txt \
  --pheno_file /root/autodl-tmp/GAT_Maize/data/raw/pheno.txt \
  --a_file Maize_A.txt \
  --edge_attr_file Maize_edge_attributes.txt \
  --node_attr_file Maize_node_attributes.txt \
  --sample_id_file sample_id.txt \
  --node_per_graph 2473 \
  --processed_file data.pt \
  --force_reprocess \
  --trait Yield \
  --split_mode env \
  --test_env DEH1_2016 \
  --save_pred Yield.csv
```

Recommended path rules:

```text
--root points to the data folder containing raw/ and processed/
--a_file, --edge_attr_file, --node_attr_file, and --sample_id_file are file names under root/raw/
--processed_file is usually a file name such as data.pt
--env_file and --pheno_file can be absolute paths
```

---

## 8. Main parameters

| Parameter | Description |
|---|---|
| `--root` | Data root folder containing `raw/` and `processed/` |
| `--env_file` | Environment feature file |
| `--pheno_file` | Phenotype file |
| `--a_file` | Graph edge file under `root/raw/` |
| `--edge_attr_file` | Edge attribute file under `root/raw/` |
| `--node_attr_file` | Node attribute file under `root/raw/` |
| `--sample_id_file` | Sample ID file under `root/raw/` |
| `--node_per_graph` | Number of SNP or marker nodes per sample graph |
| `--processed_file` | Cached graph file name |
| `--force_reprocess` | Rebuild graph cache from raw files |
| `--trait` | Target trait column in pheno.txt |
| `--split_mode` | Data split mode: `random` or `env` |
| `--test_env` | Held-out environment when `split_mode=env` |
| `--save_pred` | Output prediction file |
| `--k_folds` | Number of cross-validation folds |
| `--epochs` | Maximum training epochs |
| `--batch_size` | Batch size |
| `--pca_dim` | PCA dimension for environment features |

---

## 9. Split modes

### 9.1 Random cross-validation

```bash
python run_train.py \
  --split_mode random \
  --k_folds 10 \
  --trait Yield
```

This mode randomly splits all matched phenotype records into K folds.

### 9.2 Environment-held-out validation

```bash
python run_train.py \
  --split_mode env \
  --test_env DEH1_2016 \
  --trait Yield \
  --save_pred Yield.csv
```

This mode uses one environment as the held-out test environment.  
The remaining environments are used for K-fold training and validation.

---

## 10. Hyperparameter tuning

### 10.1 One-command tuning

If default paths and parameters in `tune_params.py` are already correct:

```bash
python tune_params.py
```

### 10.2 Full tuning command example

```bash
python tune_params.py \
  --root /root/autodl-tmp/GAT_Maize/data/ \
  --env_file /root/autodl-tmp/GAT_Maize/data/raw/env.txt \
  --pheno_file /root/autodl-tmp/GAT_Maize/data/raw/pheno.txt \
  --a_file Maize_A.txt \
  --edge_attr_file Maize_edge_attributes.txt \
  --node_attr_file Maize_node_attributes.txt \
  --sample_id_file sample_id.txt \
  --node_per_graph 2473 \
  --processed_file data.pt \
  --force_reprocess \
  --trait Yield \
  --split_mode env \
  --test_env DEH1_2016 \
  --optuna_trials 50 \
  --optuna_epochs 20 \
  --optuna_out best_params.json
```

The tuning result will be saved as:

```text
best_params.json
```

Train with tuned parameters:

```bash
python run_train.py --load_params best_params.json
```

---

## 11. Output files

For environment-held-out mode, common outputs include:

```text
Yield.csv
oof_Yield.csv
cv_fold_metrics.csv
cv_test_metrics.csv
fold_1/
fold_2/
...
```

Output meanings:

```text
Yield.csv:
  predictions on the held-out test environment

oof_Yield.csv:
  out-of-fold validation predictions

cv_fold_metrics.csv:
  validation metrics for each fold

cv_test_metrics.csv:
  test metrics for each fold

fold_i/best.pt:
  best model checkpoint for fold i

fold_i/env_imputer.joblib
fold_i/env_scaler.joblib
fold_i/env_pca.joblib:
  environment preprocessing objects for fold i
```

For random cross-validation mode, the main output is usually:

```text
fold_results.csv
```

---

## 12. Common issues

### 12.1 The graph cache is not updated

If graph files, node features, sample IDs, or `node_per_graph` are changed, use:

```bash
--force_reprocess
```

or delete the old cache manually:

```bash
rm -f /path/to/data/processed/data.pt
```

### 12.2 Incorrect `node_per_graph`

If this error appears:

```text
Total node rows cannot be divided by node_per_graph
```

check whether:

```text
number of rows in Maize_node_attributes.txt = number of samples × node_per_graph
```

If this error appears:

```text
Max node index in Maize_A.txt is larger than node_per_graph
```

increase `--node_per_graph` to match the real number of nodes per graph.

### 12.3 Sample IDs do not match

If many records are dropped because of missing genotypes, check whether the `Sample` column in `pheno.txt` exactly matches `sample_id.txt`.

### 12.4 Environment IDs do not match

If many records are dropped because of missing environments, check whether the `Env` column in `pheno.txt` exactly matches the `Env` column in `env.txt`.

### 12.5 OpenMP thread warning

If this warning appears:

```text
libgomp: Invalid value for environment variable OMP_NUM_THREADS
```

set:

```bash
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
export NUMEXPR_NUM_THREADS=4
```

Use the number of CPU cores allocated to the job.

---

## 13. Checklist before running

Before training, confirm:

```text
[ ] data/raw/Maize_A.txt exists.
[ ] data/raw/Maize_edge_attributes.txt exists.
[ ] data/raw/Maize_node_attributes.txt exists.
[ ] data/raw/sample_id.txt exists.
[ ] data/raw/env.txt exists.
[ ] data/raw/pheno.txt exists.
[ ] env.txt has one row per environment.
[ ] env.txt contains Env and numeric feature columns.
[ ] pheno.txt contains Sample, Env, and the target trait column.
[ ] node_per_graph equals the number of SNP or marker nodes in each sample graph.
[ ] sample_id.txt order matches sample blocks in Maize_node_attributes.txt.
[ ] processed/ folder exists.
[ ] --force_reprocess is used after changing graph input files.
```

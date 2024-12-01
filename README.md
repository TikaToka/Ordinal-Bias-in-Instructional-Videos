# [절차적 비디오 이해를 위한 행동 이해 태스크에서의 편향 탐구](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11705159)
Code for [Exploring bias in Action Understanding Task for Comprehending Instructional Videos](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11705159) (KSC 2023)

This repository only contains video modification and sample visualization code. Refer to each model repository for train and inference.

## Setup
`pip install numpy tqdm setuptools`

## Data
1. Download Features of 50salads, GTEA and Breakfast provided by [ASFormer](https://github.com/ChinaYi/ASFormer) and [MS-TCN](https://github.com/yabufarha/ms-tcn).
2. Unzip the data, rename it to "data" and put into the current directory

## Run
`python main.py --dataset {gtea/breakfast/50salads} --mode {blank/mask,all} --seed {seed} --name {name}`

## Evaluate (Visualize)
Use `visualize.ipynb` by changing directories in shell 2, and 3

## Output
./data_{name}

## Result
### Modification Example
![Modification](images/modification.png)
### Quantitative Result
![Quantitative](images/quantitative.png)
### Qualitative Result
![Qualitative](images/qualitative.png)

## Acknowledgement
Datasets
1. [GTEA](https://cbs.ic.gatech.edu/fpv/)
2. [50Salads](https://cvip.computing.dundee.ac.uk/datasets/foodpreparation/50salads/)
3. [Breakfast](https://serre-lab.clps.brown.edu/resource/breakfast-actions-dataset/)

Models
1. [ASFormer](https://github.com/ChinaYi/ASFormer)
2. [MS-TCN](https://github.com/yabufarha/ms-tcn)
3. [MS-TCN++](https://github.com/sj-li/MS-TCN2)
4. [DiffAct](https://github.com/Finspire13/DiffAct)

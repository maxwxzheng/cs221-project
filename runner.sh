#!/bin/bash

python feature_creator.py --verbose 2>&1 | tee logs/feature_creator.log
python scikit_kmeans_runner.py --clusters=10 2>&1 | tee logs/scikit_kmeans.log
python scikit_learn_runner.py --feature-file=data/features_k_means_10.json --save-regularization-stats 2>&1 | tee logs/scikit_runner.log
python sgd_runner.py --feature-file=data/features_k_means_10.json 2>&1 | tee logs/sgd_runner.log
python fann_data_generator.py --feature-file=data/features_k_means_10.json --postfix="-kmeans-10-pca" 2>&1 | tee logs/fann_data_gen.log
python fann.py 2>&1 | tee logs/fann.log

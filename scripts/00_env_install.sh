#!/bin/bash

conda create -n gsicpslam2 python==3.9
conda activate gsicpslam2
# conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 pytorch-cuda=12.1 -c pytorch -c nvidia
conda install pytorch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 pytorch-cuda=12.1 -c pytorch -c nvidia
pip install -r requirements.txt

pip install submodules/diff-gaussian-rasterization
pip install submodules/simple-knn

cd submodules/fast_gicp
rm -rf build
mkdir build
cd build
cmake ..
make
cd ..
python setup.py install --user
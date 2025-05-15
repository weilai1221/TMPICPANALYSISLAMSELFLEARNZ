<div align=center>

# RGBD GS-ICP SLAM (100FPS Gaussian Splatting SLAM)

[Seongbo Ha](https://riboha.github.io), [Jiung Yeon](https://humdrum-balance-b8f.notion.site/Jiung-Yeon-6754922a22814c9a95af88801a96fb4b), Hyeonwoo Yu



<h3 align="center"> ECCV 2024 </h3>

[Paper](https://arxiv.org/abs/2403.12550) | [Video](https://www.youtube.com/watch?v=e-bHh_uMMxE&t)

![github (1)](https://github.com/Lab-of-AI-and-Robotics/GS_ICP_SLAM/assets/34827206/5722e8f4-165d-4093-8064-a7ed5d9ea008)

</div>

This repository is intended to substantiate the results reported in the paper. Additional features including visualization tools will be updated soon!
---

This repository is a copy of the official implementation of the paper **"RGBD GS-ICP SLAM: Real-time RGBD SLAM with Gaussian Splatting"**. 

It is intended solely for self-learning purposes, to understand the details of the original implementation. 

For actual implementation and updates, please refer to the [original repository](https://github.com/Lab-of-AI-and-Robotics/GS_ICP_SLAM/tree/main).

## Environments
Install requirements
```bash
conda create -n gsicpslam python==3.9
conda activate gsicpslam
conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia
pip install -r requirements.txt
```
Also, PCL is needed for fast-gicp submodule.

Install submodules

```bash
conda activate gsicpslam
pip install submodules/diff-gaussian-rasterization
pip install submodules/simple-knn

cd submodules/fast_gicp
mkdir build
cd build
cmake ..
make
cd ..
python setup.py install --user
```


## Datasets

- Replica
  - Download
    ```bash
    bash download_replica.sh
    ```
  - Configure
  
    Please modify the directory structure to ours.

    The original structure
    ```bash
    Replica
        - room0
            - results (contain rgbd images)
                - frame000000.jpg
                - depth000000.jpg
                ...
            - traj.txt
        ...
    ```
    Our structure
    ```bash
    Replica
        - room0
            - images (contain rgb images)
                - frame000000.jpg
                ...
            - depth_images (contain depth images)
                - depth000000.jpg
                ...
            - traj.txt
        ...
    ```    

- TUM-RGBD
  - Download
    ```bash
        bash download_tum.sh
    ```

## Run
- Limited to 30 FPS
    ```bash
        # Replica
        bash replica.sh
        # TUM
        bash tum.sh
    ```

- Unlimited tracking speed
    ```bash
        # Replica
        bash replica_unlimit.sh
        # TUM
        bash tum_unlimit.sh
    ```

## Installing SIBR Viewer
```bash
cd SIBR_viewers
cmake -Bbuild . -DCMAKE_BUILD_TYPE=Release
cmake --build build -j24 --target install
```

## Real-time demo
### Using rerun.io viewer

Rerun viewer shows the means of trackable Gaussians, and rendered image from reconstructed 3dgs map.

![GIFMaker_me](https://github.com/Lab-of-AI-and-Robotics/GS_ICP_SLAM/assets/34827206/b4715071-2e4a-4d17-b7a2-612bbd32dbd0)

```bash
python -W ignore gs_icp_slam.py --rerun_viewer
```


### Using SIBR viewer
```bash
python -W ignore gs_icp_slam.py --dataset_path dataset/Replica/office0 --verbose

# In other terminal
cd SIBR_viewers
./install/bin/SIBR_remoteGaussian_app --rendering-size 1280 720
```

## Docker
Please see the README.md in the docker_files folder.

## Scripts
Above execution flows have been automated in the provided scripts. For detailed usage and customization, please refer to the `scripts` directory.


## Key Module Descriptions

- **mp_Mapper.py**:
    - Description: This module implements the mapping component of the SLAM system. It maintains and optimizes the 3D Gaussian Splatting representation of the environment.
    - Key responsibilities include:
        - Creating and updating 3D Gaussians from point clouds
        - Optimizing Gaussian parameters through training
        - Providing trackable Gaussians back to the Tracker
        - Calculating evaluation metrics
    - Usage(Import) in the Project: 
        - gs_icp_slam.py ```gs_icp_slam.py:17```
        - gs_icp_slam_unlimit.py ```gs_icp_slam_unlimit.py:17```
    
- **mp_Tracker.py**:
    - Description: This module implements the tracking component of the SLAM system. It estimates camera poses by aligning incoming RGB-D frames with the current map using Fast GICP.
    - Key responsibilities include:
        - Processing RGB-D images into point clouds
        - Estimating camera poses using Fast GICP
        - Keyframe selection based on overlap criteria
        - Sharing new point data with the Mapper
    - Usage(Import) in the Project: 
        - gs_icp_slam.py ```gs_icp_slam.py:16```

- **mp_Tracker_unlimit.py**:
    - Description: This is a variant of the tracker that removes performance throttling. It functions almost identically to mp_Tracker.py but eliminates the framerate limiting code, allowing the system to run at maximum speed.
    - Note: The main difference is that this version doesn't contain the delay loop that exists in mp_Tracker.py: ```mp_Tracker.py:265-266```
    - Usage(Import) in the Project: 
        - gs_icp_slam_unlimit.py ```gs_icp_slam_unlimit.py:16```


- **gaussian_renderer**:
    - Description: This module provides rendering functionality for 3D Gaussian scenes. It interfaces with the diff-gaussian-rasterization CUDA module for efficient rendering of 3D Gaussians to 2D images.
    - Key responsibilities include:
        - Rendering RGB and depth images from the Gaussian model
    - Note: The module provides three main rendering functions:
        - render() - Standard renderer
        - render_2() and render_3() - Variants that support different training stages with resolution adjustments
        - ```gaussian_renderer/__init__.py:114-120```
    - Usage(Import) in the Project: 
        - gs_icp_slam.py ```gs_icp_slam.py:15```
        - gs_icp_slam_unlimit.py ```gs_icp_slam_unlimit.py:15```
        - mp_Tracker.py ```mp_Tracker.py:16```
        - mp_Tracker_unlimit.py ```mp_Tracker_unlimit.py:17```

- **submodules/diff-gaussian-rasterization**:
    - Description: This is a CUDA-accelerated rasterization system for 3D Gaussians. It provides the core rendering capability of projecting 3D Gaussians to 2D images with proper blending and depth handling.
    - Note: The Python code interfaces with C++/CUDA code through a PyTorch extension for performance: ```setup.py:17-33```. For the detail of python and cuda implementation, please refer to the ```submodules/diff-gaussian-rasterization/diff-gaussian-rasterization/__init__.py```, ```submodules/diff-gaussian-rasterization/rasterize_points.cu```, directory ```submodules/diff-gaussian-rasterization/cuda_rasterizer```  and other related files.
    - Usage(Import) in the Project:
        - gaussian_renderer/__init__.py (imported as ```diff_gaussian_rasterization```) ```__init__.py:14```

- **submodules/fast_gicp**:
    - Description: This module implements Fast Generalized Iterative Closest Point algorithm, which is a variant of ICP that incorporates covariance information for more robust point cloud alignment.
    - Note: It's exposed to Python through the ```pygicp``` package: ```setup.py:107-115```
    - Usage(Import) in the Project:
        - mp_Tracker.py ```mp_Tracker.py:10```
        - mp_Tracker_unlimit.py ```mp_Tracker_unlimit.py:11```

- **submodules/simple-knn**:
    - Description: This is a CUDA-accelerated K-nearest neighbor search implementation. It provides efficient spatial queries for point clouds.
    - Note: Like the other C++/CUDA modules, it's exposed to Python through a PyTorch extension: ```setup.py:21-34```
    - Usage(Import) in the Project:
        - scene/gaussian_model.py (imported via ```simple_knn._C```) ```gaussian_model.py:20```


## Study Focus
In this study, we focus on acknowledging the implementation of ```gs_icp_slam_unlimit.py``` with how the ```mp_Mapper``` and ```mp_Tracker``` work, and their implementation details with python and CUDA.

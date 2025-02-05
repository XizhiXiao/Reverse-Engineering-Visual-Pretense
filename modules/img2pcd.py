import torch
import numpy as np
from diffusers import ShapEPipeline
from diffusers.utils import export_to_gif
import open3d as o3d
import os
import pandas as pd

data = pd.read_csv('exp1.csv')
real_objects = []

for index, row in data.iterrows():
    real_object1 = row['real_object1']
    real_object2 = row['real_object2']
    if real_object1 not in real_objects:
        real_objects.append(real_object1)
    if real_object2 not in real_objects:
        real_objects.append(real_object2)

print(len(real_objects))

for obj in real_objects:
    object_image_path = f"images_cropped/{obj}.jpg"
    command = f"python InstantMesh/run.py InstantMesh/configs/instant-mesh-large.yaml {object_image_path} --save_video"
    os.system(command)

for obj in real_objects:
    mesh = o3d.io.read_triangle_mesh(f'outputs/instant-mesh-large/meshes/{obj}.obj')
    pcd = o3d.geometry.PointCloud()
    pcd.points = mesh.vertices
    points = np.asarray(pcd.points)
    np.savetxt(f'outputs/instant-mesh-large/pcds/{obj}.pts', points, fmt='%.6f')

import torch
import numpy as np
import open3d as o3d
import os
import pandas as pd


def get_volume_points(mesh, spacing):
    min_bounds, max_bounds = mesh.bounds
    x_min, y_min, z_min = min_bounds
    x_max, y_max, z_max = max_bounds

    # Generate a grid of points within the bounding box
    x_vals = np.arange(x_min, x_max, spacing)
    y_vals = np.arange(y_min, y_max, spacing)
    z_vals = np.arange(z_min, z_max, spacing)

    grid_points = np.array(np.meshgrid(x_vals, y_vals, z_vals)).T.reshape(-1, 3)

    # Get the points that are inside the mesh
    volume_points = []
    for point in grid_points:
        if mesh.is_inside(point):
            volume_points.append(point)

    return volume_points


mesh_dir = '../../results/img2pcd/instant-mesh-large/meshes'
pcd_dir = '../../results/img2pcd/instant-mesh-large/pcds'

meshes = []
# for f in os.listdir(mesh_dir):
#     if f.endswith('.obj'):
#         meshes.append((f.split('.')[0], os.path.join(mesh_dir, f)))

meshes.append(('apple', '../../results/img2pcd/instant-mesh-large/meshes/apple.obj'))


for name, path in meshes:
    mesh = o3d.io.read_triangle_mesh(path)

    # normalize mesh
    mesh.apply_translation(-mesh.centroid)
    scale = max(mesh.bounds[1] - mesh.bounds[0])
    mesh.apply_scale(1.0 / scale)
    print("normalized")

    mesh_points, face_indices = mesh.sample(10000, return_index=True)

    volume_points = get_volume_points(mesh, 0.02)
    all_points = np.vstack([mesh_points, volume_points])

    print(f"{name}: mesh {len(mesh_points)} ,volumn {len(volume_points)}")

    with open(f"{pcd_dir}/{name}.pts", "w") as f:
        for point in all_points:
            f.write(f"{point[0]} {point[1]} {point[2]}\n")

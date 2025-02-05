import torch
import numpy as np
from diffusers import ShapEPipeline
from diffusers.utils import export_to_gif
import open3d as o3d
import os
import pandas as pd

pipe = ShapEPipeline.from_pretrained("openai/shap-e").to("cuda")
print("Shap-E model loaded successfully!")

data = pd.read_csv('exp_data/data4.csv')

os.makedirs('results/', exist_ok=True)

for index, row in data.iterrows():
    real_object1 = row['real_object1']
    real_object2 = row['real_object2']
    article_of_pretend_object = row['article_of_pretend_object']
    pretend_object = row['pretend_object']

    pcd_path = f'results/pcds/{pretend_object}'
    os.makedirs(pcd_path, exist_ok=True)

    meshes = pipe(
        prompt=f'{article_of_pretend_object} {pretend_object}',
        guidance_scale=15.0,
        num_inference_steps=512,
        frame_size=512,
        generator=torch.Generator("cuda").manual_seed(int(np.random.random() * 10000)),
        num_images_per_prompt=4,
        output_type="mesh",
    ).images

    for i, mesh in enumerate(meshes):
        vertices = mesh.__dict__['verts']
        print(f"{pretend_object}_{i+1}:", len(vertices))
        with open(f'{pcd_path}/{pretend_object}_{i+1}.pts', 'w') as file:
            for vertex in vertices:
                file.write(f"{vertex[0].item()} {vertex[1].item()} {vertex[2].item()}\n")

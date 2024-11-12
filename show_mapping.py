import open3d as o3d

def read_and_visualize_two_ply(file_path1, file_path2):

    point_cloud1 = o3d.io.read_point_cloud(file_path1)
    if point_cloud1.is_empty():
        print(f"Failed to read point cloud from {file_path1} or the file is empty.")
        return

    point_cloud2 = o3d.io.read_point_cloud(file_path2)
    if point_cloud2.is_empty():
        print(f"Failed to read point cloud from {file_path2} or the file is empty.")
        return

    vis1 = o3d.visualization.Visualizer()
    vis1.create_window(window_name="Point Cloud 1", width=800, height=600, left=50, top=50)
    vis1.add_geometry(point_cloud1)

    vis2 = o3d.visualization.Visualizer()
    vis2.create_window(window_name="Point Cloud 2", width=800, height=600, left=900, top=50)
    vis2.add_geometry(point_cloud2)

    while True:
        vis1.update_geometry(point_cloud1)
        if not vis1.poll_events():
            break
        vis1.update_renderer()

        vis2.update_geometry(point_cloud2)
        if not vis2.poll_events():
            break
        vis2.update_renderer()

    vis1.destroy_window()
    vis2.destroy_window()


# replace the file paths with the paths of the two point clouds you want to visualize

file_path1 = 'results/pcd_mapping/exp2_pretend-to-real/airplane_binoculars_eagle/airplane_eagle_1/airplane.ply'
file_path2 = 'results/pcd_mapping/exp2_pretend-to-real/airplane_binoculars_eagle/airplane_eagle_1/eagle_1.ply'
read_and_visualize_two_ply(file_path1, file_path2)

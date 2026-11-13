import trimesh
import numpy as np
import open3d as o3d
import os, sys

argv = sys.argv
argc = len(argv)

print('%s extracts point clound from glb' % argv[0])
print('[usage] python %s <glb>' % argv[0])

if argc < 2:
    quit()

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s.ply' % filename

scene = trimesh.load(argv[1])
for geometry_name, geometry in scene.geometry.items():
    if isinstance(geometry, trimesh.PointCloud):
        colors = geometry.visual.vertex_colors[:,:3]
        colors = colors.astype(np.float32) / 255.0
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(geometry.vertices)
        pcd.colors = o3d.utility.Vector3dVector(colors)
        o3d.io.write_point_cloud(dst_path, pcd)
        print('save %s' % dst_path)
        break
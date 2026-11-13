import cv2, glob, os, sys
import numpy as np
import open3d as o3d

def main():

    global obj, geo_type

    argv = sys.argv
    argc = len(argv)

    print('%s loads ply and visualizes 3d model' % argv[0])
    print('[usage] python %s <ply1> <ply2> .... ' % argv[0])
    print('[usage] python %s <wildcard for plys>' % argv[0])

    if argc < 2:
        quit()

    paths = None
    if argc == 2:
        paths = glob.glob(argv[1])
    else:
        paths = []
        for i in range(1, argc):
            paths.append(argv[i])

    # 可視化の設定
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()

    for p in paths:
        geo_type = o3d.io.read_file_geometry_type(p)
        print('geo_type:', geo_type)

        if geo_type == o3d.io.FileGeometry.CONTAINS_TRIANGLES:
            obj = o3d.io.read_triangle_mesh(p)
            obj.compute_vertex_normals()
        elif geo_type == o3d.io.FileGeometry.CONTAINS_LINES:
            obj = o3d.io.read_line_set(p)
        elif geo_type == o3d.io.FileGeometry.CONTAINS_POINTS:
            obj = o3d.io.read_point_cloud(p)
        else:
            print('unknown type ply')
            continue

        vis.add_geometry(obj)

    # 実行
    vis.run()

if __name__ == '__main__':
    main()

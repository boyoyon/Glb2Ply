import cv2, os, sys
import numpy as np
import open3d as o3d

def main():

    argv = sys.argv
    argc = len(argv)

    print('%s loads ply and visualizes 3d model' % argv[0])
    print('[usage] python %s <ply file>' % argv[0])

    if argc < 2:
        quit()

    pcd = o3d.io.read_point_cloud(argv[1])
    o3d.visualization.draw_geometries([pcd])

if __name__ == '__main__':
    main()

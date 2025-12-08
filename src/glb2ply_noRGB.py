import cv2, os, sys
import trimesh
import numpy as np

def save_ply(path_ply, vertices):

    nrVertices = 0

    for vertex in vertices:
        nrVertices += vertex.shape[0]

    with open(path_ply, mode='w') as f:

        line = 'ply\n'
        f.write(line)

        line = 'format ascii 1.0\n'
        f.write(line)

        line = 'element vertex %d\n' % nrVertices
        f.write(line)

        line = 'property float x\n'
        f.write(line)

        line = 'property float y\n'
        f.write(line)

        line = 'property float z\n'
        f.write(line)

        line = 'property uchar red\n'
        f.write(line)

        line = 'property uchar green\n'
        f.write(line)

        line = 'property uchar blue\n'
        f.write(line)

        line = 'end_header\n'
        f.write(line)

        for vertex in vertices:

            for i in range(vertex.shape[0]):

                x = vertex[i][0]
                y = vertex[i][1]
                z = vertex[i][2]

                b = 0
                g = 0
                r = 0

                line = '%f %f %f %d %d %d\n' % (x, y, z, r, g, b)
                f.write(line)

    f.close()          

def main():

    argv = sys.argv
    argc = len(argv)
    
    print('%s converts glb to ply' % argv[0])
    print('[usage] python %s <glb>]' % argv[0])
    
    if argc < 2:
        quit()

    base = os.path.basename(argv[1])
    filename = os.path.splitext(base)[0]
    dst_path = '%s_noRGB.ply' % filename
    
    # GLBファイルをシーンとして読み込む

    scene = trimesh.load(argv[1])
    
    print(scene)

    vertices = []
    
    for geometry_name, geometry in scene.geometry.items():
    
        vertices.append(geometry.vertices)
       
    save_ply(dst_path, vertices)
    print('save %s' % dst_path)

if __name__ == '__main__':
    main()

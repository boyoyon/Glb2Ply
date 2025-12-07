import cv2, os, sys
import trimesh
import numpy as np

skip = 100

#
# ピラミッドの頂点(5個)のindexを探す
#
# idx0: 頂点(-,    -,    zmax)
# idx1: 底辺(xmin, ymin, -   )
# idx2: 底辺(xmax, ymin, -   )
# idx3: 底辺(xmin, ymax, -   )
# idx4: 底辺(xmax, ymax, -   )
#

def find_indices_of_square_pyramid_vertices(points):

    xmin = np.min(points[:,0])
    xmax = np.max(points[:,0])
    ymin = np.min(points[:,1])
    ymax = np.max(points[:,1])

    idx0 = np.argmax(points[:,2])

    idx12 = []
    idx34 = []

    for i in range(5):

        if i == idx0:
            continue

        if points[i][1] == ymin:
            idx12.append(i)
        else:
            idx34.append(i)

    if points[idx12[0]][0] == xmin:
        idx1 = idx12[0]
        idx2 = idx12[1]
    else:
        idx1 = idx12[1]
        idx2 = idx12[0]

    if points[idx34[0]][0] == xmin:
        idx3 = idx34[0]
        idx4 = idx34[1]
    else:
        idx3 = idx34[1]
        idx4 = idx34[0]

    v1 = points[idx2] - points[idx1]
    v2 = points[idx3] - points[idx1]

    normal_vector = np.cross(v1, v2)
    A, B, C = normal_vector
    D = -np.dot(normal_vector, points[idx1])
    
    numerator = -(A * points[idx0][0] + B * points[idx0][1] + C * points[idx0][2] + D)

    return points[idx0], points[idx1], normal_vector, numerator, xmax - xmin, ymax - ymin

def find_pixelcoord(p, p0, p1, normal_vector, numerator, xscale, yscale):

    vdir = p - p0
    denominator = np.dot(normal_vector, vdir)

    t = numerator / denominator
    intersection = p0 + t * vdir - p1

    return intersection[0] / xscale, intersection[1] / yscale 


def extract_UVs_faces(vertices, img, p0, p1, normal_vector, numerator, xscale, yscale, zscale, skip):

    nrVertices0 = vertices[0].shape[0] # object
    H, W = img.shape[:2]

    idxmap = np.zeros((H,W), np.int32)

    UVs = []

    rect = (0, 0, W, H)
    point2d = []
    subdiv = cv2.Subdiv2D(rect)

    for i in range(0, nrVertices0, skip):

        x = vertices[0][i][0]
        y = vertices[0][i][1]
        z = vertices[0][i][2]

        p = np.array((x,y,z))

        px, py = find_pixelcoord(p, p0, p1, normal_vector, numerator, xscale, yscale)

        UVs.append((x,y,z * zscale, px, py))

        X = int(px * (W-1))
        Y = int(py * (H-1))

        subdiv.insert((X, Y))
        point2d.append((X, Y))

    triangles = subdiv.getTriangleList()

    faces = []

    for triangle in triangles:
        found = 0
        idx1 = -1
        idx2 = -1
        idx3 = -1

        for i in range(len(point2d)):
            if triangle[0] == point2d[i][0] and triangle[1] == point2d[i][1]:
                idx1 = i                    
                found += 1
            if triangle[2] == point2d[i][0] and triangle[3] == point2d[i][1]:
                idx2 = i                    
                found += 1
            if triangle[4] == point2d[i][0] and triangle[5] == point2d[i][1]:
                idx3 = i                    
                found += 1        

            if found == 3:
                faces.append((idx1, idx2, idx3))
                break

    return UVs, faces

def save_ply(path_ply, UVs, faces):

    with open(path_ply, mode='w') as f:

        line = 'ply\n'
        f.write(line)

        line = 'format ascii 1.0\n'
        f.write(line)

        line = 'element vertex %d\n' % len(UVs)
        f.write(line)

        line = 'property float x\n'
        f.write(line)

        line = 'property float y\n'
        f.write(line)

        line = 'property float z\n'
        f.write(line)

        line = 'property float s\n'
        f.write(line)

        line = 'property float t\n'
        f.write(line)

        line = 'element face %d\n' % len(faces)
        f.write(line)

        line = 'property list uchar int vertex_indices\n'
        f.write(line)

        line = 'end_header\n'
        f.write(line)

        for uv in UVs:

            line = '%f %f %f %f %f\n' % (uv[0], uv[1], uv[2], uv[3], uv[4])
            f.write(line)

        for face in faces:

            line = '3 %d %d %d\n' % (face[0], face[1], face[2])
            f.write(line)

    f.close()          

def main():

    global skip

    argv = sys.argv
    argc = len(argv)
    
    print('%s converts glb to ply' % argv[0])
    print('[usage] python %s <image> <glb> [<zSacle> <skip>]' % argv[0])
    
    if argc < 3:
        quit()
    
    # GLBファイルをシーンとして読み込む
    
    img = cv2.imread(argv[1])
    img = cv2.flip(img, 0)
    
    zscale = 1.0

    if argc > 3:
        zscale = float(argv[3])

    if argc > 4:
        skip = int(argv[4])
    
    scene = trimesh.load(argv[2])
    
    print(scene.geometry.items())
    
    vertices = []
    
    for geometry_name, geometry in scene.geometry.items():
    
        vertices.append(geometry.vertices)
    
    camera = np.unique(vertices[1], axis=0)
    
    p0, p1, normal_vector, numerator, xscale, yscale = find_indices_of_square_pyramid_vertices(camera)
    
    UVs, faces = extract_UVs_faces(vertices, img, p0, p1, normal_vector, numerator, xscale, yscale, zscale, skip)

    print('UVs:', len(UVs))
    print('faces:',len(faces))

    base = os.path.basename(argv[1])
    filename = os.path.splitext(base)[0]
    dst_path = '%s_glb2ply_denseUV.ply' % filename
    
    save_ply(dst_path, UVs, faces)
    print('save %s' % dst_path)

if __name__ == '__main__':
    main()

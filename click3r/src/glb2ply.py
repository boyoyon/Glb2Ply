import numpy as np
import open3d as o3d
import configparser
import cv2, sys

FLIP_FLAG = False
FLIP_MODE = 1

IMAGE_SWAP = False

def find_pyramid_apex(points):
    best_apex_idx = -1
    min_planarity_error = float('inf')

    # 5点のうち、i番目を「頂点候補」として除外し、残り4点の平面性を評価する
    for i in range(len(points)):
        # i番目を除いた4点を抽出
        base_candidates = np.delete(points, i, axis=0)
        
        # 4点の重心を引いて中心化
        centered = base_candidates - base_candidates.mean(axis=0)
        
        # 特異値分解 (SVD) を実行
        # 特異値 s の最小値 (s[2]) が、平面からのズレ（法線方向のばらつき）を表す
        _, s, _ = np.linalg.svd(centered)
        planarity_error = s[2]
        
        # 残り4点が最も綺麗に平面に乗る（ズレが最小になる）ときの i を記録
        if planarity_error < min_planarity_error:
            min_planarity_error = planarity_error
            best_apex_idx = i

    return best_apex_idx

import numpy as np


def intersect_plane_segment(p0, p1, p2, pA, pB):
    """
    3点(p0, p1, p2)が作る平面と、2点(pA, pB)が作る線分(または直線)の交点を求め、
    p0を原点、p1-p0をx軸、p2-p0をy軸とした2次元座標 (u, v) を返す。
    """
    # 基底ベクトルと方向ベクトル
    ex = p1 - p0
    ey = p2 - p0
    d = pA - pB
    b = pA - p0

    # 係数行列 A = [ex, ey, d] (各ベクトルを列として並べる)
    A = np.column_stack((ex, ey, d))

    try:
        # 連立方程式 A * [u, v, t]^T = b を解く
        u, v, t = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        # 行列が特異（直線と平面が平行、またはp0,p1,p2が一直線上）の場合
        return None

    if u < 0 or u >= 1 or v < 0 or v >= 1:
        return None

    return (u, v)

argv = sys.argv
argc = len(argv)

print('[usage] python %s <config file>' % argv[0])

if argc < 2:
    quit()

config = configparser.ConfigParser()
config.read(argv[1])

pcd_ply = config.get('PLYS',  'point_cloud')
pcd = o3d.io.read_point_cloud(pcd_ply)
points = np.asarray(pcd.points)
print(f'points:{points.shape}')
nr_points = points.shape[0]

frame1_ply = config.get('PLYS', 'frame1')
frame1_mesh = o3d.io.read_triangle_mesh(frame1_ply)
frame1 = np.asarray(frame1_mesh.vertices)
print(f'frame1:{frame1.shape}')

pyramid1_ply = config.get('PLYS', 'pyramid1')
pyramid1_mesh = o3d.io.read_triangle_mesh(pyramid1_ply)
pyramid1 = np.asarray(pyramid1_mesh.vertices[:5])
print(f'pyramid1:{pyramid1.shape}')

center1_idx = find_pyramid_apex(pyramid1)
print(f'center1:{pyramid1[center1_idx]}')

frame2_ply = config.get('PLYS', 'frame2')
frame2_mesh = o3d.io.read_triangle_mesh(frame2_ply)
frame2 = np.asarray(frame2_mesh.vertices)
print(f'frame2:{frame2.shape}')

pyramid2_ply = config.get('PLYS', 'pyramid2')
pyramid2_mesh = o3d.io.read_triangle_mesh(pyramid2_ply)
pyramid2 = np.asarray(pyramid2_mesh.vertices[:5])
print(f'pyramid2:{pyramid2.shape}')

center2_idx = find_pyramid_apex(pyramid2)
print(f'center2:{pyramid2[center2_idx]}')

if not IMAGE_SWAP:
    image1_path = config.get('IMAGES', 'image1')
    image1_mask_path = config.get('IMAGES', 'image1_mask')
    image2_path = config.get('IMAGES', 'image2')
    image2_mask_path = config.get('IMAGES', 'image2_mask')
else:
    image1_path = config.get('IMAGES', 'image2')
    image1_mask_path = config.get('IMAGES', 'image2_mask')
    image2_path = config.get('IMAGES', 'image1')
    image2_mask_path = config.get('IMAGES', 'image1_mask')

image1 = cv2.imread(image1_path)
image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
if FLIP_FLAG:
    image1 = cv2.flip(image1, FLIP_MODE)
image1 = image1.astype(np.float32) / 255.0

H1 = image1.shape[0]
W1 = image1.shape[1]

image1_mask = cv2.imread(image1_mask_path, cv2.IMREAD_GRAYSCALE)
h = image1_mask.shape[0]
w = image1_mask.shape[1]
if h != H1 or w != W1:
    print('dimension mismatch: %s(%d x %d) - %s(%d x %d)' % (image1_path, W1, H1, image1_mask_path, w, h))
    image1_mask = cv2.resize(image1_mask, (W1, H1))
if FLIP_FLAG:
    image1_mask = cv2.flip(image1_mask, FLIP_MODE)

image2 = cv2.imread(image2_path)
image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
if FLIP_FLAG:
    image2 = cv2.flip(image2, FLIP_MODE)
image2 = image2.astype(np.float32) / 255.0
H2 = image2.shape[0]
W2 = image2.shape[1]

image2_mask = cv2.imread(image2_mask_path, cv2.IMREAD_GRAYSCALE)
h = image2_mask.shape[0]
w = image2_mask.shape[1]
if h != H2 or w != W2:
    print('dimension mismatch: %s(%d x %d) - %s(%d x %d)' % (image2_path, W2, H2, image2_mask_path, w, h))
    image2_mask = cv2.resize(image2_mask, (W2, H2))

if FLIP_FLAG:
    image2_mask = cv2.flip(image2_mask, FLIP_MODE)

counts = np.zeros((nr_points), np.int32)
colors = np.zeros((nr_points, 3), np.float32)

step = nr_points // 10

print('Processing image1')
TH = step

p0 = frame1[3]
p1 = frame1[2]
p2 = frame1[0]
pA = pyramid1[center1_idx]

for i in range(nr_points):

    if i == TH:
        print('%d/%d' % (i, nr_points))
        TH += step

    p2d = intersect_plane_segment(p0, p1, p2, pA, points[i])

    if p2d is not None:
        x = int(p2d[0] * W1)
        y = int(p2d[1] * H1)

        if image1_mask[y][x] > 128:
            colors[i] = image1[y][x]
            counts[i] += 1

print('Processing image2')
TH = step

p0 = frame2[3]
p1 = frame2[2]
p2 = frame2[0]
pA = pyramid2[center2_idx]

for i in range(nr_points):

    if i == TH:
        print('%d/%d' % (i, nr_points))
        TH += step

    p2d = intersect_plane_segment(p0, p1, p2, pA, points[i])

    if p2d is not None:
        x = int(p2d[0] * W2)
        y = int(p2d[1] * H2)

        if image2_mask[y][x] > 128:
            colors[i] = image2[y][x]
            counts[i] += 1

np.save('colors.npy', colors)

print('Post processing')
TH = step

POINTS = []
COLORS = []

for i in range(nr_points):

    if i == TH:
        print('%d/%d' % (i, nr_points))
        TH += step

    cnt = counts[i]
    if cnt > 0:
        POINTS.append(points[i])
        color = colors[i] / cnt 
        COLORS.append(color)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(np.asarray(POINTS))
pcd.colors = o3d.utility.Vector3dVector(np.asarray(COLORS))

dst_path = 'glb2ply.ply'
o3d.io.write_point_cloud(dst_path, pcd)
print('save %s' % dst_path)


import numpy as np

#
# ピラミッドの頂点(5個)から頂点(1個)のindexを探す
#
def find_outlier_point(points):
    n_points = points.shape[0]
    for i in range(n_points):
        for j in range(i + 1, n_points):
            for k in range(j + 1, n_points):
                p1, p2, p3 = points[i], points[j], points[k]
                v1 = p2 - p1
                v2 = p3 - p1
                cross_prod = np.cross(v1, v2)
                if np.linalg.norm(cross_prod) < 1e-6:
                    continue
                normal_vector = cross_prod / np.linalg.norm(cross_prod)
                D = -np.dot(normal_vector, p1)
                coplanar_count = 0
                outlier_index = -1
                for l in range(n_points):
                    point_l = points[l]
                    distance = np.dot(normal_vector, point_l) + D
                    if np.abs(distance) < 1e-6:
                        coplanar_count += 1
                    else:
                        outlier_index = l
                if coplanar_count == 4:
                    return outlier_index
    return -1
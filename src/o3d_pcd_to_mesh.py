import sys
import numpy as np
import open3d as o3d

def main():

    argv = sys.argv
    argc = len(argv)

    if argc < 2:
        print('%s converts point cloud to mesh' % argv[0])
        print('[usage] python %s <pcd or ply> [<sample factor>]' % argv[0])
        quit()

    pcd = o3d.io.read_point_cloud(argv[1])

    sample_factor = 200
    
    if argc > 2:
        sample_factor = int(argv[2])

    points = np.asarray(pcd.points)
    sizeX = np.max(points[:,0]) - np.min(points[:,0])
    sizeY = np.max(points[:,1]) - np.min(points[:,1])
    sizeZ = np.max(points[:,2]) - np.min(points[:,2])

    voxel_size = np.max((sizeX, sizeY, sizeZ)) / sample_factor 

    downsampled = pcd.voxel_down_sample(voxel_size = voxel_size)

    downsampled.estimate_normals(
            search_param = o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

    downsampled.orient_normals_consistent_tangent_plane(10)

    distances = downsampled.compute_nearest_neighbor_distance()

    avg_dist = np.mean(distances)

    radius = 2 * avg_dist

    radii = [radius, radius * 2]

    recMeshBPA = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
            downsampled, o3d.utility.DoubleVector(radii))

    # 三角形のインデックスを取得して反転
    triangles = np.asarray(recMeshBPA.triangles)
    recMeshBPA.triangles = o3d.utility.Vector3iVector(triangles[:, ::-1])

    # 法線の再計算（推奨）
    recMeshBPA.compute_triangle_normals()
    recMeshBPA.compute_vertex_normals()

    o3d.io.write_triangle_mesh('o3d.ply', recMeshBPA)
    print('save o3d.ply')

    o3d.visualization.draw_geometries([recMeshBPA])

if __name__ == '__main__':
    main()

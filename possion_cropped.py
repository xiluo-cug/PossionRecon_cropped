import open3d as o3d
import numpy as np
# 加载初始点云
point_cloud = o3d.io.read_point_cloud("C:\\Users\\34066\\Desktop\\p_building2.ply")

# 加载泊松重建的三角网格
mesh = o3d.io.read_triangle_mesh("C:\\Users\\34066\\Desktop\\m_building2.ply")

# 计算点云的边界框（bbox）
bbox = point_cloud.get_axis_aligned_bounding_box()

# 获取bbox的最小和最大点坐标
min_bound = bbox.get_min_bound()
max_bound = bbox.get_max_bound()

# 获取三角网格的顶点坐标
mesh_vertices = np.asarray(mesh.vertices)

# 获取三角网格的面
mesh_triangles = np.asarray(mesh.triangles)

# 计算每个面的中心点，检查是否在bbox内，删除在bbox外的面
triangles_to_remove = []
for i, triangle in enumerate(mesh_triangles):
    v1_coords = mesh_vertices[triangle[0]]
    v2_coords = mesh_vertices[triangle[1]]
    v3_coords = mesh_vertices[triangle[2]]
    
    triangle_center = (v1_coords + v2_coords + v3_coords) / 3
    
    if (min_bound <= triangle_center).all() and (triangle_center <= max_bound).all():
        continue
    else:
        triangles_to_remove.append(i)

# 删除不在bbox内的面
mesh_triangles = np.delete(mesh_triangles, triangles_to_remove, axis=0)

# 删除不在bbox内的点
# 构建一个点索引集合，包含在bbox内的点的索引
valid_point_indices = set()
for i, triangle in enumerate(mesh_triangles):
    valid_point_indices.add(triangle[0])
    valid_point_indices.add(triangle[1])
    valid_point_indices.add(triangle[2])

# 从点云中删除不在bbox内的点
valid_point_cloud = o3d.geometry.PointCloud()
valid_point_cloud.points = o3d.utility.Vector3dVector(mesh_vertices[list(valid_point_indices)])

# 保存修改后的点云
o3d.io.write_point_cloud("C:\\Users\\34066\\Desktop\\filtered_point_cloud.ply", valid_point_cloud)

# 创建新的三角网格，只包含在bbox内的面
filtered_mesh = o3d.geometry.TriangleMesh()
filtered_mesh.vertices = o3d.utility.Vector3dVector(mesh_vertices)
filtered_mesh.triangles = o3d.utility.Vector3iVector(mesh_triangles)

# 保存修改后的三角网格
o3d.io.write_triangle_mesh("C:\\Users\\34066\\Desktop\\filtered_mesh.ply", filtered_mesh)

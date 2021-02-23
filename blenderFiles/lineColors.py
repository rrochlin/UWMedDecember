import bpy 
import csv
import pandas as pd


colorName = ["blue","cyan","green","yellow","orange","red"]
scale = [(0, 0, 1, 1), (0, 1, 1, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0.2, 0, 1), (1, 0, 0, 1)]
number_scales = 6
for i in range(number_scales):
    bpy.ops.mesh.primitive_uv_sphere_add(radius = 0.7, location=(15, 15, 15))
count = 0
for idx,obj in enumerate(bpy.context.visible_objects):
    obj.name = colorName[idx]
    current_mat = bpy.data.materials.new(name = colorName[idx])
    obj.data.materials.append(current_mat)
    current_mat.use_nodes = True
    current_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = scale[count]
    current_mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = scale[count]
    count += 1
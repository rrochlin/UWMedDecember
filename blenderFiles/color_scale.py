import bpy 


dp_name = ["dp0.3","dp0.5","dp1.0","dp2.5","dp5.0","dp10.0"]
scale = [(0, 0, 1, 1), (0, 1, 1, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0.2, 0, 1), (1, 0, 0, 1)]
number_scales = 6
for i in range(number_scales):
    bpy.ops.mesh.primitive_uv_sphere_add(radius = 0.7, location=(15, 15, 15))
count = 0
for obj in bpy.context.visible_objects:
    obj.name = dp_name[count]
    current_mat = bpy.data.materials.new(name = "color_scale")
    obj.data.materials.append(current_mat)
    current_mat.use_nodes = True
    current_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = scale[count]
    current_mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = scale[count]
    count += 1
    
obj = bpy.context.visible_objects
master_collection = bpy.context.scene.collection
new_coll = bpy.data.collections.new(name="Colors")
bpy.context.scene.collection.children.link(new_coll)
for ob in obj:
    new_coll.objects.link(ob)
    master_collection.objects.unlink(ob)
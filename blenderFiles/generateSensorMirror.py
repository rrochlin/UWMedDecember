import bpy

locationsOR7={
    'Size':[22,25],
    'S-01':[3,3,2],
    'S-02':[3,3,6],
    'S-03':[19,3,6],
    'S-04':[19,3,2],
    'S-05':[3,22,2],
    'S-06':[3,22,6],
    'S-07':[19,22,2],
    'S-08':[19,22,6],
    'S-09':[13,12.5,3.5],
    'S-10':[None,None,None],
    'S-11':[11,9.5,3.5],
    'S-12':[11,15.5,3.5],
    'S-13':[11,12.5,3.5],
    'S-14':[11,12.5,6.5],
    'S-15':[9.5,18.5,5],
    'S-BU1':[None,None,None],
    'S-BU2':[9,12.5,3.5]
    }

locationsOR16={
    'Size':[22,29],
    'S-01':[3,3,2],
    'S-02':[3,3,6],
    'S-03':[19,3,6],
    'S-04':[19,3,2],
    'S-05':[3,26,2],
    'S-06':[3,26,6],
    'S-07':[19,26,2],
    'S-08':[19,26,6],
    'S-09':[13,17.5,3.5],
    'S-10':[None,None,None],
    'S-11':[11,10.5,3.5],
    'S-12':[11,18.5,3.5],
    'S-13':[11,17.5,3.5],
    'S-14':[11,17.5,6.5],
    'S-15':[18,17.5,6.5],
    'S-BU1':[0,0,0],
    'S-BU2':[9,17.5,3.5]
    }

data = locationsOR7

label = [i for i in data if i not in ['Size','S-BU1','S-10']]

for i in label:
    b01 = bpy.ops.mesh.primitive_cube_add(size = 0.2, location=(data[i][1],-data[i][0]-1,data[i][2]))
    if i == 'S-15':
        bpy.context.active_object.name = 'Nursing Station Mirror'
    else:
        bpy.context.active_object.name = i
    
    
obj = bpy.context.visible_objects
master_collection = bpy.context.scene.collection
new_coll = bpy.data.collections.new(name="sensorsM")
bpy.context.scene.collection.children.link(new_coll)
for ob in obj:
    new_coll.objects.link(ob)
    master_collection.objects.unlink(ob)

current_mat = bpy.data.materials.new(name = "sensorDefault")
current_mat.use_nodes = True
current_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1,1,1,1)
current_mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1,1,1,1)
    
for obj in bpy.context.visible_objects:
    obj.data.materials.append(current_mat)


    
# still need to add a material
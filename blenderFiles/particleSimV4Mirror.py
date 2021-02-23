import bpy 
import csv
import pandas as pd
import os
import math

def particle_setting(obj, count, start, end, color):
    part = obj.modifiers.new("part", type='PARTICLE_SYSTEM')
    settings = part.particle_system.settings
    settings.particle_size = 0.1
    settings.effector_weights.gravity = 0
    settings.emit_from = 'VOLUME'
    settings.distribution = 'JIT'
    settings.jitter_factor = 0
    settings.distribution = 'GRID'
    settings.count = count
    settings.grid_resolution = count
    settings.grid_random = 0.65
    settings.frame_start = start
    settings.frame_end = start
    settings.render_type = 'OBJECT'
    settings.use_rotations = True
    settings.angular_velocity_factor = 1
    settings.instance_object = bpy.data.objects[color]
    settings.lifetime = 2
    settings.normal_factor = 1

def generate_sensor(expirement,localRoute,particles,colorLabel,collectionName,badSensors,sensors):

    filename = []

    badSensors.append('Size')
   
    sensorLoc = [i for i in sensors if i not in badSensors]

    for i in sensorLoc:

            b01 = bpy.ops.mesh.primitive_uv_sphere_add(
                radius = 1.4,
                location=(sensors[i][1],-sensors[i][0]-1,sensors[i][2])
                )
            if i == 'S-15':
                bpy.context.active_object.name = 'Nursing Station Mirror'
            else:
                bpy.context.active_object.name = i + 'Mirror'
                

    # put all sensor to new collections for partical generation
    obj = bpy.context.visible_objects
    master_collection = bpy.context.scene.collection
    new_coll = bpy.data.collections.new(name=collectionName)
    bpy.context.scene.collection.children.link(new_coll)

    for ob in obj:
        new_coll.objects.link(ob)
        master_collection.objects.unlink(ob)

    current_data = pd.read_csv(localRoute,parse_dates=[0])
    sensorNames = list(current_data.columns)
    
    for idx,obj in enumerate(new_coll.objects):

        obj.show_instancer_for_viewport = False
        obj.show_instancer_for_render = False

        f = 0
        increment = 2
        current = 0

        threshold = 3

        for v in current_data[sensorNames[idx]]:
            v = float(v)
            start = f
            end = f + increment
            if v < threshold:
                v = threshold
            newC = math.floor(math.log(v/threshold,3))
            if newC > 5:
                newC = 5
                    
            particle_setting(obj, math.log(v,2), start, end, colorLabel[newC])
            f = end

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
    'S-BU1':[0,0,0],
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

data = ['OR7 Unblocked','OR7 Blocked','OR16 Unblocked','OR16 Blocked 1','OR16 Blocked 2']


particle = "Dp>0.3"

colorLabel = ["dp0.3","dp0.5","dp1.0","dp2.5","dp5.0","dp10.0"]

badSensors = ['S-02','S-10']

index = 0
sensors = locationsOR7

expirement = data[index]

localRoute = os.path.join('C:/Users/Robert Rochlin/Documents/UW/covidDataProject/UWMedDecember/stretchedAvgData/'+ expirement +'.csv')

collectionName = expirement + 'Mirror'

generate_sensor(expirement,localRoute,particle,colorLabel,collectionName,badSensors,sensors)

bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.bloom_intensity = 0.5  

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
    settings.distribution = 'RAND'
    settings.count = count
    settings.grid_resolution = count
    settings.grid_random = 0.65
    settings.physics_type = 'FLUID'
    settings.frame_start = start
    settings.frame_end = end
    settings.render_type = 'OBJECT'
    settings.use_rotations = True
    settings.angular_velocity_factor = 1
    settings.instance_object = bpy.data.objects[color]
    settings.lifetime = 20
    settings.normal_factor = 1

def generate_sensor(data,localRoute,startTS,endTS,particles,colorLabel,collectionName,badSensors):
# def generate_sensor(x, y, z, num_sensor, file_pass, start_time, end_time, dp_size, color):
    filename = []

    badSensors.append('Size')
   
    sensors = [i for i in data if i not in badSensors]

    for i in label:

            b01 = bpy.ops.mesh.primitive_uv_sphere_add(
                radius = 1.4,
                location=(data[i])
                )
            if i == 'S-15':
                bpy.context.active_object.name = 'Nursing Station'
            else:
                bpy.context.active_object.name = i
                

    # put all sensor to new collections for partical generation
    obj = bpy.context.visible_objects
    master_collection = bpy.context.scene.collection
    new_coll = bpy.data.collections.new(name=collectionName)
    bpy.context.scene.collection.children.link(new_coll)

    for ob in obj:
        new_coll.objects.link(ob)
        master_collection.objects.unlink(ob)

    
    for idx,obj in enumerate(new_coll.objects):

        obj.show_instancer_for_viewport = False
        obj.show_instancer_for_render = False

        filename = os.path.join(localRoute[idx])
        current_data = pd.read_csv(filename,parse_dates=[0])

        time = current_data.iloc[:,0]
        start_time = pd.Timestamp(startTS)
        end_time = pd.Timestamp(endTS)


        for start,n in enumerate(time):
           if n >= start_time:
               break

        for end,n in enumerate(time):
            if n >= end_time:
                break
        
        dp = current_data[particles][start:end]

        f = 0
        increment = 20
        current = 0

        threshold = 2

        for v in dp:
            start = f
            end = f + increment
            if not v:
                newC = 0
            else:
                if v > threshold:
                    newC = math.floor(math.log2(v/threshold))
                    if newC > 5:
                        newC = 5
                else:
                    newC = 0
                    
            particle_setting(obj, v*2, start, end, colorLabel[newC])
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
    'S-12':[11,9.5,3.5],
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
    'S-BU1':[None,None,None],
    'S-BU2':[9,17.5,3.5]
    }

localRoute = []
data = locationsOR7
label = [i for i in data if i not in ['Size','S-02','S-BU1','S-10']]
for x in label:
    localRoute.append(os.path.join('C:/Users/Robert Rochlin/Documents/UW/covidDataProject/UWMedDecember/interpolatedData/',x+'.csv'))

#in order to find the data from certain time interval, covert time to number
startTS = '2020-12-22 12:59:00'
endTS = '2020-12-22 14:01:00'

particle = "Dp>0.3"

colorLabel = ["dp0.3","dp0.5","dp1.0","dp2.5","dp5.0","dp10.0"]

collectionName = 'First Expirement'

badSensors = ['S-02','S-BU1','S-10']

generate_sensor(data,localRoute,startTS,endTS,particle,colorLabel,collectionName,badSensors)

bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.bloom_intensity = 0.5  

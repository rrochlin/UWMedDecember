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
    settings.frame_start = start
    settings.frame_end = end
    settings.render_type = 'OBJECT'
    settings.physics_type = 'FLUID'
    settings.use_rotations = True
    settings.angular_velocity_factor = 1
    settings.instance_object = bpy.data.objects[color]
    settings.lifetime = 20
    settings.normal_factor = 1

def generate_sensor(expirement,localRoute,colorLabel):

    filename = []

    b01 = bpy.ops.mesh.primitive_uv_sphere_add(
        radius = 1.4,
        location=([0,0,0])
        )
    
    bpy.context.active_object.name = 'Sensor'
    obj = bpy.context.active_object
   
    current_data = pd.read_csv(localRoute,parse_dates=[0])
    

    obj.show_instancer_for_viewport = False
    obj.show_instancer_for_render = False

    f = 0
    increment = 20
    current = 0

    threshold = 2

    for v in current_data['Average']:
        v = float(v)
        start = f
        end = f + increment
        if not v:
            v = 1
        
        if v > threshold:
            newC = math.floor(math.log2(v/threshold))
            if newC > 5:
                newC = 5
        else:
            newC = 0
                
        particle_setting(obj, v*2, start, end, colorLabel[newC])
        f = end


data = ['OR7 Unblocked','OR7 Blocked','OR16 Unblocked','OR16 Blocked 1','OR16 Blocked 2']

colorLabel = ["dp0.3","dp0.5","dp1.0","dp2.5","dp5.0","dp10.0"]

index = 0

expirement = data[index]

localRoute = os.path.join('C:/Users/Robert Rochlin/Documents/UW/covidDataProject/UWMedDecember/averagedData/'+ expirement +'.csv')

generate_sensor(expirement,localRoute,colorLabel)

bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.bloom_intensity = 0.5  

import numpy as np
import bpy
import os
import pandas as pd
import math


data = ['OR7 Unblocked','OR7 Blocked','OR16 Unblocked','OR16 Blocked 1','OR16 Blocked 2']

index = 2

expirement = data[index]

localRoute = os.path.join('C:/Users/Robert Rochlin/Documents/UW/covidDataProject/UWMedDecember/stretchedAvgData/'+ expirement +'.csv')

current_data = pd.read_csv(localRoute,parse_dates=[0])

gridSize = len(current_data)

colorLabel = ["blue","cyan","green","yellow","orange","red"]

threshold = 3

x = np.linspace(230, -60, gridSize)
y = np.array(current_data['Average'])

master_collection = bpy.context.scene.collection
new_coll = bpy.data.collections.new(name='plot ' + data[index])
bpy.context.scene.collection.children.link(new_coll)

for i in range(gridSize):
    if y[i] < threshold:
        v = threshold
    else:
        v = y[i]
    bpy.ops.mesh.primitive_cube_add(location=(0,x[i]/30,math.log(v,threshold)/2))
    obj = bpy.context.active_object
    obj.scale= (.05,.05,.05)
    newC = math.floor(math.log(y[i]/threshold,3))
    if newC > 5:
        newC = 5
    newMaterial = bpy.data.materials[colorLabel[newC]]
    obj.data.materials.append(newMaterial)
    new_coll.objects.link(obj)
    master_collection.objects.unlink(obj)
     
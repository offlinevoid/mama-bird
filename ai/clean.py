import bpy, bmesh, mathutils
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath='/tmp/claude-0/-home-user-mama-bird/26288649-cbd8-5bf3-a79d-569a14699ba0/scratchpad/hy_raw.glb')
ob=[o for o in bpy.context.scene.objects if o.type=='MESH'][0]
bpy.context.view_layer.objects.active=ob; ob.select_set(True)
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.separate(type='LOOSE'); bpy.ops.object.mode_set(mode='OBJECT')
parts=[o for o in bpy.context.scene.objects if o.type=='MESH']
sizes=sorted(((len(o.data.polygons),o) for o in parts),key=lambda t:-t[0])
print('loose parts',[s for s,_ in sizes][:8],'total',len(sizes))
keep=[o for n,o in sizes if n>0.02*sizes[0][0]]
for o in parts:
    if o not in keep: bpy.data.objects.remove(o)
bpy.ops.object.select_all(action='DESELECT')
for o in keep: o.select_set(True)
bpy.context.view_layer.objects.active=keep[0]
if len(keep)>1: bpy.ops.object.join()
ob=bpy.context.view_layer.objects.active
# stand upright on z=0, scale to 150 mm tall (glTF is Y-up; the importer already made it Z-up)
bb=[ob.matrix_world@mathutils.Vector(c) for c in ob.bound_box]
h=max(p.z for p in bb)-min(p.z for p in bb); s=150/h
ob.scale=(s,s,s); bpy.ops.object.transform_apply(scale=True)
bb=[ob.matrix_world@mathutils.Vector(c) for c in ob.bound_box]
ob.location.z-=min(p.z for p in bb); bpy.ops.object.transform_apply(location=True)
print('kept',len(keep),'faces',len(ob.data.polygons))
bpy.ops.wm.stl_export(filepath='/tmp/claude-0/-home-user-mama-bird/26288649-cbd8-5bf3-a79d-569a14699ba0/scratchpad/mama_bird_ai_head.stl')

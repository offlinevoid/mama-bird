import bpy, bmesh
bpy.ops.wm.read_factory_settings(use_empty=True)
P='/tmp/claude-0/-home-user-mama-bird/26288649-cbd8-5bf3-a79d-569a14699ba0/scratchpad/'
bpy.ops.wm.stl_import(filepath=P+'mama_bird_ai_head_100k.stl')
ob=bpy.context.selected_objects[0]; bpy.context.view_layer.objects.active=ob
def stat():
    bm=bmesh.new(); bm.from_mesh(ob.data); r=(len(bm.faces),sum(1 for e in bm.edges if not e.is_manifold)); bm.free(); return r
print('start',stat())
for i in range(3):
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_mode(type='EDGE'); bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold(extend=False, use_wire=True, use_boundary=True, use_multi_face=True, use_non_contiguous=True, use_verts=False)
    bpy.ops.mesh.fill_holes(sides=16)
    bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT'); print('pass',i,stat())
    if stat()[1]==0: break
if stat()[1]:
    # last resort: delete the few offending faces and fill again
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.mesh.select_non_manifold(extend=False,use_multi_face=True,use_non_contiguous=True,use_verts=True)
    bpy.ops.mesh.delete(type='VERT'); bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.mesh.select_non_manifold(); bpy.ops.mesh.fill_holes(sides=64); bpy.ops.object.mode_set(mode='OBJECT'); print('last',stat())
bpy.ops.wm.stl_export(filepath=P+'mama_bird_ai_head_100k.stl')

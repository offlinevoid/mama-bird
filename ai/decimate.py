import bpy, bmesh
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath='/tmp/claude-0/-home-user-mama-bird/26288649-cbd8-5bf3-a79d-569a14699ba0/scratchpad/mama_bird_ai_head.stl')
ob=bpy.context.selected_objects[0]; bpy.context.view_layer.objects.active=ob
n0=len(ob.data.polygons)
# weld duplicate verts from STL, then collapse to ~100k triangles
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.remove_doubles(threshold=0.001); bpy.ops.object.mode_set(mode='OBJECT')
m=ob.modifiers.new('d','DECIMATE'); m.decimate_type='COLLAPSE'; m.ratio=100000/n0
bpy.ops.object.modifier_apply(modifier='d')
bm=bmesh.new(); bm.from_mesh(ob.data)
print('before',n0,'after',len(bm.faces),'verts',len(bm.verts),'nonmanifold edges',sum(1 for e in bm.edges if not e.is_manifold),'loose verts',sum(1 for v in bm.verts if not v.link_edges))
zs=[v.co.z for v in bm.verts]; print('height',round(max(zs)-min(zs),1),'minz',round(min(zs),2))
bpy.ops.wm.stl_export(filepath='/tmp/claude-0/-home-user-mama-bird/26288649-cbd8-5bf3-a79d-569a14699ba0/scratchpad/mama_bird_ai_head_100k.stl')

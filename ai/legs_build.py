import sys, bpy, bmesh, mathutils
sys.path.insert(0, '/home/user/mama-bird')
import sand3d as s3d, mama_bird as mb
P='/tmp/claude-0/-home-user-mama-bird/26288649-cbd8-5bf3-a79d-569a14699ba0/scratchpad/'
CUT=46; L=55            # the head is cut at z = CUT and stood on legs L tall
CX, CY = 5, -11         # centre of the head's underside (from the slice table)

legs=mb.chicken_legs(h=L+30, gap=34, d=10, toe_l=34, toe_w=9, toe_h=6, claws=False)
legs=[o for o in bpy.context.scene.objects if o.name=='shank'][0]
legs.location=(CX-17, CY+6, 0)    # the joined pair keeps its left leg at the origin: centre the pair on the head
bpy.context.view_layer.objects.active=legs; legs.select_set(True); bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)

for o in [o for o in bpy.context.scene.objects if o.name.startswith('Cube')]: bpy.data.objects.remove(o)
bpy.ops.wm.stl_import(filepath=P+'mama_bird_ai_head_100k.stl')
head=bpy.context.selected_objects[0]; head.name='head'

def box(name,x0,x1,y0,y1,z0,z1):
    bpy.ops.mesh.primitive_cube_add(); b=bpy.context.active_object; b.name=name
    b.scale=((x1-x0)/2,(y1-y0)/2,(z1-z0)/2); b.location=((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)
    bpy.ops.object.transform_apply(location=True,scale=True); return b
def bool_op(a,b,op):
    bpy.context.view_layer.objects.active=a; a.select_set(True)
    m=a.modifiers.new('b','BOOLEAN'); m.operation=op; m.object=b; m.solver='EXACT'
    bpy.ops.object.modifier_apply(modifier='b'); bpy.data.objects.remove(b)
def stat(o):
    bm=bmesh.new(); bm.from_mesh(o.data); r=(len(bm.faces),sum(1 for e in bm.edges if not e.is_manifold)); bm.free(); return r

# 2. keep only the head: drop the scarf below the chin and its collar around the jaw
import math
# one tilted box: its floor passes through the chin (y=-45, z=CUT) and rises toward the back of the head
bpy.ops.mesh.primitive_cube_add(); up=bpy.context.active_object; up.name='cutter_up'
up.scale=(55,100,125); up.location=(5,65,125); bpy.ops.object.transform_apply(location=True,scale=True)   # local y -35..165, z 0..250
up.rotation_euler=(math.radians(13.5),0,0); up.location=(0,-45,CUT)
bpy.ops.object.transform_apply(location=True,rotation=True)
print('cutter ready')
bool_op(head,up,'INTERSECT'); print('head after cut',stat(head))

# 3. stand it on the legs
head.location.z+=L-CUT; bpy.context.view_layer.objects.active=head; head.select_set(True); bpy.ops.object.transform_apply(location=True)
bool_op(head,legs,'UNION'); print('joined',stat(head))

# 4. clean small loose bits, fix leftover holes
bpy.ops.object.select_all(action='DESELECT'); head.select_set(True); bpy.context.view_layer.objects.active=head
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.separate(type='LOOSE'); bpy.ops.object.mode_set(mode='OBJECT')
parts=sorted([o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('head')],key=lambda o:-len(o.data.polygons))
print('loose parts',[len(o.data.polygons) for o in parts])
for o in parts[1:]: bpy.data.objects.remove(o)
final=parts[0]; print('final',stat(final))
zs=[v.co.z for v in final.data.vertices]; print('height',round(max(zs)-min(zs),1),'minz',round(min(zs),2))
bpy.ops.object.select_all(action='DESELECT'); final.select_set(True)
bpy.ops.wm.stl_export(filepath=P+'mama_bird_legs.stl',export_selected_objects=True)

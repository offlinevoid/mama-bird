import sys, math
sys.path.insert(0, '/home/user/mama-bird')
import bpy, mathutils
import mama_bird as m, sand3d as s3d
m.mama_bird()
sc = bpy.context.scene
for o in sc.objects:
    if o.type == 'MESH' and not o.data.materials:
        pass
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=24; sc.cycles.use_denoising=False
sc.render.resolution_x, sc.render.resolution_y = 600, 800
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True
sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.08, 0.09, 0.1, 1)
sc.world.node_tree.nodes['Background'].inputs[1].default_value = 0.6
for loc, e in (((-400, -500, 500), 3), ((400, -300, 200), 1.5)):
    l = bpy.data.lights.new('l', 'SUN'); l.energy = e * 1.5
    ob = bpy.data.objects.new('l', l); ob.location = loc; sc.collection.objects.link(ob)
    ob.rotation_euler = (mathutils.Vector((0, 0, 160)) - mathutils.Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
cam = bpy.data.objects.new('c', bpy.data.cameras.new('c')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = 400
for name, loc in (('front', (0, -900, 160)), ('side', (900, 0, 160))):
    cam.location = loc
    cam.rotation_euler = (mathutils.Vector((0, 0, 160)) - mathutils.Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = f'/tmp/claude-0/-home-user-mama-bird/26288649-cbd8-5bf3-a79d-569a14699ba0/scratchpad/{name}.png'
    bpy.ops.render.render(write_still=True)

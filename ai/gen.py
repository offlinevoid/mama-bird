import sys, shutil
from gradio_client import Client, handle_file
steps=int(sys.argv[1]); octree=int(sys.argv[2])
c=Client('tencent/Hunyuan3D-2mv')
r=c.predict(None, None,
    handle_file('views/front_rgba.png'), handle_file('views/back_rgba.png'),
    handle_file('views/left_rgba.png'), handle_file('views/right_rgba.png'),
    steps, 5.0, 1234, octree, False, 8000, False, api_name='/shape_generation')
print(r)
for i,f in enumerate(r[:1]):
    shutil.copy(f, f'out_{i}.glb'); print('saved', f)

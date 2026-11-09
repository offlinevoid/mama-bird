from PIL import Image
import numpy as np
U='/root/.claude/uploads/26288649-cbd8-5bf3-a79d-569a14699ba0/'
files={'top1':'edce7838','top2':'90af5b8a','left':'8149e1a5','back':'79876b21','right':'cafd7146','front':'58852fa2'}
for name,h in files.items():
    im=Image.open(U+h+'-image.png').convert('RGB'); a=np.asarray(im).astype(int)
    col=a[:,5,:].mean(axis=1)>15          # gray background rows at the left edge
    best=(0,0); s=None
    for i,v in enumerate(list(col)+[False]):
        if v and s is None: s=i
        if not v and s is not None:
            if i-s>best[1]-best[0]: best=(s,i)
            s=None
    box=(0,best[0],1160,best[1]); print(name,im.size,box)
    c=im.crop(box); side=max(c.size); sq=Image.new('RGB',(side,side),tuple(a[best[0]+5,5]))
    sq.paste(c,((side-c.width)//2,(side-c.height)//2)); sq.save(f'views/{name}.png')

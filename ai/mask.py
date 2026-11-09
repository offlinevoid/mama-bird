from PIL import Image
import numpy as np
from scipy import ndimage as ndi
for n in ('front','back','left','right'):
    a=np.asarray(Image.open(f'views/{n}.png').convert('RGB')).astype(float)
    lum=a.mean(axis=2)
    m=lum>85
    m=ndi.binary_closing(m,iterations=3); m=ndi.binary_fill_holes(m)
    lab,k=ndi.label(m); 
    if k>1:
        sizes=ndi.sum(m,lab,range(1,k+1)); m=np.isin(lab,[i+1 for i,s in enumerate(sizes) if s>0.02*m.sum()])
    alpha=(ndi.gaussian_filter(m.astype(float),1.0)*255).astype(np.uint8)
    rgba=np.dstack([a.astype(np.uint8),alpha]); 
    ys,xs=np.where(m); print(n,'fg frac',round(m.mean(),3),'bbox',xs.min(),xs.max(),ys.min(),ys.max())
    Image.fromarray(rgba,'RGBA').save(f'views/{n}_rgba.png')

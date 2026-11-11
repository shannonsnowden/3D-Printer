import numpy as np
from PIL import Image
a=np.array(Image.open('v5_unchanged_crops/v5_2_snowman.png').convert('RGB')).astype(float)
BG=np.array([192,180,120.]); DK=np.array([48,24,0.])
cx,cy,r=542.75,483.4,140.0
H,W=a.shape[:2]; yy,xx=np.mgrid[0:H,0:W]
dist=np.hypot(xx-cx,yy-cy)
box=(xx>=660)&(xx<=850)&(yy>=440)&(yy<=545)
scarf=(xx<=723)&(yy>=528)
reg=box&~scarf&(dist>r-1)
cov=np.clip(r+0.5-dist,0,1)[...,None]
new=DK*cov+BG*(1-cov)
a[reg]=new[reg]
Image.fromarray(a.astype(np.uint8)).save('christmas_2_snowman_v6.png')
Image.fromarray((reg*255).astype(np.uint8)).save('vectors/snowman_spike_edit_region_mask.png')
# remove leftover carrot-band remnant that overlapped the scarf top edge
b=np.array(Image.open('christmas_2_snowman_v6.png').convert('RGB')).astype(int)
z=(slice(524,536),slice(684,726))
sub=b[z]; amberish=(np.abs(sub-[168,96,36]).sum(2)<150)&(np.abs(sub-[192,180,120]).sum(2)>40)
sub[amberish]=[48,24,0]; b[z]=sub
Image.fromarray(b.astype(np.uint8)).save('christmas_2_snowman_v6.png')
b=np.array(Image.open('christmas_2_snowman_v6.png').convert('RGB')).astype(int)
z=(slice(522,548),slice(700,728)); sub=b[z]
white=sub.sum(2)>560; sub[white]=[48,24,0]; b[z]=sub
Image.fromarray(b.astype(np.uint8)).save('christmas_2_snowman_v6.png')
b=np.array(Image.open('christmas_2_snowman_v6.png').convert('RGB')).astype(float)
reg2=(xx>=676)&(xx<=723)&(yy>=528)&(yy<=545)&(dist>r-1)
b[reg2]=DK
reg3=(xx>=676)&(xx<=730)&(yy>=515)&(yy<528)&(dist>r-1)
b[reg3]=new[reg3]
reg4=(xx>723)&(xx<=730)&(yy>=528)&(yy<=545)
b[reg4]=BG
Image.fromarray(b.astype(np.uint8)).save('christmas_2_snowman_v6.png')

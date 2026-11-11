import re, numpy as np, cairosvg, io, sys
from PIL import Image
SRC='/cursor/stores/user/grok-bot/agents/054abeb4-0e58-46df-a62a-c76473e575fe/assets/01M70N7DK1508RZ8XW86JZMFMW.png'
BG=(192,180,120); DK=(48,24,0)
a=np.array(Image.open(SRC).convert('RGB')).astype(np.int16)
H,W=a.shape[:2]
# 1) erase old antlers: outside fitted head ellipse, above y=700, inside panel interior
cx,cy,rx,ry=627,760,241,188
yy,xx=np.mgrid[0:H,0:W]
e=((xx-cx)/rx)**2+((yy-cy)/ry)**2
inner=(xx>62)&(xx<W-62)&(yy>62)
erase=inner&(yy<700)&(e>1.012)
clean=a.copy(); clean[erase]=BG
Image.fromarray(clean.astype(np.uint8)).save('reindeer_head_only_mask_applied.png')
np.save if False else None
Image.fromarray((erase*255).astype(np.uint8)).save('vectors/old_antler_erase_mask.png')
# 2) antler vector from PhyloPic e60cd072 (left-facing), clipped
svg=open('refs/phylopic_e60cd072-d9ce-4d13-a79c-aa3d8086d37a.svg').read()
body=svg[svg.index('<g '):svg.rindex('</svg>')]
rootvb=(297.6,412.8); rootpanel=(float(sys.argv[1]) if len(sys.argv)>1 else 650, float(sys.argv[2]) if len(sys.argv)>2 else 600)
s=float(sys.argv[3]) if len(sys.argv)>3 else 0.99
xcut=float(sys.argv[4]) if len(sys.argv)>4 else 206
ycut=412.8
grow=float(sys.argv[5]) if len(sys.argv)>5 else 0
wrap=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><clipPath id="c"><rect x="0" y="0" width="2000" height="300"/><rect x="{xcut}" y="299" width="2000" height="{ycut-299}"/></clipPath></defs>
<g transform="translate({rootpanel[0]},{rootpanel[1]}) scale({s}) translate({-rootvb[0]},{-rootvb[1]})">
<g clip-path="url(#c)" fill="#301800" stroke="#301800" stroke-width="{grow}" stroke-linejoin="round">{body.replace('fill="#000000"','fill="#301800"')}</g></g></svg>'''
open('vectors/reindeer_antlers_v6.svg','w').write(wrap)
png=cairosvg.svg2png(bytestring=wrap.encode())
from scipy import ndimage
m0=np.array(Image.open(io.BytesIO(png)).convert('RGBA'))[...,3]/255.0
R=int(sys.argv[6]) if len(sys.argv)>6 else 0
if R>0:
    import numpy as _n
    yy2,xx2=_n.mgrid[-R:R+1,-R:R+1]; disk=(xx2**2+yy2**2)<=R*R
    # supersample-ish smooth dilation: dilate the soft mask then blur+threshold
    big=ndimage.zoom(m0,2,order=1)>0.5
    yy3,xx3=_n.mgrid[-2*R:2*R+1,-2*R:2*R+1]; disk2=(xx3**2+yy3**2)<=(2*R)**2
    big=ndimage.binary_dilation(big,structure=disk2)
    big=ndimage.gaussian_filter(big.astype(float),1.5)
    m0=ndimage.zoom(big,0.5,order=1)[:H,:W]
    m0=_n.clip((m0-0.5)*2+0.5,0,1)
lab,n=ndimage.label(m0>0.3)
sizes=ndimage.sum(np.ones_like(m0),lab,range(1,n+1))
for i,sz in enumerate(sizes,1):
    if sz<3000: m0[lab==i]=0
m0=m0*ndimage.binary_dilation(m0>0.3,iterations=2)
m=m0[...,None]
out=clean*(1-m)+np.array(DK)*m
out=out.astype(np.uint8)
Image.fromarray(out).save('christmas_3_reindeer_v6.png')
Image.fromarray((m[...,0]*255).astype(np.uint8)).save('vectors/reindeer_antlers_v6_mask.png')

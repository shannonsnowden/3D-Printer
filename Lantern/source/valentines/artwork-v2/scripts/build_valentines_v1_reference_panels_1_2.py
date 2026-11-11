"""2D artwork only (not CAD). Valentine's v1 panel images.
Panel px 1086x1471 = 77.5x105 mm (14.01 px/mm); origin = top-left of panel outline."""
import math, io, os, sys, re
import numpy as np, cairosvg
from PIL import Image
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W,H=1086,1471
DK='#301800'; AM='#a86024'; CR='#c0b478'
TPL=np.array(Image.open(f'{OUT}/vectors/panel_template_blank.png').convert('RGB')).astype(float)
FR=np.array(Image.open(f'{OUT}/vectors/panel_frame_mask.png'))>0
def P(x,y): return f'{x:.1f},{y:.1f}'
def heart_d(cx,cy,w,rot=0):
    s=w/32.0; pts=[]
    a=math.radians(rot)
    for i in range(181):
        t=2*math.pi*i/180
        x=16*math.sin(t)**3; y=-(13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t))
        x*=s; y=(y+2.5)*s
        pts.append(P(cx+x*math.cos(a)-y*math.sin(a),cy+x*math.sin(a)+y*math.cos(a)))
    return 'M'+' L'.join(pts)+' Z'
def heart(cx,cy,w,col,rot=0): return f'<path d="{heart_d(cx,cy,w,rot)}" fill="{col}"/>'
def star4(cx,cy,r,col=AM,w=0.34):
    pts=[P(cx+(r if k%2==0 else r*w)*math.sin(math.radians(k*45)),cy-(r if k%2==0 else r*w)*math.cos(math.radians(k*45))) for k in range(8)]
    return f'<path d="M{" L".join(pts)} Z" fill="{col}" stroke="{col}" stroke-width="10" stroke-linejoin="round"/>'
def svg(body): return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'
def inner(path):
    s=open(path).read(); return s[s.index('<g'):s.rindex('</svg>')]
ROSE=inner(f'{OUT}/refs/openclipart_221383.svg')   # GDJ, CC0
BIRD=inner(f'{OUT}/refs/phylopic_7ae5a12e-85ea-4395-9529-de821b92f74c.svg').replace('fill="#000000"','fill="'+DK+'"')  # Hugo Gruson, CC0

# ---------- 1 heart + Cupid's arrow ----------
def heart_arrow():
    b=[]; cx,cy=543,700; ang=-24; a=math.radians(ang); ux,uy=math.cos(a),math.sin(a); nx,ny=-uy,ux
    L1,L2=-430,430
    tail=(cx+ux*L1,cy+uy*L1); tip=(cx+ux*L2,cy+uy*L2)
    b.append(f'<path d="M{P(*tail)} L{P(*tip)}" stroke="{DK}" stroke-width="32" stroke-linecap="round"/>')
    # arrowhead with barbs
    hx,hy=tip; hl=130; hw=68
    hp=[(hx+ux*40,hy+uy*40),(hx-ux*hl+nx*hw,hy-uy*hl+ny*hw),(hx-ux*(hl-30),hy-uy*(hl-30)),(hx-ux*hl-nx*hw,hy-uy*hl-ny*hw)]
    b.append(f'<path d="M{" L".join(P(*p) for p in hp)} Z" fill="{DK}" stroke="{DK}" stroke-width="8" stroke-linejoin="round"/>')
    # fletching: three feather pairs
    for k in range(3):
        o=L1+20+k*56
        bx,by=cx+ux*o,cy+uy*o
        for sgn in (1,-1):
            fp=[(bx,by),(bx+ux*66+nx*sgn*16,by+uy*66+ny*sgn*16),(bx+ux*34+nx*sgn*72,by+uy*34+ny*sgn*72),(bx-ux*22+nx*sgn*66,by-uy*22+ny*sgn*66)]
            b.append(f'<path d="M{" L".join(P(*p) for p in fp)} Z" fill="{DK}" stroke="{DK}" stroke-width="6" stroke-linejoin="round"/>')
    b.append(heart(cx,cy+10,640,DK))
    b.append(heart(cx,cy+10,500,AM))
    b.append(heart(cx,cy+10,400,DK))
    for (x,y,w,c) in [(190,250,110,AM),(880,250,90,DK),(170,1200,90,DK),(905,1180,120,AM),(543,1330,70,AM)]:
        b.append(heart(x,y,w,c,rot=(-12 if x<543 else 12)))
    for (x,y,r) in [(330,170,30),(760,1330,30)]: b.append(star4(x,y,r))
    return b

# ---------- 2 bouquet of roses ----------
BLOOM_CLIP='M200,-30 L1100,-30 L1100,860 L690,860 L690,665 L200,665 Z'; BLOOM_C=(676,336); STEM_PT=(526,603)
GAP=float(os.environ.get('ROSE_GAP','3'))  # px: widens the rose stencil cut-lines (cream) by this amount
LEAF_CLIP='M88,650 L358,650 L358,1035 L88,1035 Z'; LEAF_B=(321,1020)
def place(content,clip,cid,anchor,pos,s,rot=0,mirror=False,halo=0):
    mx=-1 if mirror else 1
    tr=f'translate({pos[0]:.1f},{pos[1]:.1f}) rotate({rot}) scale({mx*s},{s}) translate({-anchor[0]},{-anchor[1]})'
    cp=f'<clipPath id="{cid}"><path d="{clip}"/></clipPath>'
    g=''
    if halo: g+=f'<g clip-path="url(#{cid})" fill="{CR}" stroke="{CR}" stroke-width="{halo/s:.0f}" stroke-linejoin="round">{content}</g>'
    g+=f'<g clip-path="url(#{cid})" fill="{DK}">{content}</g>'
    if GAP: g+=f'<g clip-path="url(#{cid})" fill="none" stroke="{CR}" stroke-width="{GAP/s:.2f}" stroke-linejoin="round">{content}</g>'
    return f'<g transform="{tr}">{cp}{g}</g>'
def to_panel(anchor,pt,pos,s,rot,mirror):
    dx,dy=(pt[0]-anchor[0])*s*(-1 if mirror else 1),(pt[1]-anchor[1])*s
    a=math.radians(rot); return (pos[0]+dx*math.cos(a)-dy*math.sin(a),pos[1]+dx*math.sin(a)+dy*math.cos(a))
def bouquet():
    b=[]; tie=(543,1090)
    blooms=[((292,720),0.42,-22,False,'bL'),((794,720),0.42,22,True,'bR'),((543,500),0.5,0,False,'bC')]
    stems=[]
    for pos,s,rot,mir,cid in blooms:
        sp=to_panel(BLOOM_C,STEM_PT,pos,s,rot,mir); stems.append(sp)
    ends=[(480,1350),(543,1360),(606,1350)]
    for sp,e in zip(stems,[ends[0],ends[2],ends[1]]):
        c=((sp[0]+tie[0])/2,(sp[1]+tie[1])/2+30)
        b.append(f'<path d="M{P(*sp)} Q{P(*c)} {P(*tie)} L{P(*e)}" fill="none" stroke="{DK}" stroke-width="26" stroke-linecap="round"/>')
    # leaves
    for pos,s,rot,mir,cid in [((500,1000),0.46,-30,False,'l1'),((586,1000),0.46,30,True,'l2'),((470,900),0.4,-62,False,'l3'),((616,900),0.4,62,True,'l4')]:
        b.append(place(ROSE,LEAF_CLIP,cid,LEAF_B,pos,s,rot,mir,halo=14))
    for pos,s,rot,mir,cid in blooms:
        b.append(place(ROSE,BLOOM_CLIP,cid,BLOOM_C,pos,s,rot,mir,halo=18))
    for sp in stems:   # re-join each stem to its bloom across the halo
        dx,dy=tie[0]-sp[0],tie[1]-sp[1]; L=math.hypot(dx,dy)
        b.append(f'<path d="M{P(*sp)} L{P(sp[0]+dx/L*60,sp[1]+dy/L*60)}" stroke="{DK}" stroke-width="26" stroke-linecap="round"/>')
    # ribbon bow at tie
    tx,ty=tie
    for sg in (1,-1):
        b.append(f'<path d="M{P(tx,ty)} C{P(tx+sg*60,ty-110)} {P(tx+sg*170,ty-70)} {P(tx+sg*150,ty-10)} C{P(tx+sg*135,ty+40)} {P(tx+sg*60,ty+20)} {P(tx,ty)} Z" fill="{DK}"/>')
        b.append(f'<path d="M{P(tx+sg*30,ty-8)} C{P(tx+sg*70,ty-70)} {P(tx+sg*130,ty-50)} {P(tx+sg*122,ty-14)} C{P(tx+sg*112,ty+14)} {P(tx+sg*70,ty+6)} {P(tx+sg*30,ty-8)} Z" fill="{AM}"/>')
        b.append(f'<path d="M{P(tx+sg*10,ty+15)} C{P(tx+sg*50,ty+90)} {P(tx+sg*70,ty+150)} {P(tx+sg*110,ty+210)} L{P(tx+sg*70,ty+215)} L{P(tx+sg*85,ty+250)} C{P(tx+sg*40,ty+180)} {P(tx+sg*20,ty+110)} {P(tx-sg*8,ty+25)} Z" fill="{DK}" stroke="{DK}" stroke-width="4" stroke-linejoin="round"/>')
    b.append(f'<ellipse cx="{tx}" cy="{ty}" rx="34" ry="30" fill="{DK}"/><ellipse cx="{tx}" cy="{ty}" rx="14" ry="12" fill="{AM}"/>')
    for (x,y,w,c) in [(150,230,90,AM),(935,240,80,AM),(150,1220,80,DK),(935,1220,90,DK)]:
        b.append(heart(x,y,w,c,rot=(-12 if x<543 else 12)))
    return b

# ---------- 3 love letter ----------
def letter():
    b=[]; cx,cy=543,800; ew,eh=760,500; rot=-6
    x0,y0,x1,y1=-ew/2,-eh/2,ew/2,eh/2; tipy=y0+eh*0.58
    g=(f'<rect x="{x0}" y="{y0}" width="{ew}" height="{eh}" rx="26" fill="none" stroke="{DK}" stroke-width="30"/>'
       f'<path d="M{P(x0+20,y0+20)} L{P(0,tipy)} L{P(x1-20,y0+20)} Z" fill="{AM}"/>'
       f'<path d="M{P(x0+8,y0+10)} L{P(0,tipy)} L{P(x1-8,y0+10)}" fill="none" stroke="{DK}" stroke-width="26" stroke-linejoin="round" stroke-linecap="round"/>'
       f'<path d="M{P(x0+14,y1-14)} L{P(-95,tipy+40)} M{P(x1-14,y1-14)} L{P(95,tipy+40)}" fill="none" stroke="{DK}" stroke-width="20" stroke-linecap="round"/>')
    # wax seal: scalloped disc + amber heart
    sy=tipy
    g+=''.join(f'<circle cx="{76*math.sin(math.radians(k*30)):.1f}" cy="{sy-76*math.cos(math.radians(k*30)):.1f}" r="26" fill="{DK}"/>' for k in range(12))
    g+=f'<circle cx="0" cy="{sy}" r="82" fill="{DK}"/>'+heart(0,sy+2,96,AM)
    b.append(f'<g transform="translate({cx},{cy}) rotate({rot})">{g}</g>')
    for (x,y,w,c,r) in [(330,370,110,DK,-14),(560,250,150,AM,6),(800,370,120,DK,14),(170,1240,80,AM,-12),(920,1230,90,AM,12)]:
        b.append(heart(x,y,w,c,rot=r))
    for (x,y,r) in [(700,170,28),(410,190,24),(543,1330,30)]: b.append(star4(x,y,r))
    return b

# ---------- 4 lovebirds on a branch ----------
BIRD_ROT=-11; BIRD_S=0.42   # vb units -> panel px
def lovebirds():
    b=[]
    # branch: gentle curve across the panel (drawn), birds' own branch stubs sit on it
    by=930
    b.append(f'<path d="M{P(122,by+20)} C{P(260,by)} {P(826,by)} {P(964,by+20)}" fill="none" stroke="{DK}" stroke-width="46" stroke-linecap="round"/>')
    bx={-1:None}
    for mir,px in ((False,345),(True,741)):
        mx=-1 if mir else 1
        # anchor: bird's feet on its branch (vb coords) -> panel (px, by-14)
        anc=(860,853)
        tr=f'translate({px},{by}) scale({mx},1) rotate({BIRD_ROT}) scale({BIRD_S}) translate({-anc[0]},{-anc[1]})'
        clip=f'<clipPath id="bc{int(mir)}"><path d="M420,-100 L1300,-100 L1300,540 L1045,545 L1000,650 L920,760 L868,822 L815,885 L790,925 L662,994 L662,1400 L300,1400 L330,1150 L390,1000 L420,800 Z"/></clipPath>'
        b.append(f'<g transform="{tr}">{clip}<g clip-path="url(#bc{int(mir)})" fill="{DK}">{BIRD}</g>'
                 f'<circle cx="1000" cy="160" r="28" fill="{AM}"/></g>')
    b.append(heart(543,560,130,AM))
    for (x,y,w,c,r) in [(543,330,80,DK,0),(380,300,60,AM,-12),(706,300,60,AM,12)]: b.append(heart(x,y,w,c,rot=r))
    for (x,y,r) in [(170,250,30),(915,250,30),(200,1250,28),(890,1240,30)]: b.append(star4(x,y,r))
    return b

PANELS={'1_heart_and_arrow':heart_arrow,'2_rose_bouquet':bouquet,'3_love_letter':letter,'4_lovebirds':lovebirds}
def render(name,fn):
    s=svg(''.join(fn())); open(f'{OUT}/vectors/valentines_{name}.svg','w').write(s)
    rgba=np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode()))).convert('RGBA')).astype(float)
    al=rgba[...,3:4]/255; img=TPL*(1-al)+rgba[...,:3]*al
    img[FR]=TPL[FR]
    Image.fromarray(img.round().astype(np.uint8)).save(f'{OUT}/valentines_{name}.png')
    P3=np.array([[192,180,120],[168,96,36],[48,24,0]],float)
    lab=((img[:,:,None,:]-P3[None,None])**2).sum(3).argmin(2).astype(np.uint8)
    Image.fromarray(lab*127).save(f'{OUT}/vectors/valentines_{name}_thickness_classes.png')
if __name__=='__main__':
    for n in (sys.argv[1:] or list(PANELS)): render(n,PANELS[n]); print('built',n)

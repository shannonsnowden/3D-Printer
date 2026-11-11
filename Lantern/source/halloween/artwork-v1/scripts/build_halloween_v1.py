"""2D artwork only (not CAD). Halloween v1: four lantern panel concept images.
Panel px 1086x1471 = 77.5x105 mm (14.01 px/mm); origin = top-left of panel outline.
Needs numpy, scipy, Pillow, cairosvg, svgelements. Paths are relative to the bundle root."""
import math, io, os, sys
import numpy as np, cairosvg, svgelements as se
from PIL import Image
from scipy import ndimage as nd
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W,H=1086,1471
DK='#301800'; AM='#a86024'; CR='#c0b478'
TPL=np.array(Image.open(f'{OUT}/vectors/panel_template_blank.png').convert('RGB')).astype(float)
FR=np.array(Image.open(f'{OUT}/vectors/panel_frame_mask.png'))>0
def P(x,y): return f'{x:.1f},{y:.1f}'
def svg(body): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'
def star4(cx,cy,r,col=AM,w=0.34):
    pts=[P(cx+(r if k%2==0 else r*w)*math.sin(math.radians(k*45)),cy-(r if k%2==0 else r*w)*math.cos(math.radians(k*45))) for k in range(8)]
    return f'<path d="M{" L".join(pts)} Z" fill="{col}" stroke="{col}" stroke-width="10" stroke-linejoin="round"/>'
def flat(path_svg):
    out=[]
    for e in se.SVG.parse(path_svg).elements():
        if isinstance(e,se.Shape):
            p=se.Path(e); p.reify(); bb=p.bbox()
            if bb: out.append((str(e.fill) if e.fill is not None else None,p.d(),bb))
    return out
def place(path_svg, box, fill=DK, stroke=4, mirror=False, keep=None):
    """fit a reference silhouette into box=(x,y,w,h) keeping aspect; returns (svg, s, ox, oy)"""
    el=[e for e in flat(path_svg) if e[0] not in (None,'none','#ffffff')]
    if keep: el=[e for i,e in enumerate(el) if i in keep]
    x0=min(e[2][0] for e in el); y0=min(e[2][1] for e in el); x1=max(e[2][2] for e in el); y1=max(e[2][3] for e in el)
    bx,by,bw,bh=box; s=min(bw/(x1-x0),bh/(y1-y0))
    ox=bx+(bw-(x1-x0)*s)/2; oy=by+(bh-(y1-y0)*s)/2
    if mirror: tr=f'translate({ox+(x1-x0)*s+x0*s:.2f},{oy-y0*s:.2f}) scale({-s:.6f},{s:.6f})'
    else: tr=f'translate({ox-x0*s:.2f},{oy-y0*s:.2f}) scale({s:.6f})'
    body=''.join(f'<path d="{d}" fill-rule="evenodd"/>' for _,d,_ in el)
    return f'<g transform="{tr}" fill="{fill}" stroke="{fill}" stroke-width="{stroke/s:.3f}" stroke-linejoin="round">{body}</g>', s, ox, oy
BAT=f'{OUT}/refs/openclipart_242212_bat_silhouette.svg'
def bat(cx,cy,w,rot=0,mirror=False):
    g,s,ox,oy=place(BAT,(-w/2,-w*0.25,w,w*0.5),DK,8,mirror)
    return f'<g transform="translate({cx},{cy}) rotate({rot})">{g}</g>'
def moon(cx,cy,r,craters=True):
    b=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{AM}"/>'
    if craters:
        for (dx,dy,cr) in [(-0.35,-0.25,0.16),(0.28,0.12,0.12),(-0.05,0.42,0.1),(0.38,-0.38,0.08)]:
            b+=f'<circle cx="{cx+dx*r:.1f}" cy="{cy+dy*r:.1f}" r="{cr*r:.1f}" fill="{CR}"/>'
    return b

# ---------- 1 jack-o'-lantern ----------
def jack():
    b=[]; cx,cy=543,800
    # ribbed pumpkin: overlapping lobes, dark, with amber rib grooves
    lobes=[(-250,200,330),(250,200,330),(-130,250,370),(130,250,370),(0,270,380)]
    for dx,rx,ry in lobes: b.append(f'<ellipse cx="{cx+dx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{DK}"/>')
    for sg in (-1,1):   # rib grooves on the outer lobes only, clear of the carved face
        b.append(f'<path d="M{P(cx+sg*215,cy-318)} Q{P(cx+sg*440,cy)} {P(cx+sg*215,cy+330)}" fill="none" stroke="{AM}" stroke-width="14" stroke-linecap="round"/>')
    # stem and curly vine with a leaf
    b.append(f'<path d="M{P(cx-30,cy-360)} C{P(cx-35,cy-430)} {P(cx-10,cy-480)} {P(cx+40,cy-520)} L{P(cx+75,cy-490)} C{P(cx+40,cy-450)} {P(cx+35,cy-410)} {P(cx+40,cy-360)} Z" fill="{DK}" stroke="{DK}" stroke-width="10" stroke-linejoin="round"/>')
    b.append(f'<path d="M{P(cx+30,cy-400)} C{P(cx+120,cy-440)} {P(cx+200,cy-400)} {P(cx+190,cy-470)} C{P(cx+180,cy-530)} {P(cx+110,cy-520)} {P(cx+130,cy-480)}" fill="none" stroke="{DK}" stroke-width="16" stroke-linecap="round"/>')
    b.append(f'<path d="M{P(cx-40,cy-400)} C{P(cx-120,cy-470)} {P(cx-230,cy-450)} {P(cx-260,cy-520)} C{P(cx-170,cy-560)} {P(cx-80,cy-520)} {P(cx-40,cy-400)} Z" fill="{DK}"/>')
    b.append(f'<path d="M{P(cx-60,cy-430)} Q{P(cx-150,cy-480)} {P(cx-225,cy-505)}" fill="none" stroke="{AM}" stroke-width="12" stroke-linecap="round"/>')
    # carved face: cream (glows brightest) with an amber inner-glow rim
    def cut(d):
        b.append(f'<path d="{d}" fill="{AM}" stroke="{AM}" stroke-width="30" stroke-linejoin="round"/>')
        b.append(f'<path d="{d}" fill="{CR}" stroke="{CR}" stroke-width="6" stroke-linejoin="round"/>')
    cut(f'M{P(cx-235,cy-60)} L{P(cx-75,cy-60)} L{P(cx-150,cy-200)} Z')
    cut(f'M{P(cx+75,cy-60)} L{P(cx+235,cy-60)} L{P(cx+150,cy-200)} Z')
    cut(f'M{P(cx-45,cy+40)} L{P(cx+45,cy+40)} L{P(cx,cy-40)} Z')
    grin=(f'M{P(cx-240,cy+60)} Q{P(cx,cy+170)} {P(cx+240,cy+60)} Q{P(cx+190,cy+280)} {P(cx,cy+290)} Q{P(cx-190,cy+280)} {P(cx-240,cy+60)} Z')
    cut(grin)
    # two square teeth: one hanging from the top lip, one rising from the bottom lip
    b.append(f'<rect x="{cx-100}" y="{cy+80}" width="62" height="78" rx="8" fill="{DK}"/>')
    b.append(f'<rect x="{cx+45}" y="{cy+222}" width="62" height="90" rx="8" fill="{DK}"/>')
    for (x,y,r) in [(170,250,30),(920,260,26),(900,1290,26),(180,1300,28),(760,210,22)]: b.append(star4(x,y,r))
    return b

# ---------- 2 witch on a broomstick across the full moon (GDJ, Openclipart 306877, PD/CC0) ----------
WITCH=f'{OUT}/refs/openclipart_306877_broom_riding_witch_silhouette.svg'
def witch():
    b=[]
    b.append(moon(560,690,350,craters=False))
    g,s,ox,oy=place(WITCH,(110,410,880,620),DK,8)
    b.append(f'<g>{g}</g>')
    for (x,y,r) in [(170,220,30),(920,230,30),(160,1130,26),(930,1110,28),(543,1180,24),(543,200,22)]: b.append(star4(x,y,r))
    b.append(bat(300,1270,190,-8)); b.append(bat(800,1290,150,10,True))
    return b

# ---------- 3 black cat on a fence under a crescent moon (kattekrab, Openclipart 26514, PD/CC0) ----------
CAT=f'{OUT}/refs/openclipart_26514_black_cat.svg'
def cat():
    b=[]
    # crescent moon (amber), upper right
    b.append(f'<path d="M{P(850,170)} A170,170 0 1 0 {P(850,510)} A200,200 0 0 1 {P(850,170)} Z" fill="{AM}"/>')
    # picket fence: rails + rounded-point pickets
    top=950; base=1385
    b.append(f'<rect x="80" y="{top+110}" width="926" height="40" rx="10" fill="{DK}"/><rect x="80" y="{top+300}" width="926" height="40" rx="10" fill="{DK}"/>')
    for k in range(7):
        x=120+k*130
        b.append(f'<path d="M{P(x,base)} L{P(x,top+40)} Q{P(x,top)} {P(x+40,top-40)} Q{P(x+80,top)} {P(x+80,top+40)} L{P(x+80,base)} Z" fill="{DK}"/>')
    # cat sits on top of the fence (centred on a picket pair)
    g,s,ox,oy=place(CAT,(330,300,420,690),DK,4)
    b.append(g)
    # glowing amber almond eyes with dark slit pupils (head occupies about x 345-590, y 300-530)
    for (ex,rot) in [(418,12),(518,-12)]:
        b.append(f'<ellipse cx="{ex}" cy="432" rx="34" ry="22" fill="{AM}" transform="rotate({rot} {ex} 432)"/>')
        b.append(f'<ellipse cx="{ex}" cy="432" rx="7" ry="19" fill="{DK}"/>')
    for (x,y,r) in [(190,230,30),(560,180,24),(300,500,22),(170,760,24),(930,760,26)]: b.append(star4(x,y,r))
    return b, (s,ox,oy)

# ---------- 4 haunted house on a hill with bats (bats: GDJ, Openclipart 242212, PD/CC0) ----------
def house():
    b=[]; base=1390
    b.append(moon(800,330,150))
    # hill
    b.append(f'<path d="M{P(80,base)} L{P(80,1190)} Q{P(543,1080)} {P(1006,1190)} L{P(1006,base)} Z" fill="{DK}"/>')
    # main house body, crooked roofs, tower
    hx=300; hw=480; hy=760
    b.append(f'<rect x="{hx}" y="{hy}" width="{hw}" height="{1200-hy}" fill="{DK}"/>')
    b.append(f'<path d="M{P(hx-40,hy+10)} L{P(hx+hw*0.45,hy-230)} L{P(hx+hw+40,hy+10)} Z" fill="{DK}" stroke="{DK}" stroke-width="16" stroke-linejoin="round"/>')
    tx,tw=hx+hw-150,170   # tower on the right
    b.append(f'<rect x="{tx}" y="{hy-260}" width="{tw}" height="300" fill="{DK}"/>')
    b.append(f'<path d="M{P(tx-30,hy-250)} L{P(tx+tw/2+15,hy-470)} L{P(tx+tw+30,hy-250)} Z" fill="{DK}" stroke="{DK}" stroke-width="16" stroke-linejoin="round"/>')
    b.append(f'<rect x="{hx-90}" y="{hy+170}" width="130" height="270" fill="{DK}"/>')   # side wing
    b.append(f'<path d="M{P(hx-115,hy+180)} L{P(hx-25,hy+60)} L{P(hx+60,hy+180)} Z" fill="{DK}" stroke="{DK}" stroke-width="14" stroke-linejoin="round"/>')
    b.append(f'<rect x="{hx+60}" y="{hy-190}" width="50" height="120" fill="{DK}"/>')   # chimney
    # lit windows (amber) with dark muntins; arched door; round attic window
    def win(x,y,w,h,arch=False):
        d=(f'M{P(x,y+h)} L{P(x,y+w/2)} A{w/2},{w/2} 0 0 1 {P(x+w,y+w/2)} L{P(x+w,y+h)} Z' if arch else f'M{P(x,y)} L{P(x+w,y)} L{P(x+w,y+h)} L{P(x,y+h)} Z')
        b.append(f'<path d="{d}" fill="{AM}"/>')
        b.append(f'<path d="M{P(x+w/2,y+(w/2 if arch else 0))} L{P(x+w/2,y+h)} M{P(x,y+h*0.55)} L{P(x+w,y+h*0.55)}" stroke="{DK}" stroke-width="12"/>')
    win(hx+50,hy+60,90,130); win(hx+190,hy+60,90,130); win(hx+50,hy+250,90,130); win(tx+45,hy-200,80,130,True)
    win(hx-62,hy+230,75,110)
    b.append(f'<circle cx="{hx+hw*0.45}" cy="{hy-80}" r="42" fill="{AM}"/><path d="M{P(hx+hw*0.45-42,hy-80)} L{P(hx+hw*0.45+42,hy-80)} M{P(hx+hw*0.45,hy-122)} L{P(hx+hw*0.45,hy-38)}" stroke="{DK}" stroke-width="12"/>')
    dx,dw=hx+300,110
    b.append(f'<path d="M{P(dx,1200)} L{P(dx,hy+300)} A{dw/2},{dw/2} 0 0 1 {P(dx+dw,hy+300)} L{P(dx+dw,1200)} Z" fill="{AM}"/>')
    b.append(f'<circle cx="{dx+dw-26}" cy="{hy+360}" r="10" fill="{DK}"/>')
    # one boarded-up window: amber pane crossed by two dark boards
    win(hx+190,hy+250,90,130)
    b.append(f'<path d="M{P(hx+178,hy+262)} L{P(hx+292,hy+368)} M{P(hx+178,hy+368)} L{P(hx+292,hy+262)}" stroke="{DK}" stroke-width="22" stroke-linecap="round"/>')
    # gravestones
    for (x,w,h) in [(130,70,100),(890,80,120),(990-40,0,0)]:
        if w: b.append(f'<path d="M{P(x,1250)} L{P(x,1250-h+w/2)} A{w/2},{w/2} 0 0 1 {P(x+w,1250-h+w/2)} L{P(x+w,1250)} Z" fill="{DK}"/>')
    # bats
    b.append(bat(250,300,220,-12)); b.append(bat(470,200,150,8,True)); b.append(bat(930,560,130,-6,True)); b.append(bat(180,560,120,10))
    for (x,y,r) in [(620,150,22),(960,140,22)]: b.append(star4(x,y,r))
    return b

PANELS={'1_jack_o_lantern':jack,'2_witch_moon':witch,'3_black_cat_fence':lambda: cat()[0],'4_haunted_house_bats':house}
SPECK=12
P3=np.array([[192,180,120],[168,96,36],[48,24,0]],float)
def render(name,fn):
    s=svg(''.join(fn())); open(f'{OUT}/vectors/halloween_{name}.svg','w').write(s)
    rgba=np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode()))).convert('RGBA')).astype(float)
    al=rgba[...,3:4]/255; img=TPL*(1-al)+rgba[...,:3]*al
    img[FR]=TPL[FR]
    lab=((img[:,:,None,:]-P3[None,None])**2).sum(3).argmin(2).astype(np.uint8)
    # speck rule: amber connected components under SPECK px (anti-alias fringes) are reassigned to the
    # most common neighbouring class, and the PNG pixels are repainted to that class colour.
    am=lab==1; l,k=nd.label(am); fixed=0
    if k:
        sz=nd.sum(am,l,range(1,k+1)); objs=nd.find_objects(l)
        for i,sv in enumerate(sz):
            if sv>=SPECK: continue
            sl=tuple(slice(max(0,a.start-2),a.stop+2) for a in objs[i])
            m=l[sl]==(i+1); ring=nd.binary_dilation(m,iterations=1)&~m
            sub=lab[sl]; vals=sub[ring]; vals=vals[vals!=1]
            c=int(np.bincount(vals,minlength=3).argmax()) if vals.size else 0
            sub[m]=c; img[sl][m]=P3[c]; fixed+=1
    img[FR]=TPL[FR]
    Image.fromarray(img.round().astype(np.uint8)).save(f'{OUT}/halloween_{name}.png')
    Image.fromarray(lab*127).save(f'{OUT}/vectors/halloween_{name}_thickness_classes.png')
    return fixed
if __name__=='__main__':
    for n in (sys.argv[1:] or list(PANELS)): print('built',n,'amber specks reassigned:',render(n,PANELS[n]))

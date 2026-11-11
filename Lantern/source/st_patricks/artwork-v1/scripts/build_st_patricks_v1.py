"""2D artwork only (not CAD). St Patrick's Day v1: four lantern panel concept images.
Panel px 1086x1471 = 77.5x105 mm (14.01 px/mm); origin = top-left of panel outline.
Needs numpy, Pillow, cairosvg, svgelements. Paths are relative to the bundle root."""
import math, io, os, sys
import numpy as np, cairosvg, svgelements as se
from PIL import Image
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
def heart_d(cx,cy,w,rot=0):
    """classic heart, tip pointing +y at rot=0; (cx,cy) = bbox centre"""
    s=w/32.0; pts=[]; a=math.radians(rot)
    for i in range(181):
        t=2*math.pi*i/180
        x=16*math.sin(t)**3; y=-(13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t))
        x*=s; y=(y+2.5)*s
        pts.append(P(cx+x*math.cos(a)-y*math.sin(a),cy+x*math.sin(a)+y*math.cos(a)))
    return 'M'+' L'.join(pts)+' Z'
def leaf(cx,cy,w,phi,col,d=None):
    """heart-shaped clover leaf whose tip sits at (cx,cy) and which points outward at angle phi (0 = up, clockwise)"""
    d=d if d is not None else w*0.47
    a=math.radians(phi); hx,hy=cx+d*math.sin(a),cy-d*math.cos(a)
    return f'<path d="{heart_d(hx,hy,w,phi)}" fill="{col}"/>'
def shamrock(cx,cy,w,col=AM,rot=0,stem=True):
    b=''
    if stem: b+=f'<path d="M{P(cx,cy)} q{P(w*0.05,w*0.45)} {P(w*0.3,w*0.75)}" fill="none" stroke="{col}" stroke-width="{max(10,w*0.09):.0f}" stroke-linecap="round" transform="rotate({rot} {cx} {cy})"/>'
    for k in range(3): b+=leaf(cx,cy,w*0.52,rot+k*120,col)
    return b
def coin(x,y,r,rim=DK,face=AM):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{face}" stroke="{rim}" stroke-width="10"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*0.5:.1f}" fill="none" stroke="{rim}" stroke-width="10"/>')
def coin_side(x,y,rx,ry):
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx}" ry="{ry}" fill="{AM}" stroke="{DK}" stroke-width="12"/>'
def flat(path_svg):
    out=[]
    for e in se.SVG.parse(path_svg).elements():
        if isinstance(e,se.Shape):
            p=se.Path(e); p.reify(); out.append((e.id,str(e.fill) if e.fill is not None else None,p.d()))
    return out

# ---------- 1 four-leaf clover ----------
def clover():
    b=[]; cx,cy=543,620; w=340
    # stem first (behind leaves), thick, gently S-curved
    b.append(f'<path d="M{P(cx,cy)} C{P(cx+10,cy+300)} {P(cx-80,cy+450)} {P(cx+40,cy+660)}" fill="none" stroke="{DK}" stroke-width="40" stroke-linecap="round"/>')
    for phi in (-45,45,135,225):
        b.append(leaf(cx,cy,w,phi,DK,d=w*0.62))
    # cream separation lines between neighbouring leaves (along the vertical/horizontal axes)
    for phi in (0,90,270):   # bottom gap is filled by the stem
        a=math.radians(phi); b.append(f'<path d="M{P(cx+45*math.sin(a),cy-45*math.cos(a))} L{P(cx+320*math.sin(a),cy-320*math.cos(a))}" stroke="{CR}" stroke-width="16" stroke-linecap="round"/>')
    # amber inset heart outline + midrib on each leaf
    for phi in (-45,45,135,225):
        a=math.radians(phi); d=70+0.61*w*0.56; hx,hy=cx+d*math.sin(a),cy-d*math.cos(a)
        b.append(f'<path d="{heart_d(hx,hy,w*0.56,phi)}" fill="none" stroke="{AM}" stroke-width="18" stroke-linejoin="round"/>')
        b.append(f'<path d="M{P(cx+50*math.sin(a),cy-50*math.cos(a))} L{P(cx+(d+w*0.1)*math.sin(a),cy-(d+w*0.1)*math.cos(a))}" stroke="{AM}" stroke-width="16" stroke-linecap="round"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="30" fill="{DK}"/>')
    for (x,y,w_,r) in [(175,215,130,-15),(910,240,120,20),(170,1200,120,10),(905,1150,140,-20)]: b.append(shamrock(x,y,w_,AM,r))
    for (x,y,r) in [(543,150,28),(880,700,26),(200,720,26)]: b.append(star4(x,y,r))
    return b

# ---------- 2 leprechaun hat with buckle and shamrock ----------
def hat():
    b=[]; cx=543; top=400; band0,band1=720,850; bw=560; tw=450
    # brim: wide, upturned at both ends
    brim=f'M{P(cx-450,band1-40)} C{P(cx-430,band1+60)} {P(cx-250,band1+110)} {P(cx,band1+110)} C{P(cx+250,band1+110)} {P(cx+430,band1+60)} {P(cx+450,band1-40)} C{P(cx+400,band1+10)} {P(cx+250,band1+30)} {P(cx,band1+30)} C{P(cx-250,band1+30)} {P(cx-400,band1+10)} {P(cx-450,band1-40)} Z'
    b.append(f'<path d="{brim}" fill="{DK}" stroke="{DK}" stroke-width="30" stroke-linejoin="round"/>')
    b.append(f'<path d="M{P(cx-400,band1+20)} C{P(cx-250,band1+80)} {P(cx+250,band1+80)} {P(cx+400,band1+20)}" fill="none" stroke="{AM}" stroke-width="16" stroke-linecap="round"/>')
    # crown: flares slightly to a softly domed top
    crown=f'M{P(cx-bw/2,band1+20)} L{P(cx-tw/2,top+30)} Q{P(cx,top-30)} {P(cx+tw/2,top+30)} L{P(cx+bw/2,band1+20)} Z'
    b.append(f'<path d="{crown}" fill="{DK}" stroke="{DK}" stroke-width="20" stroke-linejoin="round"/>')
    b.append(f'<clipPath id="cr"><path d="{crown}"/></clipPath>')
    # dark hat band edged with two amber lines; bold amber buckle frame with dark opening and amber prong
    b.append(f'<g clip-path="url(#cr)"><rect x="0" y="{band0-8}" width="{W}" height="16" fill="{AM}"/><rect x="0" y="{band1-8}" width="{W}" height="16" fill="{AM}"/>'
             f'<path d="M{P(cx-tw/2+60,top+70)} L{P(cx-bw/2+70,band0-50)}" stroke="{AM}" stroke-width="18" stroke-linecap="round"/></g>')
    bx,by=cx,(band0+band1)/2
    b.append(f'<rect x="{bx-105}" y="{by-92}" width="210" height="184" rx="18" fill="{DK}" stroke="{AM}" stroke-width="40"/>')
    b.append(f'<rect x="{bx-20}" y="{by-12}" width="125" height="24" rx="10" fill="{AM}"/>')
    b.append(f'<rect x="{bx-30}" y="{by-80}" width="24" height="160" fill="{AM}"/>')
    # shamrock tucked into the band, amber with a dark halo line so it reads on the dark crown
    sx,sy=cx+175,band0-80
    b.append(f'<g>{shamrock(sx,sy,190,AM,15,stem=False)}</g>')
    b.append(f'<path d="M{P(sx,sy)} L{P(sx+30,band0-6)}" stroke="{AM}" stroke-width="16" stroke-linecap="round"/>')
    # coins and small shamrocks around
    for k in range(4): b.append(coin_side(543,1250-k*36,78,30))      # coin stack
    for (x,y,r) in [(330,1215,52),(760,1220,50),(235,1265,40),(860,1270,40)]: b.append(coin(x,y,r))
    for (x,y,w_,r) in [(185,220,120,-15),(905,230,120,20)]: b.append(shamrock(x,y,w_,AM,r))
    for (x,y,r) in [(543,190,28),(930,1110,26),(150,1110,26),(930,560,26),(150,560,26)]: b.append(star4(x,y,r))
    return b

# ---------- 3 pot of gold at the end of the rainbow ----------
def pot_of_gold():
    b=[]
    # rainbow: four bands (dark/amber alternating) on an elliptical arc, left foot in a cloud, right foot in the pot
    cx,cy=500,990; sy=1.45
    bands=[(380,DK),(334,AM),(288,DK),(242,AM)]; bwid=36
    for r,col in bands:
        rr=r-bwid/2
        b.append(f'<path d="M{P(cx-rr,cy)} A{rr:.1f},{rr*sy:.1f} 0 0 1 {P(cx+rr,cy)}" fill="none" stroke="{col}" stroke-width="{bwid}" stroke-linecap="butt"/>')
    # cloud at the left foot: amber puffs with dark outline
    puffs=[(156,1010,58),(226,970,80),(302,1010,58),(190,1055,58),(266,1058,52)]
    b.append(''.join(f'<circle cx="{x}" cy="{y}" r="{r+14}" fill="{DK}"/>' for x,y,r in puffs))
    b.append(''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{AM}"/>' for x,y,r in puffs))
    # pot (cauldron) at the right foot
    px,py=790,1180
    b.append(f'<path d="M{P(px-130,py+120)} L{P(px-150,py+170)} L{P(px-100,py+150)} Z M{P(px+130,py+120)} L{P(px+150,py+170)} L{P(px+100,py+150)} Z" fill="{DK}" stroke="{DK}" stroke-width="14" stroke-linejoin="round"/>')
    for sg in (-1,1): b.append(f'<circle cx="{px+sg*165}" cy="{py-60}" r="30" fill="none" stroke="{DK}" stroke-width="20"/>')
    # coin heap (behind the rim), drawn bottom-up
    heap=[(px-150,py-120),(px-75,py-140),(px,py-148),(px+75,py-140),(px+150,py-120),(px-110,py-185),(px-35,py-205),(px+40,py-205),(px+112,py-185),(px-70,py-255),(px+5,py-268),(px+75,py-250),(px-15,py-325)]
    for (x,y) in heap: b.append(coin_side(x,y,52,28))
    b.append(f'<ellipse cx="{px}" cy="{py+15}" rx="200" ry="150" fill="{DK}"/>')
    b.append(f'<rect x="{px-195}" y="{py-115}" width="390" height="56" rx="28" fill="{DK}"/>')
    b.append(f'<path d="M{P(px-150,py-30)} Q{P(px,py+5)} {P(px+150,py-30)}" fill="none" stroke="{AM}" stroke-width="18" stroke-linecap="round"/>')
    b.append(f'<path d="M{P(px-120,py+40)} Q{P(px-145,py+100)} {P(px-90,py+130)}" fill="none" stroke="{AM}" stroke-width="16" stroke-linecap="round"/>')
    for (x,y,r) in [(520,1330,44),(420,1345,40)]: b.append(coin(x,y,r))
    for (x,y,w_,r) in [(190,260,130,-15),(905,250,120,20),(170,1290,110,10)]: b.append(shamrock(x,y,w_,AM,r))
    for (x,y,r) in [(500,800,30),(543,190,28),(300,440,24),(800,420,24)]: b.append(star4(x,y,r))
    return b

# ---------- 4 Celtic harp (Openclipart 8526 "Celtic Harp" by Gerald_G, Public Domain / CC0) ----------
HARP=f'{OUT}/refs/openclipart_8526_celtic_harp.svg'
def harp():
    b=[]; el=flat(HARP)
    outline=[d for (_,f,d) in el if f=='#000000'][:1]
    frame=[d for (_,f,d) in el if f=='#8d5c25']
    strings=[d for (_,f,d) in el if f=='#000000'][1:8]
    rings=[d for (_,f,d) in el if f=='#c37f33']
    dots=[d for (_,f,d) in el if f=='#000000'][8:]
    s=1040/296.826; ox=(W-245.923*s)/2; oy=200
    g=f'<g fill="{DK}" stroke="{DK}" stroke-width="{2/s:.3f}" stroke-linejoin="round">'+''.join(f'<path d="{d}" fill-rule="evenodd"/>' for d in outline)+''.join(f'<path d="{d}" fill-rule="evenodd"/>' for d in frame+strings)+'</g>'
    g+=f'<g fill="{AM}">'+''.join(f'<path d="{d}" fill-rule="evenodd"/>' for d in rings+dots)+'</g>'
    b.append(f'<g transform="translate({ox:.1f},{oy}) scale({s:.6f})">{g}</g>')
    for (x,y,w_,r) in [(930,1250,130,-15),(560,150,0,0)]:
        if w_: b.append(shamrock(x,y,w_,AM,r))
    for (x,y,r) in [(930,170,28),(760,1340,26),(560,1000,0)]:
        if r: b.append(star4(x,y,r))
    return b

PANELS={'1_four_leaf_clover':clover,'2_leprechaun_hat':hat,'3_pot_of_gold_rainbow':pot_of_gold,'4_celtic_harp':harp}
def render(name,fn):
    s=svg(''.join(fn())); open(f'{OUT}/vectors/st_patricks_{name}.svg','w').write(s)
    rgba=np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode()))).convert('RGBA')).astype(float)
    al=rgba[...,3:4]/255; img=TPL*(1-al)+rgba[...,:3]*al
    img[FR]=TPL[FR]
    Image.fromarray(img.round().astype(np.uint8)).save(f'{OUT}/st_patricks_{name}.png')
    P3=np.array([[192,180,120],[168,96,36],[48,24,0]],float)
    lab=((img[:,:,None,:]-P3[None,None])**2).sum(3).argmin(2).astype(np.uint8)
    Image.fromarray(lab*127).save(f'{OUT}/vectors/st_patricks_{name}_thickness_classes.png')
if __name__=='__main__':
    for n in (sys.argv[1:] or list(PANELS)): render(n,PANELS[n]); print('built',n)

"""2D artwork only (not CAD). Easter v1: four lantern panel concept images.
Panel px 1086x1471 = 77.5x105 mm (14.01 px/mm); origin = top-left of panel outline.
Needs numpy, Pillow, cairosvg, svgelements. Run from anywhere; paths are relative to the bundle root."""
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
def egg_d(cx,cy,w,h,rot=0,n=160):
    a=math.radians(rot); pts=[]
    for i in range(n):
        t=2*math.pi*i/n; y=-h/2*math.cos(t); x=w/2*math.sin(t)*(1-0.14*math.cos(t))
        pts.append(P(cx+x*math.cos(a)-y*math.sin(a),cy+x*math.sin(a)+y*math.cos(a)))
    return 'M'+' L'.join(pts)+' Z'
def zigzag(x0,x1,y,amp,n):
    st=(x1-x0)/n; return 'M'+' L'.join(P(x0+i*st,y+(amp if i%2 else -amp)) for i in range(n+1))
def wave(x0,x1,y,amp,n):
    st=(x1-x0)/n; return f'M{P(x0,y)}'+''.join(f' Q{P(x0+(i+.5)*st,y+(amp if i%2 else -amp))} {P(x0+(i+1)*st,y)}' for i in range(n))
def flower(cx,cy,r,pc=AM,cc=DK,n=5,rot=0):
    s=''.join(f'<ellipse cx="{cx}" cy="{cy-r*0.55:.1f}" rx="{r*0.36:.1f}" ry="{r*0.52:.1f}" fill="{pc}" transform="rotate({rot+k*360/n:.1f} {cx} {cy})"/>' for k in range(n))
    return s+f'<circle cx="{cx}" cy="{cy}" r="{r*0.3:.1f}" fill="{cc}"/>'
def tulip(x,y,h,lean=0,col=AM):
    # stem from (x,y) up h; cup-shaped bloom with three petal points; two broad leaves
    tx,ty=x+lean,y-h
    b=f'<path d="M{P(x,y)} Q{P(x+lean*0.2,y-h*0.5)} {P(tx,ty+30)}" fill="none" stroke="{DK}" stroke-width="16" stroke-linecap="round"/>'
    for sg in (-1,1):
        b+=f'<path d="M{P(x,y)} C{P(x+sg*70,y-40)} {P(x+sg*85,y-h*0.45)} {P(x+sg*60,y-h*0.6)} C{P(x+sg*40,y-h*0.4)} {P(x+sg*14,y-40)} {P(x,y)} Z" fill="{DK}"/>'
    b+=(f'<path d="M{P(tx-42,ty-38)} L{P(tx-20,ty-8)} L{P(tx,ty-46)} L{P(tx+20,ty-8)} L{P(tx+42,ty-38)} '
        f'C{P(tx+48,ty+20)} {P(tx+30,ty+42)} {P(tx,ty+42)} C{P(tx-30,ty+42)} {P(tx-48,ty+20)} {P(tx-42,ty-38)} Z" fill="{col}" stroke="{DK}" stroke-width="10" stroke-linejoin="round"/>')
    return b
def grass(x0,x1,y,h,n,col=DK,seed=0):
    rng=np.random.default_rng(seed); st=(x1-x0)/n; b=''
    for i in range(n):
        x=x0+(i+.5)*st; hh=h*(0.7+0.5*rng.random()); lean=(rng.random()-.5)*h*0.6
        b+=f'<path d="M{P(x-st*0.75,y)} Q{P(x-st*0.2,y-hh*0.55)} {P(x+lean,y-hh)} Q{P(x+st*0.25,y-hh*0.5)} {P(x+st*0.75,y)} Z" fill="{col}" stroke="{col}" stroke-width="8" stroke-linejoin="round"/>'
    return b+f'<rect x="{x0-st*0.6:.1f}" y="{y-6:.1f}" width="{x1-x0+st*1.2:.1f}" height="22" rx="11" fill="{col}"/>'
def deco_egg(cx,cy,w,h,rot,style,uid,base=DK,acc=AM,halo=True):
    b=[]
    if halo: b.append(f'<path d="{egg_d(cx,cy,w,h,rot)}" fill="none" stroke="{CR}" stroke-width="22"/>')
    b.append(f'<path d="{egg_d(cx,cy,w,h,rot)}" fill="{base}"/>')
    b.append(f'<clipPath id="{uid}"><path d="{egg_d(cx,cy,w-36,h-36,rot)}"/></clipPath>')
    g=''; L,R=cx-w,cx+w
    sw=max(12,w*0.07)
    if style=='zig':
        g+=f'<path d="{zigzag(L,R,cy-h*0.08,h*0.08,10)}" fill="none" stroke="{acc}" stroke-width="{sw:.0f}" stroke-linejoin="round"/>'
        g+=f'<rect x="{L}" y="{cy+h*0.14:.1f}" width="{2*w}" height="{sw:.0f}" fill="{acc}"/><rect x="{L}" y="{cy-h*0.32:.1f}" width="{2*w}" height="{sw:.0f}" fill="{acc}"/>'
    elif style=='dots':
        for r_,dy in ((0,-0.22),(1,0.02),(0,0.26)):
            for k in range(-3,4): g+=f'<circle cx="{cx+(k+0.5*r_)*w*0.36:.1f}" cy="{cy+dy*h:.1f}" r="{w*0.085:.1f}" fill="{acc}"/>'
    elif style=='wave':
        for dy in (-0.25,0.0,0.25): g+=f'<path d="{wave(L,R,cy+dy*h,h*0.05,6)}" fill="none" stroke="{acc}" stroke-width="{sw:.0f}" stroke-linecap="round"/>'
    elif style=='stripe':
        for dy in (-0.26,0.22): g+=f'<rect x="{L}" y="{cy+dy*h-sw:.1f}" width="{2*w}" height="{2*sw:.0f}" fill="{acc}"/>'
        for k in range(-2,3): g+=f'<circle cx="{cx+k*w*0.3:.1f}" cy="{cy-0.02*h:.1f}" r="{w*0.08:.1f}" fill="{acc}"/>'
    b.append(f'<g clip-path="url(#{uid})" transform="rotate({rot} {cx} {cy})">{g}</g>')
    return ''.join(b)

def flat(path_svg, ids=None):
    """Flatten a reference SVG to absolute path data (reference viewBox units) with fills."""
    out=[]
    for e in se.SVG.parse(path_svg).elements():
        if isinstance(e,se.Shape):
            p=se.Path(e); p.reify(); out.append((e.id,str(e.fill) if e.fill is not None else None,p.d(),e))
    return out

# ---------- 1 Easter bunny (PhyloPic Oryctolagus cuniculus, Anthony Caravaggi, CC0) ----------
RAB=f'{OUT}/refs/phylopic_d71fcd12-90f6-40c4-b918-0dac0ba3e809_oryctolagus_cuniculus.svg'
def bunny():
    b=[]; sh=[x for x in flat(RAB) if x[1] not in (None,'none')]
    bb=[se.Path(x[2]).bbox() for x in sh]; x0=min(v[0] for v in bb); y0=min(v[1] for v in bb); x1=max(v[2] for v in bb); y1=max(v[3] for v in bb)
    th=930; s=th/(y1-y0); ox=440-(x1-x0)*s/2; oy=1290-th
    tr=f'translate({ox-x0*s:.2f},{oy-y0*s:.2f}) scale({s:.6f})'
    body=''.join(f'<path d="{d}"/>' for _,_,d,_ in sh)
    b.append(f'<g transform="{tr}" fill="{DK}" stroke="{DK}" stroke-width="{4/s:.2f}" stroke-linejoin="round">{body}</g>')
    E=lambda u,v:(ox+u*(x1-x0)*s,oy+v*th)   # fractional position within silhouette bbox
    ex,ey=E(0.215,0.338); b.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="15" fill="{AM}"/>')
    # inner ear (amber) along the standing ear
    e0=E(0.44,0.065); e1=E(0.395,0.205)
    b.append(f'<path d="M{P(*e0)} L{P(*e1)}" stroke="{AM}" stroke-width="22" stroke-linecap="round"/>')
    b.append(grass(110,980,1315,70,20,seed=3))
    b.append(deco_egg(810,1205,120,160,10,'zig','e1'))
    b.append(deco_egg(935,1235,96,128,-12,'dots','e2'))
    b.append(tulip(870,1090,330,lean=-20)); 
    for (x,y,r) in [(200,250,40),(890,420,34),(600,200,30)]: b.append(flower(x,y,r))
    for (x,y,r) in [(800,260,26),(130,1000,0),(960,700,24)]: b.append(star4(x,y,r))
    return b

# ---------- 2 basket of decorated eggs ----------
def basket():
    b=[]; cx=543; top=830; bot=1260; wt=760; wb=520
    # handle (arch) behind
    b.append(f'<path d="M{P(cx-wt/2+40,top)} C{P(cx-wt/2+20,310)} {P(cx+wt/2-20,310)} {P(cx+wt/2-40,top)}" fill="none" stroke="{DK}" stroke-width="56" stroke-linecap="round"/>')
    b.append(f'<path d="M{P(cx-wt/2+40,top-40)} C{P(cx-wt/2+20,310)} {P(cx+wt/2-20,310)} {P(cx+wt/2-40,top-40)}" fill="none" stroke="{AM}" stroke-width="16" stroke-linecap="round" stroke-dasharray="40 26"/>')
    # eggs + grass inside basket, above the rim
    b.append(grass(cx-wt/2+50,cx+wt/2-50,top+10,90,16,seed=5))
    for (x,y,w,h,r,st,u) in [(cx-210,top-90,130,180,-18,'wave','b1'),(cx+215,top-95,130,180,16,'dots','b2'),
                             (cx-70,top-125,140,195,-5,'zig','b3'),(cx+85,top-120,140,195,8,'stripe','b4')]:
        b.append(deco_egg(x,y,w,h,r,st,u))
    # basket bowl
    bowl=f'M{P(cx-wt/2,top)} L{P(cx+wt/2,top)} C{P(cx+wt/2-10,bot-120)} {P(cx+wb/2+40,bot)} {P(cx+wb/2,bot)} L{P(cx-wb/2,bot)} C{P(cx-wb/2-40,bot)} {P(cx-wt/2+10,bot-120)} {P(cx-wt/2,top)} Z'
    b.append(f'<path d="{bowl}" fill="{DK}"/>')
    b.append(f'<clipPath id="bowl"><path d="{bowl}"/></clipPath>')
    g=''; rows=5; rh=(bot-top-70)/rows
    for i in range(rows):
        y=top+60+i*rh+rh/2
        for k in range(-8,9):
            x=cx+k*92+(46 if i%2 else 0)
            g+=f'<rect x="{x-34:.1f}" y="{y-rh*0.28:.1f}" width="68" height="{rh*0.56:.1f}" rx="{rh*0.28:.1f}" fill="{AM}"/>'
    b.append(f'<g clip-path="url(#bowl)">{g}</g>')
    # rim: thick rounded band with amber twist
    b.append(f'<rect x="{cx-wt/2-30}" y="{top-34}" width="{wt+60}" height="68" rx="34" fill="{DK}"/>')
    for k in range(-7,8):
        x=cx+k*52; b.append(f'<path d="M{P(x-16,top+16)} L{P(x+16,top-16)}" stroke="{AM}" stroke-width="16" stroke-linecap="round"/>')
    b.append(grass(170,920,1300,60,16,seed=9))
    for (x,y,r) in [(140,1290,34),(950,1290,34)]: b.append(flower(x,y,r))
    for (x,y,r) in [(170,330,30),(915,330,30),(543,200,26)]: b.append(star4(x,y,r))
    return b

# ---------- 3 large decorated Easter egg ----------
def big_egg():
    b=[]; cx,cy,w,h=543,770,690,940
    b.append(f'<path d="{egg_d(cx,cy,w,h)}" fill="{DK}"/>')
    b.append(f'<clipPath id="big"><path d="{egg_d(cx,cy,w-50,h-50)}"/></clipPath>')
    g=''; L,R=cx-w,cx+w
    g+=''.join(f'<circle cx="{cx+k*76:.1f}" cy="{cy-330}" r="20" fill="{AM}"/>' for k in range(-2,3))
    g+=f'<path d="{zigzag(L,R,cy-215,40,18)}" fill="none" stroke="{AM}" stroke-width="30" stroke-linejoin="miter"/>'
    g+=f'<rect x="{L}" y="{cy-120}" width="{2*w}" height="240" fill="{AM}"/>'
    g+=f'<rect x="{L}" y="{cy-120}" width="{2*w}" height="16" fill="{DK}" transform="translate(0,24)"/><rect x="{L}" y="{cy+80}" width="{2*w}" height="16" fill="{DK}"/>'
    for k in (-2,-1,0,1,2):
        x=cx+k*100; y=cy
        if k%2==0: g+=flower(x,y,74,pc=DK,cc=AM)
        else:
            g+=f'<circle cx="{x}" cy="{y}" r="16" fill="{DK}"/>'
            for sg in (-1,1): g+=f'<path d="M{P(x,y)} C{P(x+sg*28,y-40)} {P(x+sg*52,y-26)} {P(x+sg*50,y)} C{P(x+sg*44,y+14)} {P(x+sg*20,y+10)} {P(x,y)} Z" fill="{DK}"/>'
    g+=f'<path d="{wave(L,R,cy+200,34,12)}" fill="none" stroke="{AM}" stroke-width="30" stroke-linecap="round"/>'
    g+=''.join(f'<circle cx="{cx+k*76:.1f}" cy="{cy+310}" r="22" fill="{AM}"/>' for k in range(-3,4))
    b.append(f'<g clip-path="url(#big)">{g}</g>')
    b.append(grass(200,890,1290,80,18,seed=11))
    b.append(tulip(150,1285,260,lean=18)); b.append(tulip(940,1285,240,lean=-18))
    for (x,y,r) in [(170,260,34),(920,250,30),(950,820,26),(135,760,26)]: b.append(star4(x,y,r))
    return b

# ---------- 4 chick hatching (Openclipart 131089 "Funny Chick Cartoon Newborn Coming Out from the Egg", palomaironique, PD/CC0) ----------
CHK=f'{OUT}/refs/openclipart_131089_chick_from_egg.svg'
def chick():
    b=[]; el={i:x for i,x in enumerate(flat(CHK))}
    byid={x[0]:x for x in el.values()}
    s=6.0; ox,oy=543-150.79*s/2,373
    def grp(ids,fill,stroke=None,sw=0):
        body=''.join(f'<path d="{byid[i][2]}"/>' for i in ids)
        st=f' stroke="{stroke}" stroke-width="{sw/s:.3f}" stroke-linejoin="round"' if stroke else ''
        return f'<g fill="{fill}"{st}>{body}</g>'
    inner=['text2216','path2229']; cap=['path2345']; front=['text2193']
    tips=['path4169-0-2-6','path4169-2-6-3-2','path4169-2-7-3-6-9','path4169-0-9','path4169-2-6-1','path4169-2-7-3-9']
    wings=['path4166-2-8','path4166-8']; bodyp=['path4205-2-44-5-4-0']; head=['path4205-2-4-4']
    g=''
    g+=grp(inner,DK,DK,6)
    g+=grp(wings,DK,DK,26)+grp(bodyp+head,DK,DK,26)        # dark outline underlay
    g+=grp(wings,AM)+grp(bodyp,AM)+grp(head,AM)
    g+=f'<path d="{byid["path4205-2-4-4"][2]}" fill="none" stroke="{DK}" stroke-width="{12/s:.3f}"/>'  # head/body separation
    g+=grp(['path5068-6-8-0-9-7-1-0','path5068-6-8-0-9-4-2'],DK,DK,12)
    g+=grp(['path5060-6-7-9-8-9','path5068-6-8-0-8-1'],CR)
    g+=grp(['path5062-8-8-5-3-7','path5070-1-0-0-4-8'],DK)
    g+=grp(['path5064-5-2-8-1-4','path5072-8-2-0-9-0'],CR)
    g+=grp(['path4013-0-5'],DK,DK,6)
    # front shell: halo, dark shell, amber Easter-egg decoration clipped inside
    g+=grp(front,'none',CR,32)+grp(front,DK,DK,6)
    CAPR=float(os.environ.get('CAPR','-38'))   # tilt the loose shell cap so its cracked edge faces up
    cg=grp(cap,'none',CR,32)+grp(cap,DK,DK,6)
    g+=f'<clipPath id="fs"><path d="{byid["text2193"][2]}"/></clipPath><clipPath id="cs"><path d="{byid["path2345"][2]}"/></clipPath>'
    g+=f'<g clip-path="url(#fs)"><path d="{zigzag(0,80,104,5,10)}" fill="none" stroke="{AM}" stroke-width="{24/s:.2f}"/>'
    g+=''.join(f'<circle cx="{x}" cy="117" r="{13/s:.2f}" fill="{AM}"/>' for x in (16,28,40,52,64))+'</g>'
    cg+=f'<g clip-path="url(#cs)"><path d="{zigzag(80,150,112,5,9)}" fill="none" stroke="{AM}" stroke-width="{24/s:.2f}" transform="rotate(28 118 110)"/></g>'
    g+=f'<g transform="translate(7,0) rotate({CAPR} 117 128)">{cg}</g>'
    b.append(f'<g transform="translate({ox:.1f},{oy}) scale({s})">{g}</g>')
    b.append(grass(110,980,1225,70,20,seed=21))
    for (x,y,r) in [(180,250,40),(905,270,36)]: b.append(flower(x,y,r))
    for (x,y,r) in [(543,190,28),(950,560,26),(140,1350-30,0)]: 
        if r: b.append(star4(x,y,r))
    return b

PANELS={'1_easter_bunny':bunny,'2_egg_basket':basket,'3_decorated_egg':big_egg,'4_hatching_chick':chick}
def render(name,fn):
    s=svg(''.join(fn())); open(f'{OUT}/vectors/easter_{name}.svg','w').write(s)
    rgba=np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode()))).convert('RGBA')).astype(float)
    al=rgba[...,3:4]/255; img=TPL*(1-al)+rgba[...,:3]*al
    img[FR]=TPL[FR]
    Image.fromarray(img.round().astype(np.uint8)).save(f'{OUT}/easter_{name}.png')
    P3=np.array([[192,180,120],[168,96,36],[48,24,0]],float)
    lab=((img[:,:,None,:]-P3[None,None])**2).sum(3).argmin(2).astype(np.uint8)
    Image.fromarray(lab*127).save(f'{OUT}/vectors/easter_{name}_thickness_classes.png')
if __name__=='__main__':
    for n in (sys.argv[1:] or list(PANELS)): render(n,PANELS[n]); print('built',n)

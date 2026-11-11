"""2D artwork only (not CAD). Fourth of July v2 (panel 1 changed to a 50-star canton; panels 2-4 identical to v1): four lantern panel concept images.
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
def star5_d(cx,cy,r,rot=0,inner=0.45):
    pts=[]
    for k in range(10):
        a=math.radians(rot+k*36); rr=r if k%2==0 else r*inner
        pts.append(P(cx+rr*math.sin(a),cy-rr*math.cos(a)))
    return 'M'+' L'.join(pts)+' Z'
def star5(cx,cy,r,col=AM,rot=0,sw=8):
    return f'<path d="{star5_d(cx,cy,r,rot)}" fill="{col}" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/>'

# ---------- 1 waving American flag on a pole, with a star-centred bunting fan below ----------
def flag():
    b=[]; x0,x1=200,985; y0=230; fh=572; n=13; amp=30
    def wy(x,y):   # wave displacement grows from the pole outwards
        u=(x-x0)/(x1-x0); return y+amp*u*math.sin(2*math.pi*(u*1.25)+0.3)+ (y-y0-fh/2)*0.06*u
    xs=np.linspace(x0,x1,60)
    def band(ya,yb,xa=x0,xb=x1):
        xx=np.linspace(xa,xb,60)
        top=[P(x,wy(x,ya)) for x in xx]; bot=[P(x,wy(x,yb)) for x in xx[::-1]]
        return 'M'+' L'.join(top+bot)+' Z'
    sh=fh/n
    b.append(f'<path d="{band(y0,y0+fh)}" fill="{DK}" stroke="{DK}" stroke-width="10" stroke-linejoin="round"/>')
    for i in range(n):
        if i%2==1: b.append(f'<path d="{band(y0+i*sh+3,y0+(i+1)*sh-3,x0,x1-10)}" fill="{AM}"/>')
    # canton: dark field over stripes 0-6, with amber five-point stars (rows of 5 / 4)
    cw=float(os.environ.get('CANTON_W','440')); ch=7*sh
    b.append(f'<path d="{band(y0,y0+ch,x0,x0+cw)}" fill="{DK}"/>')
    b.append(f'<path d="{band(y0+ch-4,y0+ch+6,x0,x0+cw)}" fill="{DK}"/>')
    # 50 stars, real US layout: 9 staggered rows alternating 6 and 5 (6-5-6-5-6-5-6-5-6) on an 11 x 9 half-grid
    SR=float(os.environ.get('STAR_R','17.5'))
    for r in range(9):
        for c in range(11):
            if (r+c)%2: continue
            sx=x0+cw*(c+1)/12; sy=y0+ch*(r+1)/10
            b.append(star5(sx,wy(sx,sy),SR,AM,sw=4))
    # pole with ball finial and base
    b.append(f'<rect x="168" y="200" width="30" height="1150" rx="12" fill="{DK}"/>')
    b.append(f'<circle cx="183" cy="190" r="34" fill="{AM}" stroke="{DK}" stroke-width="12"/>')
    for yy in (y0+12,y0+fh-12): b.append(f'<rect x="160" y="{yy-12}" width="48" height="24" rx="8" fill="{DK}"/>')
    # bunting fan (half-rosette): alternating dark/amber pleats, star medallion
    fx,fy,fr=560,1000,300
    k=10
    for i in range(k):
        a0=math.pi*i/k; a1=math.pi*(i+1)/k
        pts=[P(fx,fy)]+[P(fx-fr*math.cos(a0+(a1-a0)*t/8),fy+fr*math.sin(a0+(a1-a0)*t/8)) for t in range(9)]
        b.append(f'<path d="M{" L".join(pts)} Z" fill="{DK if i%2==0 else AM}" stroke="{DK}" stroke-width="6" stroke-linejoin="round"/>')
    b.append(f'<path d="M{P(fx-fr-20,fy)} L{P(fx+fr+20,fy)}" stroke="{DK}" stroke-width="30" stroke-linecap="round"/>')
    scal=''.join(f'<circle cx="{fx-fr*math.cos(math.pi*(i+.5)/k):.1f}" cy="{fy+fr*math.sin(math.pi*(i+.5)/k):.1f}" r="34" fill="{DK}"/>' for i in range(k))
    b.append(f'<path d="M{P(fx-fr,fy)} A{fr},{fr} 0 0 0 {P(fx+fr,fy)}" fill="none" stroke="{DK}" stroke-width="26"/>')   # rim
    b.append(f'<circle cx="{fx}" cy="{fy+8}" r="92" fill="{DK}"/>'+star5(fx,fy+16,70,AM,sw=10))
    for (x,y,r) in [(340,1380-60,30),(800,1380-60,30)]: b.append(star5(x,y,r,AM))
    for (x,y,r) in [(950,170,26),(560,170,24)]: b.append(star4(x,y,r))
    return b

# ---------- 2 fireworks over a small-town skyline ----------
def fireworks():
    b=[]
    # A: peony burst of concentric dot rings (amber/dark alternating), star centre
    cx,cy=360,580
    for (r,nd,dr,col) in [(70,9,15,AM),(135,14,17,DK),(200,20,18,AM),(262,24,15,DK)]:
        for k in range(nd):
            a=2*math.pi*k/nd+(0.15 if col==DK else 0)
            b.append(f'<circle cx="{cx+r*math.cos(a):.1f}" cy="{cy+r*math.sin(a):.1f}" r="{dr}" fill="{col}"/>')
    b.append(star5(cx,cy,42,DK,sw=10))
    # B: star-spangled burst: inner dark dot ring, outer ring of amber five-point stars
    wx,wy=790,320
    for k in range(10):
        a=2*math.pi*k/10
        b.append(f'<path d="M{P(wx+52*math.cos(a),wy+52*math.sin(a))} L{P(wx+100*math.cos(a),wy+100*math.sin(a))}" stroke="{DK}" stroke-width="16" stroke-linecap="round"/>')
        b.append(star5(wx+160*math.cos(a),wy+160*math.sin(a),28,AM,rot=math.degrees(a)+90,sw=8))
    b.append(f'<circle cx="{wx}" cy="{wy}" r="22" fill="{AM}" stroke="{DK}" stroke-width="10"/>')
    # C: small ring burst lower right
    rx,ry=820,790
    for k in range(12):
        a=2*math.pi*k/12
        b.append(f'<path d="M{P(rx+56*math.cos(a),ry+56*math.sin(a))} L{P(rx+115*math.cos(a),ry+115*math.sin(a))}" stroke="{AM}" stroke-width="18" stroke-linecap="round"/>')
    b.append(f'<circle cx="{rx}" cy="{ry}" r="20" fill="{DK}"/>')
    # rising trail for C (curved dotted line of amber diamonds)
    for t in np.linspace(0.0,1.0,6):
        x=rx+135*t**1.6; y=ry+150+(1150-ry-150)*t
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{DK}"/>')
    # skyline: row houses with gables, a domed hall with flag, trees; amber windows
    base=1385; g=[]
    g.append(f'<rect x="80" y="{base-90}" width="926" height="90" fill="{DK}"/>')
    houses=[(85,150,170),(230,130,215),(355,170,165)]
    for (x,w,h) in houses:
        g.append(f'<path d="M{P(x,base)} L{P(x,base-h)} L{P(x+w/2,base-h-70)} L{P(x+w,base-h)} L{P(x+w,base)} Z" fill="{DK}"/>')
    # domed hall (capitol-like)
    hx,hw=545,250
    g.append(f'<rect x="{hx}" y="{base-170}" width="{hw}" height="170" fill="{DK}"/>')
    g.append(f'<rect x="{hx+60}" y="{base-230}" width="{hw-120}" height="70" fill="{DK}"/>')
    g.append(f'<path d="M{P(hx+65,base-228)} A{(hw-130)/2},{(hw-130)/2*0.95} 0 0 1 {P(hx+hw-65,base-228)} Z" fill="{DK}"/>')
    g.append(f'<rect x="{hx+hw/2-10}" y="{base-385}" width="20" height="80" fill="{DK}"/>')
    g.append(f'<path d="M{P(hx+hw/2+10,base-385)} L{P(hx+hw/2+80,base-370)} L{P(hx+hw/2+10,base-345)} Z" fill="{DK}" stroke="{DK}" stroke-width="8" stroke-linejoin="round"/>')
    for (x,w,h) in [(805,100,140),(905,100,200)]:
        g.append(f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" fill="{DK}"/>')
    for (x,r) in [(520,46),(830,0)]:
        if r: g.append(f'<circle cx="{x}" cy="{base-120}" r="{r}" fill="{DK}"/><rect x="{x-8}" y="{base-120}" width="16" height="100" fill="{DK}"/>')
    b+=g
    win=[]
    for (x,w,h) in houses:
        for j in range(2):
            win.append((x+w*0.22+j*w*0.36, base-h+40, w*0.2, 44))
        win.append((x+w/2-14, base-h-30, 28, 28))
    for k in range(4): win.append((hx+22+k*58, base-130, 30, 70))
    for (x,w,h) in [(805,100,140),(905,100,200)]:
        for r_ in range(int((h-40)//60)):
            win.append((x+22, base-h+30+r_*60, w-44, 30))
    for (x,y,w,h) in win: b.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="4" fill="{AM}"/>')
    for (x,y,r) in [(160,1000,26),(960,600,24),(600,900,26),(560,150,26),(170,190,26)]: b.append(star4(x,y,r))
    return b

# ---------- 3 soaring bald eagle (PhyloPic 3002e4de, Andy Wilson, CC0) ----------
EAG=f'{OUT}/refs/phylopic_3002e4de-eb9b-48a4-8921-57dfe0d2e169_haliaeetus_leucocephalus.svg'
def eagle():
    b=[]; els=[e for e in se.SVG.parse(EAG).elements() if isinstance(e,se.Shape)]
    p=se.Path(els[0]); p.reify(); subs=[se.Path(sp).d() for sp in p.as_subpaths()]
    eye=se.Path(els[1]); eye.reify()
    x0,y0,x1,y1=se.Path(subs[0]).bbox()
    s=1130/(y1-y0); ox=(W-(x1-x0)*s)/2-x0*s+10; oy=165-y0*s
    tr=f'translate({ox:.2f},{oy:.2f}) scale({s:.6f})'
    g=f'<path d="{subs[0]}" fill="{DK}" stroke="{DK}" stroke-width="{5/s:.2f}" stroke-linejoin="round"/>'
    for d in subs[1:]:   # white head and tail -> amber, with a firm dark outline
        g+=f'<path d="{d}" fill="{AM}" stroke="{DK}" stroke-width="{10/s:.2f}" stroke-linejoin="round"/>'
    ex,ey=(eye.bbox()[0]+eye.bbox()[2])/2,(eye.bbox()[1]+eye.bbox()[3])/2
    g+=f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{12/s:.1f}" fill="{DK}"/>'
    b.append(f'<g transform="{tr}">{g}</g>')
    for (x,y,r) in [(860,280,44),(720,170,30),(930,470,30),(190,1080,40),(300,1240,30),(140,900,28)]: b.append(star5(x,y,r,AM))
    return b

# ---------- 4 Liberty Bell with its crack, hanging from its yoke ----------
def liberty_bell():
    b=[]; cx=543
    # yoke: heavy wooden beam with shaped ends and amber grain lines
    yk=f'M{P(cx-330,330)} L{P(cx+330,330)} Q{P(cx+360,330)} {P(cx+360,360)} L{P(cx+360,400)} Q{P(cx+360,430)} {P(cx+330,430)} L{P(cx-330,430)} Q{P(cx-360,430)} {P(cx-360,400)} L{P(cx-360,360)} Q{P(cx-360,330)} {P(cx-330,330)} Z'
    b.append(f'<path d="{yk}" fill="{DK}"/>')
    b.append(f'<path d="M{P(cx-300,365)} Q{P(cx-100,355)} {P(cx-20,368)}" fill="none" stroke="{AM}" stroke-width="12" stroke-linecap="round"/>')
    b.append(f'<path d="M{P(cx+40,398)} Q{P(cx+160,388)} {P(cx+300,398)}" fill="none" stroke="{AM}" stroke-width="12" stroke-linecap="round"/>')
    for sg in (-1,1): b.append(f'<rect x="{cx+sg*300-22}" y="300" width="44" height="160" rx="10" fill="{DK}"/>')
    # crown / hanger straps
    b.append(f'<rect x="{cx-80}" y="420" width="160" height="90" rx="20" fill="{DK}"/>')
    b.append(f'<rect x="{cx-40}" y="440" width="80" height="30" rx="10" fill="{AM}"/>')
    # bell profile
    bell=(f'M{P(cx,490)} C{P(cx+110,490)} {P(cx+175,520)} {P(cx+185,620)} C{P(cx+195,780)} {P(cx+215,900)} {P(cx+310,1010)} '
          f'Q{P(cx+345,1045)} {P(cx+335,1090)} L{P(cx-335,1090)} Q{P(cx-345,1045)} {P(cx-310,1010)} '
          f'C{P(cx-215,900)} {P(cx-195,780)} {P(cx-185,620)} C{P(cx-175,520)} {P(cx-110,490)} {P(cx,490)} Z')
    b.append(f'<path d="{bell}" fill="{DK}"/>')
    b.append(f'<clipPath id="bell"><path d="{bell}"/></clipPath>')
    g=''
    for (y,h) in [(600,18),(640,18),(990,20),(1040,26)]: g+=f'<rect x="0" y="{y}" width="{W}" height="{h}" fill="{AM}"/>'
    g+=f'<path d="M{P(cx-150,560)} Q{P(cx-170,700)} {P(cx-120,900)}" fill="none" stroke="{AM}" stroke-width="16" stroke-linecap="round"/>'   # highlight
    b.append(f'<g clip-path="url(#bell)">{g}</g>')
    # the crack: jagged cream line rising from the lip, right of centre
    crack=[(cx+40,1092),(cx+25,1040),(cx+48,990),(cx+20,935),(cx+52,880),(cx+28,825),(cx+55,770),(cx+38,720),(cx+60,680)]
    b.append(f'<path d="M{" L".join(P(*p) for p in crack)}" fill="none" stroke="{CR}" stroke-width="18" stroke-linejoin="round" stroke-linecap="round"/>')
    # clapper peeking below the lip
    b.append(f'<rect x="{cx-14}" y="1085" width="28" height="70" fill="{DK}"/><circle cx="{cx}" cy="1170" r="38" fill="{DK}"/><circle cx="{cx}" cy="1170" r="18" fill="{AM}"/>')
    for (x,y,r) in [(170,620,36),(915,620,36),(150,1260,32),(935,1260,32),(543,1320,40),(350,1290,26),(740,1290,26)]: b.append(star5(x,y,r,AM))
    for (x,y,r) in [(200,190,26),(890,190,26),(543,200,28)]: b.append(star4(x,y,r))
    return b

PANELS={'1_waving_flag':flag,'2_fireworks_skyline':fireworks,'3_bald_eagle':eagle,'4_liberty_bell':liberty_bell}
def render(name,fn):
    s=svg(''.join(fn())); open(f'{OUT}/vectors/july_fourth_{name}.svg','w').write(s)
    rgba=np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode()))).convert('RGBA')).astype(float)
    al=rgba[...,3:4]/255; img=TPL*(1-al)+rgba[...,:3]*al
    img[FR]=TPL[FR]
    Image.fromarray(img.round().astype(np.uint8)).save(f'{OUT}/july_fourth_{name}.png')
    P3=np.array([[192,180,120],[168,96,36],[48,24,0]],float)
    lab=((img[:,:,None,:]-P3[None,None])**2).sum(3).argmin(2).astype(np.uint8)
    Image.fromarray(lab*127).save(f'{OUT}/vectors/july_fourth_{name}_thickness_classes.png')
if __name__=='__main__':
    for n in (sys.argv[1:] or list(PANELS)): render(n,PANELS[n]); print('built',n)

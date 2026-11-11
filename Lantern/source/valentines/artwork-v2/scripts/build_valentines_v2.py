"""2D artwork only (not CAD). Valentine's v2: builds panels 3 (box of chocolates) and 4 (Cupid).
Panels 1-2 are byte-identical copies of v1 (see build_valentines_v1_reference_panels_1_2.py).
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
    s=w/32.0; pts=[]; a=math.radians(rot)
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
def svg(body): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'
def scallop(cx,cy,r,n,br,col):
    s=''.join(f'<circle cx="{cx+r*math.cos(2*math.pi*k/n):.1f}" cy="{cy+r*math.sin(2*math.pi*k/n):.1f}" r="{br}" fill="{col}"/>' for k in range(n))
    return s+f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/>'

# ---------- 3 heart-shaped box of chocolates ----------
def chocolates():
    b=[]
    # lid propped up behind the box, tilted
    lx,ly,lw,lr=440,520,600,-22
    b.append(heart(lx,ly,lw,DK,lr))
    b.append(f'<path d="{heart_d(lx,ly,lw-70,lr)}" fill="none" stroke="{AM}" stroke-width="14"/>')
    # ribbon across the lid (amber bands clipped to lid) + bow
    b.append(f'<clipPath id="lid"><path d="{heart_d(lx,ly,lw-100,lr)}"/></clipPath>')
    b.append(f'<g clip-path="url(#lid)" transform="rotate({lr} {lx} {ly})"><rect x="{lx-22}" y="{ly-400}" width="44" height="800" fill="{AM}"/></g>')
    bx,by=lx-8,ly-40
    g=''
    for sg in (1,-1):
        g+=f'<path d="M0,0 C{P(sg*40,-80)} {P(sg*140,-70)} {P(sg*125,-10)} C{P(sg*115,35)} {P(sg*50,20)} 0,0 Z" fill="{AM}"/>'
        g+=f'<path d="M{P(sg*28,-8)} C{P(sg*55,-48)} {P(sg*100,-42)} {P(sg*95,-14)} C{P(sg*90,8)} {P(sg*55,4)} {P(sg*28,-8)} Z" fill="{DK}"/>'
        g+=f'<path d="M{P(sg*6,12)} C{P(sg*30,60)} {P(sg*45,95)} {P(sg*70,140)} L{P(sg*38,146)} L{P(sg*48,170)} C{P(sg*20,120)} {P(sg*8,75)} {P(-sg*6,18)} Z" fill="{AM}" stroke="{AM}" stroke-width="4" stroke-linejoin="round"/>'
    g+=f'<ellipse cx="0" cy="0" rx="30" ry="26" fill="{AM}"/>'
    b.append(f'<g transform="translate({bx},{by}) rotate({lr})">{g}</g>')
    # box base: halo to separate from lid, dark rim, amber tray
    cx,cy,bw=543,905,700
    b.append(f'<path d="{heart_d(cx,cy,bw)}" fill="none" stroke="{CR}" stroke-width="26"/>')
    b.append(heart(cx,cy,bw,DK)); b.append(heart(cx,cy,bw-96,AM))
    pcs=[(-150,-80,'c'),(150,-80,'h'),(-205,45,'h'),(-70,45,'c'),(70,45,'s'),(205,45,'c'),(-115,175,'s'),(115,175,'h'),(0,295,'c')]
    for dx,dy,k in pcs:
        x,y=cx+dx,cy+dy
        b.append(scallop(x,y,58,14,12,CR))        # paper cup (cream ruffle)
        if k=='c':   # round truffle with amber swirl
            b.append(f'<circle cx="{x}" cy="{y}" r="50" fill="{DK}"/>')
            b.append(f'<path d="M{P(x-26,y+4)} C{P(x-20,y-28)} {P(x+22,y-28)} {P(x+24,y-2)} C{P(x+24,y+18)} {P(x-4,y+20)} {P(x-4,y+2)}" fill="none" stroke="{AM}" stroke-width="10" stroke-linecap="round"/>')
        elif k=='h': # heart chocolate with amber drizzle
            b.append(heart(x,y-2,104,DK))
            b.append(f'<path d="M{P(x-26,y-14)} Q{P(x-8,y+4)} {P(x+4,y-14)} T{P(x+28,y-12)}" fill="none" stroke="{AM}" stroke-width="10" stroke-linecap="round"/>')
        else:        # square bonbon with amber stripes
            b.append(f'<rect x="{x-44}" y="{y-44}" width="88" height="88" rx="18" fill="{DK}"/>')
            for o in (-16,14): b.append(f'<path d="M{P(x-24,y+o)} L{P(x+24,y+o-10)}" stroke="{AM}" stroke-width="10" stroke-linecap="round"/>')
    for (x,y,w,c,r) in [(860,260,120,AM,12),(170,1230,90,AM,-12),(930,1260,80,DK,12),(900,470,70,DK,14)]:
        b.append(heart(x,y,w,c,rot=r))
    for (x,y,r) in [(170,260,30),(735,190,26),(543,1345,28)]: b.append(star4(x,y,r))
    return b

# ---------- 4 Cupid (GDJ "Martin74's Cupid Silhouette", Openclipart 244366, CC0) ----------
CUPID=open(f'{OUT}/refs/openclipart_244366_martin74s_cupid_silhouette.svg').read()
CUPID=CUPID[CUPID.index('<path'):CUPID.rindex('</svg>')]
CV=1590.8513/900.0   # source viewBox units per 900-px reference render px
def cupid():
    b=[]; s=1.0/CV*1.0   # 1 reference-render px = 1 panel px
    ox,oy=75,250        # panel position of reference render origin
    tr=f'translate({ox},{oy}) scale({s:.6f})'
    # silhouette with a 5 px dark outline stroke so feather tips and curls are not hairlines
    # remove the two pointed hair tufts (read as horns) and round the hairline with curls
    def rr(x0,y0,x1,y1): return f'M{x0*CV:.1f},{y0*CV:.1f} L{x1*CV:.1f},{y0*CV:.1f} L{x1*CV:.1f},{y1*CV:.1f} L{x0*CV:.1f},{y1*CV:.1f} Z'
    q=lambda x,y:f'{x*CV:.1f},{y*CV:.1f}'
    clip=(f'<clipPath id="hair"><path d="M-100,-100 L{q(330,-60)} L{q(330,64)} L{q(364,64)} L{q(364,-60)} L{q(476,-60)} L{q(476,96)} '
          f'L{q(560,96)} L{q(560,-60)} L3000,-100 L3000,3000 L-100,3000 Z"/></clipPath>')
    b.append(f'<g transform="{tr}">{clip}<g clip-path="url(#hair)" fill="{DK}" stroke="{DK}" stroke-width="{5/s:.2f}" stroke-linejoin="round">{CUPID}</g></g>')
    for (x,y,r) in [(474,94,28),(500,112,22),(368,66,16),(352,84,14)]:
        X,Y=ox+x,oy+y; b.append(f'<circle cx="{X}" cy="{Y}" r="{r}" fill="{DK}"/>')
    R=lambda x,y:(ox+x,oy+y)
    # thicker bowstring (drawn back to the hand) and arrow shaft over the thin originals
    t1,hnd,t2=R(624,130),R(600,392),R(684,570)
    b.append(f'<path d="M{P(*t1)} L{P(*hnd)} L{P(*t2)}" fill="none" stroke="{DK}" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"/>')
    a0,a1=R(745,326),R(850,298)
    b.append(f'<path d="M{P(*a0)} L{P(*a1)}" stroke="{DK}" stroke-width="14" stroke-linecap="round"/>')
    ang=math.degrees(math.atan2(a1[1]-a0[1],a1[0]-a0[0]))
    b.append(heart(a1[0]+22,a1[1]-6,78,DK,rot=ang-90))
    b.append(heart(a1[0]+22,a1[1]-6,40,AM,rot=ang-90))
    # amber eye
    ex,ey=R(490,152); b.append(f'<circle cx="{ex}" cy="{ey}" r="9" fill="{AM}"/>')
    for (x,y,w,c,r) in [(840,220,110,AM,12),(690,1250,80,AM,10),(200,1260,90,DK,-12),(920,1080,70,DK,14),(160,215,70,AM,-12)]:
        b.append(heart(x,y,w,c,rot=r))
    for (x,y,r) in [(500,175,28),(930,560,28),(420,1330,26)]: b.append(star4(x,y,r))
    return b

PANELS={'3_box_of_chocolates':chocolates,'4_cupid':cupid}
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

"""2D artwork only (not CAD). Builds New Year's v1 panel images from SVG motifs.
Panel px: 1086x1471 = 77.5x105 mm (14.01 px/mm), origin top-left of panel outline."""
import math, io, os, sys
import numpy as np, cairosvg
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W,H=1086,1471
DK='#301800'; AM='#a86024'; CR='#c0b478'
TPL=np.array(Image.open(f'{OUT}/vectors/panel_template_blank.png').convert('RGB')).astype(float)
FONT=TTFont('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
GS=FONT.getGlyphSet(); CMAP=FONT.getBestCmap(); UPM=FONT['head'].unitsPerEm
def P(x,y): return f'{x:.1f},{y:.1f}'
def text_path(s,cx,cy,h,rot=0):
    # glyph outlines -> path, centred at (cx,cy), cap height ~h
    sc=h/1458.0  # DejaVu Bold digit height ~1458 units
    adv=sum(GS[CMAP[ord(c)]].width for c in s)*sc
    pen=SVGPathPen(GS); x0=-adv/2
    for c in s:
        g=GS[CMAP[ord(c)]]
        tp=TransformPen(pen,(sc,0,0,-sc,x0,h/2)); g.draw(tp); x0+=g.width*sc
    return f'<path transform="translate({cx},{cy}) rotate({rot})" d="{pen.getCommands()}"/>'
def star4(cx,cy,r,w=0.28,rot=0,col=AM):
    pts=[]
    for k in range(8):
        a=math.radians(rot+k*45); rr=r if k%2==0 else r*w
        pts.append(P(cx+rr*math.sin(a),cy-rr*math.cos(a)))
    return f'<path d="M{" L".join(pts)} Z" fill="{col}" stroke="{col}" stroke-width="10" stroke-linejoin="round"/>'
def spindle(cx,cy,ang,r0,r1,wmax,tmax=0.7,wmin=13):
    # tapered ray from r0 to r1, widest at tmax
    a=math.radians(ang); ux,uy=math.sin(a),-math.cos(a); nx,ny=-uy,ux
    pts=[]; N=24
    side=[]
    for i in range(N+1):
        t=i/N; r=r0+(r1-r0)*t
        w=wmax*(t/tmax if t<tmax else 1-(t-tmax)/(1-tmax)*0.55)
        w=max(w,wmin); side.append((r,w/2))
    L=[P(cx+ux*r+nx*h,cy+uy*r+ny*h) for r,h in side]
    R=[P(cx+ux*r-nx*h,cy+uy*r-ny*h) for r,h in reversed(side)]
    return f'<path d="M{" L".join(L+R)} Z" stroke-linejoin="round"/>'
def svg(body): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'

def burst(cx,cy,R,n,phase=0,amber_sparks=True):
    d=[];a=[]
    for k in range(n):
        ang=phase+k*360/n; long=(k%2==0)
        r1=R if long else R*0.78
        d.append(spindle(cx,cy,ang,R*0.2,r1*0.86,max(20,R*0.095)))
        tx,ty=cx+r1*math.sin(math.radians(ang)),cy-r1*math.cos(math.radians(ang))
        d.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="{max(11,R*0.055):.1f}"/>')
        if amber_sparks and not long:
            rr=R*1.0; t2=math.radians(ang)
            a.append(f'<circle cx="{cx+rr*math.sin(t2):.1f}" cy="{cy-rr*math.cos(t2):.1f}" r="{max(8,R*0.035):.1f}"/>')
    d.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.16:.1f}"/>')
    a.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.07:.1f}"/>')
    return ''.join(d),''.join(a)
def trail(p0,p1,p2,n=9,r0=7,r1=14,gap=0.35):
    out=[]
    for i in range(n):
        for j in range(6):
            t=(i+j/6*(1-gap))/n
            x=(1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0]; y=(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]
            r=r0+(r1-r0)*(t)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"/>')
    return ''.join(out)

def fireworks():
    d=[];a=[]
    for (cx,cy,R,n,ph) in [(543,410,280,18,0),(265,900,160,14,8),(820,840,175,14,4)]:
        dd,aa=burst(cx,cy,R,n,ph); d.append(dd); a.append(aa)
    d.append(trail((560,1360),(450,960),(540,730),n=7,r0=9,r1=13))
    d.append(trail((320,1365),(220,1210),(265,1090),n=4,r0=9,r1=12))
    d.append(trail((760,1365),(870,1200),(820,1045),n=4,r0=9,r1=12))
    for (x,y,r) in [(150,230,44),(935,250,40),(420,1180,36),(950,1180,40),(130,620,38),(950,580,34)]:
        a.append(star4(x,y,r,0.34))
    return d,a

def clock():
    cx,cy=543,740; d=[];a=[]
    d.append(f'<circle cx="{cx}" cy="{cy}" r="400" fill="none" stroke="{DK}" stroke-width="46"/>')
    a.append(f'<circle cx="{cx}" cy="{cy}" r="352" fill="none" stroke="{AM}" stroke-width="14"/>')
    for k in range(12):
        ang=math.radians(k*30)
        if k%3==0: continue
        r=300; d.append(f'<circle cx="{cx+r*math.sin(ang):.1f}" cy="{cy-r*math.cos(ang):.1f}" r="20"/>')
    for k in range(60):
        if k%5==0: continue
        ang=math.radians(k*6); r=330
        a.append(f'<circle cx="{cx+r*math.sin(ang):.1f}" cy="{cy-r*math.cos(ang):.1f}" r="8"/>')
    for s,ang in [('12',0),('3',90),('6',180),('9',270)]:
        r=262 if s!='12' else 258
        d.append(text_path(s,cx+r*math.sin(math.radians(ang)),cy-r*math.cos(math.radians(ang)),96))
    # hour hand (short, broad, spade tip) and minute hand (long, slim) both at 12
    d.append(f'<path d="M{P(cx-22,cy+40)} L{P(cx-22,cy-95)} L{P(cx-46,cy-120)} L{P(cx,cy-165)} L{P(cx+46,cy-120)} L{P(cx+22,cy-95)} L{P(cx+22,cy+40)} Z" stroke-linejoin="round"/>')
    d.append(f'<path d="M{P(cx-13,cy+70)} L{P(cx-14,cy-160)} L{P(cx,cy-200)} L{P(cx+14,cy-160)} L{P(cx+13,cy+70)} Z"/>')
    d.append(f'<circle cx="{cx}" cy="{cy}" r="40"/>')
    a.append(f'<circle cx="{cx}" cy="{cy}" r="16"/>')
    a.append(f'<path d="M{P(cx-14,cy-120)} L{P(cx,cy-145)} L{P(cx+14,cy-120)} L{P(cx,cy-104)} Z"/>')
    # crown knob and bell feet
    d.append(f'<rect x="{cx-34}" y="{cy-470}" width="68" height="40" rx="10"/>')
    d.append(f'<circle cx="{cx}" cy="{cy-482}" r="26"/>')
    for sgn in (-1,1):
        x=cx+sgn*230
        d.append(f'<path d="M{P(x-sgn*30,cy+315)} L{P(x+sgn*40,cy+420)} L{P(x+sgn*70,cy+420)} L{P(x+sgn*20,cy+300)} Z" stroke-linejoin="round"/>')
    for (x,y,r) in [(150,190,44),(935,215,40),(150,1300,40),(935,1290,44),(543,1340,36)]:
        a.append(star4(x,y,r,0.34))
    return d,a

def flute_parts(s,tilt=0):
    # local coords: foot centre at (0,0), rim centre at (0,-760); returns (dark, amber) svg strings
    rimh=85; bot=-330
    def wall(sign):
        return f'C{P(sign*34,bot-6)} {P(sign*58,bot-60)} {P(sign*64,bot-130)} C{P(sign*72,bot-250)} {P(sign*84,-640)} {P(sign*rimh,-760)}'
    outline=(f'M{P(0,bot)} C{P(-34,bot-6)} {P(-58,bot-60)} {P(-64,bot-130)} C{P(-72,bot-250)} {P(-84,-640)} {P(-rimh,-760)} '
             f'L{P(rimh,-760)} C{P(84,-640)} {P(72,bot-250)} {P(64,bot-130)} C{P(58,bot-60)} {P(34,bot-6)} {P(0,bot)} Z')
    dark=(f'<path d="{outline}" fill="none" stroke="{DK}" stroke-width="24" stroke-linejoin="round"/>'
          f'<path d="M{P(-13,bot+5)} L{P(-11,-60)} C{P(-11,-30)} {P(-60,-30)} {P(-100,-14)} '
          f'C{P(-108,-10)} {P(-108,6)} {P(-96,8)} L{P(96,8)} C{P(108,6)} {P(108,-10)} {P(100,-14)} '
          f'C{P(60,-30)} {P(11,-30)} {P(11,-60)} L{P(13,bot+5)} Z"/>'
          f'<ellipse cx="0" cy="{(bot-25+(-60))/2:.0f}" rx="22" ry="20"/>')
    # liquid: inner region up to y=-620 (amber)
    liq=(f'<clipPath id="cl{s}"><path d="{outline}"/></clipPath>'
         f'<g clip-path="url(#cl{s})"><g transform="rotate({-tilt} 0 -600)"><rect x="-300" y="-600" width="600" height="400" fill="{AM}"/>'
         f'<path d="M-300,-600 Q-150,-618 0,-600 T300,-600 Z" fill="{AM}"/></g></g>')
    bub=''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CR}"/>' for x,y,r in [(-18,-410,10),(14,-470,11),(-8,-540,12),(22,-590,9)])
    return dark,liq+bub
def champagne():
    body=[];a=[]
    sc=1.25
    for sgn,fx in ((1,247),(-1,839)):
        dk,am=flute_parts('L' if sgn>0 else 'R',12*sgn)
        tr=f'translate({fx},1290) scale({sc}) rotate({12*sgn})'
        body.append(f'<g transform="{tr}" fill="{DK}">{am}{dk}</g>')
    # clink sparkle above contact
    sp=star4(543,265,62,0.26,col=DK)+star4(543,265,40,0.26,45,col=DK)
    body.append(f'<g fill="{DK}">{sp}</g>')
    body.append(f'<g fill="{AM}">{star4(543,265,20,0.3)}</g>')
    for (x,y,r) in [(430,200,14),(660,195,12),(395,145,10),(700,140,11),(470,120,9),(615,110,10)]:
        body.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{DK}"/>')
    for (x,y,r) in [(160,420,42),(930,460,40),(543,1180,38)]:
        body.append(f'<g fill="{AM}">{star4(x,y,r,0.34)}</g>')
    return body,[]

def ribbon(x0,y0,dx,dy,n,amp,width,turns=3,col=DK):
    pts=[]
    N=200
    for i in range(N+1):
        t=i/N*turns*2*math.pi
        x=x0+dx*t/(2*math.pi)+amp*math.cos(t+math.pi)*1.0+amp
        y=y0+dy*t/(2*math.pi)+amp*math.sin(t+math.pi)*0.9
        pts.append(P(x,y))
    return f'<path d="M{" L".join(pts)}" fill="none" stroke="{col}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
def streamer(p0,ang,L,width,col,curl=1,amp=36,lam=170,r0=85,turns=1.0,shrink=0.55):
    a=math.radians(ang); ux,uy=math.cos(a),math.sin(a); nx,ny=-uy,ux
    pts=[]; N=120
    for i in range(N+1):
        s_=L*i/N; off=amp*math.sin(2*math.pi*s_/lam)*(0.6+0.4*i/N)
        pts.append((p0[0]+ux*s_+nx*off,p0[1]+uy*s_+ny*off))
    ex,ey=pts[-1]; tx,ty=pts[-1][0]-pts[-2][0],pts[-1][1]-pts[-2][1]; tl=math.hypot(tx,ty); tx/=tl; ty/=tl
    # spiral centre to the side of the end tangent
    cnx,cny=-ty*curl,tx*curl
    cx,cy=ex+cnx*r0,ey+cny*r0
    th0=math.atan2(ey-cy,ex-cx)
    for i in range(1,90):
        t=i/89; th=th0+curl*t*turns*2*math.pi; r=r0*(1-shrink*t)
        pts.append((cx+r*math.cos(th),cy+r*math.sin(th)))
    return f'<path d="M{" L".join(P(x,y) for x,y in pts)}" fill="none" stroke="{col}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
def party_hat():
    body=[]
    # cone, rotated slightly
    ax,ay=0,-640; bl,br=-250,250
    cone=f'M{P(ax,ay)} L{P(br,0)} Q{P(0,70)} {P(bl,0)} Z'
    stripes=''.join(f'<path d="M{-400},{y} L{400},{y-260} L{400},{y-200} L{-400},{y+60} Z" fill="{AM}"/>' for y in range(-600,240,150))
    g=(f'<clipPath id="cone"><path d="{cone}"/></clipPath>'
       f'<path d="{cone}" fill="{DK}"/><g clip-path="url(#cone)">{stripes}</g>'
       f'<path d="{cone}" fill="none" stroke="{DK}" stroke-width="22" stroke-linejoin="round"/>'
       # brim band
       f'<path d="M{P(-275,-12)} Q{P(0,80)} {P(275,-12)} L{P(275,30)} Q{P(0,125)} {P(-275,30)} Z" fill="{DK}" stroke="{DK}" stroke-width="10" stroke-linejoin="round"/>'
       + ''.join(f'<circle cx="{x}" cy="{0.00085*(x*x)*-1+60:.1f}" r="11" fill="{AM}"/>' for x in range(-210,240,70)) +
       # pompom: fluffy scallops
       ''.join(f'<circle cx="{58*math.sin(math.radians(k*36)):.1f}" cy="{-650-58*math.cos(math.radians(k*36)):.1f}" r="30" fill="{DK}"/>' for k in range(10))+
       f'<circle cx="0" cy="-650" r="62" fill="{DK}"/>'
       f'<circle cx="-14" cy="-664" r="16" fill="{AM}"/><circle cx="20" cy="-640" r="11" fill="{AM}"/><circle cx="-8" cy="-628" r="8" fill="{AM}"/>')
    body.append(f'<g transform="translate(560,980) rotate(-10)">{g}</g>')
    # curled streamers (broad ribbons)
    body.append(streamer((640,215),56,400,34,DK,curl=1,r0=90))
    body.append(streamer((130,1225),8,560,34,DK,curl=-1,r0=90))
    body.append(streamer((195,230),86,470,30,AM,curl=1,amp=30,r0=82))
    # confetti (few, chunky)
    conf=[(330,215,25,DK,'r'),(930,800,-30,DK,'r'),(905,1010,40,AM,'r'),(120,960,15,AM,'r'),(420,1350,-20,DK,'r'),(880,1345,30,AM,'r')]
    for x,y,rot,col,k in conf:
        body.append(f'<rect x="{x-24}" y="{y-14}" width="48" height="28" rx="6" fill="{col}" transform="rotate({rot} {x} {y})"/>')
    for x,y,r,col in [(450,170,15,AM),(960,240,16,AM),(290,760,15,DK),(950,690,15,AM),(650,1355,15,DK),(250,1345,15,AM),(760,1150,15,AM)]:
        body.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>')
    for x,y,r in [(560,140,0),(105,1080,0)]:
        if not r: continue
        body.append(f'<g fill="{DK}">{star4(x,y,r)}</g>')
    return body,[]

PANELS={'1_fireworks':fireworks,'2_midnight_clock':clock,'3_champagne_toast':champagne,'4_party_hat_streamers':party_hat}
PAL={'cream':np.array([192,180,120.]),'amber':np.array([168,96,36.]),'dark':np.array([48,24,0.])}
def render(name,fn):
    d,a=fn()
    if name in('3_champagne_toast','4_party_hat_streamers'):
        body=''.join(d)
    else:
        body=f'<g fill="{DK}">{"".join(d)}</g><g fill="{AM}">{"".join(a)}</g>'
    s=svg(body); open(f'{OUT}/vectors/new_years_{name}.svg','w').write(s)
    rgba=np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode()))).convert('RGBA')).astype(float)
    al=rgba[...,3:4]/255; col=rgba[...,:3]
    # un-premultiplied colour from PIL already; composite
    img=TPL*(1-al)+col*al
    # keep the frame on top (art must stay inside the interior)
    fr=np.array(Image.open(f'{OUT}/vectors/panel_frame_mask.png'))>0
    img[fr]=TPL[fr]
    Image.fromarray(img.round().astype(np.uint8)).save(f'{OUT}/new_years_{name}.png')
    # thickness classes: 0 cream .7mm, 127 amber 1.1mm, 254 dark 1.8mm
    P3=np.stack([PAL['cream'],PAL['amber'],PAL['dark']])
    lab=((img[:,:,None,:]-P3[None,None])**2).sum(3).argmin(2).astype(np.uint8)
    Image.fromarray(lab*127).save(f'{OUT}/vectors/new_years_{name}_thickness_classes.png')
    return lab
if __name__=='__main__':
    sel=sys.argv[1:] or list(PANELS)
    for n in sel: render(n,PANELS[n]); print('built',n)

from PIL import Image, ImageDraw, ImageFont
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; Fr='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def f(s,b=True): return ImageFont.truetype(F if b else Fr,s)
panels=[('christmas_1_tree_v6_unchanged.png','1  Christmas tree — unchanged from v5'),
        ('christmas_2_snowman_v6.png','2  Snowman — side spike removed'),
        ('christmas_3_reindeer_v6.png','3  Reindeer — new reference-based antlers'),
        ('christmas_4_wreath_v6_unchanged.png','4  Wreath — unchanged from v5')]
PW,PH=1086,1471; M=70; top=300; cap=90
W=M*3+PW*2; H=top+(PH+cap+M)*2+60
s=Image.new('RGB',(W,H),(244,240,232)); d=ImageDraw.Draw(s)
d.text((M,50),'IMAGES FOR APPROVAL — NO NEW STL',font=f(84),fill=(48,24,0))
d.text((M,160),'Christmas lantern panels v6 · artwork concept only, not an exported STL · 77.5 × 105 mm panels',font=f(38,False),fill=(48,24,0))
d.text((M,215),'Simulated backlighting: cream = thin 0.7 mm, amber = 1.1 mm, dark brown = 1.8 mm.',font=f(34,False),fill=(90,60,30))
d.text((M,252),'The 77.5 × 105 × 1.8 mm panels have been printed and fit the lantern well (confirmed by Shannon, Nov 2026).',font=f(34,False),fill=(90,60,30))
for i,(fn,lab) in enumerate(panels):
    x=M+(i%2)*(PW+M); y=top+(i//2)*(PH+cap+M)
    s.paste(Image.open(fn).convert('RGB'),(x,y)); d.text((x,y+PH+18),lab,font=f(44),fill=(48,24,0))
s.save('CHRISTMAS_v6_FOUR_UP_IMAGES_FOR_APPROVAL.png')
s.resize((W//4,H//4),Image.LANCZOS).save('check_fourup_quarter_scale.png')
# closeups
r=Image.open('christmas_3_reindeer_v6.png').crop((380,80,1050,760))
o=Image.open('v5_unchanged_crops/v5_3_reindeer.png').crop((380,80,1050,760))
sn=Image.open('christmas_2_snowman_v6.png').crop((330,250,900,700)).resize((670,529))
so=Image.open('v5_unchanged_crops/v5_2_snowman.png').crop((330,250,900,700)).resize((670,529))
c=Image.new('RGB',(670*2+M*3,top+680+529+cap*2+M*2),(244,240,232)); d=ImageDraw.Draw(c)
d.text((M,50),'CLOSE-UPS — NOT EXPORTED STL',font=f(64),fill=(48,24,0))
d.text((M,150),'Left: v5 (rejected)   Right: v6 concept',font=f(38,False),fill=(48,24,0))
c.paste(o,(M,top)); c.paste(r,(M*2+670,top))
d.text((M,top+690),'v5 antlers',font=f(36),fill=(48,24,0)); d.text((M*2+670,top+690),'v6 antlers (caribou outline)',font=f(36),fill=(48,24,0))
y2=top+680+cap+M
c.paste(so,(M,y2)); c.paste(sn,(M*2+670,y2))
d.text((M,y2+540),'v5 snowman (side spike)',font=f(36),fill=(48,24,0)); d.text((M*2+670,y2+540),'v6: spike removed',font=f(36),fill=(48,24,0))
c.save('CLOSEUPS_v5_vs_v6.png')
# reference sheet
import cairosvg,io
ph=Image.open('refs/photo_reinbukken_AreGNilsen_CCBYSA3.jpg').convert('RGB')
sv=Image.open(io.BytesIO(cairosvg.svg2png(url='refs/phylopic_e60cd072-d9ce-4d13-a79c-aa3d8086d37a.svg',output_width=960,background_color='white'))).convert('RGB')
mk=Image.open('vectors/reindeer_antlers_v6_mask.png').crop((380,80,1050,700))
R=Image.new('RGB',(960*2+M*3,top+770+M+80),(255,255,255)); d=ImageDraw.Draw(R)
d.text((M,50),'Antler reference trail',font=f(64),fill=(48,24,0))
d.text((M,150),'Photo: Are G Nilsen, CC BY-SA 3.0 (Wikimedia Commons) · Outline: PhyloPic e60cd072, Public Domain Mark (Ando)',font=f(30,False),fill=(48,24,0))
R.paste(ph,(M,top)); R.paste(sv.resize((960,int(sv.height*960/sv.width))),(M*2+960,top))
R.save('refs/REFERENCE_TRAIL.png')

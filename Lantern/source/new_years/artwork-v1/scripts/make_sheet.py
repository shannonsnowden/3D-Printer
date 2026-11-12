from PIL import Image, ImageDraw, ImageFont
import os
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; Fr='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f=lambda s,b=True: ImageFont.truetype(F if b else Fr,s)
panels=[('new_years_1_fireworks.png','Fireworks'),('new_years_2_midnight_clock.png','Midnight clock'),
        ('new_years_3_champagne_toast.png','Champagne toast'),('new_years_4_party_hat_streamers.png','Party hat and streamers')]
PW,PH=1086,1471; M=70; top=300; cap=90
W=M*3+PW*2; H=top+(PH+cap+M)*2+40
s=Image.new('RGB',(W,H),(244,240,232)); d=ImageDraw.Draw(s)
d.text((M,50),"IMAGES FOR APPROVAL — NO STL",font=f(84),fill=(48,24,0))
d.text((M,160),"New Year's lantern panels v1 · 2D artwork only, not an exported STL · 77.5 × 105 mm panels",font=f(38,False),fill=(48,24,0))
d.text((M,215),"SIMULATED backlighting (not a photo): cream = 0.7 mm, amber = 1.1 mm, dark brown = 1.8 mm.",font=f(34,False),fill=(90,60,30))
d.text((M,252),"The 77.5 × 105 × 1.8 mm panels have been printed and fit the lantern well (confirmed by Shannon, Nov 2026).",font=f(34,False),fill=(90,60,30))
for i,(fn,lab) in enumerate(panels):
    x=M+(i%2)*(PW+M); y=top+(i//2)*(PH+cap+M)
    s.paste(Image.open(f'{OUT}/{fn}').convert('RGB'),(x,y)); d.text((x,y+PH+18),f'{i+1}  {lab}',font=f(46),fill=(48,24,0))
s.save(f'{OUT}/NEW_YEARS_v1_FOUR_UP_IMAGES_FOR_APPROVAL.png')
s.resize((W//4,H//4),Image.LANCZOS).save(f'{OUT}/check_fourup_quarter_scale.png')

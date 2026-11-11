from PIL import Image;import sys
fs=['1_fireworks','2_midnight_clock','3_champagne_toast','4_party_hat_streamers']
s=Image.new('RGB',(1086*2+30,1471*2+30),'white')
for i,f in enumerate(fs): s.paste(Image.open(f'new_years_{f}.png'),((i%2)*1116,(i//2)*1501))
s.resize((s.width//2,s.height//2),Image.LANCZOS).save(sys.argv[1])

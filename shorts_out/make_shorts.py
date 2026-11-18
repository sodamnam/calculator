import subprocess, glob, os, sys
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-calculator/92091629-437c-5ff5-ac78-cae4819d3258/scratchpad'
SRC=glob.glob('/root/.claude/uploads/92091629-437c-5ff5-ac78-cae4819d3258/580fdd2a-*.mp4')[0]
OV=S+'/ov'; W,H,HD=720,1280,300; VH=H-HD
JUA=S+'/fonts/Jua-Regular.ttf'; BHS=S+'/fonts/BlackHanSans-Regular.ttf'
F=lambda p,s: ImageFont.truetype(p,s)

# ---- header ----
im=Image.new('RGBA',(W,HD),(255,255,255,255)); d=ImageDraw.Draw(im)
d.ellipse((44,22,134,112),fill=(88,40,150)); d.ellipse((50,28,128,106),outline=(255,200,40),width=4)
d.text((89,67),'CH',font=F(BHS,34),fill=(255,220,80),anchor='mm')
d.text((156,48),'채널명',font=F(JUA,32),fill=(20,20,20),anchor='lm')
d.text((156,88),'Channel Name',font=F(JUA,26),fill=(20,20,20),anchor='lm')
f=F(JUA,58); parts=[('아기가 ',(15,15,15)),('위험해진 순간',(235,20,30))]
tw=sum(d.textlength(t,font=f) for t,_ in parts); x=(W-tw)/2
for t,c in parts:
    d.text((x,172),t,font=f,fill=c,anchor='lm'); x+=d.textlength(t,font=f)
d.text((W/2,248),'댕댕이가 보인 놀라운 행동',font=F(JUA,56),fill=(70,235,40),anchor='mm',stroke_width=5,stroke_fill=(10,10,10))
im.save(OV+'/header.png')

# ---- captions / impact ----
def cap(text,name):
    im=Image.new('RGBA',(W,220),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.multiline_text((W/2,110),text,font=F(JUA,56),fill='white',anchor='mm',align='center',stroke_width=6,stroke_fill='black',spacing=10)
    im.save(f'{OV}/{name}.png')
def impact(text,name,color=(255,225,0)):
    im=Image.new('RGBA',(W,300),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((W/2+6,156),text,font=F(BHS,150),fill=(0,0,0,255),anchor='mm',stroke_width=12,stroke_fill=(0,0,0))
    d.text((W/2,150),text,font=F(BHS,150),fill=color,anchor='mm',stroke_width=10,stroke_fill=(200,0,0))
    im.rotate(-6,resample=Image.BICUBIC).save(f'{OV}/{name}.png')

CAPS=[(0,3,'계단 쪽으로\n기어가는 아기'),(3,6.3,'그 순간 달려온 댕댕이'),(6.3,10,'온몸으로 막아섭니다'),
(10,11.3,'열려 있는 뜨거운 오븐'),(11.3,14.5,'문부터 닫아버리고'),(14.5,20,'아기 앞을 가로막은 녀석'),
(20,22,'평화롭던 마당에'),(22,25,'갑자기 차가 돌진합니다'),(25,30,'끝까지 아기를 지켜낸\n댕댕이들'),
(30,32,'혼자 놀고 있던 아기'),(32,35.5,'허스키가 급히 뛰어들어와'),(35.5,40,'곁을 떠나지 않습니다'),
(40,42.3,'열린 문으로 향하는 아기'),(42.3,45,'쏜살같이 달려가'),(45,50,'밖으로 못 나가게 막았어요'),
(50,51.3,'TV가 넘어지는 순간'),(51.3,55,'몸을 던져 아기를 감쌉니다'),(55,60,'댕댕이는 사랑입니다')]
IMP=[(3,4.1,'안 돼!!'),(11.3,12.4,'천재견?!'),(22,23.1,'쾅!!'),(42.3,43.4,'잠깐!!'),(51.3,52.4,'위험해!!')]
for i,c in enumerate(CAPS): cap(c[2],f'c{i}')
for i,c in enumerate(IMP): impact(c[2],f'i{i}')

# ---- video layout per scene ----
blur=lambda src,o: f"[{src}]split[{o}a][{o}b];[{o}a]scale={W}:{VH}:force_original_aspect_ratio=increase,crop={W}:{VH},boxblur=24:2,eq=brightness=-0.12[{o}bg];"
def scene(i,kind,arg):
    t=f"[0:v]trim={i*10}:{i*10+10},setpts=PTS-STARTPTS"
    if kind=='crop':   return f"{t},crop={W}:{VH}:0:{arg},setsar=1[s{i}];"
    if kind=='fit':    # whole frame scaled down over blurred bg
        return f"{t}[r{i}];"+blur(f'r{i}',f'q{i}')+f"[q{i}b]scale=-2:{VH}[q{i}f];[q{i}bg][q{i}f]overlay=(W-w)/2:0,setsar=1[s{i}];"
    if kind=='band':   # letterboxed: crop band, zoom, blurred bg
        y0,y1,z,cx=arg; bh=y1-y0
        return (f"{t},crop={W}:{bh}:0:{y0}[r{i}];"+blur(f'r{i}',f'q{i}')+
                f"[q{i}b]scale={int(W*z)//2*2}:-2,crop={W}:ih:(iw-{W})*{cx}:0[q{i}f];[q{i}bg][q{i}f]overlay=0:(H-h)/2,setsar=1,setsar=1[s{i}];")
L=[('crop',150),('band',(298,982,1.0,0.5)),('crop',250),('band',(422,858,1.55,0.55)),('crop',90),('fit',None)]
fc=''.join(scene(i,k,a) for i,(k,a) in enumerate(L))
fc+=''.join(f'[s{i}]' for i in range(6))+f"concat=n=6:v=1:a=0,pad={W}:{H}:0:{HD}:white[base];[base][1:v]overlay=0:0[v0];"
inputs=['-i',SRC,'-i',OV+'/header.png']; n=2; cur='v0'
for i,(a,b,_) in enumerate(CAPS):
    inputs+=['-i',f'{OV}/c{i}.png']; fc+=f"[{cur}][{n}:v]overlay=0:790:enable='between(t,{a},{b-0.03})'[v{n}];"; cur=f'v{n}'; n+=1
for i,(a,b,_) in enumerate(IMP):
    inputs+=['-i',f'{OV}/i{i}.png']; fc+=f"[{cur}][{n}:v]overlay=0:400:enable='between(t,{a},{b})'[v{n}];"; cur=f'v{n}'; n+=1
out=sys.argv[1]
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',fc.rstrip(';'),'-map',f'[{cur}]','-map','0:a','-c:v','libx264','-crf','20','-preset','medium','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart','-t','60',out],check=True)

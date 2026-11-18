import subprocess, glob, sys
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-calculator/92091629-437c-5ff5-ac78-cae4819d3258/scratchpad'
SRC=glob.glob('/root/.claude/uploads/92091629-437c-5ff5-ac78-cae4819d3258/580fdd2a-*.mp4')[0]
OV=S+'/ov3'; W,H,HD=720,1280,300; VH=H-HD
import os; os.makedirs(OV,exist_ok=True)
JUA=S+'/fonts/Jua-Regular.ttf'; BHS=S+'/fonts/BlackHanSans-Regular.ttf'
F=lambda p,s: ImageFont.truetype(p,s)

# header (숏탈)
im=Image.new('RGBA',(W,HD),(255,255,255,255)); d=ImageDraw.Draw(im)
lg=Image.open('/home/user/calculator/shorts_out/logo.png').resize((104,104),Image.LANCZOS); im.paste(lg,(40,14),lg)
d.text((162,46),'숏탈',font=F(JUA,40),fill=(20,20,20),anchor='lm')
d.text((162,90),'아무생각 없이 보기 좋은 채널',font=F(JUA,25),fill=(70,70,70),anchor='lm')
f=F(JUA,56); parts=[('아기 곁을 ',(15,15,15)),('지키는 댕댕이',(235,20,30))]
tw=sum(d.textlength(t,font=f) for t,_ in parts); x=(W-tw)/2
for t,c in parts:
    d.text((x,172),t,font=f,fill=c,anchor='lm'); x+=d.textlength(t,font=f)
d.text((W/2,248),'칭찬받는 털복숭이 보디가드',font=F(JUA,56),fill=(70,235,40),anchor='mm',stroke_width=5,stroke_fill=(10,10,10))
im.save(OV+'/header.png')

def cap(text,name):
    im=Image.new('RGBA',(W,220),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.multiline_text((W/2,110),text,font=F(JUA,54),fill='white',anchor='mm',align='center',stroke_width=6,stroke_fill='black',spacing=10)
    im.save(f'{OV}/{name}.png')
def impact(text,name,color=(255,225,0)):
    im=Image.new('RGBA',(W,300),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((W/2+6,156),text,font=F(BHS,130),fill=(0,0,0,255),anchor='mm',stroke_width=12,stroke_fill=(0,0,0))
    d.text((W/2,150),text,font=F(BHS,130),fill=color,anchor='mm',stroke_width=10,stroke_fill=(200,0,0))
    im.rotate(-6,resample=Image.BICUBIC).save(f'{OV}/{name}.png')

# (src_start, src_end, crop_y, [captions (rel_start, rel_end|None, text)], impact (rel_start,text)|None)
B=lambda y0,y1,z,cx: (f"crop=720:{y1-y0}:0:{y0},split[a][b];[a]scale={W}:{VH}:force_original_aspect_ratio=increase,crop={W}:{VH},boxblur=24:2,eq=brightness=-0.12[bg];[b]scale={int(W*z)//2*2}:-2,crop={W}:ih:(iw-{W})*{cx}:0[f];[bg][f]overlay=0:(H-h)/2,setsar=1")
C=lambda y: f"crop={W}:{VH}:0:{y},setsar=1"
CLIPS=[
 (13.0,20.0,B(298,982,1.0,0.5),[(0,2.6,'아기 옆에 딱 붙어 앉은 셰퍼드'),(2.6,None,'엄마의 폭풍 칭찬 타임')],(2.8,'잘했어!!')),
 (44.6,50.0,C(90),[(0,None,'온 가족이 달려와\n쓰담쓰담')],None),
 (35.3,40.0,B(422,858,1.55,0.55),[(0,None,'아기방 담당은 허스키')],None),
 (56.0,60.0,C(300),[(0,None,'댕댕이는 사랑입니다')],None),
]
CD=S+'/clips3'; os.makedirs(CD,exist_ok=True)
T=0; caps=[]; imps=[]; inputs=[]
for i,(a,b,y,cs,ip) in enumerate(CLIPS):
    L=b-a
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{a}','-t',f'{L}','-i',SRC,'-filter_complex',f'[0:v]fps=30,{y}[v];[0:a]afade=t=in:d=0.15,afade=t=out:st={L-0.2}:d=0.2[a]','-map','[v]','-map','[a]','-c:a','aac','-c:v','libx264','-crf','14','-preset','fast',f'{CD}/{i}.mp4'],check=True)
    inputs+=['-i',f'{CD}/{i}.mp4']
    for (c0,c1,t) in cs: caps.append((T+c0,T+(c1 if c1 else L)-0.04,t))
    if ip: imps.append((T+ip[0],T+ip[0]+1.1,ip[1]))
    T+=L
print('total',T)
N=len(CLIPS)
fc=''.join(f'[{i}:v]' for i in range(N))+f"concat=n={N}:v=1:a=0,pad={W}:{H}:0:{HD}:white[base];[base][{N}:v]overlay=0:0[v0];"
inputs+=['-i',OV+'/header.png']; n=N+1; cur='v0'
for i,(a,b,t) in enumerate(caps):
    cap(t,f'c{i}'); inputs+=['-i',f'{OV}/c{i}.png']; fc+=f"[{cur}][{n}:v]overlay=0:800:enable='between(t,{a:.2f},{b:.2f})'[v{n}];"; cur=f'v{n}'; n+=1
for i,(a,b,t) in enumerate(imps):
    impact(t,f'i{i}'); inputs+=['-i',f'{OV}/i{i}.png']; fc+=f"[{cur}][{n}:v]overlay=0:380:enable='between(t,{a:.2f},{b:.2f})'[v{n}];"; cur=f'v{n}'; n+=1
fc+=''.join(f'[{i}:a]' for i in range(N))+f'concat=n={N}:v=0:a=1[a]'
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',fc,'-map',f'[{cur}]','-map','[a]','-c:v','libx264','-crf','20','-preset','medium','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',f'{T}',sys.argv[1]],check=True)

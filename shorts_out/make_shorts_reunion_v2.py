import subprocess, glob, sys
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-calculator/92091629-437c-5ff5-ac78-cae4819d3258/scratchpad'
SRC=glob.glob('/root/.claude/uploads/92091629-437c-5ff5-ac78-cae4819d3258/f4d92131-*.mp4')[0]
OV=S+'/ov4'; W,H,HD=720,1280,300; VH=H-HD
import os; os.makedirs(OV,exist_ok=True)
JUA=S+'/fonts/Jua-Regular.ttf'; BHS=S+'/fonts/BlackHanSans-Regular.ttf'
F=lambda p,s: ImageFont.truetype(p,s)

# header (숏탈)
im=Image.new('RGBA',(W,HD),(255,255,255,255)); d=ImageDraw.Draw(im)
lg=Image.open('/home/user/calculator/shorts_out/logo_ddanjit.png').resize((199,112),Image.LANCZOS); im.paste(lg,(32,10),lg)
d.text((250,46),'딴짓극장',font=F(JUA,40),fill=(20,20,20),anchor='lm')
d.text((250,90),'아무 생각 없이 보기 좋은 채널',font=F(JUA,25),fill=(70,70,70),anchor='lm')
f=F(JUA,56); parts=[('오랜만에 ',(15,15,15)),('주인을 본 순간',(235,20,30))]
tw=sum(d.textlength(t,font=f) for t,_ in parts); x=(W-tw)/2
for t,c in parts:
    d.text((x,172),t,font=f,fill=c,anchor='lm'); x+=d.textlength(t,font=f)
d.text((W/2,248),'참지 못한 댕댕이들',font=F(JUA,56),fill=(70,235,40),anchor='mm',stroke_width=5,stroke_fill=(10,10,10))
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
C=lambda y: f"crop={W}:{VH}:0:{y}"
Z=lambda w,h,x,y: f"crop={w}:{h}:{x}:{y},scale={W}:{VH}"   # zoom-crop to drop source stickers/captions
CLIPS=[
 (113.0,120.4,C(200),[(0,3.9,'저 멀리 익숙한 실루엣...'),(3.9,None,'그대로 품에 안겨버립니다')],(3.9,'주인이다!!')),
 (53.0,58.6,C(280),[(0,2.8,'베란다에서 기다리던 비글'),(2.8,None,'주차장에서 주인을 발견!')],None),
 (59.6,61.8,C(150),[(0,None,'현관으로 전력 질주')],(0.2,'왔다!!')),
 (85.0,91.1,C(200),[(0,2.6,'공항 도착 게이트 앞'),(2.6,None,'목줄도 뿌리치고 달려갑니다')],None),
 (33.0,38.7,Z(626,852,47,290),[(0,2.4,'계단 아래 누군가 보이자'),(2.4,None,'온몸으로 반기는 녀석')],None),
 (123.2,127.75,Z(660,898,30,50),[(0,2.0,'얌전히 엎드려 있다가'),(2.0,None,'폴짝폴짝 난리가 났어요')],None),
 (91.2,96.6,C(200),[(0,2.4,'가방 내려놓을 틈도 없이'),(2.4,None,'잔디밭에서 뒹굴뒹굴')],None),
 (127.75,132.6,C(0),[(0,2.2,'기다림이 길었던 만큼'),(2.2,None,'반가움도 큽니다')],None),
]
CD=S+'/clips4'; os.makedirs(CD,exist_ok=True)
T=0; caps=[]; imps=[]; inputs=[]
for i,(a,b,y,cs,ip) in enumerate(CLIPS):
    L=b-a
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{a}','-t',f'{L}','-i',SRC,'-an','-vf',f'fps=30,scale={W}:{H},{y},setsar=1','-c:v','libx264','-crf','14','-preset','fast',f'{CD}/{i}.mp4'],check=True)
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
fc=fc.rstrip(';')
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',fc,'-map',f'[{cur}]','-c:v','libx264','-crf','20','-preset','medium','-threads','2','-pix_fmt','yuv420p','-an','-movflags','+faststart','-t',f'{T}',sys.argv[1]],check=True)

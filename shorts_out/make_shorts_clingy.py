import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-calculator/92091629-437c-5ff5-ac78-cae4819d3258/scratchpad'
SRC='/root/.claude/uploads/92091629-437c-5ff5-ac78-cae4819d3258/827f33e8-dl.mp4'
OV=S+'/ov5'; CD=S+'/clips5'; W,H,HD=720,1280,300; VH=H-HD
os.makedirs(OV,exist_ok=True); os.makedirs(CD,exist_ok=True)
JUA=S+'/fonts/Jua-Regular.ttf'; BHS=S+'/fonts/BlackHanSans-Regular.ttf'
F=lambda p,s: ImageFont.truetype(p,s)

# header (딴짓극장)
im=Image.new('RGBA',(W,HD),(255,255,255,255)); d=ImageDraw.Draw(im)
lg=Image.open('/home/user/calculator/shorts_out/logo_ddanjit.png').resize((199,112),Image.LANCZOS); im.paste(lg,(32,10),lg)
d.text((250,46),'딴짓극장',font=F(JUA,40),fill=(20,20,20),anchor='lm')
d.text((250,90),'아무 생각 없이 보기 좋은 채널',font=F(JUA,25),fill=(70,70,70),anchor='lm')
f=F(JUA,56); parts=[('잠시도 ',(15,15,15)),('못 떨어지는',(235,20,30))]
tw=sum(d.textlength(t,font=f) for t,_ in parts); x=(W-tw)/2
for t,c in parts:
    d.text((x,172),t,font=f,fill=c,anchor='lm'); x+=d.textlength(t,font=f)
d.text((W/2,248),'껌딱지 댕댕이들',font=F(JUA,56),fill=(70,235,40),anchor='mm',stroke_width=5,stroke_fill=(10,10,10))
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

# (src_start, src_end, [captions (rel_start, rel_end|None, text)], impact (rel_start,text)|None)
CLIPS=[
 (0.0,3.75,[(0,None,'소파에 누웠을 뿐인데')],(0.5,'점프!!')),
 (5.05,7.28,[(0,None,'신문 좀 읽자, 제발')],None),
 (7.32,11.28,[(0,None,'얼굴이 베개인 줄 압니다')],None),
 (22.66,26.28,[(0,None,'본인이 소형견인 줄 아는 편')],None),
 (26.32,29.8,[(0,None,'어디 가! 같이 가!')],(0.4,'못 가!!')),
 (35.1,39.5,[(0,2.2,'어깨는 원래 내 자리'),(2.2,None,'집사는 이미 체념')],None),
 (40.56,45.85,[(0,2.6,'안아줘, 안아줘'),(2.6,None,'둘 다 안아달래요')],None),
 (45.9,50.5,[(0,2.3,'나 좀 봐'),(2.3,None,'봐줄 때까지 톡톡')],None),
 (61.06,66.15,[(0,2.5,'결국 져주는 집사'),(2.5,None,'이 맛에 키웁니다')],None),
]
T=0; caps=[]; imps=[]; inputs=[]
for i,(a,b,cs,ip) in enumerate(CLIPS):
    L=b-a
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{a}','-t',f'{L}','-i',SRC,'-filter_complex',
      f'[0:v]fps=30,scale={W}:{VH},setsar=1[v];[0:a]aresample=44100,afade=t=in:d=0.06,afade=t=out:st={L-0.08}:d=0.08[a]',
      '-map','[v]','-map','[a]','-c:v','libx264','-crf','14','-preset','fast','-c:a','aac','-b:a','192k',f'{CD}/{i}.mp4'],check=True)
    inputs+=['-i',f'{CD}/{i}.mp4']
    for (c0,c1,t) in cs: caps.append((T+c0,T+(c1 if c1 else L)-0.04,t))
    if ip: imps.append((T+ip[0],T+ip[0]+1.0,ip[1]))
    T+=L
print('total',T)
N=len(CLIPS)
fc=''.join(f'[{i}:v]' for i in range(N))+f"concat=n={N}:v=1:a=0,pad={W}:{H}:0:{HD}:white[base];[base][{N}:v]overlay=0:0[v0];"
inputs+=['-i',OV+'/header.png']; n=N+1; cur='v0'
for i,(a,b,t) in enumerate(caps):
    cap(t,f'c{i}'); inputs+=['-i',f'{OV}/c{i}.png']; fc+=f"[{cur}][{n}:v]overlay=0:960:enable='between(t,{a:.2f},{b:.2f})'[v{n}];"; cur=f'v{n}'; n+=1
for i,(a,b,t) in enumerate(imps):
    impact(t,f'i{i}'); inputs+=['-i',f'{OV}/i{i}.png']; fc+=f"[{cur}][{n}:v]overlay=0:330:enable='between(t,{a:.2f},{b:.2f})'[v{n}];"; cur=f'v{n}'; n+=1
fc+=''.join(f'[{i}:a]' for i in range(N))+f'concat=n={N}:v=0:a=1[a]'
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',fc,'-map',f'[{cur}]','-map','[a]','-c:v','libx264','-crf','20','-preset','medium','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-t',f'{T}',sys.argv[1]],check=True)

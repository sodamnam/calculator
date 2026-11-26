import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-calculator/92091629-437c-5ff5-ac78-cae4819d3258/scratchpad'
SRC='/root/.claude/uploads/92091629-437c-5ff5-ac78-cae4819d3258/36d10ae9-dl_1.mp4'
OV=S+'/ov6'; CD=S+'/clips6'; W,H,HD=720,1280,300; VH=H-HD
os.makedirs(OV,exist_ok=True); os.makedirs(CD,exist_ok=True)
JUA=S+'/fonts/Jua-Regular.ttf'; BHS=S+'/fonts/BlackHanSans-Regular.ttf'; CJK='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
F=lambda p,s: ImageFont.truetype(p,s)

# header (딴짓극장) + source credit at top-right of the video area
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
d.rectangle((0,0,W,HD),fill=(255,255,255,255))
lg=Image.open('/home/user/calculator/shorts_out/logo_ddanjit.png').resize((199,112),Image.LANCZOS); im.paste(lg,(32,10),lg)
d.text((250,46),'딴짓극장',font=F(JUA,40),fill=(20,20,20),anchor='lm')
d.text((250,90),'아무 생각 없이 보기 좋은 채널',font=F(JUA,25),fill=(70,70,70),anchor='lm')
f=F(JUA,56); parts=[('목욕이 ',(15,15,15)),('세상에서 제일 좋은',(235,20,30))]
tw=sum(d.textlength(t,font=f) for t,_ in parts); x=(W-tw)/2
for t,c in parts:
    d.text((x,172),t,font=f,fill=c,anchor='lm'); x+=d.textlength(t,font=f)
d.text((W/2,248),'물아일체 댕댕이들',font=F(JUA,56),fill=(70,235,40),anchor='mm',stroke_width=5,stroke_fill=(10,10,10))
a,b='출처: ','舔一口柠檬'; fa,fb=F(JUA,20),F(CJK,20)
wa,wb=d.textlength(a,font=fa),d.textlength(b,font=fb); x1=W-12; x0=x1-wa-wb-20
d.rounded_rectangle((x0,HD+10,x1,HD+42),radius=10,fill=(0,0,0,120))
d.text((x0+10,HD+26),a,font=fa,fill=(255,255,255,235),anchor='lm'); d.text((x0+10+wa,HD+26),b,font=fb,fill=(255,255,255,235),anchor='lm')
im.save(OV+'/header.png')

def cap(text,name):
    im=Image.new('RGBA',(W,220),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.multiline_text((W/2,110),text,font=F(JUA,54),fill='white',anchor='mm',align='center',stroke_width=6,stroke_fill='black',spacing=10)
    im.save(f'{OV}/{name}.png')
def impact(text,name,color=(255,225,0)):
    im=Image.new('RGBA',(W,300),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((W/2+6,156),text,font=F(BHS,140),fill=(0,0,0,255),anchor='mm',stroke_width=12,stroke_fill=(0,0,0))
    d.text((W/2,150),text,font=F(BHS,140),fill=color,anchor='mm',stroke_width=10,stroke_fill=(200,0,0))
    im.rotate(-6,resample=Image.BICUBIC).save(f'{OV}/{name}.png')
SFXC=[(120,215,255),(255,170,210),(255,235,120)]
def sfx(text,name,k):   # onomatopoeia: pastel, tilted, white outline
    im=Image.new('RGBA',(460,200),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((233,104),text,font=F(JUA,78),fill=(0,0,0,150),anchor='mm',stroke_width=9,stroke_fill=(0,0,0,150))
    d.text((230,100),text,font=F(JUA,78),fill=SFXC[k%3],anchor='mm',stroke_width=7,stroke_fill=(255,255,255))
    im.rotate(10 if k%2==0 else -10,resample=Image.BICUBIC,expand=False).save(f'{OV}/{name}.png')

# (src_start, src_end, crop_y, [captions (rel_start, rel_end|None, text)], impact (rel_start,text)|None, sfx (rel_start, text, x, y)|None)
CLIPS=[
 (0.0,2.78,220,[(0,None,'"목욕하자" 한마디에')],(1.0,'풍덩!!'),None),
 (2.85,6.4,300,[(0,None,'여기가 바로 천국이개')],None,(0.3,'쏴아아~',250,330)),
 (28.65,32.1,250,[(0,None,'반신욕 20년 차의 자세')],None,(0.4,'노곤노곤',20,360)),
 (15.5,18.5,120,[(0,None,'눈이 스르르 감깁니다')],None,(0.3,'솨아아~',240,620)),
 (43.1,47.6,150,[(0,2.2,'씻다가 그만...'),(2.2,None,'잠들어 버렸습니다')],(2.3,'꿀잠!!'),(0.3,'꾸벅.. 꾸벅..',240,340)),
 (53.15,56.4,150,[(0,None,'배 마사지는 필수 코스')],None,(0.3,'뽀득뽀득',20,700)),
 (10.25,13.5,200,[(0,None,'등 좀 더 밀어주세요')],None,(0.3,'보글보글',20,340)),
 (39.15,43.0,300,[(0,None,'샤워기는 원래 내 거')],None,(0.3,'촤아아~',250,340)),
 (32.2,36.25,300,[(0,None,'거품 스파 VIP 고객님')],None,(0.3,'몽글몽글',240,330)),
 (48.12,51.6,200,[(0,None,'물줄기 멍 때리는 중')],None,(0.3,'주르륵~',250,340)),
 (58.65,59.97,250,[(0,None,'혼자서도 잘 씻어요')],None,None),
]
T=0; caps=[]; imps=[]; sfxs=[]; inputs=[]
for i,(a,b,y,cs,ip,sx) in enumerate(CLIPS):
    L=b-a
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{a}','-t',f'{L}','-i',SRC,'-an','-vf',f'fps=30,scale={W}:{H},crop={W}:{VH}:0:{y},setsar=1','-c:v','libx264','-crf','14','-preset','fast',f'{CD}/{i}.mp4'],check=True)
    inputs+=['-i',f'{CD}/{i}.mp4']
    for (c0,c1,t) in cs: caps.append((T+c0,T+(c1 if c1 else L)-0.04,t))
    if ip: imps.append((T+ip[0],min(T+ip[0]+1.0,T+L),ip[1]))
    if sx: sfxs.append((T+sx[0],min(T+sx[0]+1.6,T+L-0.05),sx[1],sx[2],sx[3]))
    T+=L
print('total',T)
N=len(CLIPS)
fc=''.join(f'[{i}:v]' for i in range(N))+f"concat=n={N}:v=1:a=0,pad={W}:{H}:0:{HD}:white[base];[base][{N}:v]overlay=0:0[v0];"
inputs+=['-i',OV+'/header.png']; n=N+1; cur='v0'
for i,(a,b,t) in enumerate(caps):
    cap(t,f'c{i}'); inputs+=['-i',f'{OV}/c{i}.png']; fc+=f"[{cur}][{n}:v]overlay=0:960:enable='between(t,{a:.2f},{b:.2f})'[v{n}];"; cur=f'v{n}'; n+=1
for i,(a,b,t,x,y) in enumerate(sfxs):
    sfx(t,f's{i}',i); inputs+=['-i',f'{OV}/s{i}.png']; fc+=f"[{cur}][{n}:v]overlay={x}:{y}:enable='between(t,{a:.2f},{b:.2f})'[v{n}];"; cur=f'v{n}'; n+=1
for i,(a,b,t) in enumerate(imps):
    impact(t,f'i{i}'); inputs+=['-i',f'{OV}/i{i}.png']; fc+=f"[{cur}][{n}:v]overlay=0:400:enable='between(t,{a:.2f},{b:.2f})'[v{n}];"; cur=f'v{n}'; n+=1
out=sys.argv[1]; withbgm=len(sys.argv)>2
amap=['-an']
if withbgm:
    inputs+=['-t',f'{T}','-i',SRC]; fc+=f"[{n}:a]afade=t=out:st={T-1.2}:d=1.2[a]"; amap=['-map','[a]','-c:a','aac','-b:a','192k']
else: fc=fc.rstrip(';')
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',fc,'-map',f'[{cur}]',*amap,'-c:v','libx264','-crf','20','-preset','medium','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart','-t',f'{T}',out],check=True)

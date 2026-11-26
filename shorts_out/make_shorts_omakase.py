# 딴짓극장 — "강아지 오마카세" (샤오홍슈 먹방 영상 재편집: 하이라이트만 골라 코스 요리처럼 재배치)
import subprocess, sys, os, glob
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-calculator/92091629-437c-5ff5-ac78-cae4819d3258/scratchpad'
SRC=glob.glob('/root/.claude/uploads/92091629-437c-5ff5-ac78-cae4819d3258/7b44d7a7-*.mp4')[0]
OV=S+'/ov15'; CD=S+'/clips15'; W,H,HD=720,1280,300; VH=H-HD; CY=60
os.makedirs(OV,exist_ok=True); os.makedirs(CD,exist_ok=True)
JUA=S+'/fonts/Jua-Regular.ttf'; BHS=S+'/fonts/BlackHanSans-Regular.ttf'; CJK='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
F=lambda p,s: ImageFont.truetype(p,s)
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
d.rectangle((0,0,W,HD),fill=(255,255,255,255))
lg=Image.open('/home/user/calculator/shorts_out/logo_ddanjit.png').resize((199,112),Image.LANCZOS); im.paste(lg,(32,10),lg)
d.text((250,46),'딴짓극장',font=F(JUA,40),fill=(20,20,20),anchor='lm')
d.text((250,90),'아무 생각 없이 보기 좋은 채널',font=F(JUA,25),fill=(70,70,70),anchor='lm')
f=F(JUA,54); parts=[('강아지한테 ',(15,15,15)),('오마카세를 줬더니',(235,20,30))]
tw=sum(d.textlength(t,font=f) for t,_ in parts); x=(W-tw)/2
for t,c in parts:
    d.text((x,172),t,font=f,fill=c,anchor='lm'); x+=d.textlength(t,font=f)
d.text((W/2,248),'8코스 순식간에 완식',font=F(JUA,56),fill=(70,235,40),anchor='mm',stroke_width=5,stroke_fill=(10,10,10))
a,b='출처: ','小红书'; fa,fb=F(JUA,15),F(CJK,15); wa,wb=d.textlength(a,font=fa),d.textlength(b,font=fb); x0=8; x1=x0+wa+wb+12
d.rounded_rectangle((x0,H-30,x1,H-8),radius=7,fill=(0,0,0,95))
d.text((x0+6,H-19),a,font=fa,fill=(255,255,255,215),anchor='lm'); d.text((x0+6+wa,H-19),b,font=fb,fill=(255,255,255,215),anchor='lm')
im.save(OV+'/header.png')
def cap(text,name):
    im=Image.new('RGBA',(W,240),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.multiline_text((W/2,120),text,font=F(JUA,54),fill='white',anchor='mm',align='center',stroke_width=6,stroke_fill='black',spacing=10)
    im.save(f'{OV}/{name}.png')
def impact(text,name,color=(255,225,0),size=130):
    im=Image.new('RGBA',(W,300),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((W/2+6,156),text,font=F(BHS,size),fill=(0,0,0,255),anchor='mm',stroke_width=12,stroke_fill=(0,0,0))
    d.text((W/2,150),text,font=F(BHS,size),fill=color,anchor='mm',stroke_width=10,stroke_fill=(200,0,0))
    im.rotate(-6,resample=Image.BICUBIC).save(f'{OV}/{name}.png')
SFXC=[(120,215,255),(255,170,210),(255,235,120)]
def sfx(text,name,k):
    im=Image.new('RGBA',(460,200),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((233,104),text,font=F(JUA,72),fill=(0,0,0,150),anchor='mm',stroke_width=9,stroke_fill=(0,0,0,150))
    d.text((230,100),text,font=F(JUA,72),fill=SFXC[k%3],anchor='mm',stroke_width=7,stroke_fill=(255,255,255))
    im.rotate(10 if k%2==0 else -10,resample=Image.BICUBIC).save(f'{OV}/{name}.png')
def tag(text,name,col=(235,20,30)):
    f=F(JUA,34); w=int(ImageDraw.Draw(Image.new('L',(1,1))).textlength(text,font=f))+40
    im=Image.new('RGBA',(w,64),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,w-1,63),radius=16,fill=col+(235,)); d.text((w/2,33),text,font=f,fill='white',anchor='mm'); im.save(f'{OV}/{name}.png')
# (src_start, src_end, course tag, caption, sfx (text,x,y)|None, impact (rel_start,text)|None)
CLIPS=[
 (1.55,2.9,'손님 입장','오늘의 손님 입장',None,(0.45,'와앙!!')),
 (3.6,5.4,'1코스','1코스: 연어',('냠!',250,560),None),
 (10.9,13.1,'2코스','2코스: 양념구이',('쭈욱~',10,560),None),
 (6.3,7.7,'3코스','3코스: 버섯',('와구와구',250,560),None),
 (14.3,15.6,'4코스','4코스: 면 요리',('후루룩',10,560),None),
 (16.6,17.9,'5코스','5코스: 계란',('앙!',250,560),None),
 (22.3,24.1,'6코스','6코스: 새우',('아그작',10,560),None),
 (26.4,28.8,'6코스','(손까지 먹을 기세)',None,None),
 (28.9,29.8,'잠시 대기','다음은요?',None,None),
 (30.1,31.8,'7코스','7코스: 청경채\n(채소도 가리지 않음)',None,None),
 (34.8,36.6,'8코스','8코스: 브로콜리\n편식? 그게 뭐죠',None,None),
 (37.4,39.2,'디저트','디저트까지 깔끔하게',None,(0.9,'완식!!')),
]
ENC=['-c:v','libx264','-crf','14','-preset','fast','-c:a','aac','-b:a','192k','-ar','44100','-ac','2']
T=0; inputs=[]; ov=[]
for i,(a,b,tg,cp,sx,ip) in enumerate(CLIPS):
    L=round(b-a,3)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-t',str(L),'-i',SRC,'-vf',f'fps=30,scale={W}:{H},crop={W}:{VH}:0:{CY},setsar=1','-af',f'afade=t=in:d=0.05,afade=t=out:st={L-0.07}:d=0.07',*ENC,f'{CD}/{i}.mp4'],check=True)
    inputs+=['-i',f'{CD}/{i}.mp4']
    tag(tg,f't{i}'); ov.append((f'{OV}/t{i}.png',20,HD+14,T,T+L))
    cap(cp,f'c{i}'); ov.append((f'{OV}/c{i}.png',0,960,T,T+L))
    if sx: sfx(sx[0],f's{i}',i); ov.append((f'{OV}/s{i}.png',sx[1],sx[2],T+0.15,T+L-0.05))
    if ip: impact(ip[1],f'i{i}'); ov.append((f'{OV}/i{i}.png',0,640,T+ip[0],T+L))
    T+=L
print('total',T)
N=len(CLIPS); inputs+=['-i',OV+'/header.png']; n=N+1; cur='v0'
fc=''.join(f'[{i}:v][{i}:a]' for i in range(N))+f"concat=n={N}:v=1:a=1[cv][a0];[a0]loudnorm=I=-16:TP=-1.5:LRA=11[a];[cv]pad={W}:{H}:0:{HD}:white[base];[base][{N}:v]overlay=0:0[v0];"
for (png,x,y,a,b) in ov:
    inputs+=['-i',png]; fc+=f"[{cur}][{n}:v]overlay={x}:{y}:enable='between(t,{a:.2f},{b-0.04:.2f})'[v{n}];"; cur=f'v{n}'; n+=1
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',fc.rstrip(';'),'-map',f'[{cur}]','-map','[a]','-c:v','libx264','-crf','20','-preset','medium','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','44100','-movflags','+faststart',sys.argv[1]],check=True)

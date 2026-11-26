# 딴짓극장 — "비 오는 날 라면 8봉지" (샤오홍슈 영상 재편집: 하이라이트 재배치 + 한국어 자막)
import subprocess, sys, os, glob
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-calculator/92091629-437c-5ff5-ac78-cae4819d3258/scratchpad'
SRC=glob.glob('/root/.claude/uploads/92091629-437c-5ff5-ac78-cae4819d3258/cc4a5c7a-*.mp4')[0]
OV=S+'/ov16'; CD=S+'/clips16'; W,H,HD=720,1280,300; VH=H-HD
os.makedirs(OV,exist_ok=True); os.makedirs(CD,exist_ok=True)
JUA=S+'/fonts/Jua-Regular.ttf'; BHS=S+'/fonts/BlackHanSans-Regular.ttf'; CJK='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
F=lambda p,s: ImageFont.truetype(p,s)
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
d.rectangle((0,0,W,HD),fill=(255,255,255,255))
lg=Image.open('/home/user/calculator/shorts_out/logo_ddanjit.png').resize((199,112),Image.LANCZOS); im.paste(lg,(32,10),lg)
d.text((250,46),'딴짓극장',font=F(JUA,40),fill=(20,20,20),anchor='lm')
d.text((250,90),'아무 생각 없이 보기 좋은 채널',font=F(JUA,25),fill=(70,70,70),anchor='lm')
f=F(JUA,56); parts=[('비 오는 날 ',(15,15,15)),('라면 8봉지 끓인',(235,20,30))]
tw=sum(d.textlength(t,font=f) for t,_ in parts); x=(W-tw)/2
for t,c in parts:
    d.text((x,172),t,font=f,fill=c,anchor='lm'); x+=d.textlength(t,font=f)
d.text((W/2,248),'강아지들의 캠핑',font=F(JUA,56),fill=(70,235,40),anchor='mm',stroke_width=5,stroke_fill=(10,10,10))
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
def bubble(text,name):   # pink speech box that covers the burned-in Chinese/English caption
    im=Image.new('RGBA',(420,134),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,419,133),radius=34,fill=(255,150,190,255),outline=(255,255,255,255),width=5)
    d.text((210,68),text,font=F(JUA,46),fill='white',anchor='mm',stroke_width=3,stroke_fill=(190,60,110)); im.save(f'{OV}/{name}.png')
# (src_start, src_end, crop_y(in 720x1440), caption|None, sfx (text,x,y)|None, impact (rel,text,y)|None, bubbles [(rel_s,rel_e,text)]|None)
CLIPS=[
 (28.3,30.2,375,'비 오는 날엔 역시',None,(0.5,'라면!!',340),None),
 (0.3,3.4,390,'스프 먼저 톡톡',None,None,None),
 (4.2,7.6,390,'계란은 필수',('주르륵~',250,330),None,None),
 (8.3,11.1,230,'(침 고이는 비주얼)',('보글보글',10,330),None,None),
 (15.4,20.0,375,None,None,None,[(0,2.5,'라면 8봉지, 다 끓였어~'),(2.5,4.6,'배고파아아!')]),
 (20.8,24.0,375,'드디어 한 입',('후루룩',250,330),None,None),
 (33.2,36.5,375,'폭풍 흡입',('호로록',10,330),None,None),
 (38.9,41.4,375,'8봉지가 사라졌다',None,(0.6,'순삭!!',340),None),
 (44.3,46.8,290,'배부르면 뭐다?',None,None,None),
 (47.2,50.5,290,'누워서 만화 보기',None,None,None),
 (53.5,57.5,290,'...그대로 기절',('쿨쿨',250,330),None,None),
 (58.6,61.4,200,'비 오는 날의\n완벽한 하루',None,None,None),
]
snd=len(sys.argv)>2
ENC=['-c:v','libx264','-crf','14','-preset','fast','-c:a','aac','-b:a','192k','-ar','44100','-ac','2']
T=0; inputs=[]; ov=[]
for i,(a,b,cy,cp,sx,ip,bb) in enumerate(CLIPS):
    L=round(b-a,3)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-t',str(L),'-i',SRC,'-vf',f'fps=30,crop={W}:{VH}:0:{cy},setsar=1','-af',f'afade=t=in:d=0.12,afade=t=out:st={L-0.14}:d=0.14',*ENC,f'{CD}/{i}.mp4'],check=True)
    inputs+=['-i',f'{CD}/{i}.mp4']
    if cp: cap(cp,f'c{i}'); ov.append((f'{OV}/c{i}.png',0,960,T,T+L))
    if sx: sfx(sx[0],f's{i}',i); ov.append((f'{OV}/s{i}.png',sx[1],sx[2],T+0.15,T+L-0.05))
    if ip: impact(ip[1],f'i{i}'); ov.append((f'{OV}/i{i}.png',0,ip[2],T+ip[0],T+L))
    for j,(s0,e0,tx) in enumerate(bb or []): bubble(tx,f'b{i}_{j}'); ov.append((f'{OV}/b{i}_{j}.png',150,HD+(742-cy),T+s0,T+e0+0.04))
    T+=L
print('total',T)
N=len(CLIPS); inputs+=['-i',OV+'/header.png']; n=N+1; cur='v0'
fc=''.join(f'[{i}:v][{i}:a]' for i in range(N))+f"concat=n={N}:v=1:a=1[cv][a0];[a0]loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=out:st={T-1.0}:d=1.0[a];[cv]pad={W}:{H}:0:{HD}:white[base];[base][{N}:v]overlay=0:0[v0];"
for (png,x,y,a,b) in ov:
    inputs+=['-i',png]; fc+=f"[{cur}][{n}:v]overlay={x}:{y}:enable='between(t,{a:.2f},{b-0.04:.2f})'[v{n}];"; cur=f'v{n}'; n+=1
am=['-map','[a]','-c:a','aac','-b:a','192k','-ar','44100'] if snd else ['-an']
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',fc.rstrip(';'),'-map',f'[{cur}]',*am,'-c:v','libx264','-crf','20','-preset','medium','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',sys.argv[1]],check=True)

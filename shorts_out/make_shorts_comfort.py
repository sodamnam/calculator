import subprocess, sys, os, glob
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-calculator/92091629-437c-5ff5-ac78-cae4819d3258/scratchpad'
SRC=glob.glob('/root/.claude/uploads/92091629-437c-5ff5-ac78-cae4819d3258/685654a7-*.mp4')[0]
OV=S+'/ov10'; W,H,HD=720,1280,300; VH=H-HD; CY=230
os.makedirs(OV,exist_ok=True)
JUA=S+'/fonts/Jua-Regular.ttf'; CJK='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
F=lambda p,s: ImageFont.truetype(p,s)

# header (딴짓극장) with hook title + tiny source credit bottom-left
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
d.rectangle((0,0,W,HD),fill=(255,255,255,255))
lg=Image.open('/home/user/calculator/shorts_out/logo_ddanjit.png').resize((199,112),Image.LANCZOS); im.paste(lg,(32,10),lg)
d.text((250,46),'딴짓극장',font=F(JUA,40),fill=(20,20,20),anchor='lm')
d.text((250,90),'아무 생각 없이 보기 좋은 채널',font=F(JUA,25),fill=(70,70,70),anchor='lm')
f=F(JUA,56); parts=[('외로워서 ',(15,15,15)),('고개를 돌렸더니',(235,20,30))]
tw=sum(d.textlength(t,font=f) for t,_ in parts); x=(W-tw)/2
for t,c in parts:
    d.text((x,172),t,font=f,fill=c,anchor='lm'); x+=d.textlength(t,font=f)
d.text((W/2,248),'강아지가 이러고 있었다',font=F(JUA,56),fill=(70,235,40),anchor='mm',stroke_width=5,stroke_fill=(10,10,10))
a,b='출처: ','小红书'; fa,fb=F(JUA,15),F(CJK,15); wa,wb=d.textlength(a,font=fa),d.textlength(b,font=fb); x0=8; x1=x0+wa+wb+12
d.rounded_rectangle((x0,H-30,x1,H-8),radius=7,fill=(0,0,0,95))
d.text((x0+6,H-19),a,font=fa,fill=(255,255,255,215),anchor='lm'); d.text((x0+6+wa,H-19),b,font=fb,fill=(255,255,255,215),anchor='lm')
im.save(OV+'/header.png')

def cap(text,name):
    im=Image.new('RGBA',(W,240),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.multiline_text((W/2,120),text,font=F(JUA,54),fill='white',anchor='mm',align='center',stroke_width=6,stroke_fill='black',spacing=12)
    im.save(f'{OV}/{name}.png')
def soft(text,name):   # quiet, small aside
    im=Image.new('RGBA',(360,120),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((180,60),text,font=F(JUA,52),fill=(255,240,200),anchor='mm',stroke_width=5,stroke_fill=(60,40,20))
    im.rotate(-6,resample=Image.BICUBIC).save(f'{OV}/{name}.png')

T=15.4
# Korean rendering of the on-screen Chinese caption, spread over the clip
CAPS=[(0,1.6,'혼자 오후까지 자다 깼는데'),(1.6,4.2,'외로움이 왈칵 밀려와\n고개를 돌려 보니'),(4.2,8.2,'우리 강아지가 말없이\n나를 지키고 있었다..'),
      (8.2,12.0,'이 순간,\n모든 게 다 괜찮아졌다'),(12.0,T,'늘 거기 있어 줘서 고마워')]
SOFT=[(6.0,8.0,'(지그시)',350,330)]
# remove the burned-in Chinese caption (only present until 5.8s), then frame
vf=f"fps=30,scale={W}:{H},delogo=x=118:y=222:w=290:h=206:enable='lt(t,5.8)',crop={W}:{VH}:0:{CY},setsar=1,pad={W}:{H}:0:{HD}:white"
inputs=['-i',SRC,'-i',OV+'/header.png']; n=2; cur='v0'
fc=f"[0:v]{vf}[base];[base][1:v]overlay=0:0[v0];"
def add(png,x,y,a,b):
    global n,cur,fc,inputs
    inputs+=['-i',png]; fc+=f"[{cur}][{n}:v]overlay={x}:{y}:enable='between(t,{a:.2f},{b-0.04:.2f})'[v{n}];"; cur=f'v{n}'; n+=1
for i,(a,b,t) in enumerate(CAPS): cap(t,f'c{i}'); add(f'{OV}/c{i}.png',0,960,a,b)
for i,(a,b,t,x,y) in enumerate(SOFT): soft(t,f's{i}'); add(f'{OV}/s{i}.png',x,y,a,b)
out=sys.argv[1]; snd=len(sys.argv)>2
am=['-map','0:a','-af',f'afade=t=out:st={T-1.2}:d=1.2','-c:a','aac','-b:a','192k'] if snd else ['-an']
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',fc.rstrip(';'),'-map',f'[{cur}]',*am,'-c:v','libx264','-crf','19','-preset','medium','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart','-t',f'{T}',out],check=True)

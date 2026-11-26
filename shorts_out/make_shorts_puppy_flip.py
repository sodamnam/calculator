import subprocess, sys, os, glob
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-calculator/92091629-437c-5ff5-ac78-cae4819d3258/scratchpad'
SRC=glob.glob('/root/.claude/uploads/92091629-437c-5ff5-ac78-cae4819d3258/bab2840d-*.mp4')[0]
OV=S+'/ov8'; CD=S+'/clips8'; W,H,HD=720,1280,300; VH=H-HD; SH=1310; CY=180
os.makedirs(OV,exist_ok=True); os.makedirs(CD,exist_ok=True)
JUA=S+'/fonts/Jua-Regular.ttf'; BHS=S+'/fonts/BlackHanSans-Regular.ttf'
F=lambda p,s: ImageFont.truetype(p,s)

# header (딴짓극장) with hook title
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
d.rectangle((0,0,W,HD),fill=(255,255,255,255))
lg=Image.open('/home/user/calculator/shorts_out/logo_ddanjit.png').resize((199,112),Image.LANCZOS); im.paste(lg,(32,10),lg)
d.text((250,46),'딴짓극장',font=F(JUA,40),fill=(20,20,20),anchor='lm')
d.text((250,90),'아무 생각 없이 보기 좋은 채널',font=F(JUA,25),fill=(70,70,70),anchor='lm')
f=F(JUA,58); parts=[('잘 보세요, ',(15,15,15)),('딱 2초 뒤',(235,20,30))]
tw=sum(d.textlength(t,font=f) for t,_ in parts); x=(W-tw)/2
for t,c in parts:
    d.text((x,172),t,font=f,fill=c,anchor='lm'); x+=d.textlength(t,font=f)
d.text((W/2,248),'강아지가 사라집니다',font=F(JUA,58),fill=(70,235,40),anchor='mm',stroke_width=5,stroke_fill=(10,10,10))
t='출처: @mariaelekessings'; fa=F(JUA,15); wa=d.textlength(t,font=fa); x0=8; x1=x0+wa+12
d.rounded_rectangle((x0,H-30,x1,H-8),radius=7,fill=(0,0,0,95)); d.text((x0+6,H-19),t,font=fa,fill=(255,255,255,215),anchor='lm')
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
SFXC=[(120,215,255),(255,170,210),(255,235,120)]
def sfx(text,name,k):
    im=Image.new('RGBA',(460,200),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((233,104),text,font=F(JUA,74),fill=(0,0,0,150),anchor='mm',stroke_width=9,stroke_fill=(0,0,0,150))
    d.text((230,100),text,font=F(JUA,74),fill=SFXC[k%3],anchor='mm',stroke_width=7,stroke_fill=(255,255,255))
    im.rotate(10 if k%2==0 else -10,resample=Image.BICUBIC).save(f'{OV}/{name}.png')
def label(text,name):
    im=Image.new('RGBA',(300,70),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,299,69),radius=18,fill=(235,20,30,235)); d.text((150,36),text,font=F(JUA,36),fill='white',anchor='mm'); im.save(f'{OV}/{name}.png')

ENC=['-c:v','libx264','-crf','14','-preset','fast','-c:a','aac','-b:a','192k','-ar','44100','-ac','2']
base=f'fps=30,scale={W}:{SH},crop={W}:{VH}:0:{CY},setsar=1'
subprocess.run(['ffmpeg','-v','error','-y','-i',SRC,'-t','5.5','-vf',base,'-af','afade=t=out:st=5.35:d=0.15',*ENC,f'{CD}/a.mp4'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-ss','1.15','-t','0.85','-i',SRC,'-vf',f'setpts=PTS/0.35,{base}','-af','atempo=0.5,atempo=0.7,afade=t=in:d=0.1',*ENC,f'{CD}/b.mp4'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-ss','5.4','-i',SRC,'-frames:v','1','-update','1',f'{CD}/last.png'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-t','1.6','-i',f'{CD}/last.png','-f','lavfi','-t','1.6','-i','anullsrc=r=44100:cl=stereo',
  '-vf',f"scale={W}:{SH},crop={W}:{VH}:0:{CY},scale={W*3}:{VH*3},zoompan=z='1+0.25*on/48':x='(iw-iw/zoom)*0.75':y='(ih-ih/zoom)*0.05':d=1:s={W}x{VH}:fps=30,setsar=1",
  '-shortest',*ENC,f'{CD}/c.mp4'],check=True)
dur=lambda p: float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
A,B,C=dur(f'{CD}/a.mp4'),dur(f'{CD}/b.mp4'),dur(f'{CD}/c.mp4'); T=A+B+C; print('total',A,B,C,T)

CAPS=[(0,1.3,'신난다! 신난다!'),(1.3,1.75,'어...?'),(1.75,2.7,'(화면 밖으로 퇴장)'),(2.7,3.5,'소파 뒤에서 발견'),(3.5,A,'아무 일 없었다는 듯 복귀'),
      (A,A+B,'흥이 너무 올랐던 탓'),(A+B,T,'방금 뭐가 지나갔개?')]
IMPS=[(1.7,2.6,'어어어?!',360),(A+B+0.1,T,'멀쩡!!',600)]
SFX=[(0.05,1.2,'파닥파닥',10,640),(2.7,3.4,'데구르르',250,330),(3.7,5.3,'총총총',20,330),(A+0.2,A+B-0.1,'벌러덩~',250,640)]
LAB=[(A,A+B,'다시 보기',20,HD+12)]
inputs=['-i',f'{CD}/a.mp4','-i',f'{CD}/b.mp4','-i',f'{CD}/c.mp4','-i',OV+'/header.png']; n=4; cur='v0'
fc=f"[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[cv][a];[cv]pad={W}:{H}:0:{HD}:white[base];[base][3:v]overlay=0:0[v0];"
def add(png,x,y,a,b):
    global n,cur,fc,inputs
    inputs+=['-i',png]; fc+=f"[{cur}][{n}:v]overlay={x}:{y}:enable='between(t,{a:.2f},{b-0.04:.2f})'[v{n}];"; cur=f'v{n}'; n+=1
for i,(a,b,t) in enumerate(CAPS): cap(t,f'c{i}'); add(f'{OV}/c{i}.png',0,960,a,b)
for i,(a,b,t,x,y) in enumerate(SFX): sfx(t,f's{i}',i); add(f'{OV}/s{i}.png',x,y,a,b)
for i,(a,b,t,y) in enumerate(IMPS): impact(t,f'i{i}'); add(f'{OV}/i{i}.png',0,y,a,b)
for i,(a,b,t,x,y) in enumerate(LAB): label(t,f'l{i}'); add(f'{OV}/l{i}.png',x,y,a,b)
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',fc.rstrip(';'),'-map',f'[{cur}]','-map','[a]','-c:v','libx264','-crf','20','-preset','medium','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',sys.argv[1]],check=True)

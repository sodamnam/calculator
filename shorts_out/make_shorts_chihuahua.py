import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-calculator/92091629-437c-5ff5-ac78-cae4819d3258/scratchpad'
SRC='/root/.claude/uploads/92091629-437c-5ff5-ac78-cae4819d3258/f345a90b-FurryHouseFinds_video_no_watermark.mp4'
OV=S+'/ov7'; CD=S+'/clips7'; W,H,HD=720,1280,300; VH=H-HD; CY=80
os.makedirs(OV,exist_ok=True); os.makedirs(CD,exist_ok=True)
JUA=S+'/fonts/Jua-Regular.ttf'; BHS=S+'/fonts/BlackHanSans-Regular.ttf'
F=lambda p,s: ImageFont.truetype(p,s)

# header (딴짓극장)
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
d.rectangle((0,0,W,HD),fill=(255,255,255,255))
lg=Image.open('/home/user/calculator/shorts_out/logo_ddanjit.png').resize((199,112),Image.LANCZOS); im.paste(lg,(32,10),lg)
d.text((250,46),'딴짓극장',font=F(JUA,40),fill=(20,20,20),anchor='lm')
d.text((250,90),'아무 생각 없이 보기 좋은 채널',font=F(JUA,25),fill=(70,70,70),anchor='lm')
f=F(JUA,56); parts=[('밥 먹는데 ',(15,15,15)),('옆에서 짖었더니',(235,20,30))]
tw=sum(d.textlength(t,font=f) for t,_ in parts); x=(W-tw)/2
for t,c in parts:
    d.text((x,172),t,font=f,fill=c,anchor='lm'); x+=d.textlength(t,font=f)
d.text((W/2,248),'1초 만에 조용해진 치와와',font=F(JUA,54),fill=(70,235,40),anchor='mm',stroke_width=5,stroke_fill=(10,10,10))
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
def sfx(text,name,k):
    im=Image.new('RGBA',(460,200),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((233,104),text,font=F(JUA,74),fill=(0,0,0,150),anchor='mm',stroke_width=9,stroke_fill=(0,0,0,150))
    d.text((230,100),text,font=F(JUA,74),fill=SFXC[k%3],anchor='mm',stroke_width=7,stroke_fill=(255,255,255))
    im.rotate(10 if k%2==0 else -10,resample=Image.BICUBIC).save(f'{OV}/{name}.png')
def label(text,name):
    im=Image.new('RGBA',(300,70),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,299,69),radius=18,fill=(235,20,30,235)); d.text((150,36),text,font=F(JUA,36),fill='white',anchor='mm'); im.save(f'{OV}/{name}.png')

ENC=['-c:v','libx264','-crf','14','-preset','fast','-c:a','aac','-b:a','192k','-ar','44100','-ac','2']
base=f'fps=30,scale={W}:{H},crop={W}:{VH}:0:{CY},setsar=1'
# A: full clip, original sound
subprocess.run(['ffmpeg','-v','error','-y','-i',SRC,'-t','9.45','-vf',base,'-af','afade=t=out:st=9.3:d=0.15',*ENC,f'{CD}/a.mp4'],check=True)
# B: slow replay of the key moment (0.35x), slowed original sound
subprocess.run(['ffmpeg','-v','error','-y','-ss','1.0','-t','0.95','-i',SRC,'-vf',f'setpts=PTS/0.35,{base}','-af','atempo=0.5,atempo=0.7,afade=t=in:d=0.1',*ENC,f'{CD}/b.mp4'],check=True)
# C: slow zoom on the final frame, silent
subprocess.run(['ffmpeg','-v','error','-y','-ss','9.3','-i',SRC,'-frames:v','1','-update','1',f'{CD}/last.png'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-t','1.8','-i',f'{CD}/last.png','-f','lavfi','-t','1.8','-i','anullsrc=r=44100:cl=stereo',
  '-vf',f"scale={W}:{H},crop={W}:{VH}:0:{CY},scale={W*3}:{VH*3},zoompan=z='1+0.18*on/54':x='(iw-iw/zoom)*0.42':y='(ih-ih/zoom)*0.30':d=1:s={W}x{VH}:fps=30,setsar=1",
  '-shortest',*ENC,f'{CD}/c.mp4'],check=True)
dur=lambda p: float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
A,B,C=dur(f'{CD}/a.mp4'),dur(f'{CD}/b.mp4'),dur(f'{CD}/c.mp4'); T=A+B+C; print('total',A,B,C,T)

CAPS=[(0,1.15,'밥 먹는데 옆에서 계속...'),(1.15,2.4,'"좀 조용히 해"'),(2.4,4.4,'그대로 음소거'),(4.4,6.2,'천천히 고개를 듭니다'),(6.2,A,'집사야... 방금 봤지?'),
      (A,A+B,'정수리에 정확히 "꾹"'),(A+B,T,'오늘의 교훈:\n밥 먹을 땐 조용히')]
IMPS=[(1.2,2.2,'꾹!!',380),(A+B+0.15,T,'팩 완료!!',330)]
SFX=[(0.05,1.1,'왈왈왈!',10,330),(2.6,4.2,'(정적)',250,330),(6.4,8.6,'뚝.. 뚝..',250,640),(A+0.2,A+B-0.1,'꾸우욱~',240,330)]
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

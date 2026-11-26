# 딴짓극장 — "간식 도둑 검거" (원본: 王多多). 구성 각색: 콜드오픈 → 사건 20초 전 → 본편 → 유사 사건 컷 → 사건 종결 카드
import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
S='/tmp/claude-0/-home-user-calculator/92091629-437c-5ff5-ac78-cae4819d3258/scratchpad'
U='/root/.claude/uploads/92091629-437c-5ff5-ac78-cae4819d3258/'
SRC=U+'2721cace-dl.mp4'; CHI=U+'f345a90b-FurryHouseFinds_video_no_watermark.mp4'; BANNER=U+'f07f03ee-image.png'
OV=S+'/ov14'; CD=S+'/clips14'; W,H,HD=720,1280,300; VH=H-HD
os.makedirs(OV,exist_ok=True); os.makedirs(CD,exist_ok=True)
JUA=S+'/fonts/Jua-Regular.ttf'; BHS=S+'/fonts/BlackHanSans-Regular.ttf'; CJK='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
F=lambda p,s: ImageFont.truetype(p,s)
def grab(src,t,out,vf):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',src,'-frames:v','1','-vf',vf,'-update','1',out],check=True); return Image.open(out).convert('RGB')
TOP="crop=706:960:7:0,scale=720:980"     # keep the top part only: the burned-in Chinese captions sit below it

# ---------- header ----------
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
d.rectangle((0,0,W,HD),fill=(255,255,255,255))
lg=Image.open('/home/user/calculator/shorts_out/logo_ddanjit.png').resize((199,112),Image.LANCZOS); im.paste(lg,(32,10),lg)
d.text((250,46),'딴짓극장',font=F(JUA,40),fill=(20,20,20),anchor='lm')
d.text((250,90),'아무 생각 없이 보기 좋은 채널',font=F(JUA,25),fill=(70,70,70),anchor='lm')
f=F(JUA,56); parts=[('간식 훔쳐 먹고 ',(15,15,15)),('자는 척',(235,20,30))]
tw=sum(d.textlength(t,font=f) for t,_ in parts); x=(W-tw)/2
for t,c in parts:
    d.text((x,172),t,font=f,fill=c,anchor='lm'); x+=d.textlength(t,font=f)
d.text((W/2,248),'(입에 증거가 남아 있음)',font=F(JUA,54),fill=(70,235,40),anchor='mm',stroke_width=5,stroke_fill=(10,10,10))
a,b='출처: ','王多多'; fa,fb=F(JUA,15),F(CJK,15); wa,wb=d.textlength(a,font=fa),d.textlength(b,font=fb); x0=8; x1=x0+wa+wb+12
d.rounded_rectangle((x0,H-30,x1,H-8),radius=7,fill=(0,0,0,95))
d.text((x0+6,H-19),a,font=fa,fill=(255,255,255,215),anchor='lm'); d.text((x0+6+wa,H-19),b,font=fb,fill=(255,255,255,215),anchor='lm')
im.save(OV+'/header.png')

# ---------- text helpers ----------
def cap(text,name):
    im=Image.new('RGBA',(W,240),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.multiline_text((W/2,120),text,font=F(JUA,52),fill='white',anchor='mm',align='center',stroke_width=6,stroke_fill='black',spacing=10)
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
    d.rounded_rectangle((0,0,w-1,63),radius=16,fill=col+(235,)); d.text((w/2,33),text,font=f,fill='white',anchor='mm'); im.save(f'{OV}/{name}.png'); return w
def framed(img,size,label,name):   # evidence photo: white frame + red label
    w,h=size; im=Image.new('RGBA',(w+16,h+62),(255,255,255,255)); im.paste(img.resize((w,h),Image.LANCZOS),(8,8))
    d=ImageDraw.Draw(im); d.text(((w+16)/2,h+34),label,font=F(JUA,28),fill=(200,20,30),anchor='mm')
    sh=Image.new('RGBA',(w+56,h+102),(0,0,0,0)); ImageDraw.Draw(sh).rectangle((24,26,w+40,h+88),fill=(0,0,0,150)); sh=sh.filter(ImageFilter.GaussianBlur(8)); sh.alpha_composite(im,(20,20))
    sh.save(f'{OV}/{name}.png'); return sh

# ---------- stills ----------
dash=grab(SRC,2.6,CD+'/dash.png',TOP); crumbs=grab(SRC,7.5,CD+'/crumbs.png',TOP); loot=grab(SRC,20.2,CD+'/loot.png',TOP)
ev_crumbs=crumbs.crop((180,360,640,760)); ev_dash=dash.crop((90,440,450,760)); ev_loot=loot.crop((250,330,720,740))
# B: "사건 발생 20초 전" card
b=ImageEnhance.Brightness(dash.filter(ImageFilter.GaussianBlur(14))).enhance(0.45).convert('RGBA'); d=ImageDraw.Draw(b)
d.text((W/2,400),'사건 발생',font=F(BHS,92),fill='white',anchor='mm',stroke_width=8,stroke_fill='black')
d.text((W/2,520),'20초 전',font=F(BHS,130),fill=(255,225,0),anchor='mm',stroke_width=10,stroke_fill=(200,0,0))
b.convert('RGB').save(CD+'/cardB.png')
# E: "사건 종결" card with three evidence photos
ban=Image.open(BANNER).convert('RGB'); e=ban.resize((int(980*ban.width/ban.height),980),Image.LANCZOS).crop((300,0,1020,980)).filter(ImageFilter.GaussianBlur(20))
e=ImageEnhance.Brightness(e).enhance(0.4).convert('RGBA'); d=ImageDraw.Draw(e)
d.text((W/2,110),'사건 종결',font=F(BHS,110),fill=(255,225,0),anchor='mm',stroke_width=10,stroke_fill=(200,0,0))
for i,(img,lab,ang,pos) in enumerate([(ev_dash,'1. 도주 장면',-5,(20,230)),(ev_crumbs,'2. 범행 현장',4,(370,250)),(ev_loot,'3. 압수품',-2,(185,560))]):
    ph=framed(img,(300,230) if i<2 else (330,250),lab,f'ph{i}').rotate(ang,resample=Image.BICUBIC,expand=True); e.alpha_composite(ph,pos)
d.text((W/2,925),'딴짓극장 수사대',font=F(JUA,40),fill='white',anchor='mm',stroke_width=5,stroke_fill='black')
e.convert('RGB').save(CD+'/cardE.png')
framed(ev_crumbs,(210,180),'증거 1','inset')

# ---------- segments ----------
ENC=['-c:v','libx264','-crf','14','-preset','fast','-r','30','-c:a','aac','-b:a','192k','-ar','44100','-ac','2']
def clip(name,src,ss,t,vf,af='anull'):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(ss),'-t',str(t),'-i',src,'-vf',f'fps=30,{vf},setsar=1','-af',f'{af},afade=t=in:d=0.05,afade=t=out:st={t-0.08}:d=0.08',*ENC,f'{CD}/{name}.mp4'],check=True)
def still(name,png,t):
    subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-t',str(t),'-i',png,'-f','lavfi','-t',str(t),'-i','anullsrc=r=44100:cl=stereo','-vf',f"scale={W*2}:{VH*2},zoompan=z='1+0.05*on/{int(t*30)}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s={W}x{VH}:fps=30,setsar=1",'-shortest',*ENC,f'{CD}/{name}.mp4'],check=True)
clip('a',SRC,10.7,1.7,"crop=560:762:40:150,scale=720:980")          # cold open: the suspect "asleep"
still('b',CD+'/cardB.png',1.0)
clip('c',SRC,0.8,23.05,TOP)                                           # the full story
clip('d',CHI,8.3,1.3,"scale=720:1280,crop=720:980:0:80")              # cutaway: an earlier "case" from this channel
still('e',CD+'/cardE.png',2.2)
dur=lambda n: float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{CD}/{n}.mp4']))
A,B,C,D,E=[dur(n) for n in 'abcde']; tB=A; tC=A+B; tD=tC+C; tE=tD+D; T=tE+E; print('total',T)
o=lambda s: tC+(s-0.8)      # source time of the main story -> output time

# Korean dub lines: (source start time, wav index, speed, caption). Chinese speech is muted and replaced by these.
DUB=[(1.0,0,1.0,'"나 왔어~"'),(3.1,1,1.0,'"어? 왜 도망가?"'),(6.8,2,1.0,'"하... 진짜 못 말려"'),(8.6,3,1.0,'"누가 훔쳐 먹었어, 둬둬?"'),
     (10.9,5,1.1,'"아니, 너 진짜 웃긴다"'),(13.55,6,1.12,'"나 어릴 때 몰래 TV 보던 거랑\n똑같네"'),(16.5,8,1.0,'"잠깐!"'),
     (17.5,9,1.0,'"입에 이건 뭐야?"'),(20.2,10,1.1,'"미처 못 삼켰구나"'),(22.45,11,1.0,'"현행범 검거!"')]
DD='/home/user/calculator/shorts_out/snack_thief_dub'
import wave, numpy as np
def rd(p):
    w=wave.open(p); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768; w.close(); return x
LINES=[]
for (st,i,sp,txt) in DUB:
    p=f'{CD}/dub{i}.wav'; subprocess.run(['ffmpeg','-v','error','-y','-i',f'{DD}/t{i}.wav','-af',f'atempo={sp}','-ar','44100','-ac','1','-c:a','pcm_s16le',p],check=True)
    x=rd(p); x=x/max(1e-6,abs(x).max())*0.7; LINES.append((st,x,txt))
CAPS=[(0,A,'지금 이 강아지는\n자는 척을 하고 있습니다')]
for j,(st,x,txt) in enumerate(LINES):
    en=st+len(x)/44100; nxt=LINES[j+1][0] if j+1<len(LINES) else 99
    CAPS.append((o(st),min(o(min(en+0.5,nxt-0.03)),tD),txt))
CAPS+=[(o(5.3),o(6.7),'(수상한 예감)'),(o(19.3),o(20.2),'(배 보이며 선처 호소 중)'),(tD,tE,'유사 사건: 증거를 얼굴에\n묻히고 다닌 용의자')]
IMPS=[(o(16.5),o(17.4),'잠깐!!',380,130),(o(22.5),tD,'검거!!',330,130)]
SFX=[(o(2.45),o(3.0),'후다닥!',240,480),(o(9.9),o(10.9),'쿨쿨...',250,330),(o(19.0),o(20.2),'발라당~',10,330)]
TAGS=[(0,A,'용의자',20,HD+14),(o(6.5),o(9.8),'범행 현장',20,HD+14),(o(11.0),o(22.0),'용의자 취조 중',20,HD+14),(tD,tE,'딴짓극장 사건 파일',20,HD+14)]
INSET=(o(11.0),o(16.0),W-266,HD+8)
inputs=[]; 
for n in 'abcde': inputs+=['-i',f'{CD}/{n}.mp4']
inputs+=['-i',OV+'/header.png']; n=6; cur='v0'
fc=''.join(f'[{i}:v][{i}:a]' for i in range(5))+f"concat=n=5:v=1:a=1[cv][a];[cv]pad={W}:{H}:0:{HD}:white[base];[base][5:v]overlay=0:0[v0];"
def add(png,x,y,a,b):
    global n,cur,fc,inputs
    inputs+=['-i',png]; fc+=f"[{cur}][{n}:v]overlay={x}:{y}:enable='between(t,{a:.2f},{b-0.04:.2f})'[v{n}];"; cur=f'v{n}'; n+=1
add(OV+'/inset.png',INSET[2],INSET[3],INSET[0],INSET[1])
for i,(a,b,t,x,y) in enumerate(TAGS): tag(t,f't{i}'); add(f'{OV}/t{i}.png',x,y,a,b)
for i,(a,b,t) in enumerate(CAPS): cap(t,f'c{i}'); add(f'{OV}/c{i}.png',0,960,a,b)
for i,(a,b,t,x,y) in enumerate(SFX): sfx(t,f's{i}',i); add(f'{OV}/s{i}.png',x,y,a,b)
for i,(a,b,t,y,sz) in enumerate(IMPS): impact(t,f'i{i}',size=sz); add(f'{OV}/i{i}.png',0,y,a,b)
tmp=CD+'/video_orig_audio.mp4'
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',fc.rstrip(';'),'-map',f'[{cur}]','-map','[a]','-c:v','libx264','-crf','20','-preset','medium','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',tmp],check=True)
# ---------- audio: mute the Chinese speech, lay room tone under the gaps, add the Korean lines ----------
SR=44100
subprocess.run(['ffmpeg','-v','error','-y','-i',tmp,'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',CD+'/mix_in.wav'],check=True); mix=rd(CD+'/mix_in.wav').copy()
subprocess.run(['ffmpeg','-v','error','-y','-ss','2.05','-t','0.8','-i',SRC,'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',CD+'/tone.wav'],check=True); tone=rd(CD+'/tone.wav')
fd=int(0.04*SR); ramp=np.linspace(0,1,fd); tone[:fd]*=ramp; tone[-fd:]*=ramp[::-1]
MUTE=[(0,A)]+[(o(a),min(o(b),tD)) for a,b in [(0.85,2.0),(3.0,5.6),(6.7,17.3),(17.4,19.5),(20.1,23.9)]]
gain=np.ones(len(mix),dtype=np.float32)
for a0,b0 in MUTE:
    i0,i1=int(a0*SR),min(int(b0*SR),len(mix)); gain[i0:i1]=0
    gain[max(0,i0-fd):i0]=np.minimum(gain[max(0,i0-fd):i0],ramp[::-1][-(i0-max(0,i0-fd)):] if i0>0 else 1); gain[i1:i1+fd]=np.minimum(gain[i1:i1+fd],ramp[:len(gain[i1:i1+fd])])
bed=np.tile(tone,int(len(mix)/len(tone))+2)[:len(mix)]*(1-gain); bed[int(tD*SR):]=0
mix=mix*gain+bed
for (st,x,txt) in LINES:
    i0=int(o(st)*SR); x=x[:max(0,len(mix)-i0)]; mix[i0:i0+len(x)]+=x
mix=np.clip(mix,-1,1); w=wave.open(CD+'/mix_out.wav','w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes()); w.close()
subprocess.run(['ffmpeg','-v','error','-y','-i',tmp,'-i',CD+'/mix_out.wav','-map','0:v','-map','1:a','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','192k','-ar','44100','-movflags','+faststart','-shortest',sys.argv[1]],check=True)

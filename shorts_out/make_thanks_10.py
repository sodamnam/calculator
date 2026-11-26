# 구독자 10명 감사 영상 (딴짓극장) — 배너 + 편지형 자막. 내레이션 파일을 주면 그 길이에 맞춰 붙인다.
import subprocess, sys, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
S='/tmp/claude-0/-home-user-calculator/92091629-437c-5ff5-ac78-cae4819d3258/scratchpad'
BANNER='/root/.claude/uploads/92091629-437c-5ff5-ac78-cae4819d3258/f07f03ee-image.png'
W,H,FPS=720,1280,30
JUA=S+'/fonts/Jua-Regular.ttf'; F=lambda s: ImageFont.truetype(JUA,s)
DISP=['딴짓극장에\n열 분이 앉아 계십니다.','누군가에겐\n작은 숫자겠지만','저에겐 객석에\n불이 켜진 날입니다.','다시 처음부터\n문을 연 극장에','먼저 찾아와 주셔서\n고맙습니다.',
      '귀한 시간,\n잠깐 머무르시는 동안','그 시간만큼은 오로지','아무 생각 없이 쉬어 가는\n안식처가 되도록 만들겠습니다.','추운 날씨,\n감기 조심하세요.','딴짓극장 올림']
import json
LEAD=0.6   # silence before the narration starts
TM=json.load(open('/home/user/calculator/shorts_out/thanks_10_timing.json'))   # [start, end, text] per line from the TTS alignment
LINES=[]
for i,(st,en,_) in enumerate(TM):
    nxt=TM[i+1][0] if i+1<len(TM) else en+1.6
    LINES.append((LEAD+st-0.1, LEAD+min(nxt-0.05, en+0.9) if i+1<len(TM) else LEAD+nxt, DISP[i]))
T=LINES[-1][1]+0.7
ban=Image.open(BANNER).convert('RGB')
# background: blurred, darkened banner covering the frame (slightly oversized for slow drift)
bg=ban.resize((int(1400*ban.width/ban.height),1400),Image.LANCZOS).filter(ImageFilter.GaussianBlur(28))
bg=ImageEnhance.Brightness(bg).enhance(0.42)
CW,CH=664,int(664*ban.height/ban.width)
def card(z):   # banner card with gentle zoom, rounded corners
    w,h=ban.width/z,ban.height/z; x0,y0=(ban.width-w)*0.45,(ban.height-h)*0.5
    c=ban.crop((int(x0),int(y0),int(x0+w),int(y0+h))).resize((CW,CH),Image.BICUBIC)
    m=Image.new('L',(CW,CH),0); ImageDraw.Draw(m).rounded_rectangle((0,0,CW-1,CH-1),radius=34,fill=255); return c,m
def text_layer(text,size,fill,stroke,alpha,spacing=16,sw=6):
    im=Image.new('RGBA',(W,360),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.multiline_text((W/2,180),text,font=F(size),fill=fill,anchor='mm',align='center',stroke_width=sw,stroke_fill=stroke,spacing=spacing)
    if alpha<1: im.putalpha(im.getchannel('A').point(lambda v:int(v*alpha)))
    return im
random.seed(7); snow=[(random.random()*W,random.random()*H,1.5+random.random()*3,25+random.random()*45,random.random()*6.28) for _ in range(70)]
title1=text_layer('관객 10명 돌파',84,(255,222,70),(40,25,5),1,sw=7); title2=text_layer('감사합니다',52,(255,255,255),(20,20,30),1,sw=5)
out=sys.argv[1]; audio=sys.argv[2] if len(sys.argv)>2 else None
cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-']
if audio: cmd+=['-i',audio,'-af',f'adelay={int(LEAD*1000)}:all=1,apad,loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','192k','-t',f'{T}']
cmd+=['-c:v','libx264','-crf','19','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',out]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
N=int(T*FPS)
for i in range(N):
    t=i/FPS; k=t/T
    dx=int((bg.width-W)*(0.15+0.5*k)); fr=bg.crop((dx,60,dx+W,60+H)).convert('RGBA')
    c,m=card(1.0+0.07*k); sh=Image.new('RGBA',(CW+40,CH+40),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((20,24,CW+20,CH+24),radius=34,fill=(0,0,0,150))
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)),((W-CW)//2-20,330-20)); fr.paste(c,((W-CW)//2,330),m)
    a=min(1,t/0.8); 
    if a<1:
        t1=title1.copy(); t1.putalpha(t1.getchannel('A').point(lambda v:int(v*a))); t2=title2.copy(); t2.putalpha(t2.getchannel('A').point(lambda v:int(v*a)))
    else: t1,t2=title1,title2
    fr.alpha_composite(t1,(0,-20)); fr.alpha_composite(t2,(0,70))
    for (s,e,tx) in LINES:
        if s<=t<e:
            al=min(1,(t-s)/0.35,(e-t)/0.3); big=tx=='딴짓극장 올림'
            fr.alpha_composite(text_layer(tx,70 if big else 56,(255,236,170) if big else (255,255,255),(15,15,25),max(0,al)),(0,760+int(14*(1-min(1,(t-s)/0.35)))))
    d=ImageDraw.Draw(fr)
    for (x,y,r,v,ph) in snow:
        yy=(y+v*t)%H; xx=(x+18*math.sin(t*0.8+ph))%W; d.ellipse((xx-r,yy-r,xx+r,yy+r),fill=(255,255,255,150))
    if t>T-0.6: fr=Image.blend(fr,Image.new('RGBA',(W,H),(0,0,0,255)),min(1,(t-(T-0.6))/0.6))
    p.stdin.write(fr.convert('RGB').tobytes())
p.stdin.close(); p.wait()

"""Render the profile HUD: Pillow + FFmpeg, 240 frames / 4 seconds / 60 fps."""
from pathlib import Path
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
W, H, SCALE, FPS, COUNT = 1000, 560, 2, 60, 240
CYAN, WHITE, MUTED = '#75e6ed', '#e0edf0', '#6e929f'

def font(size, mono=False):
    names = (['C:/Windows/Fonts/consola.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'] if mono else
             ['C:/Windows/Fonts/segoeuil.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size * SCALE)
    raise RuntimeError('Install DejaVu Sans or Segoe UI fonts to render the hero.')

FONTS = {(s, m): font(s, m) for s, m in [(10,True),(11,True),(12,True),(14,True),(18,False),(48,False),(56,False)]}

def line(d, points, fill, width=1):
    d.line([(int(x*SCALE),int(y*SCALE)) for x,y in points], fill=fill, width=max(1,round(width*SCALE)))

def text(d, xy, value, size=11, fill=MUTED, mono=True):
    d.text((xy[0]*SCALE,xy[1]*SCALE), value, font=FONTS[size,mono], fill=fill)

def arc(d, r, start, end, fill, width=1, center=(747,279)):
    x,y=center
    d.arc(tuple(round(v*SCALE) for v in (x-r,y-r,x+r,y+r)), start, end, fill=fill, width=max(1,round(width*SCALE)))

def polar(r,a):
    return (747+r*math.cos(a),279+r*math.sin(a))

base = Image.new('RGB',(W*SCALE,H*SCALE),'#050a10')
bd=ImageDraw.Draw(base)
# Subtle radial illumination, integrated into the panel instead of a black viewport.
for r in range(290,0,-1):
    strength=(1-r/290)**2
    c=(5,10+int(10*strength),16+int(15*strength))
    bd.ellipse(((747-r)*SCALE,(279-r)*SCALE,(747+r)*SCALE,(279+r)*SCALE), fill=c)
for x in range(525,980,24):
    for y in range(70,495,24):
        bd.point((x*SCALE,y*SCALE),fill='#20333d')
line(bd,[(28,49),(972,49)],'#20313c')
line(bd,[(28,507),(972,507)],'#20313c')
text(bd,(32,20),'R / R',12,CYAN)
text(bd,(103,21),'PERSONAL SYSTEM  /  SAI RUTHVIK',10)
text(bd,(813,21),'PORTFOLIO     /  01',10)
text(bd,(40,107),'DEVELOPER  /  DESIGNER  /  BUILDER',11,CYAN)
line(bd,[(40,145),(76,145)],CYAN,2)
text(bd,(37,164),'SAI RUTHVIK',48,WHITE,False)
text(bd,(37,217),'REDDY',56,WHITE,False)
text(bd,(40,309),'Full Stack Developer',18,WHITE,False)
text(bd,(40,341),'UI/UX ENTHUSIAST  /  AI INTERFACES',11)
text(bd,(40,420),'Build with intent.',18,WHITE,False)
text(bd,(40,453),'HYDERABAD, INDIA  /  @erenseret56-del',10)
text(bd,(32,527),'01 / IDENTITY',10,CYAN)
text(bd,(210,527),'02 / TOOLKIT',10)
text(bd,(380,527),'03 / BUILDS',10)
text(bd,(788,527),'FOCUS > FRICTION',10,CYAN)
text(bd,(568,76),'NEURAL INTERFACE',10,CYAN)
text(bd,(872,76),'SYS.01',10)
text(bd,(575,465),'COGNITIVE ENGINE',10)
text(bd,(856,465),'ACTIVE',10,CYAN)
for r in [84,114,150,177,193]:
    arc(bd,r,0,360,'#17313c',.6)
for i in range(120):
    a=math.tau*i/120
    line(bd,[polar(182 if i%5 else 178,a),polar(187,a)], '#3e626e' if i%5 else '#85bbc6',.6)
for a in [0,math.pi/2,math.pi,3*math.pi/2]:
    line(bd,[polar(199,a),polar(209,a)],'#5a8895')
for side in [-1,1]:
    x=747+side*205
    line(bd,[(x,260),(x,298)],'#2b5360')


# Keep the supplied artwork still inside the moving iris, with a soft circular edge.
center_radius = 64
center_size = center_radius * 2 * SCALE
with Image.open(ROOT / 'assets' / 'jarvis-center.jpg') as source:
    center_art = ImageOps.fit(ImageOps.exif_transpose(source).convert('RGB'),
                              (center_size, center_size), Image.Resampling.LANCZOS)
center_mask = Image.new('L', (center_size, center_size), 0)
ImageDraw.Draw(center_mask).ellipse((2*SCALE, 2*SCALE, center_size-2*SCALE-1,
                                   center_size-2*SCALE-1), fill=255)
center_mask = center_mask.filter(ImageFilter.GaussianBlur(1*SCALE))
base.paste(center_art, ((747-center_radius)*SCALE, (279-center_radius)*SCALE), center_mask)


def render(index):
    t=index/COUNT
    im=base.copy()
    glow=Image.new('RGB',im.size)
    gd=ImageDraw.Draw(glow)
    d=ImageDraw.Draw(im)
    for r,start,span,turns,width in [(168,15,72,1,2),(159,190,112,-1,1),(141,45,46,-1,3),(130,260,84,1,1),(103,0,90,2,1),(94,180,42,-2,2)]:
        a=start+t*360*turns
        arc(d,r,a,a+span,CYAN,width)
        arc(gd,r,a,a+span,'#237b87',width*2)
        arc(d,r,a+180,a+180+span*.48,'#347885',width)
    # A finely segmented inner iris, with a circulating brightness envelope.
    for i in range(72):
        a=i*5
        v=(.5+.5*math.cos(math.radians(a)-t*math.tau))**6
        c=(int(30+90*v),int(68+150*v),int(80+150*v))
        arc(d,73,a,a+2,c,4)
    for i in range(48):
        a=math.tau*i/48
        r=120+4*math.sin(a*6+t*math.tau)
        line(d,[polar(r,a),polar(r+3,a)],'#49818f',.7)
    # Sparse data points sweep around the outer track.
    for i in range(6):
        a=t*math.tau+i*math.tau/6
        x,y=polar(193,a)
        d.ellipse(((x-1)*SCALE,(y-1)*SCALE,(x+1)*SCALE,(y+1)*SCALE),fill=WHITE)
    from PIL import ImageChops
    im=ImageChops.add(im,glow.filter(ImageFilter.GaussianBlur(5*SCALE)))
    return im.resize((W,H),Image.Resampling.LANCZOS)

if __name__=='__main__':
    assets=ROOT/'assets'
    frames=[]
    command=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(assets/'jarvis-core.mp4')]
    proc=subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        for i in range(COUNT):
            frame=render(i)
            frames.append(frame)
            proc.stdin.write(frame.tobytes())
            if i%60==0: print(f'Rendered {i}/{COUNT}',flush=True)
    finally:
        proc.stdin.close()
    if proc.wait()!=0: raise RuntimeError('FFmpeg encoding failed')
    frames[0].save(assets/'jarvis-poster.png')
    # Millisecond timestamps alternate 17/16/17 ms: exactly 4 seconds at 60 fps.
    durations=[round((i+1)*1000/FPS)-round(i*1000/FPS) for i in range(COUNT)]
    frames[0].save(assets/'jarvis-core.webp',save_all=True,append_images=frames[1:],duration=durations,loop=0,quality=88,method=4)
    print('Built 60 fps WebP, MP4 and static poster.',flush=True)

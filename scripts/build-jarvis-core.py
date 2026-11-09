"""Render the profile HUD: Pillow + FFmpeg, 240 frames / 4 seconds / 60 fps."""
from pathlib import Path
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
W, H, SCALE, FPS, COUNT = 1000, 560, 1, 60, 240
CYAN, WHITE, MUTED = '#75e6ed', '#e0edf0', '#6e929f'

def font(size, mono=False):
    names = (['C:/Windows/Fonts/consola.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'] if mono else
             ['C:/Windows/Fonts/segoeuil.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size * SCALE)
    raise RuntimeError('Install DejaVu Sans or Segoe UI fonts to render the hero.')

FONTS = {(s, m): font(s, m) for s, m in [(9,True),(10,True),(11,True),(12,True),(14,True),(18,False),(48,False),(56,False)]}

def bold_font(size):
    names = ['C:/Windows/Fonts/consolab.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf']
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size * SCALE)
    return FONTS[size, True]

BOLD_FONTS = {size: bold_font(size) for size in (10, 11)}

def line(d, points, fill, width=1):
    d.line([(int(x*SCALE),int(y*SCALE)) for x,y in points], fill=fill, width=max(1,round(width*SCALE)))

def text(d, xy, value, size=11, fill=MUTED, mono=True):
    d.text((xy[0]*SCALE,xy[1]*SCALE), value, font=FONTS[size,mono], fill=fill)

def bold_text(d, xy, value, size=11, fill=MUTED):
    d.text((xy[0]*SCALE,xy[1]*SCALE), value, font=BOLD_FONTS[size], fill=fill)

def arc(d, r, start, end, fill, width=1, center=(747,279)):
    x,y=center
    d.arc(tuple(round(v*SCALE) for v in (x-r,y-r,x+r,y+r)), start, end, fill=fill, width=max(1,round(width*SCALE)))

def polar(r,a):
    return (747+r*math.cos(a),279+r*math.sin(a))

def clamp(value):
    return max(0, min(1, value))

def mix(a, b, amount):
    return tuple(round(start + (end-start)*amount) for start, end in zip(a, b))

def point_on_polyline(points, progress):
    lengths = [math.dist(a, b) for a, b in zip(points, points[1:])]
    remaining = sum(lengths) * progress
    for start, end, length in zip(points, points[1:], lengths):
        if remaining <= length:
            ratio = remaining / length if length else 0
            return (start[0] + (end[0]-start[0])*ratio, start[1] + (end[1]-start[1])*ratio)
        remaining -= length
    return points[-1]

def draw_connection(draw, glow_draw, points, progress, opacity):
    if progress <= 0 or opacity <= 0:
        return
    visible = [points[0]]
    lengths = [math.dist(a, b) for a, b in zip(points, points[1:])]
    distance = sum(lengths) * progress
    for start, end, length in zip(points, points[1:], lengths):
        if distance >= length:
            visible.append(end)
            distance -= length
        else:
            visible.append((start[0] + (end[0]-start[0])*(distance/length), start[1] + (end[1]-start[1])*(distance/length)))
            break
    colour = mix((0, 0, 0), (104, 237, 244), opacity)
    glow_colour = mix((0, 0, 0), (23, 123, 143), opacity)
    line(draw, visible, colour, 1.25)
    line(glow_draw, visible, glow_colour, 4)
    if progress > .96:
        x, y = points[-1]
        radius = 2.3
        draw.ellipse(((x-radius)*SCALE, (y-radius)*SCALE, (x+radius)*SCALE, (y+radius)*SCALE), fill=colour)
        glow_draw.ellipse(((x-radius*2)*SCALE, (y-radius*2)*SCALE, (x+radius*2)*SCALE, (y+radius*2)*SCALE), fill=glow_colour)

CONNECTIONS = [
    ((685,194), (615,116), (535,116), (275,82),  'CONNECTION 01  /  FULL STACK DEVELOPMENT', 'React.js / Next.js / Node.js / TypeScript', .11),
    ((670,242), (610,202), (535,202), (275,136), 'CONNECTION 02  /  AI AGENT ENGINEERING',    'OpenAI / Gemini / LLMs / AI Agents',        .25),
    ((671,287), (610,315), (535,315), (275,281), 'CONNECTION 03  /  VOICE AI & AUTOMATION',  'Retell AI / ElevenLabs / Twilio / n8n',     .39),
    ((685,326), (618,404), (535,404), (275,370), 'CONNECTION 04  /  CLOUD & INFRASTRUCTURE', 'AWS / Hostinger VPS / Vercel / Netlify',   .53),
]

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
    # Four staged technical callouts originate at the core, then settle into a calm pulse loop.
    # The last phase fades away before frame zero so the WebP loop has no abrupt reset.
    sequence_fade = 1 if t < .88 else clamp((1-t)/.12)
    activation = clamp(t/.10) * sequence_fade
    core_radius = 71 + math.sin(t*math.tau*2)*3
    d.ellipse(((747-core_radius)*SCALE, (279-core_radius)*SCALE,
               (747+core_radius)*SCALE, (279+core_radius)*SCALE),
              outline=mix((0,0,0), (64,206,226), activation), width=max(1, round(SCALE)))
    gd.ellipse(((747-core_radius)*SCALE, (279-core_radius)*SCALE,
                (747+core_radius)*SCALE, (279+core_radius)*SCALE),
               outline=mix((0,0,0), (18,105,128), activation), width=5*SCALE)
    for points_start, elbow, endpoint, label_at, heading, detail, delay in CONNECTIONS:
        line_progress = clamp((t-delay)/.13)
        line_opacity = sequence_fade * clamp((t-delay)/.05)
        draw_connection(d, gd, (points_start, elbow, endpoint), line_progress, line_opacity)
        label_opacity = sequence_fade * clamp((t-(delay+.11))/.06)
        if label_opacity:
            heading_colour = mix((0,0,0), (183,250,253), label_opacity)
            detail_colour = mix((0,0,0), (176,220,231), label_opacity)
            bold_text(d, label_at, heading, 11, heading_colour)
            text(d, (label_at[0], label_at[1]+15), detail, 10, detail_colour)
        # A small emissive pulse repeatedly travels from the core to the endpoint after reveal.
        if line_progress > .98:
            pulse = ((t-(delay+.24))*2.4) % 1
            x, y = point_on_polyline((points_start, elbow, endpoint), pulse)
            radius = 1.7
            d.ellipse(((x-radius)*SCALE, (y-radius)*SCALE, (x+radius)*SCALE, (y+radius)*SCALE), fill=(213,255,255))
            gd.ellipse(((x-radius*2)*SCALE, (y-radius*2)*SCALE, (x+radius*2)*SCALE, (y+radius*2)*SCALE), fill=(37,142,158))
    from PIL import ImageChops
    im=ImageChops.add(im,glow.filter(ImageFilter.GaussianBlur(5*SCALE)))
    return im.resize((W,H),Image.Resampling.LANCZOS)

if __name__=='__main__':
    assets=ROOT/'assets'
    source=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an']
    mp4_proc=subprocess.Popen(source + ['-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(assets/'jarvis-core.mp4')], stdin=subprocess.PIPE)
    webp_proc=subprocess.Popen(source + ['-c:v','libwebp_anim','-q:v','82','-loop','0',str(assets/'jarvis-core.webp')], stdin=subprocess.PIPE)
    first_frame=None
    try:
        for i in range(COUNT):
            frame=render(i)
            if i == 0:
                first_frame=frame
            raw_frame=frame.tobytes()
            mp4_proc.stdin.write(raw_frame)
            webp_proc.stdin.write(raw_frame)
            if i%60==0: print(f'Rendered {i}/{COUNT}',flush=True)
    finally:
        mp4_proc.stdin.close()
        webp_proc.stdin.close()
    if mp4_proc.wait()!=0 or webp_proc.wait()!=0: raise RuntimeError('FFmpeg encoding failed')
    render(int(COUNT*.72)).save(assets/'jarvis-poster.png')
    print('Built 60 fps WebP, MP4 and static poster.',flush=True)

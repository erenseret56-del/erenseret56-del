"""Build a seamless, animated identity panel for the GitHub profile README."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

ROOT = Path(__file__).resolve().parents[1]
W, H, SCALE, FPS, COUNT = 1000, 500, 2, 60, 240


def load_font(size, mono=False):
    names = (['C:/Windows/Fonts/consolab.ttf', 'C:/Windows/Fonts/consola.ttf'] if mono
             else ['C:/Windows/Fonts/segoeuib.ttf', 'C:/Windows/Fonts/segoeuil.ttf'])
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size * SCALE)
    raise RuntimeError('Segoe UI and Consolas fonts are required.')


FONTS = {(size, mono): load_font(size, mono) for size, mono in [
    (10, True), (11, True), (18, False), (42, False), (124, False)
]}


def px(value): return round(value * SCALE)


def label(draw, at, value, size=11, colour='#8daab5', mono=True):
    draw.text((px(at[0]), px(at[1])), value, font=FONTS[size, mono], fill=colour)


def stroke(draw, points, colour, width=1):
    draw.line([(px(x), px(y)) for x, y in points], fill=colour, width=max(1, px(width)))


def background():
    image = Image.new('RGB', (W*SCALE, H*SCALE), '#050a0f')
    draw = ImageDraw.Draw(image)
    for radius in range(520, 0, -1):
        intensity = (1-radius/520)**2
        draw.ellipse((px(735-radius), px(250-radius), px(735+radius), px(250+radius)),
                     fill=(5, 10+int(9*intensity), 15+int(14*intensity)))
    draw.rounded_rectangle((px(10), px(10), px(990), px(490)), radius=px(15), outline='#203845', width=px(1))
    stroke(draw, [(38,69), (962,69)], '#233b46')
    stroke(draw, [(38,436), (962,436)], '#233b46')
    label(draw, (39,31), 'IDENTITY / PERSONAL INTERFACE', 11, '#70e6ef')
    label(draw, (799,31), 'LIVE PROFILE  /  01', 10)
    label(draw, (48,99), 'SAI RUTHVIK', 42, '#edf7f8', False)
    label(draw, (48,150), 'REDDY', 42, '#edf7f8', False)
    label(draw, (50,213), 'FULL STACK DEVELOPER', 18, '#d8f3f5', False)
    label(draw, (50,245), 'UI/UX  |  PRODUCT  |  AI INTERACTIONS', 11, '#70e6ef')
    label(draw, (50,321), 'HYDERABAD, INDIA', 11)
    label(draw, (50,346), 'MLR INSTITUTE OF TECHNOLOGY', 11)
    label(draw, (50,371), '@erenseret56-del', 11)
    label(draw, (375,458), 'BUILD WITH INTENT  /  KEEP IMPROVING', 10, '#70e6ef')
    return image


BASE = background()


def render(index):
    time = index / COUNT
    image = BASE.copy()
    draw = ImageDraw.Draw(image)
    glow = Image.new('RGB', image.size)
    glow_draw = ImageDraw.Draw(glow)
    cx, cy = 748, 252
    for radius, start, length, turns, width in [
        (168,20,82,1,2), (149,205,115,-1,1), (125,70,60,2,2),
        (104,250,100,-2,1), (76,10,70,3,2),
    ]:
        angle = start + time*360*turns
        box = (px(cx-radius), px(cy-radius), px(cx+radius), px(cy+radius))
        draw.arc(box, angle, angle+length, fill='#6ee9ef', width=px(width))
        glow_draw.arc(box, angle, angle+length, fill='#1e8b99', width=px(width+2))
        draw.arc(box, angle+180, angle+180+length*.38, fill='#3c8290', width=px(1))
    for radius in (92,114,140,168):
        draw.ellipse((px(cx-radius),px(cy-radius),px(cx+radius),px(cy+radius)), outline='#173945', width=px(.6))
    for tick in range(56):
        angle = tick*math.tau/56
        radius = 174
        start = (cx+math.cos(angle)*radius, cy+math.sin(angle)*radius)
        end = (cx+math.cos(angle)*(radius+(8 if tick%7 == 0 else 4)), cy+math.sin(angle)*(radius+(8 if tick%7 == 0 else 4)))
        stroke(draw, [start,end], '#74aeb8' if tick%7 == 0 else '#345660', .7)
    for point in range(6):
        angle = time*math.tau + point*math.tau/6
        x, y = cx+math.cos(angle)*178, cy+math.sin(angle)*178
        draw.ellipse((px(x-1.4),px(y-1.4),px(x+1.4),px(y+1.4)), fill='#e6fbfc')
    pulse = 58*(1+math.sin(time*math.tau*2)*.045)
    draw.ellipse((px(cx-pulse),px(cy-pulse),px(cx+pulse),px(cy+pulse)), fill='#071720', outline='#69dfe8', width=px(2))
    glow_draw.ellipse((px(cx-pulse),px(cy-pulse),px(cx+pulse),px(cy+pulse)), outline='#248997', width=px(5))
    label(draw, (cx-42,cy-74), 'R', 124, '#dffbfc', False)
    scan_y = cy-52 + ((time*104) % 104)
    stroke(draw, [(cx-51,scan_y),(cx+51,scan_y)], '#a8ffff', 1)
    stroke(glow_draw, [(cx-52,scan_y),(cx+52,scan_y)], '#278e9b', 4)
    label(draw, (cx-35,cy+74), 'CORE ACTIVE', 10, '#71e7ef')
    image = ImageChops.add(image, glow.filter(ImageFilter.GaussianBlur(px(4))))
    return image.resize((W,H), Image.Resampling.LANCZOS)


if __name__ == '__main__':
    print('Rendering 240 identity frames...', flush=True)
    first_frame = render(0)
    def remaining_frames():
        for index in range(1, COUNT):
            if index % 60 == 0:
                print(f'Rendered {index}/{COUNT}', flush=True)
            yield render(index)
    durations = [round((index+1)*1000/FPS)-round(index*1000/FPS) for index in range(COUNT)]
    first_frame.save(ROOT/'assets'/'identity-card.webp', save_all=True, append_images=remaining_frames(), duration=durations, loop=0, quality=88, method=4)
    first_frame.save(ROOT/'assets'/'identity-card.png')
    print('Built identity-card.webp: 240 frames at 60 fps.', flush=True)

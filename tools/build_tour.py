"""Build a clearly labeled screenshot tour; no phone or sensor access required."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SCREENS = [
    ('home.png', '01  HOME', 'Choose a familiar starting point'),
    ('scenarios.png', '02  SCENARIOS', '10 moments to explore'),
    ('expression-coach.png', '03  EXPRESSION COACH', 'Watch, together, your turn'),
    ('games.png', '04  GAMES', '12 groups and 36 activities'),
    ('settings.png', '05  YOUR PREFERENCES', 'A pace that feels comfortable'),
]

def font(size):
    for name in ('C:/Windows/Fonts/segoeuib.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()

frames = []
for filename, title, subtitle in SCREENS:
    screen = Image.open(ROOT / 'docs' / 'screenshots' / filename).convert('RGB')
    screen.thumbnail((360, 802), Image.Resampling.LANCZOS)
    frame = Image.new('RGB', (420, 950), '#F8F7F3')
    draw = ImageDraw.Draw(frame)
    draw.text((30, 17), 'Expressify AI', font=font(25), fill='#12665F')
    draw.text((30, 54), title, font=font(13), fill='#18313C')
    frame.paste(screen, ((420 - screen.width) // 2, 82))
    draw.text((30, 894), subtitle, font=font(16), fill='#18313C')
    draw.text((30, 924), 'SCREENSHOT TOUR  /  ANDROID PROTOTYPE', font=font(10), fill='#4A625E')
    frames.append(frame.quantize(colors=192, method=Image.Quantize.MEDIANCUT))

out = ROOT / 'docs' / 'media' / 'expressify-tour.gif'
out.parent.mkdir(parents=True, exist_ok=True)
frames[0].save(out, save_all=True, append_images=frames[1:], duration=3000, loop=0, optimize=True, disposal=2)
print(out)

"""Build images/og-card.jpg (1200x627) from the site banner with name and title text."""
# Usage: python tools/make_og_card.py images/GitHubIOBanner.png images/og-card.jpg  (needs Pillow and Ubuntu Sans)
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src, dest = sys.argv[1], sys.argv[2]
W, H = 1200, 627
im = Image.open(src).convert("RGB")
w, h = im.size
cw = round(h * W / H)                      # crop width at 1.91:1, centered
left = (w - cw) // 2
im = im.crop((left, 0, left + cw, h)).resize((W, H), Image.LANCZOS)
# darken the centre band so the text reads over the network graphic
shade = Image.new("L", (W, H), 0)
ImageDraw.Draw(shade).rectangle((0, 170, W, 470), fill=150)
shade = shade.filter(ImageFilter.GaussianBlur(70))
im = Image.composite(Image.new("RGB", (W, H), (2, 10, 40)), im, shade)
d = ImageDraw.Draw(im)
font = "/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf"
def face(size, weight):
    f = ImageFont.truetype(font, size)
    f.set_variation_by_axes([100, weight])
    return f
lines = [("Todd Espy", face(96, 700), 0),
         ("Principal Software Architect", face(46, 500), 34),
         ("Building software with AI for organizations", face(34, 400), 30),
         ("that can't afford it to fail", face(34, 400), 8)]
heights = [d.textbbox((0, 0), t, font=f)[3] for t, f, _ in lines]
y = (H - (sum(heights) + sum(g for *_, g in lines))) // 2 - 10
for (text, f, gap), lh in zip(lines, heights):
    y += gap
    tw = d.textlength(text, font=f)
    d.text(((W - tw) / 2, y), text, font=f, fill="white", stroke_width=2 if f.size > 40 else 1, stroke_fill=(2, 10, 40))
    y += lh
im.save(dest, "JPEG", quality=85, optimize=True, progressive=True)
print(Image.open(dest).size)

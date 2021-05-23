from pathlib import Path

from PIL import Image, ImageFont, ImageDraw
import textwrap


def text_generate(top_text: str, bottom_text: str, image_path: Path) -> Image.Image:
    im = Image.open(str(image_path))
    draw = ImageDraw.Draw(im)
    image_width, image_height = im.size
    font = ImageFont.truetype(font=r'C:\Users\ashir\Downloads\impact\impact.ttf', size=(int(image_height / 12)))
    top_text, bottom_text = top_text.upper(), bottom_text.upper()
    char_width, char_height = font.getsize('A')
    char_per_line = image_width // char_width
    top_lines = textwrap.wrap(top_text, width=char_per_line)
    bottom_lines = textwrap.wrap(bottom_text, width=char_per_line)
    y = 10
    for line in top_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font)
        y += line_height

    y = image_height - char_height * len(bottom_lines) - 15
    for line in bottom_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font)
        y += line_height

    return im

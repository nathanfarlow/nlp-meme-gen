import numpy as np
import config
import util
import tempfile
import os

from PIL import Image, ImageDraw, ImageFont


def text_width(text, draw, font):
    return draw.textbbox((0, 0), text, font=font)[2]


def split_line(line, draw, font, box_width, padding):
    result = []
    current = ""
    for word in line.split():
        if text_width(current + " " + word, draw, font) > box_width - padding:
            result.append(current.strip())
            current = ""
        current += word + " "

    if current:
        result.append(current.strip())

    return result


def text_in_box(text, draw, font, box_width, padding, color):
    lines = []
    for line in text.split("\n"):
        lines.extend(split_line(line, draw, font, box_width, padding))

    height = draw.multiline_textbbox((0, 0), "\n".join(lines), font=font)[3] + padding

    height += height % 2

    caption_image = Image.new("RGBA", (box_width, height), color=color)
    draw = ImageDraw.Draw(caption_image)

    draw.multiline_text((padding, 0), "\n".join(lines), font=font, fill="black")

    return caption_image


class Renderer:
    def __init__(self, arial_path, impact_path):
        self.arial_path = arial_path
        self.impact_path = impact_path

    def make_caption(self, image_width, image_height, text):
        text_height = image_height // 10
        font = ImageFont.truetype(self.arial_path, text_height)
        caption_image = Image.new("RGB", (0, 0), color="white")
        draw = ImageDraw.Draw(caption_image)
        padding = draw.textbbox((0, 0), "A", font=font)[1]
        return text_in_box(text, draw, font, image_width, padding, color="white")

    def render_video(self, filepath, caption):
        command = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{filepath}"'
        output = os.popen(command).read()
        width, height = map(int, output.split("x"))
        caption_image = self.make_caption(width, height, caption)
        output = tempfile.NamedTemporaryFile(suffix=".mp4")
        with tempfile.NamedTemporaryFile(suffix=".png") as caption_file:
            caption_image.save(caption_file.name)
            image_height = caption_image.height
            command = f'ffmpeg -i "{caption_file.name}" -i "{filepath}" -filter_complex vstack -vsync 2 -y "{output.name}"'
            os.system(command)
        return output

    def render_image(self, meme: config.Meme, textbox_assignments: dict[str, str]):
        image = Image.open(meme.filepath)
        image = image.convert("RGBA")
        draw = ImageDraw.Draw(image)
        image_width, image_height = image.size

        def make_with_caption():
            caption = textbox_assignments["caption"]
            if not caption:
                return image
            caption_image = self.make_caption(image_width, image_height, caption)
            combined_image = Image.new(
                "RGBA",
                (image_width, image_height + caption_image.height),
                color="white",
            )
            combined_image.paste(caption_image, (0, 0))
            combined_image.paste(image, (0, caption_image.height))
            return combined_image

        def draw_textbox(box: config.TextBox):
            text = textbox_assignments[box.tag]
            if not text:
                return

            print(f'Drawing "{text}" in box "{box.tag}"')

            top_left, top_right, bottom_right, bottom_left = box.bounds
            box_width = top_right[0] - top_left[0]
            box_height = bottom_left[1] - top_left[1]
            text_height = box_height // 4
            font_path = (
                self.arial_path if box.font == config.Font.ARIAL else self.impact_path
            )
            font = ImageFont.truetype(font_path, text_height)
            caption_image = Image.new("RGBA", (0, 0), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(caption_image)
            padding = draw.textbbox((0, 0), "A", font=font)[1]
            caption_image = text_in_box(
                text, draw, font, box_width, padding, color=(0, 0, 0, 0)
            )

            image.paste(caption_image, top_left, caption_image)

        for box in meme.textboxes:
            draw_textbox(box)
        image = make_with_caption()
        output = tempfile.NamedTemporaryFile(suffix=".png")
        image.save(output.name)
        return output

    def render(self, meme: config.Meme, textbox_assignments: dict[str, str]):
        if util.is_video(meme.filepath):
            return self.render_video(meme.filepath, textbox_assignments["caption"])
        return self.render_image(meme, textbox_assignments)

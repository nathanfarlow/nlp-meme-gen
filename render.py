import config
import util
import tempfile
import os

from PIL import Image, ImageDraw, ImageFont


class Renderer:
    def __init__(self, arial_path, impact_path):
        self.arial_path = arial_path
        self.impact_path = impact_path

    def make_caption(self, image_width, image_height, text):
        text_height = image_height // 8
        font = ImageFont.truetype(self.arial_path, text_height)

        caption_image = Image.new("RGB", (0, 0), color="white")
        draw = ImageDraw.Draw(caption_image)

        def text_width(text):
            return draw.textbbox((0, 0), text, font=font)[2]

        padding = draw.textbbox((0, 0), "A", font=font)[1]

        def split_line(line):
            result = []
            current = ""
            for word in line.split():
                if text_width(current + " " + word) > image_width - padding:
                    result.append(current.strip())
                    current = ""
                current += word + " "

            if current:
                result.append(current.strip())

            return result

        lines = []
        for line in text.split("\n"):
            lines.extend(split_line(line))

        height = (
            draw.multiline_textbbox((0, 0), "\n".join(lines), font=font)[3] + padding
        )

        height += height % 2

        caption_image = Image.new("RGB", (image_width, height), color="white")
        draw = ImageDraw.Draw(caption_image)

        draw.multiline_text((padding, 0), "\n".join(lines), font=font, fill="black")

        return caption_image

    def render_video(self, filepath, caption):
        if not caption:
            return filepath
        command = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{filepath}"'
        output = os.popen(command).read()
        width, height = map(int, output.split("x"))
        caption_image = self.make_caption(width, height, caption)
        output = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        # get temp name, but don't create the file yet
        with tempfile.NamedTemporaryFile(suffix=".png") as caption_file:
            caption_image.save(caption_file.name)
            image_height = caption_image.height
            command = f'ffmpeg -i "{caption_file.name}" -i "{filepath}" -filter_complex vstack -vsync 2 -y "{output.name}"'

            os.system(command)
        return output.name

    def render(self, meme: config.Meme, textbox_assignments: dict[str, str]):
        if util.is_video(meme.filepath):
            return self.render_video(meme.filepath, textbox_assignments["caption"])
        raise NotImplementedError()

from search import Search
from segment import Segmenter
import config
import render
import os

config = config.load("memes/config.json")

s = Segmenter(
    model_path="/home/nathan/Downloads/codellama-13b-instruct.Q5_K_S.gguf",
    n_gpu_layers=43,
)
search = Search(config)
renderer = render.Renderer(
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
)


def generate_meme(description):
    template_query = s.get_template_query(description)
    if template_query:
        meme = search.search(template_query)
        if meme:
            text = s.get_text(meme, description)
            if text:
                return renderer.render(meme, text)
    return None

from search import Search
from segment import Segmenter
import config
import render
import os

config = config.load("test/config.json")

s = Segmenter(
    model_path="/home/nathan/Downloads/codellama-13b-instruct.Q5_K_S.gguf",
    n_gpu_layers=43,
)
search = Search(config)
renderer = render.Renderer(
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
)

query = "is this a pigeon meme with the caption 'is this a pigeon???'"
template_query = s.get_template_query(query)
print(f'Template query: "{template_query}"')
if template_query:
    meme = search.search(template_query)
    print(f'Meme: "{meme.filepath}"')
    if meme:
        text = s.get_text(meme, query)
        print(f'Text: "{text}"')
        if text:
            file = renderer.render(meme, text)

            os.system(f'google-chrome "{file.name}"')
            import time

            time.sleep(2)

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

# query = "the expanding brain meme with the tiniest brain as 'bruh bruh guh guh' and the hugest brain as 'gonk gonk' and the top text is 'foo'"
query = "nerd emoji gif with caption 'um actually'"
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

            os.system(f'google-chrome "{file}"')

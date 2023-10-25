from search import Search
from segment import Segmenter
import config

config = config.load("test/config.json")

s = Segmenter(
    model_path="/home/nathan/Downloads/codellama-13b-instruct.Q5_K_S.gguf",
    n_gpu_layers=43,
)
search = Search(config)

query = "expanding brain meme with caption 'bruh'"
template_query = s.get_template_query(query)
print(f"{template_query=}")
if template_query:
    meme = search.search(template_query)
    print(f"{meme=}")
    if meme:
        text = s.get_text(meme, query)
        print(f"Using meme {meme.filepath}")
        print(f"with textboxes {text=}")

from search import Search
from segment import Segmenter
import config

config = config.load("test/config.json")

s = Segmenter(
    model_path="/home/nathan/Downloads/codellama-13b-instruct.Q5_K_S.gguf",
    n_gpu_layers=40,
)
search = Search(config)

query = "pigeon meme"
template_query = s.get_template_query(query)
print(template_query)
if template_query:
    print(search.search(template_query).filepath)

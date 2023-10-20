import logging
from llama_cpp import Llama
import json


class Segmenter:
    def __init__(self, model_path, n_gpu_layers) -> None:
        logging.info(
            f"initializing LLM with model_path={model_path} and n_gpu_layers={n_gpu_layers}"
        )
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=n_gpu_layers,
            n_ctx=1000,
        )

    def get_template_query(self, sentence):
        prompt = "".join(
            [
                "[INST] You are a meme search engine. A user ",
                "submits a meme description and you output a search query that can be ",
                "used to google for the specified meme template. Your output will be in ",
                "json format. Ignore captions and other text. Here are some examples. \n\n",
                'description: """is this a x meme which says \'foo bar\' as a caption"""\n',
                'response: {"query": "is this a x"}\n\n',
                'description: """that one spiderman meme where they are all pointing at each other which says "hey we\'re all the same that\'s crazy""""\n'
                'response: {"query": "pointing spiderman}\n\n'
                'description: """the rock gif where he is raising his eyebrow with caption xyz and text \'other text\'"""\n'
                'response: {"query": "rock raising eyebrow gif"}\n'
                "[/INST]\n",
                'description: """%DESCRIPTION%"""\n',
                'response: {"query": "',
            ]
        ).replace("%DESCRIPTION%", sentence)

        output = self.llm(
            prompt,
            max_tokens=5000,
            stop="}",
            temperature=0.2,
        )

        output = '{"query": "' + output["choices"][0]["text"] + "}"
        try:
            j = json.loads(output)
            return j["query"]
        except:
            return None

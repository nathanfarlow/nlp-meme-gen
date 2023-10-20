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

    def get_text(self, meme, sentence):
        prompt = "".join(
            [
                "[INST] You are a meme generator. You extract the caption and other text from ",
                "a user's description. Assign the output results ",
                "in the same order as the corresonding tags appear. If it's not clear, then put them ",
                "in the order they appear in the description. If it's still not clear, and there is only ",
                "one text, then make it the caption, leaving empty strings where necessary. Your output will ",
                "be in json format. There should be an equal number of responses to the number of tags. ",
                "If the specific text is not specified, it should be an empty string. Here are some examples. ",
                "You should only use these as a reference, and you should always use only the applicable tags.\n\n",
                'tags: ["butterfly, pigeon", "word, x", "caption"]\n',
                'description: """is this a x meme which says \'foo bar\' as a caption and the butterfly says \'guh guh butterfly\'"""\n',
                'response: ["guh guh butterfly", "", "foo bar"]\n\n',
                'tags: ["first, one", "second, two", "third, three", "caption"]\n',
                'description: """the pointing spiderman meme with caption "this is my caption lol" and with the spidermen being labeled steve, george, and bob"""\n',
                'response: ["steve", "george", "bob", "this is my caption lol"]\n\n',
                'tags: ["bad, boo", "good, yay", "caption"]\n',
                'description: """drake meme where bad is "dog" and good is cat"""]\n',
                'response: ["dog", "cat", ""]\n',
                'tags: ["small brain, dumb", "medium brain", "intermediate brain", "big brain", "caption"]\n',
                'description: """the expanding brain meme with caption \'when you forget your phone\'"""]\n',
                'response: ["", "", "", "", "when you forget your phone"]\n',
                'tags: ["good thing", "caption"]\n',
                'description: """the good meme with caption \'foo bar\'"""]\n',
                'response: ["", "foo bar"]\n',
                "[/INST]\n",
                'tags: ["%TAGS%"]\n',
                'description: """%DESCRIPTION%"""\n',
                'response: ["',
            ]
        )
        tags = [box.tag for box in meme.textboxes]
        prompt = prompt.replace("%TAGS%", '", "'.join(tags))
        prompt = prompt.replace("%DESCRIPTION%", sentence)

        output = self.llm(
            prompt,
            max_tokens=5000,
            stop="]",
            temperature=0.2,
        )

        output = '{"text": ["' + output["choices"][0]["text"] + "]}"
        try:
            j = json.loads(output)
            return j["text"]
        except:
            return None


segmenter = Segmenter(
    model_path="/home/nathan/Downloads/codellama-13b-instruct.Q5_K_S.gguf",
    n_gpu_layers=40,
)

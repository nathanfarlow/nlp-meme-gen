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
                "json format. Do not include string literals like captions. Here are some examples. \n\n",
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
        prompt = (
            "[INST] You are a meme generator. You extract the caption and other text from "
            "a user's description. Choose the best text for each text box given the "
            "tags and the user's description. Feel free to leave some tags blank. "
            "Your output will be in json format. There should be an equal number of responses to the number of tags. "
            "In your json response, copy the tag string exactly, so that it can be used for identification. "
            "Keep escape sequences in the text. "
            "Here are some examples. You should only use these as a reference, and you should always use only the applicable tags.\n\n"
            'description: """is this a x meme which says \'foo bar\' as a caption and the butterfly says \'guh guh butterfly\'"""\n'
            'tags: ["butterfly, pigeon", "word, x", "caption"]\n'
            'response: {"butterfly, pigeon": "guh guh butterfly", "word, x": "", "caption": "foo bar"}\n\n'
            'description: """the pointing spiderman meme with caption "this is my caption lol" and with the spidermen being labeled steve, george, and bob"""\n'
            'tags: ["first, one", "second, two", "third, three", "caption"]\n'
            'response: {"first, one": "steve", "second, two": "george", "third, three": "bob", "caption": "this is my caption lol"}\n\n'
            'description: """drake meme with bad "dog" and good is cat"""]\n'
            'tags: ["bad, boo", "good, yay", "caption"]\n'
            'response: {"bad, boo": "dog", "good, yay": "cat", "caption": ""}\n\n'
            'description: """the expanding brain meme with caption \'when you forget your phone\'"""]\n'
            'tags: ["small brain, dumb", "medium brain", "intermediate brain", "big brain", "caption"]\n'
            'response: {"small brain, dumb": "", "medium brain": "", "intermediate brain": "", "big brain": "", "caption": "when you forget your phone"}\n\n'
            'description: """the good meme with good thing \'Alice: haha you\'re funny\\nBob: thanks lol"""]\n'
            'tags: ["caption", good thing"]\n'
            'response: {"caption": "", good thing": "Alice: haha you\'re funny\\nBob: thanks lol"}\n\n'
            "[/INST]\n"
            'description: """%DESCRIPTION%"""\n'
            'tags: ["%TAGS%"]\n'
            'response: {"'
        )

        tags = [box.tag for box in meme.textboxes] + ["caption"]
        prompt = prompt.replace("%TAGS%", '", "'.join(tags))
        prompt = prompt.replace("%DESCRIPTION%", sentence)

        print(prompt)

        output = self.llm(
            prompt,
            max_tokens=5000,
            stop="}",
            temperature=0.3,
        )

        output = '{"' + output["choices"][0]["text"] + "}"
        try:

            def normalize(s):
                return "".join(s.split()).lower()

            j = json.loads(output)
            normalized_to_original = {normalize(tag): tag for tag in tags}
            j = {normalized_to_original[normalize(key)]: j[key] for key in j}

            for tag in tags:
                assert tag in j

            return j
        except:
            return None

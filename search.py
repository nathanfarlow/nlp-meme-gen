import config
import logging
from txtai.embeddings import Embeddings


class Search:
    def __init__(self, config: config.Config) -> None:
        logging.info("initializing search")
        self.config = config

        def templates():
            for meme in config.memes:
                yield (meme.filepath, meme.description)

        self.memes_by_filepath = {meme.filepath: meme for meme in config.memes}

        self.embeddings = Embeddings(
            method="sentence-transformers",
            path="sentence-transformers/clip-ViT-B-32",
        )
        self.embeddings.index(templates())

    def search(self, query: str):
        filepath = self.embeddings.search(query, 1)[0][0]
        return self.memes_by_filepath[filepath]

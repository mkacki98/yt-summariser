import re

from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")


class VideoProcessor:
    def __init__(self, url: str, language: str = "en"):
        self.language = language
        self.video_id = url[32:]

    def token_counter(self, transcript):
        return len(tokenizer(transcript))

    def process_video(self):
        """Scrape information about the video and transcripts."""
        loader = YoutubeLoader(
            self.video_id, add_video_info=True, language=self.language
        )

        title, n_keypoints = self.get_video_info(loader)
        transcripts = self.get_transcripts(loader)

        return title, n_keypoints, transcripts

    def get_transcripts(self, loader: YoutubeLoader) -> list[str]:
        """Get a raw transcript from the loader and split it into shorter bits to make it fit into the model."""

        splitter = RecursiveCharacterTextSplitter(
            length_function=self.token_counter, chunk_size=4000, chunk_overlap=0
        )
        splitted_transcripts = splitter.split_documents(loader.load())

        transcripts = [doc.page_content for doc in splitted_transcripts]
        return transcripts

    def get_video_info(self, loader: YoutubeLoader) -> tuple:
        video_info = loader._get_video_info()
        n_keypoints = self.get_n_keypoints(video_info["title"])

        return video_info["title"], n_keypoints

    def get_n_keypoints(self, title: str) -> int:
        """Get number of keypoints to be extracted from the transcript.
        E.g. for input `5 Productivity Tips` -> 5."""

        match = re.search(r"\d+", title)
        if match:
            return int(match.group())
        return 0

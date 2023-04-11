from langchain.llms import OpenAI
from langchain import PromptTemplate


class Summariser:
    def __init__(self, model: OpenAI):
        template = """ Answer the question based on the context below. If the question can't be answered using the infromation provided, output an empty string. 
        Make sure you extract exactly as many points as the query is asking for.

        Context: {context}
        Query: Summarise {n_keypoints} key points of the YouTube video of which transcripts are your context. Return each point in a single, numbered sentence from 1 to {n_keypoints}. Make sure the whole output is shorter than 250 characters.
        """
        self.prompt_template = PromptTemplate(
            input_variables=["context", "n_keypoints"], template=template
        )

        self.model = model

    def get_transcript_summary(self, context: list[str], n_keypoints: int) -> str:
        output = self.model(
            self.prompt_template.format(context=context, n_keypoints=n_keypoints)
        )
        if len(output) < 30:
            raise ValueError("Summary was suspiciously short!")

        return output

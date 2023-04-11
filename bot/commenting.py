import os

from langchain.llms import OpenAI
from langchain import PromptTemplate

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from urllib.parse import urlparse, parse_qs
from google.oauth2.credentials import Credentials


class Commentator:
    def __init__(self, model: OpenAI):
        self.client = self.get_authenticated_client()

        template = """ Answer the question based on the context below. If the question can't be answered using the infromation provided, output an empty string. 

        Context: {title}
        Query: Generate a single short sentence where you thank an author of the video for creating it and say why it may be useful to others.
        """

        self.prompt_template = PromptTemplate(
            input_variables=["title"], template=template
        )

        self.model = model

    def get_authenticated_client(self):
        """Function that leads either to Google authentication via web (and saving `Auth` token) or using the token to do so without the web."""

        CLIENT_SECRETS_FILE = "bot/secrets/client_secret_desktop.json"
        SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
        API_SERVICE_NAME = "youtube"
        API_VERSION = "v3"

        if not os.path.exists("bot/secrets/token.json"):
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

            with open("bot/secrets/token.json", "w") as token_file:
                token_file.write(creds.to_json())

            return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

        creds = Credentials.from_authorized_user_file(
            "bot/secrets/token.json", SCOPES
        )
        return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    def post_comment(
        self, url: str, summary: str, title: str, n_keypoints: int
    ) -> None:
        """Send a post request to Google API to create a given comment under a given video URL."""
        channel_id, video_id = self.get_video_info(url)

        title_related_comment = self.get_title_related_comment(title)
        comment_text = f"{title_related_comment} Here are the {n_keypoints} key points of the video.\n\n{summary}"

        self.client.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "channelId": channel_id,
                    "topLevelComment": {"snippet": {"textOriginal": comment_text}},
                }
            },
        ).execute()

        return comment_text

    def get_title_related_comment(self, title: str) -> str:
        """Generate a comment that will appreciate author's work. I'm a very kind bot indeed!"""

        output = self.model(self.prompt_template.format(title=title))
        return output

    def get_video_info(self, url: str) -> tuple:
        video_id = self.get_video_id(url)
        channel_id = self.get_channel_id(video_id)

        return channel_id, video_id

    def get_video_id(self, url: str) -> str:
        """Extracts the video ID from a YouTube video URL."""
        parsed_url = urlparse(url)

        if parsed_url.netloc == "youtu.be":
            # for short URLs like https://youtu.be/VIDEOID
            video_id = parsed_url.path[1:]
        else:
            # for long URLs like https://www.youtube.com/watch?v=VIDEOID
            query_params = parse_qs(parsed_url.query)
            video_id = query_params["v"][0]

        return video_id

    def get_channel_id(self, video_id: str) -> str:
        """Use Google API to get channel ID that produced a video with a given ID."""

        response = self.client.videos().list(part="snippet", id=video_id).execute()
        channel_id = response["items"][0]["snippet"]["channelId"]

        return channel_id

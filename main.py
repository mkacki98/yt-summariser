import uuid
import os
import random
from datetime import datetime
from typing import Optional, List

from langchain.llms import OpenAI
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from database import SessionLocal, Video as Video_SQL_Schema
from bot import Summariser, VideoProcessor, Commentator

# Allow communications from other servers (frontend)
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.environ["OPENAI_KEY"])

summariser = Summariser(model=model)
commentator = Commentator(model=model)


class Video(BaseModel):
    id: Optional[str] = None
    url: str
    created_at: Optional[datetime] = None
    title: Optional[str] = None
    n_keypoints: Optional[int] = None
    summary: Optional[str] = None

    class Config:
        orm_mode = True


db = SessionLocal()


@app.options("/videos")
async def videos_options():
    allowed_methods = ["GET", "POST"]
    headers = {"Allow": ", ".join(allowed_methods)}
    return JSONResponse(content={}, status_code=status.HTTP_200_OK, headers=headers)


@app.post(
    "/videos",
    response_model=Video,
    status_code=status.HTTP_201_CREATED,
)
async def add_video_summary(video: Video):
    """This request either creates summary and adds a new record, or retireves an old record with the summary. In both cases it returns the video for a given url."""

    database_record = (
        db.query(Video_SQL_Schema).filter(Video_SQL_Schema.url == video.url).first()
    )
    if database_record:
        return database_record

    video_processor = VideoProcessor(video.url)
    title, n_keypoints, transcripts = video_processor.process_video()

    if sum(video_processor.token_counter(x) for x in transcripts) > 4096:
        raise ValueError("The token limit for model has been exceeded for the video.")

    summary = summariser.get_transcript_summary(
        context=transcripts, n_keypoints=n_keypoints
    )

    new_video = Video_SQL_Schema(
        id=str(uuid.uuid4()),
        url=video.url,
        created_at=datetime.now(),
        title=title,
        n_keypoints=n_keypoints,
        summary=summary,
    )

    db.add(new_video)
    db.commit()

    return new_video


@app.get(
    "/videos",
    response_model=List[Video],
    status_code=status.HTTP_200_OK,
)
async def get_all_videos():
    """This requests gives all the videos/summaries in the current database, so the user can pick from them."""
    videos = db.query(Video_SQL_Schema).all()
    return videos


@app.get(
    "/summary_random",
    response_model=Video,
    status_code=status.HTTP_200_OK,
)
async def get_random_summary():
    """This requests retrieves a random summary from the database"""
    videos = db.query(Video_SQL_Schema).all()
    if videos:
        return random.choice(videos)
    else:
        raise ValueError("No videos in the database.")


@app.put(
    "/comments",
    response_model=str,
    status_code=status.HTTP_200_OK,
)
async def post_summary_comment(video: Video):
    """This request gets the video with a given url and posts a comment with its summary on YouTube."""

    retrieved_video = (
        db.query(Video_SQL_Schema).filter(Video_SQL_Schema.url == video.url).first()
    )

    if not retrieved_video:
        raise HTTPException(status_code=404, detail="This video could not be found.")

    summary = retrieved_video.summary
    title = retrieved_video.title
    n_keypoints = retrieved_video.n_keypoints

    comment = commentator.post_comment(
        url=video.url, summary=summary, title=title, n_keypoints=n_keypoints
    )

    print(f"Summary posted sucessfully at {video.url}.")

    return comment

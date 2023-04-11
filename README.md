# YouTube Summariser

A GPT-based YouTube bot that leaves lovely comments with summaries of key points from YouTube videos.

# Setup

### Environment

Create the environment:

```
conda env create -f environment.yaml
conda activate yt-summariser
```

Set environment variables (replace `zshrc` with `bash_profile` if that's what you use):

```
echo "export OPENAI_KEY="imyouropenaikey"" >> ~/.zshrc
echo "export POSTGRES_PASSWORD="imyourpostreskey"" >> ~/.zshrc
source ~/.zshrc
```

Create the database:

```
python create_db.py
```

### Google API

1. You need to create an account at Google Developers.
2. Go to `Google Cloud` > `Console`.
    * create a new project (top of the page)
3. Go to `API & Services` (left menu) > `Enable APIs and Services` > search for `YouTube API`.
    * make sure you are at the right project, then `Enable the API`
    * go to `Credentials` > `Create Credentials` > `OAuth client ID`
4. This should prompt you to `Configure consent screen` do it, keep clicking next and fill up the application name (any name).
5. Now you can get `OAuth client ID`.
    * `make sure to choose Desktop`, otherwise the authentification process is a bit more complicated
    *  download the secrest file, that's your `secrets/client_secret_desktop.json`
6. Make sure to enable the bot's (or your own) gmail address as one of users permitted to use the app (you can add up around 100 emails there).
7. The API gives you 10 000 credits a day for free, which should equal to around 100 published comments or so.

# Background on the problem

Have you noticed this weird phenomena where people try to bullet-point summarise YouTube videos in the comment section? 

-----

Like this one:
![Screenshot](imgs/tim-bcoder.png)

-----

It's actually quite funny, people seem to like doing summarisation olympics sometimes.

![Screenshot](imgs/olympics-alux.png)

-----

What is even more interesting is that these comments usually get a shit ton of upvotes. Clearly our attention spans are not long enough to watch a 10 minute video in x2 + skipping the content. I encourage you to try [this](https://www.youtube.com/watch?v=Edx9D2yaOGs&embeds_euri=https%3A%2F%2Fwww.notion.so%2F&source_ve_path=Mjg2NjMsMjM4NTE&feature=emb_title
) if you think you're not in that group. I certainly am.

-----

I tried to tackle this problem on one of my past uni assignments with making slight changes to BertSum architecture. Long-story short - lack of available data on the problem leads to inability to properly fine-tune the model and we had to bias it towards certain keywords. It certainly worked better, but it was far from ideal.

Generative text models (like GPT) don't have these problems. I revisited the problem, and it I must conclude the hype is surely real. Here's a generative text bot take on the task:

-----

![Screenshot](imgs/alux-bot.png)

-----

I don't want to spam README.md too much, see `/imgs` for more examples.

# ChatRPG

This project is an attempt to get bots to play an RPG game, with text generated by large language models (LLMs) such as ChatGPT.

## Installation

Clone the repo:

```bash
git clone git@github.com:LomaxOnTheRun/ChatRPG.git
```

Install dependencies (the current Python version is 3.10.8):

```bash
cd ChatRPG
pip install -r requirements.txt
```

Run migrations:

```bash
cd src
./manage.py migrate
```

Run the server:

```bash
./manage.py runserver
```

## Environment variables

It's recommended to have a `.env` file at the top of the repository, with the variables:

* `DJANGO_SECRET_KEY`
* `OPENAI_API_KEY` (you'll need to get this from your OpenAI account)

## Admin page

All data saved can be viewed in the Django admin page, even if there isn't a page for it yet (e.g. character descriptions, historical games).

---
date: 2024-04-23T13:09:22.943618
author: AutoGPT <info@agpt.co>
---

<div align="center">
    <img src="https://github.com/agpt-coder/promptrefinereda704db-49d4-49e4-a0ef-0eb53cf5e6c9/assets/22963551/834fec58-9f4b-4483-b551-39ba2525a06e" width="250" height="250">
</div>

# PromptRefiner

Create a single API endpoint that takes in a string LLM prompt, and returns a refined version which has been improved by GPT4. To "refine" the prompt, use the OpenAI Python package to interface with their AI, and use the GPT4 model. Use this system message: "You are a prompt refiner. Use advanced prompt engineering techniques to refine the user's prompt." and send the user's prompt as the user message.

**Features**

- **Output Interface** Returns the refined prompt back to the user.

- **Input Interface** Takes in a string LLM prompt from the user.

- **Prompt Refinement Processing** Processes the input prompt using GPT-4 to refine it based on advanced prompt engineering techniques.


## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'PromptRefiner'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow

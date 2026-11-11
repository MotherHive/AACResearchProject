# AAC Project
Software created by Cian Wescott under the guidance of Dr. Bruce Wisenburn and David Reese

## Overview
This project is meant to demonstrate a method for accomplishing AAC (Augmentative and Alternative communication). The main target audience for this application are unable to physically speak and require assistance for communication. A well-made system needs to be 1. Accurate to the intentions of the user, 2. Be as close to the speed of normal human communication as possible, and 3. Be intuitive to use. It's also assumed that eye tracking may very-well be necessary in the majority of situations. 

## System Overview
This prototype attempts to use three main inputs, context (including partner speech), communicated intent, and topic selection to reduce the number of inputs. Eye tracking is not included in this project.

### Context
Context currently only includes the partner speech and past conversation, but could include database retrieval in the future.
Context is stored in a local SQLite database and fed initially via microphone alongside STT.

### Topic Selection
Topics are the important phrases in the conversation, such as "I would love to go to the baseball game." -> ["love", "baseball game"] with "baseball game" being preferable, since "love" may be handled by the intent.
Topic selection is captured through input on an on-screen keyboard. When the keyboard gets any input, it uses a custom model to attempt to suggest up to 6 likely topics the user is chasing. Topics are also retrieved from the previous topics and the current sentence. This creates an auto-correct for topic typing and selection.

### Intent
Intent selection voices the desired purpose of a sentence. The intent is second in each example: "When is that?" -> Question, "Can you give me a time?" -> Action, "I couldn't hear you. What time?" -> Fix
Intent is captured through on-screen buttons.

### Output
The information above is then fed to a well-prompted LLM to portray the information on-screen for selection from the user. Once selected, TTS converts it to audio to be played for the speech partner.

## Demo
A gif demonstrating the full process from start to finish.
TODO

## Research Goals
The main goals of this project are the following:
1. Determine if topic selection is intuitive.
2. Research whether contextual topic suggestions reduce typing from the user.
3. See if an LLM can properly capture user intent given enough context.
4. Determine whether relevant topic prediction is an improvement over default topic prediction (inferred vs non-context based)

## Architecture Overview
- Frontend -> Built in React/Typescript
- Backend -> FastAPI and SQLite storage
- TTS -> Inworld API
- STT -> AssemblyAI API
- LLM -> Groq (oss-120b)

### Libraries:
- Topic Extraction -> spaCy
- Topic inference -> Locally trained encoder


## Installation
The commands below use Bash and start from the project root (`AACResearchProject`).

### 1. Check prerequisites
- Python 3.12 or newer.
- Node.js 22.12 or newer and npm.
- An NVIDIA GPU with a CUDA-compatible PyTorch installation. For `device="cuda"`,
- API keys for Groq, AssemblyAI, and Inworld.

### 2. Install Python dependencies
Create and activate the venv + install requirements

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt -r research/topic_encoder/requirements.txt
```

### 3. Configure API keys
Copy the example configuration:

```bash
cp backend/.env.example backend/.env
```

If `backend/.env` already exists, edit it instead of replacing it. Fill in all three values:

```dotenv
GROQ_API_KEY="your_groq_api_key"
INWORLD_API_KEY="your_inworld_api_key"
ASSEMBLYAI_API_KEY="your_assemblyai_api_key"
```

### 4. Prepare the topic model
The backend requires the trained model at `research/topic_encoder/primary_topics_model/` and the topic vocabulary at `research/topic_encoder/data/finished/topics.json`.

If you already have the trained model in that location, skip the commands below. Otherwise, download the base model and train it using the prepared examples and vocabulary included in `data/finished/`:

```bash
cd research/topic_encoder
python download.py
python train.py
cd ../..
```

The download requires internet access. Training uses the GPU and saves the result to `primary_topics_model/`. You do not need to run `download_data.py` or `prepare_data.py` to use the existing prepared training data.

### 5. Install frontend dependencies
From the project root:

```bash
cd frontend
npm ci
cd ..
```

### 6. Start the backend
From the project root, activate the virtual environment and start FastAPI from the `backend` directory so it loads `backend/.env`:

```bash
source .venv/bin/activate
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 7. Start the frontend
In a second terminal, open the project root and run:

```bash
cd frontend
npm run dev -- --port 5173 --strictPort
```

Open <http://localhost:5173> and allow microphone access.

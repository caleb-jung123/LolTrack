# LoLTrack

LolTrack is an application that allows users to find their League of Legends profile and check their match history, as well as their overall statistics.

# Features

- Leverages the Riot API to fetch player information
- Users can get a detailed view of how specific matches went
- Users can see an overview of their last 10 games

# Tech Stack

- Frontend: React.js, Bootstrap 5 (supplemented by custom CSS)
- Backend: FastAPI (Python), Riot API
- Database: SQLite

# Setup Guide

### 1. Obtain a Riot API Key

- Visit https://developer.riotgames.com/
- Create or use an existing Riot account to sign up for a developer key
- Navigate to the user dashboard and find your development key in the 'Development API Key' section
- Copy the development key

### 2. Clone the Repository

- Before we continue with the guide, we must clone the repository
- Open a terminal and then navigate to your directory of choice
- Type in the following command:

  ```bash
  git clone https://github.com/caleb-jung123/LolTrack.git
  ```

- You will now see a folder called LolTrack which contains the application

### 3. Backend Setup

Navigate to the LolTrack folder and do the following:

```bash
cd backend
python -m venv .venv
```

Activate your virtual environment for the terminal you are on:
- bash: `.venv/Scripts/activate`
- PowerShell: `.venv/Scripts/Activate.ps1`
- cmd: `.venv/Scripts/activate.bat`

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a .env file in the backend folder. You can copy the contents of the env.template file over to your newly created .env

Copy your Riot development key into the RIOT_API_KEY part of the .env file. The following is an example of what you should have:

```
RIOT_API_KEY=RGAPI-your-actual-key-here
REGION_GROUP=americas
CACHE_TTL_SECONDS=600
```

You can change the REGION_GROUP accordingly between americas, europe, and asia

### 4. Frontend Setup

Navigate to the LolTrack folder and do the following:

```bash
cd frontend
npm install
```

### 5. Running the Application

Terminal 1 (Backend):
1. Navigate to the backend folder
2. Activate your virtual environment using the correct command from step 3
3. Run:

   ```bash
   uvicorn app:app --reload
   ```

Terminal 2 (Frontend):
1. Navigate to the frontend folder
2. Run:

   ```bash
   npm run dev
   ```

You can now use the application by navigating to `http://localhost:5173` in the browser of your choice

# Attributions

### Riot Games

LoLTrack is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc.

This project is a personal, non-commercial application built using the official Riot Games API. LoLTrack is an independent project and is not affiliated with, sponsored by, or endorsed by Riot Games, Inc.

All game data, champion names, and images are the property of Riot Games, Inc.

### Twemoji

Emoji graphics used in this project are from [Twemoji](https://twemoji.twitter.com/) by Twitter, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Copyright 2020 Twitter, Inc and other contributors.
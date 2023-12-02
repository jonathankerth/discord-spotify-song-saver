# Discord & Spotify Song Saver

## Overview

The Discord Spotify Song Saver project emerged from brainstorming with friends about building something beneficial and enjoyable for our group. It captures songs shared in Discord and assembles them into an ever-updating Spotify playlist, mirroring our collective musical preferences. This endeavor not only elevates our music-sharing experience but also serves as a platform for expanding my knowledge and honing my technical skills, making it a rewarding and educational venture.

## Features

- **Discord Bot**: Detects Spotify track links in Discord messages and saves them to Firebase.
- **Spotify Bot**: Runs twice a day to add new songs from Firebase to a Spotify playlist.

## Requirements

- Python 3.12
- Discord and Spotify API credentials
- Firebase account and credentials
- Heroku account for hosting (optional)

## Dependencies

Listed in `requirements.txt` file. Key libraries include:

- `discord.py`
- `firebase-admin`
- `spotipy`
- `python-dotenv`

## Installation

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file (refer to `.env.example`).

## Configuration

- Set your Spotify API credentials in the `.env` file.
- Set your Firebase service account credentials in the `.env` file.
- Configure Discord bot token and channel IDs in the `.env` file.

## Usage

### Discord Bot (`bot.py`)

- Deploy on a server or hosting platform like Heroku.
- The bot listens for Spotify track links in a specified Discord channel and saves them to Firebase.

### Spotify Bot (`spotify_bot.py`)

- Can be scheduled to run periodically (e.g., using Heroku Scheduler).
- Retrieves song links from Firebase and adds them to the specified Spotify playlist.

## Hosting

- The project is configured for Heroku deployment.
- Set up the Heroku environment with Python buildpack and necessary config vars.

## Contributing

- Fork the repository.
- Create a new branch for your feature.
- Submit a pull request.

## License

- Specify the license under which the project is released.

## Contact

- Provide contact information for users to report issues or contribute to the project.

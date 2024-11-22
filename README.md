# TikTok Favorite Videos Downloader

This project is a Python script to download every video from your favorites on TikTok. It uses the Cobalt API to download videos and slideshows. Unfortuneatly cobalt has discontinued the free hosted api and you must now self host. Luckily it is incredibly easy to do and I have provided instructions from chatgpt on how to do exactly that.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Starting the Cobalt API](#starting-the-cobalt-api)
- [Usage](#usage)
- [Errors](#errors)
- [Getting Your TikTok Data](#getting-your-tiktok-data)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/JackB296/tiktok-favorites-downloader.git
    cd tiktok-favorites-downloader
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Open that baby up and mess with these parameters if ya want. It would be pretty easy to change the script to not delete the `IMG_DIR` after the video is generated. I use plex to view these video afterwards so I prefer the video format but your more than likely to keep each image directory and make a special more tiktok esque viewer.

- `RETRY_DELAY`: Time in seconds between each retry attempt.
- `DOWNLOAD_DIR`: Directory where downloaded videos will be stored.
- `IMG_DIR`: Temporary directory for creating slideshows.
- `LAST_DOWNLOADED_LINK_FILE`: File to store the last downloaded link.
- `VIDEO_LINKS_FILE`: TikTok data file containing favorite video links.
- `DURATION_PER_IMAGE`: Duration each slide is shown in the slideshow video.
- `TARGET_SIZE`: Target resolution for images.

## Starting the Cobalt API

This script relies on the Cobalt API for downloading videos. Follow these steps to set up and start your own instance of the API on Windows using WSL:

### Prerequisites

- **Windows Subsystem for Linux (WSL)** with a Linux distribution installed (e.g., Ubuntu).
- **Node.js** version 18 or higher.
- **Git** for cloning repositories.
- **pnpm** (a fast, disk space-efficient package manager).

### Steps to Set Up the Cobalt API

1. **Install WSL and a Linux Distribution (if not already installed):**

    Open PowerShell as an administrator and run:

    ```bash
    wsl --install
    ```

    Restart your computer when prompted, and complete the installation of Ubuntu.

2. **Update and Upgrade Your Linux Distribution:**

    Open your Ubuntu terminal and run:

    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

3. **Install Node.js (Version 18 or Higher):**

    Install the Node.js version manager (nvm):

    ```bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash
    source ~/.bashrc
    ```

    Install Node.js 18 and use it:

    ```bash
    nvm install 18
    nvm use 18
    ```

    Verify the installation:

    ```bash
    node -v
    ```

4. **Install Git:**

    ```bash
    sudo apt install git -y
    ```

5. **Install pnpm:**

    ```bash
    npm install -g pnpm
    ```

6. **Clone the Cobalt Repository:**

    ```bash
    git clone https://github.com/imputnet/cobalt.git
    ```

7. **Navigate to the API Directory:**

    ```bash
    cd cobalt/api/src
    ```

8. **Install Dependencies:**

    ```bash
    pnpm install
    ```

9. **Create a `.env` File with Required Environment Variables:**

    Create and edit the `.env` file:

    ```bash
    nano .env
    ```

    Add the following content:

    ```env
    API_URL=http://localhost:9000/
    ```

    Save and exit the editor (`Ctrl+O` to save, `Ctrl+X` to exit in nano).

10. **Start the Cobalt API Server:**

    ```bash
    pnpm start
    ```

    The server should now be running on port 9000.

11. **Stopping the Server:**

    You can use Ctrl+C in the terminal running the api to stop the server.

## Usage

1. Ensure you have your TikTok data file (`user_data_tiktok.json`) in the project directory. For instructions on how to get this data, see the [Getting Your TikTok Data](#getting-your-tiktok-data) section.

2. Start the Cobalt API (see [Starting the Cobalt API](#starting-the-cobalt-api)).

3. Run the script:

    ```bash
    python tiktok.py
    ```

## Errors

- If the program has an error, my best suggestion is to copy the last link from the terminal and put it into the `last_downloaded_link.txt` file, then rerun the program. 
- If you get a 404 error, your API may not be working correctly.
- If your links just dont seem to be working I reccomend re-downloading your data and trying again. This had happened to me on multiple occasions.

## Getting Your TikTok Data

To download your favorites you will need to get your TikTok data:

1. **Go to Settings**: On the TikTok web, navigate to the settings page.
2. **Request Data**: Find the `Data` section and click on the `Download Your Data` button. Choose all data and JSON format.
3. **Wait and Download**: Wait a few minutes for TikTok to process your request. Reload the page and you should be able to download your data.
4. **Extract Data**: Extract the `user_data_tiktok.json` file from the downloaded zip and place it in the project directory.

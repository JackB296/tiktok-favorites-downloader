# TikTok Favorite Videos Downloader

This project is a Python script to download every video from your favorites on TikTok. It uses the Cobalt API to download videos and slideshows. 

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
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

Open that baby up and mess with these paremeters if ya want. It would be pretty easy to change the script to not delete the IMG_DIR after the video is generated.

- `RETRY_DELAY`: Time in seconds between each retry attempt.
- `DOWNLOAD_DIR`: Directory where downloaded videos will be stored.
- `IMG_DIR`: Temporary directory for creating slideshows.
- `LAST_DOWNLOADED_LINK_FILE`: File to store the last downloaded link.
- `VIDEO_LINKS_FILE`: TikTok data file containing favorite video links.
- `DURATION_PER_IMAGE`: Duration each slide is shown in the slideshow video.
- `TARGET_SIZE`: Target resolution for images.

## Usage

1. Ensure you have your TikTok data file (`user_data_tiktok.json`) in the project directory. For instructions on how to get this data, see the [Getting Your TikTok Data](#getting-your-tiktok-data) section.

2. Run the script:

    ```bash
    python tiktok.py
    ```
## Errors

If the program has an error my best suggestion is to copy the last link from the terminal and put it into the last_downloaded_link.txt and rerun the program.

## Getting Your TikTok Data

To download your TikTok favorites, you need to get your TikTok data:

1. **Go to Settings**: On the TikTok web, navigate to the settings page.
2. **Request Data**: Find the `Data` section and click on the `Download Your Data` button. Choose all data and JSON format.
3. **Wait and Download**: Wait a few minutes for TikTok to process your request. Reload the page, and you should be able to download your data.
4. **Extract Data**: Extract the `user_data_tiktok.json` file from the downloaded zip and place it in the project directory.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

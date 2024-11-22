import requests
import json
import re
import os
import time
import logging
from requests.exceptions import ChunkedEncodingError, ConnectionError, Timeout
import shutil
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_audioclips
from PIL import Image

# Configuration
COBALT_API_URL = "http://localhost:9000/"
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
RETRY_DELAY = 0.5  # Seconds between each download attempt
DOWNLOAD_DIR = "downloads"  # Directory to download videos
IMG_DIR = "img_dir"  # Temporary directory for creating slideshows
LAST_DOWNLOADED_LINK_FILE = "last_downloaded_link.txt"  # File to store the last downloaded link
VIDEO_LINKS_FILE = "user_data_tiktok.json"  # TikTok data file
DURATION_PER_IMAGE = 2.5  # Duration each slide is shown in the slideshow
TARGET_SIZE = (1280, 720)  # Target resolution for images

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_payload(url):
    return {
        "url": url,
        "videoQuality": "max",
        "tiktokH265": True,
        "audioFormat": "best",
    }

def download_file(url, filename, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            logging.info(f"Downloaded: {filename}")
            if os.path.getsize(filename) == 0:
                return False
            return True
        except (ChunkedEncodingError, ConnectionError, Timeout) as e:
            logging.error(f"Error downloading {url}: {e}. Retrying {attempt + 1}/{max_retries}...")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            logging.exception(f"Failed to download {url} due to an unexpected error: {e}")
            break
    logging.error(f"Failed to download {url} after {max_retries} attempts.")
    return False

def download_images(image_urls, download_dir):
    image_filenames = []
    for idx, img_url in enumerate(image_urls):
        filename = os.path.join(download_dir, f"slide_{idx}.jpg")
        if download_file(img_url, filename):
            image_filenames.append(filename)
    return image_filenames

def read_video_links(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        logging.error(f"Video links file not found: {file_path}")
        return []
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from file: {file_path}")
        return []

    item_favorite_list = data.get("Activity", {}).get("Favorite Videos", {}).get("FavoriteVideoList", [])

    modified_lines = [
        re.sub(r'tiktokv.com', 'tiktok.com', item["Link"])
        for item in item_favorite_list if "Link" in item
    ][::-1]

    last_downloaded_link = read_last_downloaded_link(LAST_DOWNLOADED_LINK_FILE)
    if last_downloaded_link:
        try:
            last_link_index = modified_lines.index(last_downloaded_link)
            new_links = modified_lines[last_link_index + 1:]
        except ValueError:
            new_links = modified_lines
    else:
        new_links = modified_lines

    if new_links:
        write_last_downloaded_link(LAST_DOWNLOADED_LINK_FILE, new_links[-1])

    return new_links

def resize_and_pad_image(image_path, target_size):
    try:
        image = Image.open(image_path)
        image.thumbnail(target_size, Image.Resampling.LANCZOS)
        new_image = Image.new("RGB", target_size, (0, 0, 0))
        new_image.paste(image, ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2))
        new_image.save(image_path)
    except Exception as e:
        logging.exception(f"Failed to resize and pad image {image_path}: {e}")

def preprocess_images(image_paths, target_size):
    for image_path in image_paths:
        resize_and_pad_image(image_path, target_size)

def get_next_starting_count(directory):
    if not os.path.exists(directory):
        return 1
    existing_files = os.listdir(directory)
    video_numbers = [int(f.split('.')[0]) for f in existing_files if f.endswith('.mp4') and f.split('.')[0].isdigit()]
    return max(video_numbers, default=0) + 1

def read_last_downloaded_link(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            last_link = f.read().strip()
    except FileNotFoundError:
        last_link = None
    return last_link

def write_last_downloaded_link(file_path, last_link):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(last_link)
    except Exception as e:
        logging.error(f"Error writing last downloaded link: {e}")

def create_slideshow(images, audio, output_filename, duration_per_image):
    preprocess_images(images, TARGET_SIZE)
    clip = ImageSequenceClip(images, durations=[duration_per_image] * len(images))

    try:
        audio_clip = AudioFileClip(audio)
        slideshow_duration = len(images) * duration_per_image

        num_loops = int(slideshow_duration / audio_clip.duration) + 1
        looped_audio = concatenate_audioclips([audio_clip] * num_loops)
        looped_audio = looped_audio.subclip(0, slideshow_duration)

        clip = clip.set_audio(looped_audio)
        clip.write_videofile(output_filename, codec="libx264", fps=24)

        clip.close()
        audio_clip.close()
        looped_audio.close()
    except Exception as e:
        logging.exception(f"Failed to create slideshow: {e}")

def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    video_links = read_video_links(VIDEO_LINKS_FILE)
    start_count = get_next_starting_count(DOWNLOAD_DIR)
    for count, video_link in enumerate(video_links, start_count):
        payload = create_payload(video_link)
        response = requests.post(COBALT_API_URL, headers=HEADERS, data=json.dumps(payload))
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Response for {video_link}: {data}")

            status = data.get("status")

            if status in ["redirect", "tunnel"]:
                download_url = data["url"]
                filename = os.path.join(DOWNLOAD_DIR, f"{count}.mp4")
                if not download_file(download_url, filename):
                    logging.error(f"Failed to download video: {video_link}")
            elif status == "picker":
                picker = data.get("picker", [])
                if picker and picker[0].get("type") == "photo":
                    image_urls = [item["url"] for item in picker]
                    audio_url = data.get("audio")
                    if image_urls:
                        os.makedirs(IMG_DIR, exist_ok=True)
                        image_files = download_images(image_urls, IMG_DIR)
                        if audio_url:
                            audio_file = os.path.join(IMG_DIR, "audio.mp3")
                            if not download_file(audio_url, audio_file):
                                logging.warning("The audio for this slideshow no longer exists, using default audio")
                                shutil.copy('default.mp3', audio_file)
                        else:
                            logging.warning("No audio found in picker response, using default audio")
                            audio_file = 'default.mp3'
                        filename = os.path.join(DOWNLOAD_DIR, f"{count}.mp4")
                        create_slideshow(image_files, audio_file, filename, DURATION_PER_IMAGE)
                        shutil.rmtree(IMG_DIR)
                    else:
                        logging.error(f"No images found in picker response for {video_link}")
                else:
                    logging.error(f"Picker response contains unsupported media types for {video_link}")
            elif status == "error":
                error_info = data.get("error", {})
                logging.error(f"Error in response for {video_link}: {error_info}")
            else:
                logging.error(f"Unknown status '{status}' in response for {video_link}")
        else:
            logging.error(f"Failed to process video {video_link}: HTTP {response.status_code}")
            logging.error(f"Response: {response.text}")

        time.sleep(RETRY_DELAY)

if __name__ == "__main__":
    main()

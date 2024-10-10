# Text-to-Video Pipeline README

## Overview
This Python script generates a video by utilizing given text as input. The process involves splitting the text into sentences, generating images for each sentence using DALL·E, converting sentences to speech, and finally creating a video with subtitles for each sentence. The generated video clips are then concatenated to produce the final output video.

## Prerequisites
To run this script, you need to install the following Python packages and dependencies:

1. **openai** (for DALL·E API integration)
   ```sh
   pip install openai
   ```

2. **gtts** (for text-to-speech conversion)
   ```sh
   pip install gtts
   ```

3. **moviepy** (for creating video clips)
   ```sh
   pip install moviepy
   ```

4. **requests** (for downloading generated images)
   ```sh
   pip install requests
   ```

5. **Pillow** (for image processing)
   ```sh
   pip install Pillow
   ```

6. **python-dotenv** (for managing environment variables)
   ```sh
   pip install python-dotenv
   ```

Additionally, you need to install **ImageMagick**:
- [ImageMagick Download Page](https://imagemagick.org/script/download.php)
  - Make sure to add ImageMagick to your system's PATH during installation.

## Environment Setup
Create a `.env` file in the project directory with the following content:

```env
OPENAI_API_KEY=your_openai_api_key_here
IMAGEMAGICK_BINARY_PATH="C:\\Program Files\\ImageMagick-VERSION\\magick.exe"
```
Replace `your_openai_api_key_here` with your actual OpenAI API key, and update the `IMAGEMAGICK_BINARY_PATH` to point to your ImageMagick installation.

## Running the Script
1. **Load Environment Variables**: The script uses `dotenv` to load the API key and ImageMagick path from the `.env` file.
2. **Text Splitting**: The input text is split into sentences based on Chinese punctuation.
3. **Image Generation**: For each sentence, an image is generated using OpenAI's DALL·E API.
4. **Text-to-Speech Conversion**: Each sentence is converted to audio using Google Text-to-Speech (gTTS).
5. **Video Creation**: Video clips are generated using MoviePy by combining images, audio, and subtitles.
6. **Video Concatenation**: All generated clips are concatenated into the final output video.

To run the script, use the following command:

```sh
python your_script_name.py
```

## Debugging
The script contains several print statements that provide detailed information about each step's progress, such as:
- Whether the API keys and ImageMagick paths are loaded correctly.
- The results of text splitting.
- URLs of generated images and paths of saved files.
- Status updates for text-to-speech conversions and video creation steps.

These logs can help trace any issues during the script's execution.

## Example
The default example text is:

```python
text = "一只小猫在河边钓鱼，一只小猫在河边抓蝶虫"
```
The script will generate images, audio, and a video for each sentence, then combine them into a single video.

## Output
The final output video will be saved as `final_output.mp4` in the current working directory, with an FPS of 24 frames per second.

## Troubleshooting
- **FileNotFoundError**: If you encounter this error while creating text clips, ensure that ImageMagick is properly installed and the binary path is correctly configured.
- **OpenAI API Issues**: Make sure the API key is valid and has access to use the DALL·E API.

## License
This project is intended for educational purposes and personal use. Be sure to follow the usage policies of OpenAI, Google Text-to-Speech, and other dependencies used in this project.


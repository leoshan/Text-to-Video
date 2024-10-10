from openai import OpenAI
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import requests
from PIL import Image
from io import BytesIO
import os
from moviepy.config import change_settings
import dotenv

# 加载环境变量
dotenv.load_dotenv()

# 设置 OpenAI 客户端和 API 密钥
openai_api_key = os.getenv("OPENAI_API_KEY")  # 从环境变量中加载 OpenAI API 密钥
print(f"Loaded OpenAI API key: {openai_api_key is not None}")
client = OpenAI(api_key=openai_api_key)

# 设置 ImageMagick 的路径
imagemagick_binary_path = os.getenv("IMAGEMAGICK_BINARY_PATH")  # 从环境变量中加载 ImageMagick 路径
print(f"Loaded ImageMagick binary path: {imagemagick_binary_path}")
os.environ["IMAGEMAGICK_BINARY"] = imagemagick_binary_path
change_settings({"IMAGEMAGICK_BINARY": imagemagick_binary_path})

# Step 1: Text splitting (basic sentence splitting)
def split_text(text):
    sentences = text.split('，')  # 基于中文逗号分句
    print(f"Split text into sentences: {sentences}")
    return sentences

# 示例文本
text = "一只小猫在河边钓鱼，一只小猫在河边抓蝶虫"
sentences = split_text(text)
print(sentences)

# Step 2: Generate image using DALL·E API
def generate_image_from_text(prompt):
    # 增加描述性词语，使生成的图像更具细节和效果
    detailed_prompt = f"{prompt}, highly detailed, realistic, vibrant colors, cinematic lighting"
    print(f"Generating image with prompt: {detailed_prompt}")
    response = client.images.generate(
        model="dall-e-3",
        prompt=detailed_prompt,
        size="1024x1024",  # 可以根据需要调整图像大小
        quality="standard",
        n=1
    )
    image_url = response.data[0].url
    print(f"Generated image URL: {image_url}")
    return image_url

# 从生成的图像 URL 下载并保存图片
def save_image_from_url(image_url, filename):
    print(f"Downloading image from URL: {image_url}")
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save(filename)
    print(f"Saved image as: {filename}")

# 为每个句子生成图片并保存
image_files = []
for i, sentence in enumerate(sentences):
    print(f"Processing sentence {i + 1}/{len(sentences)}: {sentence}")
    image_url = generate_image_from_text(sentence)
    image_filename = f"image_{i}.png"
    save_image_from_url(image_url, image_filename)
    image_files.append(image_filename)

# Step 3: Convert text to speech (using gTTS)
def text_to_speech(text, output_file):
    print(f"Converting text to speech: {text}")
    tts = gTTS(text=text, lang='zh')
    tts.save(output_file)
    print(f"Saved audio as: {output_file}")

# 将每个句子转换为语音并保存为 mp3 文件
for i, sentence in enumerate(sentences):
    print(f"Processing text-to-speech for sentence {i + 1}/{len(sentences)}")
    text_to_speech(sentence, f"output_{i}.mp3")

# Step 4: Create video clips using MoviePy with subtitles
def create_video(image, audio, text, duration=5):
    print(f"Creating video clip for image: {image} and audio: {audio}")
    # 创建图片片段
    img_clip = ImageClip(image).set_duration(duration)
    # 加语音片段
    audio_clip = AudioFileClip(audio)
    video_clip = img_clip.set_audio(audio_clip)
    # 创建字幕片段
    txt_clip = TextClip(text, fontsize=40, color='gold', font="SimHei", stroke_color='black', stroke_width=2)
    txt_clip = txt_clip.set_position(lambda t: ('center', img_clip.h * 0.85)).set_duration(duration)
    # 合并图片和字幕
    composite_clip = CompositeVideoClip([video_clip, txt_clip])
    print(f"Created composite video clip for: {text}")
    return composite_clip

# 为每个图像和对应的音频生成视频片段
video_clips = []
for i in range(len(sentences)):
    print(f"Creating video clip {i + 1}/{len(sentences)}")
    video_clips.append(create_video(f"image_{i}.png", f"output_{i}.mp3", sentences[i]))

# Step 5: Concatenate video clips into the final video and set FPS
print("Concatenating all video clips into the final video.")
final_clip = concatenate_videoclips(video_clips)

# 指定 FPS 参数
output_filename = "final_output.mp4"
print(f"Writing final video to {output_filename} with fps=24")
final_clip.write_videofile(output_filename, fps=24)  # 将 fps 设置为 24 或其他适合的帧率
print(f"Final video saved as: {output_filename}")
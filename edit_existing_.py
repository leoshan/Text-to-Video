from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import os
from moviepy.config import change_settings
import dotenv
# 加载环境变量
dotenv.load_dotenv()

# 设置 ImageMagick 的路径
imagemagick_binary_path = os.getenv("IMAGEMAGICK_BINARY_PATH")  # 从环境变量中加载 ImageMagick 路径
os.environ["IMAGEMAGICK_BINARY"] = imagemagick_binary_path
change_settings({"IMAGEMAGICK_BINARY": imagemagick_binary_path})

# Step 1: Get existing images and audio files
def get_existing_files():
    image_files = sorted([f for f in os.listdir() if f.startswith("image_") and f.endswith(".png")])
    audio_files = sorted([f for f in os.listdir() if f.startswith("output_") and f.endswith(".mp3")])
    return image_files, audio_files

image_files, audio_files = get_existing_files()

# 示例句子列表（与已有素材对应的文本）
sentences = ["一只小猫在河边钓鱼", "一只小猫在河边抓蝶虫"]

# Step 2: Create video clips using MoviePy with subtitles
def create_video(image, audio, text, duration=5):
    # 创建图片片段
    img_clip = ImageClip(image).set_duration(duration)
    # 加语音片段
    audio_clip = AudioFileClip(audio)
    video_clip = img_clip.set_audio(audio_clip)
    # 创建字幕片段
    txt_clip = TextClip(text, fontsize=80, color='red', font="SimHei", stroke_color='black', stroke_width=2)
    txt_clip = txt_clip.set_position(lambda t: ('center', img_clip.h * 0.85)).set_duration(duration)
    # 合并图片和字幕
    composite_clip = CompositeVideoClip([video_clip, txt_clip])
    return composite_clip

# 为每个图像和对应的音频生成视频片段
video_clips = []
for i in range(len(image_files)):
    video_clips.append(create_video(image_files[i], audio_files[i], sentences[i]))

# Step 3: Concatenate video clips into the final video and set FPS
final_clip = concatenate_videoclips(video_clips)

# 指定 FPS 参数
final_clip.write_videofile("final_output.mp4", fps=24)  # 将 fps 设置为 24 或其他适合的帧率
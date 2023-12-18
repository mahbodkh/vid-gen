import csv
import os
import random
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.editor import *
from moviepy.editor import AudioFileClip
import datetime




def wrap_text(text, max_chars_per_line):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + " " + word) <= max_chars_per_line:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    wrapped_text = "\n".join(lines)
    return wrapped_text



def create_short_videos(csv_file):
    background_folder = "backgrounds/"
    font_name = "calibri-bold"
    music_folder = "music/"
    output_folder = "output/"
    duration = 11.0  # Total duration of each video in seconds
    max_font_size = 130  # Maximum font size for {FIRST} and {SECOND}
    max_chars_per_line = 19


    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)

        # for row in reader:
        for count, row in enumerate(reader, 1):
            if row['Topic'] is None or row['First'] is None or row['Second'] is None:
                continue  # Skip this row and move to the next row

            topic = row['Topic']
            first = row['First']
            second = row['Second']
            tags = row['Tags']


            # Choose a random background video from the folder
            background_files = [file for file in os.listdir(background_folder) if file.endswith(".mp4") and file != ".DS_Store"]
            background_file = random.choice(background_files)
            background_path = os.path.join(background_folder, background_file)
            background = VideoFileClip(background_path)

            music_files = [file for file in os.listdir(music_folder) if file.endswith(".mp3") and file != ".DS_Store"]
            music_file = random.choice(music_files)
            music_path = os.path.join(music_folder, music_file)
            music = AudioFileClip(music_path)
            
            if music.duration < duration:
                print("music duration is less and the duration as you expected: " + duration )
                return
            music = music.subclip(0, min(duration, music.duration))


            # Fix the background duration
            if background.duration < duration:
                repetitions = int(duration / background.duration) + 1
                background = concatenate_videoclips([background] * repetitions)
            background = background.subclip(0, duration)

            # Add text overlays
            # Adjust positioning of text if it exceeds background width
            text_topic = TextClip(topic, fontsize=100, color='black', stroke_color='white', stroke_width=3,
                                  method='label', font=font_name)
            channel_name = TextClip('@WorthEveryFacts', fontsize=40, color='white', stroke_color='black', stroke_width=1,
                                  method='label', font=font_name)
            text_first = TextClip(wrap_text(first, max_chars_per_line), fontsize=max_font_size, color='white',
                                   stroke_color='black', stroke_width=4, method='label', font=font_name)
            text_second = TextClip(wrap_text(second, max_chars_per_line), fontsize=max_font_size, color='white',
                                    stroke_color='black', stroke_width=4, method='label', font=font_name)

            text_topic_pos = (background.w / 2 - text_topic.w / 2, 150)
            channel_name_pos = (background.w / 2 - text_topic.w / 2, 250) #130 up
            text_first_pos = (background.w / 2 - text_first.w / 2, background.h / 2 - text_first.h / 2)
            text_second_pos = (background.w / 2 - text_second.w / 2, background.h - text_second.h - 300)

            text_topic = text_topic.set_position(text_topic_pos).set_duration(duration)
            channel_name = channel_name.set_position(channel_name_pos).set_duration(duration)
            text_first = text_first.set_position(text_first_pos).set_duration(duration)
            text_second = text_second.set_position(text_second_pos).set_duration(duration)
            



            # Apply fade-in and fade-out effects to the first and second texts
            fade_duration = 1.0
            fade_out_end = 11.0
            
            # text_first = text_first.fadein(fade_duration).set_start(0.0).set_end(1.0)
            text_first = text_first.fadeout(fade_duration).set_start(0.0).set_end(8.5)

            # text_second = text_second.fadein(fade_duration).set_start(8.5).set_end(9.0)
            text_second = text_second.fadeout(fade_duration).set_start(9.0).set_end(10.0)
        
            # Create a CompositeVideoClip with the {TOPIC} text and the box
            video = CompositeVideoClip([background, text_topic, channel_name, text_first, text_second])

            # Set the video duration and write to output file
            video = video.set_duration(duration)
            video = video.set_audio(music)

            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            output_file = os.path.join(output_folder, f"{count}_{first}_{topic}_{tags.lower()}.mp4")
            video.write_videofile(output_file, codec='libx264', audio_codec="aac", fps=30, remove_temp=True)

# Usage
create_short_videos('/Users/admin/Documents/bulkvid/videos.csv')
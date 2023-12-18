import csv
import os
import random
import math
from moviepy.editor import *
from moviepy.video.fx import fadein, fadeout
import datetime


def wrap_text(text, max_chars_per_line):
    lines = []
    num_lines = math.ceil(len(text) / max_chars_per_line)
    for i in range(num_lines):
        start = i * max_chars_per_line
        end = start + max_chars_per_line
        line = text[start:end]
        lines.append(line)
    return lines



def create_short_videos(csv_file):
    background_folder = "backgrounds/"
    output_folder = "output/"
    duration = 11.0  # Total duration of each video in seconds
    max_font_size = 120  # Maximum font size for {FIRST} and {SECOND}
    line_spacing = 10  # Spacing between lines in pixels



    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            topic = row['Topic']
            first = row['First']
            second = row['Second']

            # Choose a random background video from the folder
            background_files = [file for file in os.listdir(background_folder) if file != ".DS_Store"]
            background_file = random.choice(background_files)
            background_path = os.path.join(background_folder, background_file)
            background = VideoFileClip(background_path)

            # Fix the background duration
            if background.duration < duration:
                repetitions = int(duration / background.duration) + 1
                background = concatenate_videoclips([background] * repetitions)
                background = background.subclip(0, duration)

            # Add text overlays
            text_topic = TextClip(topic, fontsize=90, color='white', stroke_color='black', stroke_width=5, method='label', font='calibri-bold')
            text_first = TextClip(first, fontsize=max_font_size, color='white', stroke_color='black', stroke_width=5, method='label', font='calibri-bold')
            text_second = TextClip(second, fontsize=max_font_size, color='white', stroke_color='black', stroke_width=5, method='label', font='calibri-bold')

            # Adjust font size until it fits within the background width
            while text_first.w > background.w:
                max_font_size -= 5
                text_first = TextClip(first, fontsize=max_font_size, color='white', stroke_color='black',
                                       stroke_width=3, method='label', font='calibri-bold')

            while text_second.w > background.w:
                max_font_size -= 5
                text_second = TextClip(second, fontsize=max_font_size, color='white', stroke_color='black',
                                        stroke_width=3, method='label', font='calibri-bold')


            # Adjust positioning of text if it exceeds background width
            text_width = text_first.w
            text_topic_pos = (background.w / 2 - text_topic.w / 2, 150)
            text_first_pos = (background.w / 2 - text_first.w / 2, background.h / 2 - text_first.h / 2)
            text_second_pos = (background.w / 2 - text_second.w / 2, background.h - text_second.h - 50)


            if text_first.w > background.w:
                text_first = text_first.set_position(text_first_pos).set_duration(duration)
                text_second = text_second.set_position(text_second_pos).set_duration(duration)
            else:
                text_first = text_first.set_position(text_first_pos).set_duration(duration)
                text_second = text_second.set_position(text_second_pos).set_duration(duration)
            text_topic = text_topic.set_position(text_topic_pos).set_duration(duration)

            # Apply fade-in and fade-out effects to the first and second texts
            fade_duration = 1.0
            fade_out_end = 11.0
            
            # text_first = text_first.fadein(fade_duration).set_start(0.0).set_end(1.0)
            text_first = text_first.fadeout(fade_duration).set_start(0.0).set_end(8.5)

            # text_second = text_second.fadein(fade_duration).set_start(8.5).set_end(9.0)
            text_second = text_second.fadeout(fade_duration).set_start(9.0).set_end(10.0)
        
            video = CompositeVideoClip([background, text_topic, text_first, text_second])

            # Set the video duration and write to output file
            video = video.set_duration(duration)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            output_file = os.path.join(output_folder, f"{topic}_{timestamp}.mp4")
            video.write_videofile(output_file, codec='libx264', audio_codec="aac", fps=30, remove_temp=True)

# Usage
create_short_videos('/Users/admin/Documents/bulkvid/videos.csv')

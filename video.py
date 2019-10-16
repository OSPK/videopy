import ffmpeg
import sys
import os
import json, subprocess
from moviepy.editor import *

directory = "/home/waqas/Videos/"
logo = directory + "brt_logo.jpg"
f_input = directory+sys.argv[1]
f_output = directory+sys.argv[2]
start_time = float(sys.argv[3])
end_time = float(sys.argv[4])
ending_clip = directory+"end_tail.mp4"

# stream = ffmpeg.input(f_input)
# stream = ffmpeg.trim(stream, start_frame=190)
# stream = ffmpeg.output(stream, f_output)
# ffmpeg.run(stream)
if start_time is None:
	# Detect scene change
	ffprobe_cmd = 'ffprobe -show_frames -of compact=p=0 -f lavfi "movie={},select=gt(scene\,.4)"'.format(f_input)

	s = subprocess.Popen(ffprobe_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	# get scene change output
	ffprobe_out, err = s.communicate()
	ffprobe_str = str(ffprobe_out)

	#fint the timestamp
	first = ffprobe_str.find("best_effort_timestamp_time")
	start_time = ffprobe_str[first:].split("|")[0].split("=")[1]
	start_time = "%.2f" % float(start_time)
	start_time = float(start_time)

print("Start Time:", start_time)

# start conversion with moviepy
video = VideoFileClip(f_input)
endingclip = VideoFileClip(ending_clip)

if end_time is None:
	end_time = video.duration

print("Duration:", video.duration)
video = video.subclip(start_time, end_time)
video = video.resize( (1280,720) )

logo = ImageClip(logo)\
          .set_duration(video.duration)\
          .resize(height=60)\
          .margin(right=15, top=15, opacity=0)\
          .set_opacity(0.9)\
          .set_pos(("right","top"))

video = CompositeVideoClip([video, logo])
final = concatenate_videoclips([video,endingclip])
final.write_videofile(f_output)

#remove temp file and overwrite original file - get done with it
# os.system("rm {}".format(f_input))
# os.system("mv {} {}".format(f_output, f_input))
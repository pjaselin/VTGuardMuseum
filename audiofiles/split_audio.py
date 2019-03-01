# file to split main audio file into smaller sections
from pydub import AudioSegment
# import full audio files from archives.org
sound = AudioSegment.from_mp3("/home/pi/VTGuard/audiofiles/fdr_full.mp3")

# obtain and save audio segments

# interval for audio split (len() and slicing are in milliseconds)
# split length is total time/number of spluts
split_length = len(sound)/5

i = 0
while (i * split_length) <= len(sound):
    sample = sound[(split_length * i):(split_length * (i + 1))]
    save_filepath = "/home/pi/VTGuard/audiofiles/sample_" + str(i) + ".mp3"
    sample.export(save_filepath, format="mp3")
    i += 1

# Concatenation is just adding
#second_half_3_times = second_half + second_half + second_half

# writing mp3 files is a one liner
#second_half_3_times.export("/path/to/new/file.mp3", format="mp3")
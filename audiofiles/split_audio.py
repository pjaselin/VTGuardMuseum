# file to split main audio file into smaller sections
from pydub import AudioSegment
# import full audio files from archives.org
sound = AudioSegment.from_mp3("/home/pi/VTGuard/audiofiles/fdr_full.mp3")
sound.export("/home/pi/VTGuard/audiofiles/fdr_full.wav", format="wav")
# obtain and save audio segments

# interval for audio split (len() and slicing are in milliseconds)
# split length is total time/number of spluts
num_segments = 5
split_length = len(sound)/num_segments

i = 0
while i < num_segments:
    sample = sound[(split_length * i):(split_length * (i + 1))]
    save_filepath = "/home/pi/VTGuard/audiofiles/sample_" + str(i) + ".wav"
    sample.export(save_filepath, format="wav")
    i += 1

# Concatenation is just adding
#second_half_3_times = second_half + second_half + second_half

# writing mp3 files is a one liner
#second_half_3_times.export("/path/to/new/file.mp3", format="mp3")
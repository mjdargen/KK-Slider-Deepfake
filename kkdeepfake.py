# KK Slider Deepfake
#
# Michael D'Argenio
# mjdargen@gmail.com
# https://dargenio.dev
# https://github.com/mjdargen
# Created: May 26, 2020
# Revised: December 18, 2020
#
# This program uses moviepy and pydub to generate video and audio of KK
# Slider. This program works like cameo.com where you can ask a celebrity
# to record a custom message for your or your friend's special occasion.
# This program allows you to request KK Slider to record a custom message
# for any occasion.
#
# To run this code in your environment, you will need to:
#   * Install Python 3, ImageMagick, ffmpeg
#       * May have to configure moviepy with ImageMagick for your environment
#   * Install python dependencies
#       * pip install nltk
#       * pip install pydub
#       * pip install moviepy[optional]==1.0.3
#           * previous versions of moviepy cause errors in my environment

import moviepy.editor as mp
from nltk import tokenize
import wave
import contextlib
import textwrap
import subprocess
import gc
import time
import random
from pydub import AudioSegment

# main processing
def main():
    # enable garbage collection
    gc.enable()
    # prompt for script
    script = input('What would you like KK Slider to say?\n')
    # process text
    print("\n\nCreating cue cards...")
    frames = text_processing(script)
    # process video and audio
    print("\n\nRecording scenes...")
    frame_num = video_processing(frames)
    # use ffmpeg to combine video files
    print("\n\nSplicing together scenes...")
    video_concatenation(frame_num)  # mac/linux
    # video_concatenation_windows(frame_num)  # windows
    print("\n\nDone!")


##############################################
#              text processing               #
##############################################
def text_processing(script):
    # tokenize into sentences
    sentences = tokenize.sent_tokenize(script)
    # print(sentences)

    # total text, line1, line2, line3
    new_frame = ['', '', '', '']
    frames = []
    num_sentences = len(sentences)
    i = 0

    # for sentence in sentences:
    while i < num_sentences:
        remaining = ''
        # get remaining sentences
        for j in range(i, len(sentences)):
            remaining += sentences[j] + ' '
        lines = textwrap.TextWrapper(width=40).wrap(text=remaining)
        # if more than 3 lines remaining
        if len(lines) > 3:
            for j in range(0, 3):
                new_frame[0] += lines[j] + ' '
            frm_sntcs = tokenize.sent_tokenize(new_frame[0])
            # if 1st sentence larger than frame
            if len(frm_sntcs) == 1:
                # add ...
                if len(lines[2]) < 37:
                    partial = '... ' + str(sentences[i][sentences[i].find(lines[2])+len(lines[2]):])
                    sentences[i] = partial
                    lines[2] = lines[2] + '...'
                # can't fit ... so subtract word
                else:
                    words = lines[2].split()
                    remove = 0
                    j = 1
                    while remove < 3:
                        remove += len(words[len(words)-j])
                        j += 1
                    partial = '... ' + str(sentences[i][sentences[i].find(lines[2])+len(lines[2])-remove-1:])
                    sentences[i] = partial
                    lines[2] = lines[2][:-(remove+1)] + '...'
                # add lines in
                new_frame[0] = ''
                for j in range(0, 3):
                    new_frame[0] += lines[j] + ' '
            # more than one sentence
            elif len(frm_sntcs) == 2:
                new_frame[0] = ''
                for j in range(0, len(frm_sntcs) - 1):
                    new_frame[0] += frm_sntcs[j] + ' '
                i += len(frm_sntcs) - 1
            # more than two sentences
            else:
                new_frame[0] = ''
                for j in range(0, len(frm_sntcs) - 2):
                    new_frame[0] += frm_sntcs[j] + ' '
                i += len(frm_sntcs) - 2
        # if less than 3 lines remaining, just print them
        else:
            for j in range(0, len(lines)):
                new_frame[0] += lines[j] + ' '
            i = num_sentences  # to exit
        frames.append(new_frame)
        new_frame = ['', '', '', '']

    # all frames are done
    for frame in frames:
        lines = textwrap.TextWrapper(width=40).wrap(text=frame[0])
        j = 0
        while j < len(lines):
            frame[j+1] = lines[j]
            j += 1
        print(frame)

    return frames


##############################################
#              video processing              #
##############################################
def video_processing(frames):
    # max text length - 40 characters
    # max number of lines - 3 lines
    # 85 space between line
    # 1st line - 420, 724
    # 2nd line - 420, 809
    # 2nd line - 420, 894
    X_PIX = 420
    Y_PIX = 724
    LINE_SPACE = 85
    frame_num = 0

    # for every frame of text
    for frame in frames:
        # generate audio
        speak(frame[0])
        # get length of audio
        fname = './sound.wav'
        with contextlib.closing(wave.open(fname, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        # find lengths for current frame
        lengths = [0, 0, 0, 0]
        for i in range(0, 4):
            lengths[i] = len(frame[i]) + 1

        # calculate seconds per character
        SPC = duration / (lengths[1]+lengths[2]+lengths[3])
        first = True

        # initialize txt_lines
        txt_linex = (mp.TextClip(" ", fontsize=62,
                                 font='./FinkHeavy.ttf', color='white')
                     .set_position(("center"))
                     .set_duration(SPC))
        txt_line1 = (mp.TextClip(" ", fontsize=62,
                                 font='./FinkHeavy.ttf', color='white')
                     .set_position(("center"))
                     .set_duration(SPC))
        txt_line2 = (mp.TextClip(" ", fontsize=62,
                                 font='./FinkHeavy.ttf', color='white')
                     .set_position(("center"))
                     .set_duration(SPC))

        # for every line in the frame
        for i in range(1, 4):
            # write characters on a line
            # for every character on a line
            for chars in range(1, lengths[i]):
                # add the duration of writing the first couple lines
                # makes video play continuously instead of resetting after every line
                dur1 = lengths[2] if i == 2 else 0
                dur2 = lengths[3] if i == 3 else 0
                dur = dur1 + dur2
                # open talking clip and write current line of text
                talk_raw = mp.VideoFileClip("./videos/talk.mp4").subclip((chars+dur)*SPC, (chars+1+dur)*SPC)
                txt_linex = (mp.TextClip(frame[i][0:chars], fontsize=62,
                                         font='./FinkHeavy.ttf', color='white')
                             .set_position((X_PIX, Y_PIX + ((i-1) * LINE_SPACE)))
                             .set_duration(SPC))
                # line 1, don't worry about writing other lines of text
                if i == 1:
                    talk_vid = mp.CompositeVideoClip([talk_raw, txt_linex])
                # line 2, so write entire length of line 1 as well
                elif i == 2:
                    txt_line1 = (mp.TextClip(frame[i-1][0:lengths[i-1]], fontsize=62,
                                             font='./FinkHeavy.ttf', color='white')
                                 .set_position((X_PIX, Y_PIX + ((i-2) * LINE_SPACE)))
                                 .set_duration(SPC))
                    talk_vid = mp.CompositeVideoClip([talk_raw, txt_linex, txt_line1])
                # line 3, so write entire length of lines 1 & 2 as well
                elif i == 3:
                    txt_line1 = (mp.TextClip(frame[i-2][0:lengths[i-2]], fontsize=62,
                                             font='./FinkHeavy.ttf', color='white')
                                 .set_position((X_PIX, Y_PIX + ((i-3) * LINE_SPACE)))
                                 .set_duration(SPC))
                    txt_line2 = (mp.TextClip(frame[i-1][0:lengths[i-1]], fontsize=62,
                                             font='./FinkHeavy.ttf', color='white')
                                 .set_position((X_PIX, Y_PIX + ((i-2) * LINE_SPACE)))
                                 .set_duration(SPC))
                    talk_vid = mp.CompositeVideoClip([talk_raw, txt_linex, txt_line1, txt_line2])

                # concatenate clips of one frame
                talk_raw.close()
                del talk_raw
                if first:
                    first = False
                    concat_clip = talk_vid
                else:
                    clips = [concat_clip, talk_vid]
                    concat_clip = mp.concatenate_videoclips(clips)
                # talk_vid.close()  # makes it fail
                chars += 1
            print(f"Line {i} is done!")

        # add audio
        gc.collect()
        time.sleep(5)
        audio = mp.AudioFileClip("sound.wav")
        print(f"audio length {audio.duration}")
        print(f"video length {concat_clip.duration}")
        concat_clip = concat_clip.set_audio(audio)

        # concatenate pause
        pause_raw = mp.VideoFileClip("./videos/pause.mp4").subclip(1, 2)
        # add the entire text and hold for duration of pause
        txt_line1 = txt_line1.set_duration(1)
        txt_line2 = txt_line2.set_duration(1)
        txt_linex = txt_linex.set_duration(1)
        if lengths[3]:
            pause_vid = mp.CompositeVideoClip([pause_raw, txt_linex, txt_line1, txt_line2])
        elif lengths[2]:
            pause_vid = mp.CompositeVideoClip([pause_raw, txt_line1, txt_line2])
        elif lengths[1]:
            pause_vid = mp.CompositeVideoClip([pause_raw, txt_line1])

        # now concatenate the pause to final vid
        clips = [concat_clip, pause_vid]
        final_vid = mp.concatenate_videoclips(clips)
        # write out to file to save RAM
        final_vid.write_videofile(f"temp{frame_num}.mp4", audio_codec='aac')
        # help with ram issues
        # close and del all objects
        talk_vid.close()
        pause_raw.close()
        concat_clip.close()
        final_vid.close()
        pause_vid.close()
        del audio
        del txt_line1
        del txt_line2
        del txt_linex
        del clips
        del talk_vid
        del pause_raw
        del concat_clip
        del final_vid
        del pause_vid
        # call garbage collector and wait
        gc.collect()
        time.sleep(5)

        # reset variables
        first = True
        frame_num += 1

    return frame_num


##############################################
#              audio processing              #
##############################################
# source code for animalese generator from equalo-official
# modified for project. original source provided below:
# https://github.com/equalo-official/animalese-generator
def speak(stringy):

    stringy = stringy.lower()
    sounds = {}

    keys = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
            'p','q','r','s','t','u','v','w','x','y','z','th','sh',' ','.']
    for index, ltr in enumerate(keys):
        num = index + 1
        if num < 10:
            num = '0' + str(num)
        sounds[ltr] = f"./sounds/sound{num}.wav"

    rnd_factor = .35

    infiles = []

    for i, char in enumerate(stringy):
        try:
            # test for 'sh' sound
            if char == 's' and stringy[i+1] == 'h':
                infiles.append(sounds['sh'])
                continue
            # test for 'th' sound
            elif char == 't' and stringy[i+1] == 'h':
                infiles.append(sounds['th'])
                continue
            # test if previous letter was 's' or 's' and current letter is 'h'
            elif char == 'h' and (stringy[i-1] == 's' or stringy[i-1] == 't'):
                continue
            elif char == ',' or char == '?':
                infiles.append(sounds['.'])
                continue
            elif char == stringy[i-1]:  # skip repeat letters
                continue
        except:
            pass
        # skip characters that are not letters or periods.
        if not char.isalpha() and char != '.':
            continue
        infiles.append(sounds[char])

    combined_sounds = None

    # print(len(infiles))
    for index, sound in enumerate(infiles):
        tempsound = AudioSegment.from_wav(sound)
        if stringy[len(stringy)-1] == '?':
            if index >= len(infiles)*.8:
                # shift the pitch up by half an octave (speed will increase proportionally)
                octaves = random.random() * rnd_factor + (index-index*.8) * .1 + 2.1
            else:
                octaves = random.random() * rnd_factor + 2.0
        else:
            # shift the pitch up by half an octave (speed will increase proportionally)
            octaves = random.random() * rnd_factor + 2.3
            new_sample_rate = int(tempsound.frame_rate * (2.0 ** octaves))
            new_sound = tempsound._spawn(tempsound.raw_data, overrides={'frame_rate': new_sample_rate})
            new_sound = new_sound.set_frame_rate(44100)  # set uniform sample rate
            combined_sounds = new_sound if combined_sounds is None else combined_sounds + new_sound

    combined_sounds = combined_sounds.apply_gain(-11.1)
    combined_sounds.export("./sound.wav", format="wav")


###############################################
#         ffmpeg video concatentation         #
###############################################
# use ffmpeg to concatenate videos
# Windows implementation
def video_concatenation_windows(frame_num):
    subprocess.call("del list.txt", shell=True)
    subprocess.call("del output.mp4", shell=True)
    subprocess.call("(echo file './videos/beginning.mp4')>>list.txt", shell=True)
    for i in range(0, frame_num):
        subprocess.call(f"(echo file 'temp{i}.mp4')>>list.txt", shell=True)
    subprocess.call("(echo file './videos/ending.mp4')>>list.txt", shell=True)
    subprocess.call("ffmpeg -safe 0 -f concat -i list.txt -c copy output.mp4", shell=True)
    for i in range(0, frame_num):
        subprocess.call(f"del temp{i}.mp4", shell=True)
    subprocess.call("del list.txt", shell=True)
    subprocess.call("del sound.wav", shell=True)


# use ffmpeg to concatenate videos
# Mac/Linux implementation
def video_concatenation(frame_num):
    subprocess.call("rm -f list.txt", shell=True)
    subprocess.call("rm -f output.mp4", shell=True)
    subprocess.call("echo 'file './videos/beginning.mp4'' | cat >> list.txt", shell=True)
    for i in range(0, frame_num):
        subprocess.call(f"echo 'file 'temp{i}.mp4'' | cat >> list.txt", shell=True)
    subprocess.call("echo 'file './videos/ending.mp4'' | cat >> list.txt", shell=True)
    subprocess.call("ffmpeg -safe 0 -f concat -i list.txt -c copy output.mp4", shell=True)
    for i in range(0, frame_num):
        subprocess.call(f"rm -f temp{i}.mp4", shell=True)
    subprocess.call("rm -f list.txt", shell=True)
    subprocess.call("rm -f sound.wav", shell=True)


if __name__ == "__main__":
    main()

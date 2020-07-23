# source code for animalese generator from equalo-official
# modified for use in this project
# source provided in GitHub repository:
# https://github.com/equalo-official/animalese-generator

import random
from pydub import AudioSegment


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

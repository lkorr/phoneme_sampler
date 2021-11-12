import os
from allosaurus.app import read_recognizer
from mido import Message, MidiFile, MidiTrack, second2tick
import time
starttime = time.time()
phone_to_midi_dict = {}
eng_phone_list = ['a', 'aː','ɐː', 'ɑ', 'ɑː', 'o', 'oː', 'i', 'iː', 'ɐ', 'u', 'uː', 'æ', 'e', 'eː', 'e̞', 'ɘ', 'ə', 'əː', 'ɛ', 'ɛː', 'ɜː', 'ɒ', 'ɒː',
                  'n', 'p', 'pʰ', 'r', 's', 't', 'tʰ', 't̠', 'v', 'w', 'x', 'z', 'd', 'b', 'd̠','f', 'h', 'j', 'k', 'kʰ', 'l', 'm',
                  'ð', 'øː', 'ŋ', 'ɔ', 'ɔː', 'ɡ', 'ɪ', 'ɪ̯', 'ɯ', 'ɵː', 'ɹ', 'ɻ', 'ʃ', 'ʉ', 'ʉː', 'ʊ', 'ʌ', 'ʍ', 'ʒ', 'ʔ', 'θ']

for i, v in enumerate(eng_phone_list):
    phone_to_midi_dict[v] = i
path = os.getcwd()
filelist = []
for root, dirs, files in os.walk(path):
    for file in files:
        if (file.endswith(".wav")):
            sample = file.split('\\')[0]
            print(sample)
            filelist.append(sample)

print(filelist)

def vocals_to_midi(sample, emission):
    phonemes = []
    times = [0]
    model = read_recognizer()
    token = (model.recognize(sample, timestamp=True, lang_id = 'eng', emit= emission))
    token = token.split('\n')
    for i in range(len(token)):
        phonemes += [token[i].split(' ')[2]]
        times +=  [float(token[i].split(' ')[0])]
    print(set(phonemes)- set(times))
    print(len(phonemes))
    print(phonemes)
    print(times)
    mid = MidiFile(type=0)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('note_on', note=10,
                             velocity=64,
                             time= 0))

    track.append(Message('note_off', note=10,
                             velocity=64,
                             time= 100))
    for i in range(len(phonemes)):
        track.append(Message('note_on', note=36 + phone_to_midi_dict[phonemes[i]],
                             velocity=64,
                             time= int(second2tick((times[i+1]), ticks_per_beat= 1, tempo= 800)) -
                                  int(second2tick((times[i]), ticks_per_beat= 1, tempo= 800))))
        track.append(Message('note_off', note=36 + phone_to_midi_dict[phonemes[i]], velocity=127, time=100))
    name = sample.split('.wav')[0]
    mid.save(name + '(' + str(emission) + ')' + '.mid')


for sample in filelist:
    for emission in [1.0, 1.25, 1.5]:
        vocals_to_midi(sample, emission)
print(time.time() - starttime)
import os
from allosaurus.app import read_recognizer
from mido import Message, MidiFile, MidiTrack, second2tick
import librosa
import time
import random
starttime = time.time()
phone_to_midi_dict = {}
eng_phone_list = ['a', 'aː','ɐː', 'ɑ', 'ɑː', 'o', 'oː', 'i', 'iː', 'ɐ', 'u', 'uː', 'æ', 'e', 'eː', 'e̞', 'ɘ', 'ə', 'əː', 'ɛ', 'ɛː', 'ɜː', 'ɒ', 'ɒː',
                  'n', 'p', 'pʰ', 'r', 's', 't', 'tʰ', 't̠', 'v', 'w', 'x', 'z', 'd', 'b', 'd̠','f', 'h', 'j', 'k', 'kʰ', 'l', 'm',
                  'ð', 'øː', 'ŋ', 'ɔ', 'ɔː', 'ɡ', 'ɪ', 'ɪ̯', 'ɯ', 'ɵː', 'ɹ', 'ɻ', 'ʃ', 'ʉ', 'ʉː', 'ʊ', 'ʌ', 'ʍ', 'ʒ', 'ʔ', 'θ']

for i, v in enumerate(eng_phone_list):
    phone_to_midi_dict[v] = i
phone_to_midi_dict['<blk>'] = -20
path = os.getcwd()
filelist = []
for root, dirs, files in os.walk(path):
    for file in files:
        if (file.endswith(".wav")):
            sample = file.split('\\')[0]
            print(sample)
            filelist.append(sample)

print(filelist)

def vocals_to_midi(sample, emission, topk, exponent, episodes):
    tempo = 10000
    tpb = 1
    phonemes = []
    times = [0]
    model = read_recognizer()
    token = (model.recognize(sample, timestamp=True, lang_id = 'eng', emit= emission, topk=topk))
    token = token.split('\n')
    all_prob_tokens = []
    for i in token:
        prob_tokens = []
        normalizer = 0
        for j in i.split(') '):
            if len((j.split(' ('))[0]) > 10:
                prob_tokens += [(([((j.split(' ('))[0]).split(' ')[-1], float((j.split(' ('))[1])/(1-normalizer)]))]
            else:
                prob_tokens += [(([(j.split(' ('))[0], float((j.split(' ('))[1].split(')')[0])/(1-normalizer)]))]

        all_prob_tokens += [(prob_tokens)]

    for i in range(len(token)):
        phonemes += [token[i].split(' ')[2]]
        times +=  [float(token[i].split(' ')[0])]

    for episode in range(episodes):
        for i in range(len((all_prob_tokens))):
            epsilon = random.random()**exponent
            threshold = all_prob_tokens[i][-1][1]
            for j in all_prob_tokens[i][::-1]:
                if epsilon < threshold:
                    # if phonemes[i-1] != j[0]:
                    #     print('changing ' + str(phonemes[i]) + ' to ' + str(j[0]))
                    phonemes[i] = j[0]
                    break
                else:
                    threshold += j[1]
        print(phonemes)
        # print(times)
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
                                 time= int(second2tick((times[i+1]), ticks_per_beat= tpb, tempo= tempo)) -
                                      int(second2tick((times[i]), ticks_per_beat= tpb, tempo= tempo))))
            track.append(Message('note_off', note=36 + phone_to_midi_dict[phonemes[i]], velocity=127, time=100))
        # signal the end of sample
        track.append(Message('note_on', note=10,
                             velocity=64,
                             time=int(second2tick((librosa.get_duration(filename=sample)), ticks_per_beat=tpb, tempo=tempo)) -
                     int(second2tick((times[-1]), ticks_per_beat= tpb, tempo= tempo))))

        track.append(Message('note_off', note=10,
                             velocity=64,
                             time=100))
        name = sample.split('.wav')[0]
        print()
        mid.save(name + '(' + str(emission) + ')' + '(' + str(episode) + ')' + '.mid')


for sample in filelist:
    for emission in [0.8]:
        vocals_to_midi(sample, emission, topk = 5, exponent = 2, episodes = 3)
print(time.time() - starttime)

# phoneme_sampler
WIP python program that converts recorded speech into midi, by mapping spoken phonemes into discrete midi notes to be used in a sampler.

1. Put samples in .wav format in the same folder as the .py file
2. Run the program, it will output 3 midi files for each .wav sample in the folder, each with a different emission rate. 1.0 is the default emission rate, but depending on the source material, the 1.25 and 1.5 emission rate midi files will map more accurately. 
3. A note at c0 will be appended at the beginning of the midi message and at the end, which serve as timestamps for the beginning and end of the sample. Warp and stretch the midi file to sync with the .wav sample in the DAW
4. Each phoneme is mapped starting at c1. Vowel sounds are mapped from c1 to c3, and consonants are mapped from c3 and above. This is configured to be used within ableton, as using a sampler on 'slice' mode will begin slicing and mapping midi notes to sliced samples starting at c1. 

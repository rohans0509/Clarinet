# Clarinet

## About Clarinet

A MIDI based approach for music recognition is proposed and implemented in this paper. Our Clarinet music retrieval system is designed to search piano MIDI files with high recall and speed. We design a novel melody extraction algorithm that improves recall results by more than 10%. We also implement 3 algorithms for retrieval-two self designed (RSA Note and RSA Time), and a modified version of the Mongeau Sankoff Algorithm. Algorithms to achieve tempo and scale invariance are also discussed in this paper. The paper also contains detailed experimentation and benchmarks with four different metrics. Clarinet achieves recall scores of more than 94%.

Link to the final report containing the results and explanations of algorithms: [Clarinet_TGKFC.pdf](./Reports/Clarinet_TGKFC.pdf)

## Directory Layout

```go
 CLARINET
   +--- Clarinet 
        +--- converter
            +--- audio2midi.py // convert audio to midi
            +--- midi2audio.py // convert midi to audio
        +--- discarded // contains discarded files
        +--- evaluation // contains evaluation files
            +--- __init__.py // contains the script for running the evaluations
            +--- getScores.py // contains the various metric functions
        +--- melodyextraction // contains melody extraction scripts
            +--- __init__.py // contains the script for running the melody extraction
            +--- skyline.py // skyline algorithm
            +--- modified_skyline.py // modified skyline algorithm
        +--- preprocessing 
            +--- __init__.py // contains the script for running the preprocessing
            +--- clipper.py // used for clipping the audio
            +--- getBPM.py // gets beats per minute from audio
            +--- transpose.py // transposes the audio to C
        +--- search 
            +--- similarity_time.py // RSA time algorithm
            +--- similarity_text.py // RSA note algorithm 
            +--- similarity_sankoff.py // Sankoff algorithm
        +--- utils
            +--- clipFolder.py // clips the audio files in a folder 
            +--- extractMelodyFolder // extracts the melody from the audio files in a folder
            +--- extractNotes.py // extracts the notes from the midi files in a folder and stores in JSON file
            +--- preprocessFolder.py // preprocesses the audio files in a folder
        +--- visualiser // contains the visualiser scripts
            +--- __init__.py // contains the script for running the visualiser
            +--- Visualiser.py // visualises the results
   +--- Data  // contains all the data for the project
   |
   +--- Results // contains all the results obtained and the relevant scripts for generating the results
   |
   +--- Reports // contains the reports submitted for COL764
   +--- Papers // contains some of the key papers used during the project
   +--- README // basic information
```

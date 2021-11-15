from omnizart.music import app as music
from omnizart.chord import app as chord
from omnizart.drum import app as drum
from omnizart.vocal import app as vocal
from omnizart.vocal_contour import app as vocal_contour
from omnizart.beat import app as beat

from pydub import AudioSegment

import scipy.io.wavfile as wave

from mido import MidiFile
from skyline import skyline
from Visualiser import Visualiser

from midi2audio import FluidSynth


class AudioProcessor:
    def __init__(self) -> None:
        self.app = {
            "music": music,
            "chord": chord,
            "drum": drum,
            "vocal": vocal,
            "vocal-contour": vocal_contour,
            "beat": beat
        }

        self.model = {
            "piano": "Piano",
            "piano-v2": "PianoV2",
            "assemble": "Stream",
            "pop-song": "Pop",
            "": None
        }
        self.fs = FluidSynth()

    def convertToWave(self, file: str):
        filename, ext = tuple(file.split("."))
        if ext == "wav":
            return True
        elif ext == "mp3":
            out = f"{filename}.wav"
            sound = AudioSegment.from_mp3(file)
            sound.export(out, format="wav")
            return True
        else:
            print("Only mp3 and Wav files supported")
            return False

    def transcribe(self, file, mode, output_dir="Midi"):
        converted = self.convertToWave(file)

        if not converted:
            print("Can not convert given file")
            return

        filename, ext = tuple(file.split("."))
        file = f"{filename}.wav"

        model = ""
        if mode.startswith("music"):
            mode_list = mode.split("-")
            mode = mode_list[0]
            model = "-".join(mode_list[1:])

        app = self.app[mode]
        model = self.model[model]

        app.transcribe(file, model_path=model, output=output_dir)
        return(f"{output_dir}/{file.split('/')[-1].split('.')[0]}.mid")

    def toWav(self, file, output_dir="Wav"):
        out = f"{output_dir}/{file.split('/')[-1].split('.')[0]}.wav"
        self.fs.midi_to_audio(file, out)

    def extractMelody(self, filename, output_dir="./Midi"):
        mid_out = skyline(filename)
        mid_out.dump(f"{output_dir}/{filename.split('/')[-1].split('.')[0]}_melody.mid")
        return(f"{output_dir}/{filename.split('/')[-1].split('.')[0]}_melody.mid")

    def visualise(self, file, output_dir="Images"):
        visualiser = Visualiser(file)
        # get the np array of piano roll image
        roll = visualiser.get_roll()
        visualiser.draw_roll(filename=f"{output_dir}/{file.split('/')[-1].split('.')[0]}.png")

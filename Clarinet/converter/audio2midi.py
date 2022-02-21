from omnizart.music import app as music
from omnizart.chord import app as chord
from omnizart.drum import app as drum
from omnizart.vocal import app as vocal
from omnizart.vocal_contour import app as vocal_contour
from omnizart.beat import app as beat
from pydub import AudioSegment

APP = {
    "music": music,
    "chord": chord,
    "drum": drum,
    "vocal": vocal,
    "vocal-contour": vocal_contour,
    "beat": beat
}

MODEL = {
    "piano": "Piano",
    "piano-v2": "PianoV2",
    "assemble": "Stream",
    "pop-song": "Pop",
    "": None
}


def convertToWave(file: str):
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

def audio2midi(file, mode, output_dir="Data/Midi"):
    converted = convertToWave(file)

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

    app = APP[mode]
    model = MODEL[model]

    folder_name,filename=file.split('/')[-2],file.split('/')[-1].split('.')[0]

    output_dir=f"{output_dir}/{folder_name}"
    app.transcribe(file, model_path=model, output=output_dir)

    
    return(f"{output_dir}/{filename}.mid")
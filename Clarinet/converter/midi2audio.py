from midi2audio import FluidSynth
fs = FluidSynth()

def midi2audio(file, output_dir="Data/Audio"):
    folder_name,filename=file.split('/')[-2],file.split('/')[-1].split('.')[0]

    output_dir=f"{output_dir}/{folder_name}"

    out=f"{output_dir}/{filename}_converted.wav"

    fs.midi_to_audio(file, out)

    return(out)
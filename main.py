from AudioProcessor import AudioProcessor

ap=AudioProcessor()
filename="Data/test.wav"
mode="music-piano-v2"
output_dir="Midi"

ap.transcribe(file=filename,mode=mode,output_dir=output_dir)
import os
import music21
def getKey(midi_filename):
    score = music21.converter.parse(midi_filename)
    key = score.analyze('key')
    return(key.tonic.name)



majors = dict([("A-", 4),("A", 3),("B-", 2),("B", 1),("C", 0),("D-", -1),("D", -2),("E-", -3),("E", -4),("F", -5),("G-", 6),("G", 5)])
minors = dict([("A-", 1),("A", 0),("B-", -1),("B", -2),("C", -3),("D-", -4),("D", -5),("E-", 6),("E", 5),("F", 4),("G-", 3),("G", 2)])


def transpose(file,output_dir="Data/Midi"):
    score = music21.converter.parse(file)
    key = score.analyze('key')

    if key.mode == "major":
        halfSteps = majors[key.tonic.name]
        
    elif key.mode == "minor":
        halfSteps = minors[key.tonic.name]

    folder_name,filename=file.split('/')[-2],file.split('/')[-1].split('.')[0]

    output_dir=f"{output_dir}/{folder_name}_processed"

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    out=f"{output_dir}/{filename}.mid"

    newscore = score.transpose(halfSteps)
    key = newscore.analyze('key')

    newscore.write('midi',out)

    return(out)
            
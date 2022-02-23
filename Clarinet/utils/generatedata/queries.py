import miditoolkit
import os
import random
from tqdm import tqdm
random.seed(42)
import os
import shutil
import glob
import datetime
import itertools
from Clarinet.usermodel import User
from Clarinet.converter import midi2text

def genQuery(fname_or_mido_Obj,num_notes=-1,channel=0):
    try:
        filename=fname_or_mido_Obj
        mido_obj= miditoolkit.midi.parser.MidiFile(filename)
    except:
        mido_obj=fname_or_mido_Obj
    
    notes = mido_obj.instruments[channel].notes
    if num_notes==-1:
        num_notes=len(notes)
    notes = [note for note in notes if note.start < note.end]
    notes = sorted(notes,key=lambda note: note.start)
    query_notes = []
    if len(notes) > num_notes:
        idx = random.randint(0,len(notes)-num_notes-1)
        query_notes = notes[idx:idx+num_notes]

        delta = query_notes[0].start
        for note in query_notes:
            note.start -= delta
            note.end -= delta

        query_notes = sorted(query_notes,key=lambda note: note.end)
        
        new_mido_obj = miditoolkit.midi.parser.MidiFile()
        new_mido_obj.ticks_per_beat = mido_obj.ticks_per_beat
        new_mido_obj.instruments.append(miditoolkit.midi.parser.Instrument(0))
        new_mido_obj.instruments[channel].notes = query_notes
        return True, new_mido_obj
    else:
        return False, mido_obj

def genMidiQueries(collection_dir,type,output_folder,delete_data=True,num_notes=-1,num_queries=-1,*args,**kwargs):
    # Delete or Move Files
    if delete_data:
        # Delete all folders in output_folder
        for folder in glob.glob(f"{output_folder}/*"):
            shutil.rmtree(folder)
        # Delete all files in output_folder
        for file in glob.glob(f"{output_folder}/*"):
            os.remove(file)
    else:
        date=str(datetime.date.today())
        time=str(datetime.datetime.now())
        date_time=date+"_"+time
        discarded_folder=f"Data/Discarded/Midi/Queries/{type} Queries/{date_time}"
        # Move all folders and files in output_folder to discarded_folder
        for file in glob.glob(f"{output_folder}/*"):
            shutil.move(file,discarded_folder)

    keys=list(kwargs.keys())
    values=list(kwargs.values())
    product=list(itertools.product(*values))

    # convert 2 lists to dictionary
    for tup in tqdm(product):
        args=[]
        kwargs={keys[i]:tup[i] for i in range(len(keys))}
        name_list=[f"{key.capitalize()} {value}" for key,value in kwargs.items()]
        output_dir=f"{output_folder}/{'/'.join(name_list)}"

        useFolder(collection_dir,output_dir,type,num_notes=num_notes,num_queries=num_queries,*args,**kwargs)


def genTextQueries(collection_dir,type,output_folder,delete_data=True,num_notes=-1,num_queries=-1,*args,**kwargs):
    text_output_folder=output_folder.replace("Midi","Text")
    # Delete or Move Files
    if delete_data:
        for folder in glob.glob(f"{output_folder}/*"):
            try:
                shutil.rmtree(folder)
            except NotADirectoryError:
                os.remove(folder)
        for folder in glob.glob(f"{text_output_folder}/*"):
            try:
                shutil.rmtree(folder)
            except NotADirectoryError:
                os.remove(folder)
    else:
        date=str(datetime.date.today())
        time=str(datetime.datetime.now())
        date_time=date+"_"+time
        discarded_folder=f"Data/Discarded/Midi/Queries/{type} Queries/{date_time}"
        # Move all folders and files in output_folder to discarded_folder
        for file in glob.glob(f"{output_folder}/*"):
            shutil.move(file,discarded_folder)

    keys=list(kwargs.keys())
    values=list(kwargs.values())
    product=list(itertools.product(*values))

    # convert 2 lists to dictionary
    for tup in tqdm(product):
        args=[]
        kwargs={keys[i]:tup[i] for i in range(len(keys))}
        name_list=[f"{key.capitalize()} {value}" for key,value in kwargs.items()]
        output_dir=f"{output_folder}/{'/'.join(name_list)}"

        useFolder(collection_dir,output_dir,type,num_notes=num_notes,num_queries=num_queries,text=True,*args,**kwargs)



def getAvgLen(input):
    total_len = 0
    num_files = 0
    for fname in tqdm(os.listdir(input)):
        if fname.endswith(".mid"):
            mido_obj = miditoolkit.midi.parser.MidiFile(os.path.join(input,fname))
            notes = mido_obj.instruments[0].notes
            notes = [note for note in notes if note.start < note.end]
            total_len += len(notes)
            num_files += 1
    return total_len/num_files

def useFolder(collection_dir,output_folder,type="Noisy",num_queries=-1,num_notes=-1,text=False,*args,**kwargs):
    text_output_folder=output_folder.replace("Midi","Text")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(text_output_folder):
        os.makedirs(text_output_folder)
    # get all files in input folder ending with ".mid"
    mido_files = [fname for fname in os.listdir(collection_dir) if fname.endswith(".mid")]

    if num_queries==-1:
        num_queries=len(mido_files)
    
    files = random.sample(mido_files,num_queries)

    for fname in tqdm(files):
        user=User(type)
        mido_in=user.use(midi_file=f"{collection_dir}/{fname}",output_folder=output_folder,save=False,*args,**kwargs)
                 
        flag, mido_obj = genQuery(mido_in,num_notes,channel=kwargs["channel"])
        
        if flag:
            output_filename=os.path.join(output_folder,fname)
            mido_obj.dump(output_filename)
            if text:
                out=midi2text(mido_obj,channel=kwargs["channel"],num_notes=num_notes)
                text_output_filename=output_filename.replace("Midi","Text").replace(".mid",".txt")
                with open(text_output_filename,"w") as f:
                    f.write(out)
                
        else:
            print(f"{fname} is too short")
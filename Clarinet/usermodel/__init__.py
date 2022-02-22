from Clarinet.usermodel import NoisyUser,IdealUser
import os
from Clarinet.constants import midi_folder


models={
    "Noisy":NoisyUser,
    "Ideal":IdealUser
}

class User:
    def __init__(self,type):
        self.type = type
        self.model = models[type]


    def use(self,midi_file,output_folder="",save=True,*args,**kwargs):
        mido_obj=self.model.use(midi_file,*args,**kwargs)

        if save:

            if output_folder=="":
                folder_name=f"{self.type} {midi_file.split('/')[-2]}"
                output_folder=f"{midi_folder}/{folder_name}" # Data/Midi/Noisy Queries for input Data/Midi/Queries/1.mid
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
                
            fname = midi_file.split('/')[-1]
            path = os.path.join(output_folder,fname)
            self.dump(mido_obj,path)
        
        return mido_obj

    def dump(self,mido_obj,output_file=""):
        if output_file=="":
            print("No output file specified")
            return
        
        mido_obj.dump(output_file)
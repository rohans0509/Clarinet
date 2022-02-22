import miditoolkit
import numpy as np
import random
random.seed(seed)
from constants import random_seed_noisyuser as seed
import os



'''
==============
NOISYUSER CLASS
==============
'''
class NoisyUser:
    def __init__(self,origName, mido_obj,melody_channel=0):
        self.mido_obj = mido_obj
        self.origName = origName
        self.melody_channel = melody_channel

    def addNoiseToChannel(self,channel,pitch,extra,deleted,velocity,length):
        self.addVelocityNoise(channel,velocity)
        self.addLengthNoise(channel,length)
        self.addPitchNoise(channel,pitch)
        self.addExtraNotes(channel,extra)
        self.deleteNotes(channel,deleted)
    

    def addNoiseToFull(self,pitch,extra,deleted,velocity,length):
        instruments=self.mido_obj.instruments
        for channel in range(len(instruments)):
            notes=instruments[channel].notes
            if len(notes)>0:
                self.addNoiseToChannel(channel,pitch,extra,deleted,velocity,length)

    def addVelocityNoise(self,channel,contamination,noise_perc=0.2):
        notes=self.mido_obj.instruments[channel].notes
        length = len(notes)
        idx = random.sample(range(0,length),int(length*contamination))
        for i in idx:
            vel = notes[i].velocity
            max_del_v = int(vel*noise_perc)
            del_v = random.randint(-max_del_v,max_del_v+1)
            self.mido_obj.instruments[channel].notes[i].velocity = min(vel+del_v,127)

    def addPitchNoise(self,channel,contamination,del_change=8):
        notes=self.mido_obj.instruments[channel].notes
        length = len(notes)
        idx = random.sample(range(0,length),int(length*contamination))
        for i in idx:
            pitch = notes[i].pitch
            change = random.randint(-del_change,del_change+1)
            self.mido_obj.instruments[channel].notes[i].pitch = min(pitch+change,127)

    def addExtraNotes(self,channel,contamination,thresh=0.2):
        if channel == self.melody_channel:
            extra_notes = []
            notes=self.mido_obj.instruments[channel].notes
            for i in range(1,len(notes)):
                if random.random() < contamination:
                    try:
                        prev_start =notes[i-1].start
                        prev_end = notes[i-1].end
                        cur_start = notes[i].start
                        cur_end = notes[i].end

                        prev_len = prev_end - prev_start
                        cur_len = cur_end - cur_start

                        if cur_start - prev_end > 0:
                            avg_len = int((prev_len + cur_len)/2)
                            del_len = random.randint(-int(avg_len*thresh),int(avg_len*thresh))
                            new_len = avg_len + del_len

                            if (prev_end + new_len) < cur_start:
                                length = new_len
                            else:
                                length = random.randint(0,cur_start-prev_end)
                            
                            if length == 0:
                                continue

                            start = prev_end
                            end = prev_end + length
                            prev_pitch = notes[i-1].pitch
                            cur_pitch = notes[i].pitch
                            pitch = random.randint(min(prev_pitch,cur_pitch),max(prev_pitch,cur_pitch))
                            prev_vel = notes[i-1].velocity
                            cur_vel = notes[i].velocity
                            vel = random.randint(min(prev_vel,cur_vel),max(prev_vel,cur_vel))
                            if self.check_validity(vel,pitch,start,end):
                                extra_notes.append(miditoolkit.Note(vel,pitch,start,end))
                    except:
                        pass
            extra_notes = extra_notes[1:]
            self.mido_obj.instruments[channel].notes.extend(extra_notes)
            self.mido_obj.instruments[channel].notes.sort(key=lambda x: x.end)
        else:
            notes=self.mido_obj.instruments[channel].notes
            extra_notes = []
            for i in range(1,len(notes) -1):
                if random.random() < contamination:
                    try:
                        cur_start = notes[i].start
                        cur_end = notes[i].end
                        origLength = cur_end-cur_start
                        noiseDisp = int(origLength*thresh)
                        startnoise = random.randint(-noiseDisp,noiseDisp)
                        endnoise = random.randint(-noiseDisp,noiseDisp)
                        starttime = max(0,cur_start+startnoise)
                        endtime = cur_start+endnoise
                        prev_pitch = notes[i-1].pitch
                        cur_pitch = notes[i].pitch
                        next_pitch = notes[i+1].pitch
                        pitch = random.randint(min(prev_pitch,cur_pitch,next_pitch),max(prev_pitch,cur_pitch,next_pitch))
                        prev_vel = notes[i-1].velocity
                        cur_vel = notes[i].velocity
                        next_vel = notes[i+1].velocity
                        vel = random.randint(min(prev_vel,cur_vel,next_vel),max(prev_vel,cur_vel,next_vel))
                        if self.check_validity(vel,pitch,starttime,endtime):
                            extra_notes.append(miditoolkit.Note(vel,pitch,starttime,endtime))
                    except:
                        pass
            extra_notes = extra_notes[1:]
            self.mido_obj.instruments[channel].notes.extend(extra_notes)
            self.mido_obj.instruments[channel].notes.sort(key=lambda x: x.end)

    def deleteNotes(self,channel,contamination=0.05):
        notes=self.mido_obj.instruments[channel].notes
        new_notes = []
        for i in range(len(notes)):
            if random.random() > contamination:
                new_notes.append(notes[i])
        self.mido_obj.instruments[channel].notes = new_notes
                
    def addLengthNoise(self,channel,contamination,thresh=0.1):
        if channel != self.melody_channel:
            notes=self.mido_obj.instruments[channel].notes
            for i in range(len(self.mido_obj.instruments[channel].notes)):
                if random.random() < contamination:
                    start = notes[i].start
                    end = notes[i].end
                    length = int((end-start)*thresh)
                    startnoise = random.randint(-length,length)
                    endnoise = random.randint(-length,length)
                    self.mido_obj.instruments[channel].notes[i].start = max(0,start+startnoise)
                    self.mido_obj.instruments[channel].notes[i].end = end+endnoise
        else:
            notes=self.mido_obj.instruments[channel].notes
            for i in range(1,len(notes)):
                if random.random() < contamination:
                    prev_start = notes[i-1].start
                    prev_end = notes[i-1].end
                    cur_start = notes[i].start
                    cur_end = notes[i].end

                    prev_len = prev_end-prev_start
                    cur_len = cur_end-cur_start

                    end_noise = random.randint(0,int(prev_len * thresh))
                    start_noise = random.randint(0,int(cur_len * thresh))

                    prev_end_new = prev_end - end_noise
                    cur_start_new = cur_start + start_noise

                    self.mido_obj.instruments[channel].notes[i-1].end = max(0,prev_end_new)
                    self.mido_obj.instruments[channel].notes[i].start = max(0,cur_start_new)

    def dumpNoiseMIDI(self,fname,folder,pitch_contamination,extra_contamination,delete_contamination):
        self.addNoiseToMelody(pitch_contamination,extra_contamination,delete_contamination)
        fname = fname.split('/')[-1]
        path = os.path.join(folder,fname.replace(".mid","_noise.mid"))
        self.mido_obj.dump(path)
        
    def check_validity(self,vel,pitch,start,end):
        if vel<=0 or vel>=127:
            return False
        if pitch<=0 or pitch>=127:
            return False
        if start<=0 or start>=end:
            return False
        return True

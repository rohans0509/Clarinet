import miditoolkit
import numpy as np
import random

class NoiseModule:
    def __init__(self, mido_obj,melody_channel=0):
        self.mido_obj = mido_obj
        self.melody_channel = melody_channel

    def addNoiseToMelody(self):
        # TODO : decide what all noise to add
        pass

    def addNoiseToFull(self):
        # TODO : decide what all noise to add
        self.addVelocityNoise(0,0.3)
        self.addLengthNoise(0,0.3)
        self.addPitchNoise(2,0.3)
        self.addExtraNotes(0,0.2)
        self.addExtraNotes(1,0.2)

    def addVelocityNoise(self,channel,contamination,noise_perc=0.2):
        """
        Add noise to velocity of notes
        :param channel: channel to add noise to
        :param contamination: percentage of notes to add noise to
        :param noise_perc: max noise calculated as percentage of velocity
        """
        length = len(self.mido_obj.instruments[channel].notes)
        idx = random.sample(range(0,length),int(length*contamination))
        for i in idx:
            vel = self.mido_obj.instruments[channel].notes[i].velocity
            max_del_v = int(vel*noise_perc)
            del_v = random.randint(-max_del_v,max_del_v+1)
            self.mido_obj.instruments[channel].notes[i].velocity = min(vel+del_v,127)

    def addPitchNoise(self,channel,contamination,del_change=8):
        """
        Add noise to pitch of notes
        :param channel: channel to add noise to
        :param contamination: percentage of notes to add noise to
        :param del_change: max delta change in pitch
        """
        length = len(self.mido_obj.instruments[channel].notes)
        idx = random.sample(range(0,length),int(length*contamination))
        for i in idx:
            pitch = self.mido_obj.instruments[channel].notes[i].pitch
            change = random.randint(-del_change,del_change+1)
            self.mido_obj.instruments[channel].notes[i].pitch = min(pitch+change,127)

    def addExtraNotes(self,channel,contamination,thresh=0.2):
        """
        Add extra notes noise to the channel
        :param channel: channel to add noise to
        :param contamination: percentage of notes to add noise between
        :param thresh: percentage of length of notes to add noise between
        """
        if channel == self.melody_channel:
            extra_notes = []
            for i in range(1,len(self.mido_obj.instruments[channel].notes)):
                if random.random() < contamination:
                    try:
                        prev_end = self.mido_obj.instruments[channel].notes[i-1].end
                        cur_start = self.mido_obj.instruments[channel].notes[i].start
                        length = int((cur_start-prev_end)*thresh)
                        startnoise = random.randint(0,length)
                        endnoise = random.randint(0,length)
                        starttime = prev_end+startnoise
                        endtime = cur_start-endnoise
                        prev_pitch = self.mido_obj.instruments[channel].notes[i-1].pitch
                        cur_pitch = self.mido_obj.instruments[channel].notes[i].pitch
                        pitch = random.randint(min(prev_pitch,cur_pitch),max(prev_pitch,cur_pitch))
                        #pitch = min(68,pitch)
                        prev_vel = self.mido_obj.instruments[channel].notes[i-1].velocity
                        cur_vel = self.mido_obj.instruments[channel].notes[i].velocity
                        vel = random.randint(min(prev_vel,cur_vel),max(prev_vel,cur_vel))
                        #vel = min(120,vel)
                        extra_notes.append(miditoolkit.Note(vel,pitch,starttime,endtime))
                    except:
                        pass
            extra_notes = extra_notes[1:]
            self.mido_obj.instruments[channel].notes.extend(extra_notes)
            self.mido_obj.instruments[channel].notes.sort(key=lambda x: x.start)
        else:
            extra_notes = []
            for i in range(1,len(self.mido_obj.instruments[channel].notes) -1):
                if random.random() < contamination:
                    try:
                        cur_start = self.mido_obj.instruments[channel].notes[i].start
                        cur_end = self.mido_obj.instruments[channel].notes[i].end
                        origLength = cur_end-cur_start
                        noiseDisp = int(origLength*thresh)
                        startnoise = random.randint(-noiseDisp,noiseDisp)
                        endnoise = random.randint(-noiseDisp,noiseDisp)
                        starttime = max(0,cur_start+startnoise)
                        endtime = cur_start+endnoise
                        prev_pitch = self.mido_obj.instruments[channel].notes[i-1].pitch
                        cur_pitch = self.mido_obj.instruments[channel].notes[i].pitch
                        next_pitch = self.mido_obj.instruments[channel].notes[i+1].pitch
                        pitch = random.randint(min(prev_pitch,cur_pitch,next_pitch),max(prev_pitch,cur_pitch,next_pitch))
                        #pitch = min(68,pitch)
                        prev_vel = self.mido_obj.instruments[channel].notes[i-1].velocity
                        cur_vel = self.mido_obj.instruments[channel].notes[i].velocity
                        next_vel = self.mido_obj.instruments[channel].notes[i+1].velocity
                        vel = random.randint(min(prev_vel,cur_vel,next_vel),max(prev_vel,cur_vel,next_vel))
                        #vel = min(120,vel)
                        extra_notes.append(miditoolkit.Note(vel,pitch,starttime,endtime))
                    except:
                        pass
            extra_notes = extra_notes[1:]
            self.mido_obj.instruments[channel].notes.extend(extra_notes)
            self.mido_obj.instruments[channel].notes.sort(key=lambda x: x.end)

    def deleteNotesNoise(self,channel,contamination=0.05):
        """
        Add delete-notes noise on the channel
        :param channel: channel to add noise to
        :param contamination: percentage of notes to delete for noise
        """
        new_notes = []
        for i in range(len(self.mido_obj.instruments[channel].notes)):
            if random.random() > contamination:
                new_notes.append(self.mido_obj.instruments[channel].notes[i])
        self.mido_obj.instruments[channel].notes = new_notes
                
    def addLengthNoise(self,channel,contamination,thresh=0.1):
        """
        Add length noise to notes
        :param channel: channel to add noise to
        :param contamination: percentage of notes to add noise to
        :param thresh: max noise = thresh * (length of note)
        """
        if channel != self.melody_channel:
            for i in range(len(self.mido_obj.instruments[channel].notes)):
                if random.random() < contamination:
                    start = self.mido_obj.instruments[channel].notes[i].start
                    end = self.mido_obj.instruments[channel].notes[i].end
                    length = int((end-start)*thresh)
                    startnoise = random.randint(-length,length)
                    endnoise = random.randint(-length,length)
                    self.mido_obj.instruments[channel].notes[i].start = start+startnoise
                    self.mido_obj.instruments[channel].notes[i].end = end+endnoise
        else:
            for i in range(1,len(self.mido_obj.instruments[channel].notes)):
                if random.random() < contamination:
                    prev_start = self.mido_obj.instruments[channel].notes[i-1].start
                    prev_end = self.mido_obj.instruments[channel].notes[i-1].end
                    cur_start = self.mido_obj.instruments[channel].notes[i].start
                    cur_end = self.mido_obj.instruments[channel].notes[i].end
                    length = int((cur_start-prev_end)*thresh)
                    startnoise = random.randint(-length,length)
                    endnoise = random.randint(-length,length)
                    self.mido_obj.instruments[channel].notes[i].start = max(prev_end+startnoise,prev_start)
                    self.mido_obj.instruments[channel].notes[i].end = min(cur_start+endnoise,cur_end)

    def dumpNoiseMIDI(self,fname):
        """
        Dump the MIDI object with noise to a file
        :param fname: file name to dump to
        """
        self.mido_obj.dump(fname)



if __name__ == "__main__":
    fname = "POP909_001_001.mid"
    mido_obj = miditoolkit.midi.parser.MidiFile(fname)
    noise = NoiseModule(mido_obj)
    noise.addNoiseToFull()
    output = noise.mido_obj
    output_fname = fname.replace(".mid","_noise.mid")
    output.dump(output_fname)

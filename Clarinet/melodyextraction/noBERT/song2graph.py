from Clarinet.melodyextraction.noBERT.quantize import quantize
import miditoolkit
import numpy as np

def process_midiFile(midi_file):
    mid_in=miditoolkit.midi.parser.MidiFile(midi_file)    
    notes = []
    for i in range(len(mid_in.instruments)):
        notes.extend(mid_in.instruments[i].notes)
    notes.sort(key=lambda x: x.start)
    return notes

class Node:
    def __init__(self,pitch,velocity,weight_list,layer_idx,parent_idx):
        self.pitch = pitch
        self.velocity = velocity
        self.weight_list = weight_list
        self.layer_idx = layer_idx
        self.parent_idx = parent_idx

class Graph:
    def __init__(self, midi_file,weight_matrix):
        self.midi_file = midi_file
        self.box_list = quantize(process_midiFile(midi_file),planck=1)
        #self.box_list = [(-1,-1)] + self.box_list + [(-1,-1)]
        self.weight_matrix = weight_matrix
        self.layers = [[] for i in range(len(self.box_list))]
        # each layer will contain [ [(pitch,velocity,[list of weights corresponding next layer])], ... ]
    
    def create_graph(self):
        for i in range(0,len(self.box_list)-1):
            box1 = self.box_list[i]
            box2 = self.box_list[i+1]
            for note1 in box1:
                weight_list = []
                for note2 in box2:
                    weight_list.append(self.get_weights(note1,note2))
                #self.layers[i].append([note1, weight_list])
                pitch = note1[0]
                velocity = note1[1]
                self.layers[i].append(Node(pitch=pitch,velocity=velocity,weight_list=weight_list,layer_idx=i,parent_idx=-1))

    def get_weights(self,note1,note2):
        p1 = note1[0]
        p2 = note2[0]
        return self.weight_matrix[p1][p2]

    def shortestPath(self):
        shortestpathsdist = []
        for i in range(len(self.layers)):
            shortestpathsdist.append(np.zeros((len(self.layers[i]))))
        shortestpathsdist[0][0] = 0
        for i in range(1,len(self.layers)-1):
            for j in range(len(self.layers[i])):
                for k in range(len(self.layers[i-1])):
                    newdist = shortestpathsdist[i-1][k] + self.weight_matrix[self.layers[i-1][k].pitch][self.layers[i][j].pitch]
                    if newdist < shortestpathsdist[i][j]:
                        shortestpathsdist[i][j] = newdist
                        self.layers[i][j].parent_idx = k
        return self.getPath()
    
    def getPath(self):
        path = []
        # [TODO] fix this last empty box 
        path.append(self.layers[-2][0])
        for i in range(len(self.layers)-3,0,-1):
            parent = path[-1].parent_idx
            path.append(self.layers[i][parent])
        path.reverse()
        notes = []
        for i in range(len(path)):
            notes.append(path[i].pitch)
        return notes
    
    def melody(self):
        pitches=self.shortestPath()
        melody=[]
        for i in range(len(pitches)):
            if len(melody)==0:
                melody.append(pitches[i])
            else:
                if pitches[i]!=melody[-1]:
                    melody.append(pitches[i])
        return(melody)
                    

def song2graph(midi_file,weight_matrix):
    g=Graph(midi_file,weight_matrix)
    g.createGraph()
    return g
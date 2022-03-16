from Clarinet.melodyextraction.noBERT.quantize import quantize
import miditoolkit
import numpy as np

class Graph:
    def __init__(self, midi_file,weight_matrix):
        self.midi_file = midi_file
        self.box_list = self.createBoxList()
        self.weight_matrix = weight_matrix
        self.layers = [[] for i in range(len(self.box_list))]
        # each layer will contain [ [(pitch,velocity,[list of weights corresponding next layer])], ... ]
    
    def createBoxList(self):
        mid_in=miditoolkit.midi.parser.MidiFile(self.midi_file)    
        notes = []
        for i in range(len(mid_in.instruments)):
            notes.extend(mid_in.instruments[i].notes)
        notes.sort(key=lambda x: x.start)
        return(quantize(notes))

    def createGraph(self):
        for i in range(len(self.box_list)-1):
            box1 = self.box_list[i]
            box2 = self.box_list[i+1]
            for note1 in box1:
                weight_list = []
                for note2 in box2:
                    weight_list.append(self.weight(note1,note2))
                self.layers[i].append([note1, weight_list])
    
    def weight(self,note1,note2):
        p1 = note1[0]
        p2 = note2[0]
        return self.weight_matrix[p1][p2]

    def shortestPath(self):
        '''
        input   -> layers information (nD array of numberoflayer,...)
                    layers number of neurons per layer
                -> dist (3D array of layer,start,end)
                    dist (layer idx, neuron in idx^th layer, neuron in idx+1^th layer)
                -> neurons (1D array of number of neurons in each layer)

        '''
        # neurons=[]
        # for i in range(len(self.layers)):
        #     neurons.append(len(self.layers[i]))
        # dist=np.zeros((len(self.layers),neurons[0],neurons[-1]))

        layers = []
        for i in range(len(self.layers)):
            layers.append(len(self.layers[i]))
        
        neurons = []
        for i in range(len(layers)):
            num_neurons = layers[i]
            neurons.append(np.arange(num_neurons))

        maxnum_neurons = max(layers)
        dist = np.zeros((len(layers),maxnum_neurons,maxnum_neurons))

        for i in range(len(layers)-1):
            for j in range(layers[i]):
                for k in range(layers[i+1]):
                    dist[i][j][k] = self.weight_matrix[self.layers[i][j][0][0]][self.layers[i+1][k][0][0]]

        shortestpaths = []
        shortestpathsdist = []
        for i in range(self.layers):
            shortestpaths.append(np.zeros(neurons[i],i))
            shortestpathsdist.append(np.zeros(neurons[i]))
        for i in range(self.layers):
            for j,neuron in enumerate(neurons[i]):
                if i == 0:
                    shortestpaths[i,j]
                    shortestpathsdist[i,j] 
                else:
                    dummy = [shortestpathsdist[i-1, k] + dist[i-1, k, j] for k in self.layers[i-1]]
                    shortestpathsdist[i,j] = np.min(dummy)
                    prevstate = np.argmin(dummy)
                    shortestpaths[i,j] = shortestpaths[i-1,prevstate].copy().append(j)
        return shortestpaths

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
def planck(notes):
    return 1

def quantize(notes, rest=True):
    planck=planck(notes)
    start = notes[0].start

    for note in notes:
        note.start = note.start - start
        note.end = note.end - start
    
    notes.sort(key=lambda x: x.end)
    end = notes[-1].end
    notes.sort(key=lambda x: x.start)

    quantized_notes = []
    for i in range(int(end/planck)):
        quantized_notes.append([])
    
    for note in notes:
        cur_start = note.start
        cur_end = note.end
        first_idx = int(cur_start/planck)
        last_idx = int(cur_end/planck)
        pitch = note.pitch
        vel = note.velocity
        for i in range(first_idx, last_idx):
            quantized_notes[i].append((pitch,vel))
            
    if rest:
        for i in range(len(quantized_notes)):
            quantized_notes[i].append((-1,-1))
    else:
        for i in range(len(quantized_notes)):
            if len(quantized_notes[i]) == 0:
                quantized_notes[i].append((-1,-1))
    return quantized_notes
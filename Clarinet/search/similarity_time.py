factor = 768


def edit_distance(s1, s2):
    m = len(s1)
    n = len(s2)
    dp = [[0 for x in range(n+1)] for x in range(m+1)]
    for i in range(m+1):
        for j in range(n+1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])
    return dp[m][n]


# a function which calculates the similarity between two strings
def similarity(s1, s2):
    return 1 - edit_distance(s1, s2) / max(len(s1), len(s2))


midiEt_to_note = {
    12: "C",
    13: "C#",
    14: "D",
    15: "D#",
    16: "E",
    17: "F",
    18: "F#",
    19: "G",
    20: "G#",
    21: "A",
    22: "A#",
    23: "B"
}


# a function which converts a sequence of midiEt to a sequence of notes
def midiEt_to_note_sequence(midiEt_sequence):
    note_sequence = []
    for midiEt in midiEt_sequence:
        num = midiEt % 12
        note_sequence.append(midiEt_to_note[num + 12])
    return "".join(note_sequence)


def splitNotes(notes):
    new_notes = []
    for note in notes:
        start = note[1]/factor
        end = note[2]/factor
        startSec = int(start)
        endSec = int(end)

        if startSec == endSec:
            new_notes.append(note)
        else:
            new_notes.append([note[0], note[1], (startSec+1)*factor, note[3]])
            for i in range(startSec+1, endSec-1):
                new_notes.append([note[0], int(i*factor), int(i+1)*factor, note[3]])
            new_notes.append([note[0], int(endSec*factor), note[2], note[3]])
    return new_notes


def getStrides(notes, size):
    notes = sorted(notes, key=lambda x: x[1])
    chunks = []
    for _ in range(len(notes)+factor):
        chunks.append([])

    curT = 0
    nextidx = 0
    flag = False

    i = 0
    while(i < len(notes)):
        st = notes[i][1]
        maxT = curT + size
        if st >= maxT:
            curT += factor
            i = nextidx
            flag = False
            continue

        if st % factor == 0 and flag == False and st != curT:
            nextidx = i
            flag = True

        pos = int(curT/factor)
        chunks[pos].append(notes[i])
        i += 1
    ans = []
    for c in chunks:
        if len(c) > 0:
            ans.append(c)
    return ans

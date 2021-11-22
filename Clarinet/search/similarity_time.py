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

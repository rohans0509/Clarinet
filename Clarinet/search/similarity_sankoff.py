
import math
from math import inf
from tqdm import tqdm


class Note:
    def __init__(self, note, duration, rest=False, scale="major"):
        self.note = note
        self.pitch = NOTE_PITCH[note]
        self.rest = rest
        self.duration = duration
        self.scale = scale

    def __eq__(self, obj: object) -> bool:
        return isinstance(obj, Note) and obj.duration == self.duration and obj.pitch == self.pitch and obj.rest == self.rest


# Constants from original paper:
K1 = 0.348

# weights for intervals out of scale
TON = {
    0: 0.6,
    1: 2.6,
    2: 2.3,
    3: 1,
    4: 1,
    5: 1.6,
    6: 1.8,
    7: 0.8,
    8: 1.3,
    9: 1.3,
    10: 2.2,
    11: 2.5
}

MINOR_DEG = {
    "C": 1,
    "D": 2,
    "D#": 3,
    "F": 4,
    "G": 5,
    "G#": 6,
    "A#": 7
}

MAJOR_DEG = {
    "C": 1,
    "D": 2,
    "E": 3,
    "F": 4,
    "G": 5,
    "A": 6,
    "B": 7
}

DEG_DIFF = {
    0: 0,
    1: 0.9,
    2: 0.2,
    3: 0.5,
    4: 0.1,
    5: 0.35,
    6: 0.8
}

REST = 0.1

MU = 2

D = 0.6

F = 0

C = 0

NOTE_PITCH = {
    "C": 12,
    "C#": 13,
    "D": 14,
    "D#": 15,
    "E": 16,
    "F": 17,
    "F#": 18,
    "G": 19,
    "G#": 20,
    "A": 21,
    "A#": 22,
    "B": 23
}


# Insertion Weight
def w_ins(note):
    return K1 * note.duration

# Deletion Weight


def w_del(note):
    return K1 * note.duration

# Substitution Weight


def w_sub(note_a, note_b):
    return w_interval(note_a, note_b) + K1 * w_len(note_a.duration, note_b.duration)

# Fragmentation weight


def w_frag(dp, a, b, i, j):
    min_weight = math.inf

    for new_notes in range(2, min(j-1, F)+1):
        k = new_notes

        weight = dp[i-1][j-k]
        durations = 0

        while k > 0:
            weight += w_interval(a[i-1], b[j-k])
            durations += b[j-k].duration
            k -= 1

        weight += K1 * w_len(a[i-1].duration, durations)

        if weight < min_weight:
            min_weight = weight

    return min_weight

# Consolidation Weight


def w_cons(dp, a, b, i, j):
    min_weight = math.inf

    for x in range(2, min(i-1, C)+1):

        k = x

        weight = dp[i-k][j-1]
        durations = 0

        while k > 0:
            weight += w_interval(a[i-k], b[j-1])
            durations += a[i-k].duration
            k -= 1

        weight += K1 * w_len(durations, b[j-1].duration)

        if min_weight > weight:
            min_weight = weight

    return min_weight


# Interval Weight
def w_interval(note_a, note_b):
    if note_a.rest or note_b.rest:
        if note_a.rest and note_b.rest:
            return DEG_DIFF[0]
        return REST
    # If same scale find degree difference
    if note_a.scale == note_b.scale:
        if note_a.scale == "major":
            try:
                degree_a = MAJOR_DEG[note_a.note]
                degree_b = MAJOR_DEG[note_b.note]
                return DEG_DIFF[abs(degree_a - degree_b)]
            except:
                return TON[abs(note_a.pitch - note_b.pitch)]
        elif note_a.scale == "minor":
            try:
                degree_a = MINOR_DEG[note_a.note]
                degree_b = MINOR_DEG[note_b.note]
                return DEG_DIFF[abs(degree_a - degree_b)]
            except:
                return TON[abs(note_a.pitch - note_b.pitch)]

    else:
        # If different scales return absolute difference
        return TON[abs(note_a.pitch - note_b.pitch)]


# Duration Weight
def w_len(duration_a, duration_b):
    return abs(duration_a - duration_b)


def distance(s1, s2):
    global C, F
    m = len(s1)
    n = len(s2)

    if m == 0 or n == 0:
        return 0

    # Set C and F
    max_duration_s1 = max(s1, key=lambda note: note.duration).duration
    min_duration_s2 = min(s2, key=lambda note: note.duration).duration

    F = int(max_duration_s1 / min_duration_s2)

    max_duration_s2 = max(s2, key=lambda note: note.duration).duration
    min_duration_s1 = min(s1, key=lambda note: note.duration).duration

    C = int(max_duration_s2 / min_duration_s1)

    dp = [[0 for i in range(n+1)] for j in range(m+1)]

    # Initial Conditions
    for i in range(1, len(s1)+1):
        dp[i][0] = dp[i-1][0] + w_del(s1[i-1])

    for j in range(1, len(s2)+1):
        dp[0][j] = dp[0][j-1]+w_ins(s2[j-1])

    for i in range(m+1):
        note_a = s1[i-1]
        for j in range(n+1):
            note_b = s2[j-1]

            if note_a == note_b:
                dp[i][j] = dp[i-1][j-1]
                continue

            substitution = dp[i-1][j-1] + w_sub(note_a, note_b)
            deletion = dp[i-1][j] + w_del(note_a)
            insertion = dp[i][j-1] + w_ins(note_b)
            consolidation = w_cons(dp, s1, s2, i, j)
            fragmentation = w_frag(dp, s1, s2, i, j)

            dp[i][j] = min(deletion, insertion, substitution, fragmentation, consolidation)

    return dp[m][n]


def similarity(query: list, data: list):
    query_len = len(query)
    data_len = len(data)

    s1 = query

    score = float("inf")

    start = -1
    end = -1
    pbar = tqdm(total=int(data_len/query_len) + 1)

    while end < data_len:
        start = start+1
        end = min(start+query_len, data_len)

        s2 = data[start:end]

        edit_distance = distance(s1, s2)
        if edit_distance < score:
            score = edit_distance
        pbar.update(1)

    sim = 1-score/query_len
    return(sim)

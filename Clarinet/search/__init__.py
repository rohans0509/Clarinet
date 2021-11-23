from similarity_sankoff import similarity as similarity_sankoff
from similarity_text import similarity as similarity_text
from similarity_time import similarity as similarity_time

SIM_DICT={
    "sankoff":similarity_sankoff,
    "text":similarity_text,
    "time":similarity_time
}

def similarity(query,data,similarity_type="text"):
    sim_method=SIM_DICT[similarity_type]
    return(sim_method(query,data))

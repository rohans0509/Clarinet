from Clarinet.search.similarity import similarity_sankoff,similarity_text,similarity_time

SIM_DICT = {
    "sankoff": similarity_sankoff,
    "text": similarity_text,
    "time": similarity_time
}


def similarity(query, data, similarity_type="text",stride_length=0):
    sim_method = SIM_DICT[similarity_type]
    return(sim_method(query, data,stride_length))

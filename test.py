from Clarinet.converter import remi2midi
input_file="Adele_remi.npy"
predicted_file="Adele_predicted.npy"
dictionary_file="remi.pkl"
output_file=""
remi2midi(input_file,predicted_file,dictionary_file,output_file=output_file)
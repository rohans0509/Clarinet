# Set Pitch, Extra, Deleted range here and In misc.ipynb. 
# Run test.py first then Run first box in misc.ipynb. 
# Second box is for plotting which works but the graphs aren't great


from Clarinet.utils.convert import remi2midi
input_file="Adele_remi.npy"
predicted_file="Adele_predicted.npy"
dictionary_file="remi.pkl"
output_file=""
remi2midi(input_file,predicted_file,dictionary_file,output_file=output_file)

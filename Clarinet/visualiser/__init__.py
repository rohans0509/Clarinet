import os
from .Visualiser import Visualiser
def visualise(file, output_dir="Data/Images"):
    visualiser = Visualiser(file)
    # get the np array of piano roll image
    roll = visualiser.get_roll()

    folder_name,filename=file.split('/')[-2],file.split('/')[-1].split('.')[0]

    output_dir=f"{output_dir}/{folder_name}"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    out=f"{output_dir}/{filename}.png"
    visualiser.draw_roll(filename=f"{output_dir}/{file.split('/')[-1].split('.')[0]}.png")

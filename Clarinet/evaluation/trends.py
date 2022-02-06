import matplotlib.pyplot as plt
import pandas as pd
import os

def trends(file,x):
    plt.figure()
    output_dir="/".join(file.split("/")[:-2])+"/Plots"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    y=f"{file.split('/')[-1].split('.')[0]}"


    df=pd.read_csv(file)

    plt.plot(df[x],df[y],color='red')
    plt.xlabel(x)
    plt.ylabel(y)
    
    plt.title(f"{y} vs {x}",fontsize=12,fontweight='bold')
    plt.xticks(range(int(min(df[x])-1),int(max(df[x]))+2))

    plt.savefig(f"{output_dir}/{y} vs {x}.png")
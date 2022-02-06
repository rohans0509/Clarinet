import matplotlib.pyplot as plt
import pandas as pd
import os

def trends(file,x):
    try:
        plt.figure()
        output_dir="/".join(file.split("/")[:-2])+"/Plots"

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        y=f"{file.split('/')[-1].split('.')[0]}"


        df=pd.read_csv(file)
        # sort df by x
        df=df.sort_values(by=x)

        plt.plot(df[x],df[y],color="red")
        plt.xlabel(x)
        plt.ylabel(y)
        
        query_type=f"{file.split('Analysis/')[-1].split('/CSV')[0].replace('Queries','').replace('Expected','').replace(' ','')}"

        plt.title(f"{y} ({query_type})",fontsize=12,fontweight='bold')
        # plt.xticks(range(int(min(df[x])-1),int(max(df[x]))+2))

        plt.savefig(f"{output_dir}/{y} vs {x}.png",dpi=120)
    except:
        print(f"{file} failed")
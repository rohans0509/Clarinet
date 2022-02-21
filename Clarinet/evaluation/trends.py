import matplotlib.pyplot as plt
import pandas as pd
import os

def trends(file,x,type="plot"):
    try:
        plt.figure()
        output_dir="/".join(file.split("/")[:-2])+"/Plots"

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        y=f"{file.split('/')[-1].split('.')[0]}"


        df=pd.read_csv(file)
        # sort df by x
        df=df.sort_values(by=x)
        if type=="plot":
            plt.plot(df[x],df[y],color="red")
        elif type=="scatter":
            plt.scatter(df[x],df[y],color="red")
        else:
            print("Invalid type")
            return
        plt.xlabel(x)
        plt.ylabel(y)
        
       
        plt.title(f"{y} vs {x}",fontsize=12,fontweight='bold')
        # plt.xticks(range(int(min(df[x])-1),int(max(df[x]))+2))

        plt.savefig(f"{output_dir}/{y} vs {x}.png",dpi=120)
    except:
        print(f"{file} failed")
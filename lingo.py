import random
random.seed(121)

out=[[random.random() for i in range(5)] for i in range(10)] 
j=0
for points in out:
    if j<5:
        y=1
    else:
        y=-1 
    string=""
    for i in range(len(points)):
        val=i+1
        string+=(f"w{val}*{points[i]}+")
    out=f'{y}*({string}b)+q{j+1}>=1;'
    print(out)
    j+=1
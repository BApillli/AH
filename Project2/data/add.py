newf=""
with open('cuisines.csv','r') as f:
    for line in f:
        newf+="{id:"+line.strip()+"}\n"
    f.close()
with open('cuisines.csv','w') as f:
    f.write(newf)
    f.close()

import csv
  
  
def cl(): 
    t=[]
    m=0
    file_name = "jum.csv"
    with open(file_name) as file:
        csv_reader_object = csv.reader(file)
        i=0
        for line in csv_reader_object:
            if (i!=0):
                line[1]=float(line[1])
                m=m+line[1]
                t.append(line)
            i+=1 
    m=m/len(t)
    f=[]
    for a in t:
        if (a[1]<1.3*m and a[1]>0.7*m):
            f.append(a)
    f=sorted(f,key=(lambda x:x[1]))
    return f[:10]
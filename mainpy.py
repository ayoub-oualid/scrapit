import eel
import jumia
import amaz
import os
import csv
from threading import *

eel.init('web')
class App1(Thread):
    def f(self, a):
        amaz.main(a)
class App2(Thread):
    def f(self, a):
        jumia.main(a)
app1=App1()
app2=App2()

@eel.expose
def scrap(vars):
    t1 = Thread(target=app1.f, args=(vars,))
    t1.start()
    t2 = Thread(target=app2.f, args=(vars,))
    t2.start()
    t1.join()
    t2.join()
@eel.expose
def dispjum():
    i=0
    tr=""
    for line in cl():
        des = line[0]
        price = line [1]
        ln= line [2]
        img = line[3] 
        tr += '<tr scope="row">'                
        tr += '<td><img src="%s" class="img"></td>' % img
        tr += "<td>%s</td>" % des               
        tr += '<td>$%s</td>' % price  
        tr += '<td><a href="%s" target="_blank" class="more">Link</a></td>' % ln          
        tr += "</tr>"
        i=i+1
    return tr
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
    file_name2 = "ama.csv"
    with open(file_name2) as file:
        csv_reader_object = csv.reader(file)
        k=0
        for line2 in csv_reader_object:
            if (k!=0 and line2[1] not in t):
                line2[1]=line2[1]
                line2[1]=float(line2[1])
                line2[3]=str(line2[3]).strip()
                m=m+line2[1]
                t.append(line2)
            k+=1 
    m=m/len(t)
    f=[]
    for a in t:
        if (a[1]<1.3*m and a[1]>m):
            f.append(a)
    f=sorted(f,key=(lambda x:x[1]))
    return f[:5]
@eel.expose
def dispjum_old():
    tr=""
    file_name = "jum.csv"
    with open(file_name) as file:
        csv_reader_object = csv.reader(file)
        i=0
        for line in csv_reader_object:
            if (i!=0): 
                des = line[0]
                price = line [1]
                ln= line [2]
                img= line [3]
                tr += "<tr>"                
                tr += '<td><img src=%s></td>' % img
                tr += "<td>%s</td>" % des               
                tr += "<td class='dollars'>%s</td>" % str(price)
                tr += '<td><a href="%s" target="_blank" class="more">Link</a></td>' % ln          
                tr += "</tr>"
            i+=1  
    return tr
#print(dispjum())
eel.start('main.html', mode='chrome-app', port=8080, cmdline_args=['--start-fullscreen', '--browser-startup-dialog'])
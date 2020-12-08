import random
import os

def random_sequence(r):
    sequence=[]

    for epoch in range(r):
        while True:
            x=random.randint(0,r-1)
            if x not in sequence:
                sequence.append(x)
                break

    return sequence

def suffle(filedir = "static/assets/img/number"):
   l=os.listdir(filedir)
   seq=random_sequence(len(l))

   for i in range(len(l)):
       x=l[i].split('.')
       oldname=filedir+'/'+l[i]
       newname=filedir+'/'+x[0]+'xxx'+'.'+x[1]
       os.rename(oldname,newname)

   for i in range(len(l)):
       x=l[i].split('.')
       oldname=filedir+'/'+x[0]+'xxx'+'.'+x[1]
       newname="static/assets/img"+'/'+l[seq[i]]
       os.rename(oldname,newname)

   return seq



## example  
#  function suffle() could randomly suffle all the fils' names in a given dir
suffle()


    

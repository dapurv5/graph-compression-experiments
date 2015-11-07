#!/usr/bin/env/python
#

def readGraphDIMACS(filePath):
  fp = open(filePath,"r")
  firstLine = fp.readline().split()
  nv = int(firstLine[0])
  ne = int(firstLine[1])
  nv+=1
  ne*=2
  off=[None]*(nv+1)
  ind=[None]*(ne)

  off[0]=0
  off[1]=0    
  v=1
  e=0
  for line in fp:
    vAdj=line.split();
    for u in vAdj:
      ind[e]=int(u)
      e+=1;

    off[v+1]=off[v]+len(vAdj)
    v+=1
  fp.close()
  return nv,ne,ind,off;
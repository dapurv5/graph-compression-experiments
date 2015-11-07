#!/usr/bin/env/python
#

import math
import matplotlib.pyplot as plt

NUM_BITS_FOR_SIGN_BIT = 1
SIZE_ELEM = 8

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

def get_consec_diff(u, adjacency):
  consec_diff = [None] * len(adjacency)
  consec_diff[0] = adjacency[0] - u
  for i in range(1,len(adjacency)):
    consec_diff[i] = adjacency[i] - adjacency[i-1]
  return consec_diff

def count_no_chunks(u, adjacency):
  """Given the vertex u and its adjacency"""
  consec_diff = get_consec_diff(u, adjacency)
  num_bits = 0
  if consec_diff[0] < 0:
    consec_diff[0] *= -1.0

  greatest_elem = max(consec_diff)
  num_bits = math.ceil(math.log(greatest_elem, 2))
  return num_bits * len(adjacency) + SIZE_ELEM + NUM_BITS_FOR_SIGN_BIT #extra sign bit for first vertex


def count_fixed_chunks(u, adjacency, t):
  """Given vertex u and its adjacency and a chunk size t"""
  consec_diff = get_consec_diff(u, adjacency)
  bits = 0
  begin = 0
  while begin < len(adjacency):
    finish = min(len(adjacency), begin+t)
    chunk = adjacency[begin: finish]
    begin += t
    bits += count_no_chunks(u, chunk)    
  return bits


def count_steepest_jump_chunks(u, adjacency, jump):
  """Given vertex u and its adjacency and a jump"""  
  bits = 0
  j = 1
  consec_diff_chunk = [adjacency[0] - u]
  
  if consec_diff_chunk[0] < 0:
    consec_diff_chunk[0] *= -1.0
  
  while j < len(adjacency):
    max_in_chunk = max(consec_diff_chunk)
    num_bits = math.ceil(math.log(max_in_chunk, 2)) + 1
    
    #Bits required before adding this element
    bits_before_adding = num_bits * len(consec_diff_chunk)
    
    new_max_in_chunk = max(max_in_chunk, adjacency[j]-adjacency[j-1])
    new_num_bits = math.ceil(math.log(new_max_in_chunk, 2)) + 1
    
    #Bits required after adding this element
    bits_after_adding = new_num_bits * (len(consec_diff_chunk)+1)
    
    if (bits_after_adding - bits_before_adding) < jump:
      consec_diff_chunk.append(adjacency[j]-adjacency[j-1])
    else:
      bits += 16 + SIZE_ELEM + NUM_BITS_FOR_SIGN_BIT #number of elements in the chunk + #bits required to encode each value in the chunk + sign bit
      greatest_elem = max(consec_diff_chunk)
      num_bits = max(1, math.ceil(math.log(greatest_elem, 2)))
      bits += num_bits * len(consec_diff_chunk)
      
      consec_diff_chunk = [adjacency[j] - u]
      if consec_diff_chunk[0] < 0:
        consec_diff_chunk[0] *= -1.0
    j += 1
  
  if len(consec_diff_chunk) > 0:
    greatest_elem = max(consec_diff_chunk)
    num_bits = max(1, math.ceil(math.log(greatest_elem, 2)))
    bits = bits + 16 + SIZE_ELEM + NUM_BITS_FOR_SIGN_BIT
    bits = bits + num_bits * len(consec_diff_chunk)
    consec_diff_chunk = []
  return bits


def plot_steepest_jump_chunks_over_no_chunks(ind, off):
  J = []
  CR = []
  
  total_no_chunks = 0
  for i in range(1, len(off)-1):
    adjacency = ind[off[i] : off[i+1]]
    total_no_chunks += count_no_chunks(i, adjacency)

  for j in range(10,300,10):
    total_steepest_jump_chunks = 0
    sum_adjacency = 0
    max_adjacency = 0
    for i in range(1,len(off)-1):
      adjacency = ind[off[i] : off[i+1]]
      adjacency.sort()
      sum_adjacency += len(adjacency)
      max_adjacency = max(max_adjacency, len(adjacency))
      total_steepest_jump_chunks += count_steepest_jump_chunks(i, adjacency, j)
    J.append(j)
    CR.append(total_no_chunks/total_steepest_jump_chunks)

  print J
  print CR
  print "Avg length of adjacency = ", sum_adjacency/(len(off)-1)
  print "Max length of adjacency = ", max_adjacency
  
  plt.plot(J, CR)
  plt.ylabel('compression ratio')
  plt.xlabel('jump size in bits')
  plt.show()
  

def plot_fixed_chunks_over_no_chunks(ind, off):
  T = []
  CR = []

  total_no_chunks = 0
  for i in range(1, len(off)-1):
    adjacency = ind[off[i] : off[i+1]]
    total_no_chunks += count_no_chunks(i, adjacency)

  for t in range(2,80,4):
    total_fixed_chunks = 0
    sum_adjacency = 0
    max_adjacency = 0
    for i in range(1,len(off)-1):
      adjacency = ind[off[i] : off[i+1]]
      adjacency.sort()
      sum_adjacency += len(adjacency)
      max_adjacency = max(max_adjacency, len(adjacency))
      total_fixed_chunks += count_fixed_chunks(i, adjacency, t)
    T.append(t)
    CR.append(total_no_chunks/total_fixed_chunks)

  print T
  print CR
  print "Avg length of adjacency = ", sum_adjacency/(len(off)-1)
  print "Max length of adjacency = ", max_adjacency
  
  plt.plot(T, CR)
  plt.ylabel('compression ratio')
  plt.xlabel('size of chunk')
  plt.show()
  
  
def main():
  #path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/cnr-2000.graph"
  #path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/audikw1.graph"
  path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/citationCiteseer.graph"
  #path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/preferentialAttachment.graph"
  #path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/smallworld.graph"
  num_vertices, num_edges, ind, off = readGraphDIMACS(path)
  #plot_fixed_chunks_over_no_chunks(ind, off)
  #plot_steepest_jump_chunks_over_no_chunks(ind, off)
  count_no_chunks(2704, [116164, 135733, 148114, 185431, 242311])
  print "howdie"

if __name__ == "__main__":
  main()

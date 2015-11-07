#!/usr/bin/env/python
#

import math
import matplotlib.pyplot as plt
import graph_readers as reader

from math import log
from math import ceil

NUM_BITS_FOR_SIGN_BIT = 1
SIZE_ELEM = 8
NUM_BITS_FOR_BITS_TO_ENCODE = 8

def plot(X, Y, xlabel, ylabel):
  plt.plot(X, Y)
  plt.ylabel(ylabel)
  plt.xlabel(xlabel)
  plt.show()

def get_consec_diff(u, adjacency):
  consec_diff = [None] * len(adjacency)
  consec_diff[0] = adjacency[0] - u
  for i in range(1,len(adjacency)):
    consec_diff[i] = adjacency[i] - adjacency[i-1]
  return consec_diff

def count_no_chunks(u, adjacency):
  """Given the vertex u and its adjacency,
     counts the number of bits required to encode the adjacency list
     in a differential encoding scheme. (no chunks)
  """
  consec_diff = get_consec_diff(u, adjacency)
  num_bits_to_encode = 0
  #take_incorrect_bits = False
  if consec_diff[0] < 0:
    #take_incorrect_bits = False
    consec_diff[0] *= -1.0

  greatest_elem = max(consec_diff)
  num_bits_to_encode = ceil(log(greatest_elem, 2))
  num_bits_to_encode = max(1, num_bits_to_encode)
  
  #if take_incorrect_bits:
  #  num_bits_to_encode -= 1
    
  #write down the sign bit
  #write down the num of bits req. to encode each value, call this e
  #Write e bits, len(adjacency) number of times
  return num_bits_to_encode * len(adjacency) + NUM_BITS_FOR_BITS_TO_ENCODE + NUM_BITS_FOR_SIGN_BIT


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


def count_variable_chunks(u, adjacency, jump):
  """Given vertex u and its adjacency and a jump"""  
  bits = 0
  j = 1
  consec_diff_chunk = [adjacency[0] - u]
  
  if consec_diff_chunk[0] < 0:
    consec_diff_chunk[0] *= -1.0
  greatest_elem = max(consec_diff_chunk)
  
  while j < len(adjacency):
    num_bits_to_encode = ceil(log(greatest_elem, 2))
    num_bits_to_encode = max(1, num_bits_to_encode)
    
    #Bits required before adding this element
    bits_before_adding = num_bits_to_encode * len(consec_diff_chunk)
    
    new_greatest_elem = max(greatest_elem, adjacency[j]-adjacency[j-1])
    new_num_bits_to_encode = ceil(log(new_greatest_elem, 2))
    new_num_bits_to_encode = max(1, new_num_bits_to_encode)
    
    #Bits required after adding this element
    bits_after_adding = new_num_bits_to_encode * (len(consec_diff_chunk)+1)
    
    if (bits_after_adding - bits_before_adding) < jump:
      diff = adjacency[j]-adjacency[j-1]
      consec_diff_chunk.append(diff)
      greatest_elem = max(greatest_elem, diff)
    else:
      #number of elements in the chunk + #bits required to encode each value in the chunk + sign bit
      bits = bits + 16 + NUM_BITS_FOR_BITS_TO_ENCODE + NUM_BITS_FOR_SIGN_BIT
      greatest_elem = max(consec_diff_chunk)
      num_bits_to_encode = ceil(log(greatest_elem, 2))
      num_bits_to_encode = max(1, num_bits_to_encode)
      bits += num_bits_to_encode * len(consec_diff_chunk)
      
      consec_diff_chunk = [adjacency[j] - u]
      if consec_diff_chunk[0] < 0:
        consec_diff_chunk[0] *= -1.0
      greatest_elem = consec_diff_chunk[0]
    j += 1
  
  if len(consec_diff_chunk) > 0:
    greatest_elem = max(consec_diff_chunk)
    num_bits_to_encode = max(1, ceil(log(greatest_elem, 2)))
    bits = bits + 16 + NUM_BITS_FOR_BITS_TO_ENCODE + NUM_BITS_FOR_SIGN_BIT
    bits = bits + num_bits_to_encode * len(consec_diff_chunk)
    consec_diff_chunk = []
  return bits


def plot_variable_chunks_over_no_chunks(ind, off):
  j_min = 10
  j_max = 100
  j_step = 10
  
  J = [] #jump sizes
  CR = [] #compression ratios
  sum_adjacency = 0
  max_adjacency = 0  
  total_no_chunks = 0
  for i in range(1, len(off)-1):
    adjacency = ind[off[i] : off[i+1]]
    adjacency.sort()
    total_no_chunks += count_no_chunks(i, adjacency)
    sum_adjacency += len(adjacency)
    max_adjacency = max(max_adjacency, len(adjacency))

  for j in range(j_min,j_max,j_step):
    total_variable_chunks = 0
    for i in range(1,len(off)-1):
      adjacency = ind[off[i] : off[i+1]]
      adjacency.sort()
      total_variable_chunks += count_variable_chunks(i, adjacency, j)
    J.append(j)
    CR.append(total_no_chunks/total_variable_chunks)

  print J
  print CR
  print "Avg length of adjacency = ", sum_adjacency/(len(off)-1)
  print "Max length of adjacency = ", max_adjacency  
  plot(J, CR, 'jump size in bits', 'compression ratio')
  

def plot_fixed_chunks_over_no_chunks(ind, off):  
  t_min = 10
  t_max = 200
  t_step = 10
  
  T = [] #chunk sizes
  CR = [] #compression ratios
  sum_adjacency = 0
  max_adjacency = 0
  total_no_chunks = 0
  for i in range(1, len(off)-1):
    adjacency = ind[off[i] : off[i+1]]
    adjacency.sort()
    total_no_chunks += count_no_chunks(i, adjacency)
    sum_adjacency += len(adjacency)
    max_adjacency = max(max_adjacency, len(adjacency))

  for t in range(t_min,t_max,t_step):
    total_fixed_chunks = 0
    for i in range(1,len(off)-1):
      adjacency = ind[off[i] : off[i+1]]
      adjacency.sort()
      total_fixed_chunks += count_fixed_chunks(i, adjacency, t)
    T.append(t)
    CR.append(total_no_chunks/total_fixed_chunks)

  print T
  print CR
  print "Avg length of adjacency = ", sum_adjacency/(len(off)-1)
  print "Max length of adjacency = ", max_adjacency
  plot(T, CR, 'size of chunk', 'compression ratio')


def main():
  #path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/cnr-2000.graph"
  path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/audikw1.graph"
  #path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/citationCiteseer.graph"
  #path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/preferentialAttachment.graph"
  #path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/smallworld.graph"
  num_vertices, num_edges, ind, off = reader.readGraphDIMACS(path)
  #plot_fixed_chunks_over_no_chunks(ind, off)
  plot_variable_chunks_over_no_chunks(ind, off)

if __name__ == "__main__":
  main()

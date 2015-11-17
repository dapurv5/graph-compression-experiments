#!/usr/bin/env/python
#

import csv
import subprocess
import matplotlib.pyplot as plt
from pylab import *


graph_dir="/home/dapurv5/Desktop/Semesters/1st_semester/GRA"
plots_dir="/home/dapurv5/MyCode/gatech-projects/graph-compression-experiments/plots"
bits_to_encode="64"
graphs=['audikw1', 'cnr-2000', 'citationCiteseer', 'preferentialAttachment', 'smallworld']

plots_tmp_file="/home/dapurv5/MyCode/gatech-projects/graph-compression-experiments/tmp/plot.tsv"
results_tmp_file="/home/dapurv5/MyCode/gatech-projects/graph-compression-experiments/tmp/results.tsv"
results_file="/home/dapurv5/MyCode/gatech-projects/graph-compression-experiments/results.tsv"

max_compression = {}
axis_name = {}

def execute(graph, compressor, param_min=-1, param_max=-1, param_step=-1):
  cmd = ['java',
         '-jar',
         'target/graph-compression-experiments-1.0-jar-with-dependencies.jar',
         graph,
         compressor,
         bits_to_encode,
         plots_tmp_file,
         results_tmp_file]  
  if param_min > 0:
    cmd.append(str(param_min))
    cmd.append(str(param_max))
    cmd.append(str(param_step))
  subprocess.call(cmd)

def plot(X, Y, xlabel, ylabel):
  plt.plot(X, Y)
  plt.ylabel(ylabel)
  plt.xlabel(xlabel)
  #plt.show()

def run_all_graphs(graphs, compressor, param_min=-1, param_max=-1, param_step=-1):
  for graph in graphs:
    graph_file = graph_dir + "/" + graph + ".graph"
    if param_min > 0:
      execute(graph_file, compressor, param_min, param_max, param_step)
      
      with open(plots_tmp_file, 'rb') as plotdata:
        params = []
        CR = []
        for line in plotdata:
          line = line.strip('\n')
          param, cr = line.split(" ")
          params.append(param)
          CR.append(cr)
      plot(params, CR, axis_name[compressor], 'compression-ratio')
      savefig(plots_dir+"/"+compressor+"_"+graph+".png")
      plt.clf()
    else:
      execute(graph_file, compressor)
      
    with open(results_tmp_file, 'rb') as result:
      line = result.readline()
      line = line.strip('\n')
      best_compression_ratio = line
      
      line = result.readline()
      line = line.strip('\n')
      param = int(line)
      if param == -1:
        param = " "
      if compressor not in max_compression:
        max_compression[compressor] = {}
      max_compression[compressor][graph]=best_compression_ratio + "("+str(param)+")"
      
  
  
#Experiments
compressor="adj_diff"
run_all_graphs(graphs, compressor)

compressor="adj_diff_fixed_edges"
axis_name[compressor] = 'num edges in the block'
block_size_min = 10
block_size_max = 200
block_size_step = 10
run_all_graphs(graphs, compressor,
               param_min = block_size_min,
               param_max = block_size_max,
               param_step = block_size_step)

compressor="adj_diff_variable_edges"
axis_name[compressor] = 'jump in num of bits'
jump_min = 10
jump_max = 100
jump_step = 10
run_all_graphs(graphs, compressor,
               param_min = jump_min,
               param_max = jump_max,
               param_step = jump_step)

#Experiments
compressor="pfor"
run_all_graphs(graphs, compressor)

compressor="src_diff_fixed_edges"
axis_name[compressor] = 'num edges in the block'
block_size_min = 10
block_size_max = 200
block_size_step = 10
run_all_graphs(graphs, compressor,
               param_min = block_size_min,
               param_max = block_size_max,
               param_step = block_size_step)

#write the max compression tsv file
with open(results_file, 'wb') as csvfile:
  fieldnames=['compressor']
  fieldnames.extend(graphs)
  
  writer=csv.DictWriter(csvfile, delimiter="\t", fieldnames=fieldnames)
  writer.writeheader()
  for compressor in max_compression.keys():
    dict = max_compression[compressor]
    dict['compressor']=compressor
    writer.writerow(dict)
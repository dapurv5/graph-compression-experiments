#!/usr/bin/env/python
#

import csv
import subprocess

graph_dir="/home/dapurv5/Desktop/Semesters/1st_semester/GRA"
plots_dir="/home/dapurv5/MyCode/gatech-projects/graph-compression-experiments/plots"
bits_to_encode="64"
graphs=['audikw1', 'cnr-2000', 'citationCiteseer', 'preferentialAttachment', 'smallworld']

plots_tmp_file="/home/dapurv5/MyCode/gatech-projects/graph-compression-experiments/tmp/plot.tsv"
results_tmp_file="/home/dapurv5/MyCode/gatech-projects/graph-compression-experiments/tmp/results.tsv"
results_file="/home/dapurv5/MyCode/gatech-projects/graph-compression-experiments/results.tsv"

max_compression = {}

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
    cmd.append(param_min)
    cmd.append(param_max)
    cmd.append(param_step)    
  subprocess.call(cmd)


def run_all_graphs(graphs, compressor, param_min=-1, param_max=-1, param_step=-1):
  for graph in graphs:
    graph_file = graph_dir + "/" + graph + ".graph"
    if param_min > 0:
      execute(graph_file, compressor, param_min, param_max, param_step)
      #read plots_tmp_file
      #plot the graph and save it in a file
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
      max_compression[compressor][graph]=best_compression_ratio + "("+param+")"
      
  
  
#Experiments
compressor="adj_diff"
run_all_graphs(graphs, compressor)


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
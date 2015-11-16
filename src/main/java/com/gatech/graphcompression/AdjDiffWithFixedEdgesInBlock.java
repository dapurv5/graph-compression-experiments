package com.gatech.graphcompression;

import java.util.Arrays;

/**
 * Adjacent Difference encoding where the adjacency in divided into blocks
 * Each block has a fixed number of pre-determined edges in it.
 *
 */
public class AdjDiffWithFixedEdgesInBlock extends Compressor {

  public final static String NAME = "adj_diff_fixed_edges";
  
  @Override
  public int compress(int u, int[] adjacency) {
    int bits = 0;
    int begin = 0;
    int t = getParam();
    Compressor adjDiffComp = new AdjDifference();
    
    while(begin < adjacency.length) {
      int finish = Math.min(adjacency.length, begin+t);
      int[] block = Arrays.copyOfRange(adjacency, begin, finish);
      begin+=t;
      bits+= adjDiffComp.compress(u, block);
    }
    return bits;
  }

}

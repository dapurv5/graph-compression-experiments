package com.gatech.graphcompression;

import java.util.Arrays;

public class SrcDiffWithFixedEdgesInBlock extends Compressor {

  public final static String NAME = "src_diff_fixed_edges";
  
  @Override
  public int compress(int u, int[] adjacency) {
    int bits = 0;
    int begin = 0;
    int t = getParam(); //size of the block
    Compressor srcDiffComp = new SrcDifference();
    
    while(begin < adjacency.length) {
      int finish = Math.min(adjacency.length, begin+t);
      int[] block = Arrays.copyOfRange(adjacency, begin, finish);
      begin+=t;
      bits+= srcDiffComp.compress(u, block);
    }
    return bits;
  }

}

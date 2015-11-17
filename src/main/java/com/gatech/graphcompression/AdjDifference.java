package com.gatech.graphcompression;

import static java.lang.Math.*;

/**
 * Adjacent Difference Encoding
 * Just take difference with adjacent element, the first element
 * takes a difference with the source vertex.
 * @author dapurv5
 */
public class AdjDifference extends Compressor{
  
  public final static String NAME = "adj_diff";
  
  public int compress(int u, int[] adjacency) {
    int[] consecDiff = getConsecDiffWithAdjElem(u, adjacency);
    int numBitsToEncode = 0;
    if(consecDiff[0] < 0) {
      consecDiff[0] *= -1.0;
    }
    
    int greatestElem = -1;
    for(int i = 0; i < adjacency.length; i++) {
      greatestElem = max(greatestElem, consecDiff[i]);
    }
    
    numBitsToEncode = (int)ceil(log2(greatestElem));
    numBitsToEncode = max(1, numBitsToEncode);
    
    return numBitsToEncode*adjacency.length 
        + 8 //how many bits were used to compress each element
        + 1; //sign bit for the first value
  }
}

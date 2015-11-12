package com.gatech.graphcompression;

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
      greatestElem = Math.max(greatestElem, consecDiff[i]);
    }
    
    double log2 = Math.log(2);
    numBitsToEncode = (int)Math.ceil( Math.log(greatestElem)/log2);
    numBitsToEncode = Math.max(1, numBitsToEncode);
    
    return numBitsToEncode*adjacency.length 
        + 8 //how many bits were used to compress each element
        + 1; //sign bit for the first value
  }
}

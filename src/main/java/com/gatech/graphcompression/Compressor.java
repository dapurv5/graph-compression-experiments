package com.gatech.graphcompression;

import java.util.Arrays;

import me.lemire.integercompression.IntWrapper;
import me.lemire.integercompression.differential.IntegratedBinaryPacking;
import me.lemire.integercompression.differential.IntegratedComposition;
import me.lemire.integercompression.differential.IntegratedIntegerCODEC;
import me.lemire.integercompression.differential.IntegratedVariableByte;

public class Compressor {
  
  private final static int NUM_BITS_FOR_SIGN_BIT = 1;
  private final static int NUM_BITS_FOR_BITS_TO_ENCODE = 8;
  
  private IntegratedIntegerCODEC codecPFOR = null;
  
  public Compressor() {
     codecPFOR =  new IntegratedComposition(
        new IntegratedBinaryPacking(),
        new IntegratedVariableByte());
  }
  
  public int countPFOR(int[] adjacency) {
    int[] compressed = new int[adjacency.length+1024];
    IntWrapper inputoffset = new IntWrapper(0);
    IntWrapper outputoffset = new IntWrapper(0);
    codecPFOR.compress(adjacency,inputoffset,adjacency.length,compressed,outputoffset);
    compressed = Arrays.copyOf(compressed, outputoffset.intValue());
    return compressed.length*32;
  }
  
  private int[] getConsecDiff(int u, int[] adjacency) {
    int[] consecDiff = new int[adjacency.length];
    consecDiff[0] = adjacency[0] - u;
    for(int i = 1; i < adjacency.length; i++) {
      consecDiff[i] = adjacency[i] - adjacency[i-1];
    }
    return consecDiff;
  }
  
  public int countNoChunks(int u, int[] adjacency) {
    int[] consecDiff = getConsecDiff(u, adjacency);
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
        + NUM_BITS_FOR_BITS_TO_ENCODE
        + NUM_BITS_FOR_SIGN_BIT;
  }
  
  
  public int countFixedChunks(int u, int[] adjacency, int t) {
    int bits = 0;
    int begin = 0;
    while(begin < adjacency.length) {
      int finish = Math.min(adjacency.length, begin+t);
      int[] chunk = Arrays.copyOfRange(adjacency, begin, finish);
      begin+=t;
      bits+= countNoChunks(u, chunk);
    }
    return bits;
  }

  
  /**
   * Assuming we use 8 bytes to encode each value in the array.
   */
  public int countUncompressed(int[] adjacency) {
    return adjacency.length * 64;
  }
}

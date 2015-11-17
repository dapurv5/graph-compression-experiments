package com.gatech.graphcompression;

import static java.lang.Math.*;

public class AdjDiffWithVariableEdgesInBlock extends Compressor {
  
  public final static String NAME = "adj_diff_variable_edges";

  @Override
  public int compress(int u, int[] adjacency) {
    int bits = 0;
    
    int jump = getParam(); //jump size
    int firstElemInTheBlock = adjacency[0] - u;    
    if(firstElemInTheBlock < 0) {
      firstElemInTheBlock *= -1.0;
    }
    int greatestElem = firstElemInTheBlock; //current greatest element in the block
    int lengthOfBlock = 1; //length of the current block
    
    for(int j = 1; j < adjacency.length; j++) {
      int numBitsToEncode = (int) ceil(log2(greatestElem));
      numBitsToEncode = max(1, numBitsToEncode);
      
      //Bits required before adding this element
      int bitsBeforeAdding = numBitsToEncode * lengthOfBlock;
      
      int newGreatestElem = max(greatestElem, adjacency[j]-adjacency[j-1]);
      int newNumBitsToEncode = (int) ceil(log(newGreatestElem));
      newNumBitsToEncode = max(1, newNumBitsToEncode);
      
      //Bits req. after adding this element
      int bitsAfterAdding = newNumBitsToEncode * (lengthOfBlock+1);
      
      if(bitsAfterAdding - bitsBeforeAdding < jump) {
        lengthOfBlock += 1;
        greatestElem = max(greatestElem, newGreatestElem);
      } else {
        //num of elements in the block
        //+ sign bit for the 1st element
        //+ nr. of bits req. to encode nr. of bits taken by each element
        bits += 16 + 1 + 8;
        bits += numBitsToEncode * lengthOfBlock;
        
        //reset the block, start a new block
        lengthOfBlock = 1;
        firstElemInTheBlock = adjacency[j] - u;
        if(firstElemInTheBlock < 0) {
          firstElemInTheBlock *= -1.0;
        }
        greatestElem = firstElemInTheBlock;
      }
    }
    
    if(lengthOfBlock > 0) {
      int numBitsToEncode = (int)(ceil(log2(greatestElem)));
      bits += 16+1+8;
      bits += numBitsToEncode * lengthOfBlock;
      lengthOfBlock = 0;
    }
    return bits;
  }
}
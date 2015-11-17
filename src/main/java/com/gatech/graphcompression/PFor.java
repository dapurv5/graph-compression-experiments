package com.gatech.graphcompression;

import java.util.Arrays;

import me.lemire.integercompression.IntWrapper;
import me.lemire.integercompression.differential.IntegratedBinaryPacking;
import me.lemire.integercompression.differential.IntegratedComposition;
import me.lemire.integercompression.differential.IntegratedIntegerCODEC;
import me.lemire.integercompression.differential.IntegratedVariableByte;

public class PFor extends Compressor {

  public final static String NAME = "pfor";
  
  private IntegratedIntegerCODEC codecPFOR = new IntegratedComposition(
      new IntegratedBinaryPacking(),
      new IntegratedVariableByte());
  
  @Override
  public int compress(int u, int[] adjacency) {
    int[] compressed = new int[adjacency.length+1024];
    IntWrapper inputoffset = new IntWrapper(0);
    IntWrapper outputoffset = new IntWrapper(0);
    codecPFOR.compress(adjacency,inputoffset,adjacency.length,compressed,outputoffset);
    compressed = Arrays.copyOf(compressed, outputoffset.intValue());
    return compressed.length*32;
  }
}

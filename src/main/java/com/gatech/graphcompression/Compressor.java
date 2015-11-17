package com.gatech.graphcompression;

public abstract class Compressor {
  
  private int param = -1;
  private boolean isParameterized = false;
  private int bitsToEncode = 64;
  private final double log2 = Math.log(2);
  
  /**
   * Returns the number of bits req. to encode this adjacency
   */
  public abstract int compress(int u, int[] adjacency);
  
  /**
   * Returns true if the compressor is parameterized
   * eg. any compressor using block size or number of edges in a block or jump in bits, etc
   * @return
   */
  public boolean isParameterized() {
    return isParameterized;
  }
  
  /**
   * Sets the value of the parameter if its a parameterized compressor.
   * @param param
   */
  public void setParam(int param) {
    this.isParameterized = true;
    this.param = param;
  }
  
  protected int getParam() {
    return param;
  }
  
  /**
   * Set number of bits to encode a vertex, this can either
   * be 32 or 64.
   */
  public void setBitsToEncode(int bits) {
    this.bitsToEncode = bits;
  }
  
  public int getBitsToEncode(int[] adjacency) {
    return adjacency.length * this.bitsToEncode;
  }
  
  protected int[] getDiffWithAdjElem(int u, int[] adjacency) {
    int[] consecDiff = new int[adjacency.length];
    consecDiff[0] = adjacency[0] - u;
    for(int i = 1; i < adjacency.length; i++) {
      consecDiff[i] = adjacency[i] - adjacency[i-1];
    }
    return consecDiff;
  }
  
  protected int[] getDiffWithSrcElem(int u, int[] adjacency) {
    int[] consecDiff = new int[adjacency.length];
    consecDiff[0] = adjacency[0] - u;
    for(int i = 1; i < adjacency.length; i++) {
      consecDiff[i] = adjacency[i] - u;
    }
    return consecDiff;
  }
  
  protected double log2(int n) {
    return Math.log(n)/log2;
  }
}

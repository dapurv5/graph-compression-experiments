package com.gatech.graphcompression;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.DecimalFormat;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;


public class GraphCompressionExperiment {
  
  private final Compressor compressor;
  private int paramMin=-1;
  private int paramMax=-1;
  private int paramStep=-1;
  
  private PrintWriter plotsWriter;
  private PrintWriter resultsWriter;
  private DecimalFormat df2 = new DecimalFormat("###.##");
  
  public GraphCompressionExperiment(Compressor compressor, String plotsTmpFile, String resultsFile) throws IOException {
    this.compressor = compressor;
    this.plotsWriter = new PrintWriter(new FileWriter(plotsTmpFile));
    this.resultsWriter = new PrintWriter(new FileWriter(resultsFile));
  }
  
  private int getBits(int[] ind, int[] off, boolean compressed) {
    int totalBits = 0;
    for(int i = 1; i < off.length-1; i++) {
      int adjStart = off[i];
      int adjEnd = off[i+1];
      int[] adjacency = new int[adjEnd-adjStart];
      for(int j = adjStart; j < adjEnd; j++) {
        adjacency[j-adjStart] = ind[j];
      }
      Arrays.sort(adjacency);
      if(compressed) {
        totalBits += compressor.compress(i, adjacency);
      } else {
        totalBits += compressor.getBitsToEncode(adjacency);
      }      
    }
    return totalBits;
  }
    
  private void runExperiment(int[] ind, int[] off) throws IOException {
    int totalUncompressed = getBits(ind, off, false);
    int totalCompressed = 0;
    int minTotalCompressed = Integer.MAX_VALUE;
    int optimalParamValue = -1;
    
    for(int param = paramMin; param <= paramMax; param += paramStep) {
      compressor.setParam(param);
      totalCompressed = getBits(ind, off, true);
      
      if(totalCompressed < minTotalCompressed) {
        minTotalCompressed = totalCompressed;
        optimalParamValue = param;
      }
      
      //Write this to the tsv file
    }
    
    double cr = (double)totalUncompressed/(double)totalCompressed;
    cr = Double.valueOf(df2.format(cr));
    resultsWriter.println(cr);
    resultsWriter.println(optimalParamValue);
    resultsWriter.close();
  }
  
  
  private static Map<String, Compressor> getCompressors() {
    Map<String, Compressor> compressors = new HashMap<String, Compressor>();
    compressors.put(AdjDifference.NAME, new AdjDifference());
    return compressors;
  }
  
  public static void main( String[] args ) throws IOException {
    //Read command line params and construct a compressor
    Map<String, Compressor> compressors = getCompressors();
    String path = args[0];
    cct cct = new cct();
    cct.readGraphDIMACS(path);
    int[] off = cct.off;
    int[] ind = cct.ind;
        
    String compressorName = args[1];
    Compressor compressor = compressors.get(compressorName);
    
    compressor.setBitsToEncode(Integer.parseInt(args[2]));
    String plotsTmpFile = args[3];
    String resultsFile = args[4];
    
    //Read cmd params and construct an experiment and set its params and the output files.
    GraphCompressionExperiment exp = new GraphCompressionExperiment(compressor, plotsTmpFile, resultsFile);
    
    //Begin ugly code!
    if(args.length > 5) {
      exp.paramMin = Integer.parseInt(args[5]);
      exp.paramMax = Integer.parseInt(args[6]);
      exp.paramStep = Integer.parseInt(args[7]);
    } else {
      exp.paramMin = -1;
      exp.paramMax = -1;
      exp.paramStep = 1;
    }
    //End ugly code!
        
    exp.runExperiment(ind, off);
  }
}

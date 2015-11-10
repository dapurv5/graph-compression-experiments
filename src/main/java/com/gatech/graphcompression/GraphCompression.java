package com.gatech.graphcompression;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtilities;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;

/**
 * WARNING: This code can cause eye cancer!
 */
public class GraphCompression {
  
  private Compressor compressor = null;
  private int paramMin = -1;
  private int paramMax = -1;
  private int paramStep = -1;
  
  public GraphCompression() {
    compressor = new Compressor();
  }
  
  public void setParamMin(int paramMin) {
    this.paramMin = paramMin;
  }
  
  public void setParamMax(int paramMax) {
    this.paramMax = paramMax;
  }
  
  public void setParamStep(int paramStep) {
    this.paramStep = paramStep;
  }
  
  private void plot(int[] ind, int[] off) throws IOException {
    DefaultCategoryDataset lineChart = new DefaultCategoryDataset();
    
    long totalUncompressed = 0;
    long totalCompressed = 0;
    
    for(int i = 1; i < off.length-1; i++) {
      int adjStart = off[i];
      int adjEnd = off[i+1];
      int[] adjacency = new int[adjEnd-adjStart];
      for(int j = adjStart; j < adjEnd; j++) {
        adjacency[j-adjStart] = ind[j];
      }
      Arrays.sort(adjacency);
      totalUncompressed += compressor.countUncompressed(adjacency);
    }
 
    int minTotalCompressed = Integer.MAX_VALUE;
    for(int param = paramMin; param <= paramMax; param += paramStep) {
      totalCompressed = 0;
      for(int i = 1; i < off.length-1; i++) {
        int adjStart = off[i];
        int adjEnd = off[i+1];
        int[] adjacency = new int[adjEnd-adjStart];
        for(int j = adjStart; j < adjEnd; j++) {
          adjacency[j-adjStart] = ind[j];
        }
        Arrays.sort(adjacency);
        //totalCompressed += compressor.countNoChunks(i, adjacency);
        totalCompressed += compressor.countFixedChunks(i, adjacency, param);
      }
      lineChart.addValue((double)totalUncompressed/(double)totalCompressed, "CR", ""+param);
      minTotalCompressed = (int)Math.min(totalCompressed, minTotalCompressed);
    }
    System.out.println("Max Compression Ratio = "+(double)totalUncompressed/(double)minTotalCompressed);
    
    JFreeChart lineChartObject = ChartFactory.createLineChart(
        "CR Vs size","size",
        "CR",
        lineChart,PlotOrientation.VERTICAL,
        true,true,false);

     int width = 1280; /* Width of the image */
     int height = 960; /* Height of the image */ 
     File lineChartFile = new File( "LineChart.jpeg" ); 
     ChartUtilities.saveChartAsJPEG(lineChartFile ,lineChartObject, width ,height);
  }
  
  
  public static void main( String[] args ) throws IOException {
    //String path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/cnr-2000.graph";
    //String path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/audikw1.graph";
    //String path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/citationCiteseer.graph";
    String path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/preferentialAttachment.graph";
    //String path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/smallworld.graph";
    cct cct = new cct();
    cct.readGraphDIMACS(path);
    int[] off = cct.off;
    int[] ind = cct.ind;
    
    GraphCompression exp = new GraphCompression();
    exp.setParamMin(4);
    exp.setParamMax(80);
    exp.setParamStep(4);
    exp.plot(ind, off);
  }
}

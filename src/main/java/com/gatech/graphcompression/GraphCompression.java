package com.gatech.graphcompression;

public class GraphCompression {
  
  
  public static void main( String[] args ) {
    //String path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/cnr-2000.graph";
    //String path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/audikw1.graph";
    //String path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/citationCiteseer.graph";
    //String path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/preferentialAttachment.graph";
    String path = "/home/dapurv5/Desktop/Semesters/1st_semester/GRA/smallworld.graph";
    cct cct = new cct();
    cct.readGraphDIMACS(path);
    int[] off = cct.off;
    int[] ind = cct.ind;
    
    for(int i = 0; i < 10; i++) {
      System.out.print(off[i]+",");
    }
  }
}

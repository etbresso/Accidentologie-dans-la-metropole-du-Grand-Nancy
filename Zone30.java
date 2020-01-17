
import java.awt.geom.Path2D;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class Zone30 {

	private ArrayList <Path2D> listZone30 = new <Path2D> ArrayList();

	public Zone30() throws IOException{
		BufferedReader br = new BufferedReader(new FileReader("zones30.kml"));
		try {
		    StringBuilder sb = new StringBuilder();
		    String line = br.readLine();

		    while (line != null) {
		    	if(line.contains("<coordinates>")){
		    		String[] splitPoly = line.split("<Polygon>");
		    		for (int i = 1; i<splitPoly.length; i++){ //pour chaque ploygone
		    			
		    			String[] splitCoordsBegin = splitPoly[i].split("<coordinates>"); //recupetation de toute les coordonées d'un polygone
		    			String[] splitCoordsEnd = splitCoordsBegin[1].split("</coordinates>");
		    			
		    			String[] pairCoord = splitCoordsEnd[0].split(" "); //paire de coordonnée
		    			
		    			double[] xpoints = new double[pairCoord.length];
		    			double[] ypoints = new double[pairCoord.length];
		    			Path2D path = new Path2D.Double();
		    			for(int j = 0; j <pairCoord.length; j++){ //pour chaque paire, sépare les 2 points
		    				String[] point = pairCoord[j].split(",");
		    				xpoints[j]= Double.parseDouble(point[0]);
		    				ypoints[j]= Double.parseDouble(point[1]);
		    				
		    				if(j!= 0){
		    					path.lineTo(xpoints[j], ypoints[j]);
		    				}else{
		    					path.moveTo(xpoints[0], ypoints[0]);
		    				}
		    			}
		    			path.closePath();
		    			listZone30.add(path);
		    		}
		    	}
		        line = br.readLine();
		    }
		} finally {
		    br.close();
		}
	}
	
	public Boolean contientPoint(double x, double y){
		for (int i = 0; i<listZone30.size(); i++){
			if(listZone30.get(i).contains(x, y)){
				return true;
			}
		}
		return false;
	}
	
}

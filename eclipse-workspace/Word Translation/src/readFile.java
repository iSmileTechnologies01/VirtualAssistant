import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;
/**
 * This class reads the text from the file and store it.
 * 
 * @author Sarnam Patel
 * @version 12/13/2020
 *
 */
public class readFile {

	//Reads the text from file and stores it in book object
		public static ArrayList<String> read(String filename) {
			ArrayList<String> words = new ArrayList<>(); //creating new ArrayList object named words
			String word = "";
			File file = new File(filename); //creating new File object named file
			
			try (Scanner input = new Scanner(file)) {
	            while (input.hasNextLine()) {
	                word = input.nextLine();
	                words.add(word);
	            }
	        } catch (FileNotFoundException e) {
	            e.printStackTrace();
	        }

	        return words;

	    }
	}

import java.util.ArrayList;
/**
 * This class 
 * 
 * @author Sarnam Patel
 * @version 12/13/2020
 *
 */
public class wordManager {
	// creating ArrayList objects and storing the values in englishWords, hindiWords, allWords respectively
	protected static ArrayList<String> englishWords = new ArrayList<>();
	protected static ArrayList<String> hindiWords = new ArrayList<>();
	protected static ArrayList<String> allWords = new ArrayList<>();

	/**
	 * Constructor reads the english.txt and hindi.txt files
	 */
	public wordManager() {
		englishWords = readFile.read("english.txt");
		hindiWords = readFile.read("hindi.txt");
		
	}
	/**
	 * Returns englishWords
	 * 
	 * @return englishWords
	 */
	public static ArrayList<String> getEnglish() {
		return englishWords;
	}

	/**
	 * Sets englishWords
	 * 
	 * @param englishWords to set
	 */
	public static void setEnglish(ArrayList<String> english) {
		wordManager.englishWords = english;
	}

	/**
	 * Returns hindiWords
	 * 
	 * @return hindiWords
	 */
	public static ArrayList<String> getHindi() {
		return hindiWords;
	}

	/**
	 * Sets hindiWords
	 * 
	 * @param hindiWords
	 */
	public static void setHindi(ArrayList<String> hindi) {
		wordManager.hindiWords = hindi;
	}

	/**
	 * 
	 * 
	 * @param wordToTranslate the word that user is suppose to translate 
	 * @param userInput user's answer
	 * @return false
	 */
	public boolean correctTranslation(String wordToTranslate , String userInput ) {
		
		return false;
	}
	
	/**
	 * adding words
	 */
	public static void fillStringArrayList() {
		
		for (int i = 0; i < englishWords.size(); i++) {
			allWords.add(englishWords.get(i));
		}
		
		for (int i = 0; i < hindiWords.size(); i++) {
			allWords.add(hindiWords.get(i));
		}
		
	}
}

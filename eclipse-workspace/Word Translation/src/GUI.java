import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;

public class GUI extends wordManager implements ActionListener {
	
	//private fields
    private static Random rd = new Random();
    private static JPanel panel;
    private static JFrame frame;
    private static JLabel label;
    private static JLabel instruction;
    private static JTextField userText;
    private static JButton button;
    private static JLabel correct;
    
   static Boolean decider = rd.nextBoolean();
   static int indexVal;
   
    public GUI() {

    }
  
   
    public static void main(String[] args) {
        panel = new JPanel(); //creating panel object
        frame = new JFrame(); //creating frame object
        frame.setSize(450, 150);
        populateFrame();
    }
    
    /**
     * This method creates a GUI and reads the words from the english.txt and hindi.txt files
     * 
     */
        public static void populateFrame(){
        	
        //setting title and close operation to the frame, and adding frame to the panel	
        frame.setTitle("LanguageGUI");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(panel);

        panel.setLayout(null);

        //creating new label object and adding it to the panel
        instruction = new JLabel("Type the translation into the field below.");
        instruction.setBounds(80, 0, 300, 40);
        panel.add(instruction);

        
        // ADDED wordManager OBJECT TO INITIALIZE ARRAYLIST
        wordManager words = new wordManager();
        
        //creating new label object and adding it to the panel
        label = new JLabel();
        label.setBounds(10, 50, 80, 25);
        panel.add(label);

        //creating new TextField object and adding it to the panel
        userText = new JTextField(20);
        userText.setBounds(100, 50, 220, 25);
        panel.add(userText);

        //creating new button object and added it to the panel
        button = new JButton("Ok");
        button.setBounds(350, 50, 50, 33);
        panel.add(button);
        
        //creating new label object and adding it to the panel
        correct = new JLabel();
        panel.add(correct);
        
        frame.setVisible(true);

        //randomly pulling index from the file
        int index = rd.nextInt(wordManager.getEnglish().size());
        indexVal = index;
        
        
        if (decider == true) { //read english.txt file
            label.setText(wordManager.getEnglish().get(index));
        }
        else if (decider == false){//read hindi.txt file
            label.setText(wordManager.getHindi().get(index));
        }

        button.addActionListener(new GUI());
        userText.addActionListener(new GUI());
    }

        /**
         * Action performed method to check the result of the user text
         */
    @Override
    public void actionPerformed(ActionEvent arg0) {
        String user = userText.getText(); //getting user text
        boolean check = false;

        instruction.setText("");
       
        
        if(decider == true) { //read hindi.txt
        	//get the same index word from the other file to check the user's translation
        	//looking for correct translation from hindi.txt file
           if (user.equals(wordManager.getHindi().get(indexVal))) {
              correct.setBounds(175, 0, 300, 40);
                correct.setText("Correct!");
              
           }
           else { //looking for incorrect translation form hindi.txt file
               instruction.setText(" ");
                correct.setBounds(130, 0, 300, 40);
                correct.setText("Incorrect! Answer: " + wordManager.getHindi().get(indexVal));
            }
           userText.setText("");
            int index = rd.nextInt(wordManager.getEnglish().size());
            indexVal = index;

            //display other word for the user to translate
            if (decider == true) {//read english.txt
                label.setText(wordManager.getEnglish().get(index));
            }
            else if (decider == false){//read hindi.txt
                label.setText(wordManager.getHindi().get(index));
            }
           
        }
        else if(decider == false) { //read english.txt
        	//looking for correct translation from english.txt file
           if (user.equals(wordManager.getEnglish().get(indexVal))) {
              correct.setBounds(175, 0, 300, 40);
                correct.setText("Correct!");
              
           }
           else {
        	 //looking for incorrect translation from english.txt file
               instruction.setText(" ");
                correct.setBounds(130, 0, 300, 40);
                correct.setText("Incorrect! Answer: " + wordManager.getEnglish().get(indexVal));
            }
           userText.setText("");
           
    }
      
        int index = rd.nextInt(wordManager.getEnglish().size());
        indexVal = index;

        //display other word for the user to translate
        if (decider == true) {
            label.setText(wordManager.getEnglish().get(index));
        }
        else if (decider == false){
            label.setText(wordManager.getHindi().get(index));
        }
        
    }
}
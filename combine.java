import java.io.*;
import java.util.HashMap;
import java.util.Map;

public class Solution {
    public static void main(String[] args) {
        Map<String, String> wordToIDMap = new HashMap<>();

        try (BufferedReader inReader = new BufferedReader(new FileReader("solution.in"))) {
            String line;
            while ((line = inReader.readLine()) != null) {
                String[] parts = line.split(":");
                if (parts.length == 2) {
                    String word = parts[0].trim();
                    String wordID = parts[1].trim();
                    wordToIDMap.put(word, wordID);
                }
            }
        } catch (IOException e) {
            System.err.println("Error reading solution.in: " + e.getMessage());
        }

        try (BufferedReader outReader = new BufferedReader(new FileReader("solution.out"))) {
            String line;
            while ((line = outReader.readLine()) != null) {
                String[] parts = line.split(":");
                if (parts.length == 2) {
                    String wordLineNumber = parts[0].trim();
                    String word = parts[1].trim();

                    String normalizedWord = word.replaceAll("\\s*\\(.*?\\)", "").trim();

                    String wordID = wordToIDMap.get(normalizedWord);

                    if (wordID != null) {
                        System.out.println(wordLineNumber + ":" + wordID);
                    } else {
                        System.err.println("Word not found in solution.in: " + word);
                    }
                }
            }
        } catch (IOException e) {
            System.err.println("Error reading solution.out: " + e.getMessage());
        }
    }
}

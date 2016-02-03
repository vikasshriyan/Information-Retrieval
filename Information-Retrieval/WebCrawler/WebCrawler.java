/*
@author VIKAS SHRIYAN
*/
import java.io.IOException;
import java.io.*;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.util.LinkedHashMap;


public class WebCrawler {
    
    // URLs to be found, the maximum depth to be crawled, delay between requests
    static final int UNIQUE_URLS = 1000;
    static final int DEPTH = 5;
    static final int DELAY = 1000;
    static String seed= "";
    static String keyphrase= "";
    static LinkedHashMap<String, Integer> childLinks = new LinkedHashMap<String, Integer>();
    static LinkedHashMap<String, Integer> started = new LinkedHashMap<String, Integer>();
    static List visited = new ArrayList();
            
    public static void main(String args[]) throws IOException, InterruptedException{
        
        int argsLength = args.length;
        
        if(argsLength > 2){
            System.out.println ("Number of arguments exceeded");
        }
        // Focused Crawling
        else if(argsLength == 2){
            seed = args[0];
            keyphrase = args[1];
             
            System.out.println("Seed ->" + seed);
            System.out.println("Keyphrase ->" + keyphrase);
            started.put(seed, 1);
            webCrawl(keyphrase);
            for(Object link: visited){
                System.out.println(link);
            }
            System.out.println("Total unique URLs Crawled -> " + visited.size());
            System.out.println("Total number of URLs Crawled ->" + started.size());
        }
        // Unfocused Crawling
        else 
        {   
            seed = args[0];
            keyphrase = "";
             
            System.out.println("Seed ->" + seed);
            System.out.println("Keyphrase ->" + keyphrase);
            started.put(seed, 1);
            webCrawl(keyphrase);
            for(Object link: visited){
                System.out.println(link);
            }
            System.out.println("Total Unique URLs Crawled -> " + visited.size());
            System.out.println("Total number of URLs Crawled ->" + started.size());
        }        
    }
    
    // Crawl the first link and remove it.  
    public static void webCrawl(String keyphrase) throws IOException, InterruptedException{
        int current_Depth;
        String firstLink = "";
        while(!(started.size() == 0 || visited.size() == UNIQUE_URLS))
        {
            while(true){
            firstLink = getFirstLink(started);
            current_Depth = started.get(firstLink);
            if(firstLink.contentEquals("")) 
                return;
            else if(visited.contains(firstLink)){ 
                started.remove(firstLink);
            }
            else 
                break;
        }
            crawl(firstLink,current_Depth, keyphrase);
         //   Thread.sleep(DELAY); // Add delay of 1 second between requests
        }       
    }
    
    // Crawl the url after validating the url for the conditions.
    public static void crawl(String seed, int current_Depth,  String keyphrase) throws MalformedURLException, IOException{
        StringBuilder sb = new StringBuilder();
        URLConnection connection = new URL(seed).openConnection();
     //   connection.connect();
        if(validateURL(new URL(seed).toString())){
            URL newURL = connection.getURL();
            newURL = new URL("https://" + newURL.getHost() + newURL.getPath());
            String updatedSeed = new String(newURL.toString());
            
            //Retrieve the HTML content
            URLConnection newConnection = new URL(updatedSeed).openConnection();
            InputStreamReader res = new InputStreamReader(newConnection.getInputStream());
            BufferedReader br = new BufferedReader(res);
            if (br != null) {
                String cp;
                while ((cp = br.readLine()) != null) {
                    sb.append(cp);
                }
                br.close();
            }
            
            // Check the keyphrase in the HTML content or Crawl the links
            String response = sb.toString();
            if(keyphrase == null){
                visited.add(newURL.toString());
                System.out.println("Crawled ->" +visited.size());
            } else if(focusedCrawl(response, keyphrase)){
                visited.add(newURL.toString());
                System.out.println("Crawled ->" +visited.size());
                }
                else {
                    started.remove(seed);
                    return;
            }

            // Parse the HTML content
            if(current_Depth < DEPTH){
                //Parse the HTML content and look for links
                Document doc = Jsoup.parse(sb.toString());
                Elements links = doc.select("a[href]");
            
                for (Element link : links){ 
                    if(validateURL(link.attr("href"))){
                        String l = checkProtocol(link.attr("href"));
                        childLinks.put(l, current_Depth + 1);
                    }  
                }
            
                //Child links added
                for(String l : childLinks.keySet()){
                    if(started.containsKey(l) || visited.contains((l)))
                        continue;
                    else
                    started.put(l,childLinks.get(l)); 
                }
                //Clear the links from the childLinks
                childLinks.clear();
            } 
        
        }
        started.remove(seed);
        
    }
    
    // Checking the keyphrase in the HTML document
    public static boolean focusedCrawl(String res, String keyphrase){
        Document doc = Jsoup.parse(res);
        String htmlContent = doc.text();
        htmlContent = htmlContent.toLowerCase();
        return(htmlContent.contains(keyphrase));
    }
    
    // Checking the URL to meet the given conditions
    private static boolean validateURL(String urlString) throws MalformedURLException {
        // Check each link to meet the conditions
        urlString = checkProtocol(urlString);
        if(urlString.contentEquals("")){
            return false;
        }
        URL url = new URL(urlString);
        String host = url.getHost();
        String path = url.getPath();
        boolean condition1 = host.contentEquals("en.wikipedia.org");
        boolean condition2 = path.startsWith("/wiki/");
        boolean condition3 = !path.contains(":");
        boolean condition4 = !path.contentEquals("/wiki/Main_Page");
        boolean condition5 = !path.contains("#");
        return (condition1 && condition2 && condition3 && condition4 && condition5);
    }
    
    // Check for the URL's protocol, if not present add the protocol.
    public static String checkProtocol(String urlString){
    
        if(!urlString.startsWith("http")){
            if(urlString.startsWith("//"))
                urlString = "https:" + urlString;
            else if(urlString.startsWith("/"))
                urlString = "https://en.wikipedia.org" + urlString;
            else if(urlString.startsWith("#"))
                return "";
            else
                return "";
        }        
        return urlString;
    }
    
    // Get the first element of the list
    public static String getFirstLink(LinkedHashMap<String, Integer> childLinks){
        String firstLink = "";
        for(String l : childLinks.keySet()){
            firstLink = l;
            break;
        }
        return firstLink;
    }
}

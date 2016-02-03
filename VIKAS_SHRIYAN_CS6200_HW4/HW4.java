
import java.awt.RenderingHints;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import org.apache.lucene.index.Fields;
import static javax.swing.text.html.HTML.Attribute.CONTENT;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.DocsEnum;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.MultiFields;
import org.apache.lucene.index.SlowCompositeReaderWrapper;
import org.apache.lucene.index.Term;
import org.apache.lucene.index.Terms;
import org.apache.lucene.index.TermsEnum;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.DocIdSetIterator;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.search.similarities.DefaultSimilarity;
import org.apache.lucene.search.similarities.TFIDFSimilarity;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Bits;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.util.Version;
import org.jsoup.Jsoup;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class HW4 {
    //private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);
    private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

    
    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<File>();
    static HashMap<String, Integer> indexes = new HashMap<String, Integer>();

    public static void main(String[] args) throws IOException {
	System.out.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

	String indexLocation = null;
	BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
	String s = br.readLine();

	HW4 indexer = null;
	try {
	    indexLocation = s;
	    indexer = new HW4(s);
	} catch (Exception ex) {
	    System.out.println("Cannot create index..." + ex.getMessage());
	    System.exit(-1);
	}

	// ===================================================
	// read input from user until he enters q for quit
	// ===================================================
	while (!s.equalsIgnoreCase("q")) {
	    try {
		System.out
			.println("Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
		System.out
			.println("[Acceptable file types: .xml, .html, .html, .txt]");
		s = br.readLine();
		if (s.equalsIgnoreCase("q")) {
		    break;
		}

		// try to add file into the index
		indexer.indexFileOrDirectory(s);
	    } catch (Exception e) {
		System.out.println("Error indexing " + s + " : "
			+ e);
	    }
	}

	// ===================================================
	// after adding, we always have to call the
	// closeIndex, otherwise the index is not created
	// ===================================================
	indexer.closeIndex();

	// =========================================================
	// Now search
	// =========================================================
	IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
		indexLocation)));
	IndexSearcher searcher = new IndexSearcher(reader);       
        

        //Code to find terms and their term frequencies
        IndexReader indexReader = DirectoryReader.open(FSDirectory.open(new File(
		indexLocation)));
        Bits liveDocs = MultiFields.getLiveDocs(indexReader);
        Fields fields = MultiFields.getFields(indexReader);
        Terms terms = fields.terms("contents");
        TermsEnum termEnum = terms.iterator(null);
        BytesRef bytesRef;
        while ((bytesRef = termEnum.next()) != null) {
            if (termEnum.seekExact(bytesRef)) {
                DocsEnum docsEnum = termEnum.docs(liveDocs, null);
                if (docsEnum != null) {
                    int doc;
                    while ((doc = docsEnum.nextDoc()) != DocIdSetIterator.NO_MORE_DOCS){
                        if(indexes.containsKey(bytesRef.utf8ToString())){
                            indexes.put(bytesRef.utf8ToString(), indexes.get(bytesRef.utf8ToString()) + docsEnum.freq());
                        }
                        else{
                            indexes.put(bytesRef.utf8ToString(), 1);
                        }
                    }   
                }
            }
        }

        // Sorting of terms based on term frequencies
        Set<Entry<String, Integer>> set = indexes.entrySet();
        List<Entry<String, Integer>> list = new ArrayList<Entry<String, Integer>>(set);
        Collections.sort( list, new Comparator<Map.Entry<String, Integer>>()
        {
            public int compare( Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2 )
            {
                return (o2.getValue()).compareTo( o1.getValue() );
            }
        } );
        
        // Printing of the term and their term Frequencies        
        for(Map.Entry<String, Integer> entry : list){
            System.out.println("Term -> " + entry.getKey() + " Term Frequency ->" +entry.getValue());
        }

        // Searching the query
	s = "";
	while (!s.equalsIgnoreCase("q")) {
	    try {
                TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
		System.out.println("Enter the search query (q=quit):");
		s = br.readLine();
		if (s.equalsIgnoreCase("q")) {
		    break;
		}
                
                // Check for special characters, for e.g., <html> will be html. [Code Added]
                s = s.toLowerCase();
                s = s.replaceAll("[^A-Za-z ]", "");
                System.out.println("Query Term ->" +s);

		Query q = new QueryParser(Version.LUCENE_47, "contents",
			sAnalyzer).parse(s);
		searcher.search(q, collector);
		ScoreDoc[] hits = collector.topDocs().scoreDocs;

		// 4. display results
		System.out.println("Found " + hits.length + " hits.");
		for (int i = 0; i < hits.length; ++i) {
		    int docId = hits[i].doc;
		    Document d = searcher.doc(docId);
		    System.out.println((i + 1) + ". " + d.get("filename")
			    + " Score = " + hits[i].score);
		}
		
                // 5. term stats --> watch out for which "version" of the term
		// must be checked here instead!
                                
                for (String each : s.split(" ")){  // for each term in the query [Code Added]
                    Term termInstance = new Term("contents", each);
                    long termFreq = reader.totalTermFreq(termInstance);
                    long docCount = reader.docFreq(termInstance);
                    System.out.println("Term -> " + each + " Term Frequency -> " + termFreq
			+ " - Document Frequency -> " + docCount);
                }

	    } catch (Exception e) {
		System.out.println("Error searching " + s + " : "
			+ e.getMessage());
		break;
	    }

	}

    }

    /**
     * Constructor
     * 
     * @param indexDir
     *            the name of the folder in which the index should be created
     * @throws java.io.IOException
     *             when exception creating index.
     */
    HW4(String indexDir) throws IOException {

	FSDirectory dir = FSDirectory.open(new File(indexDir));

	IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47, sAnalyzer);

	writer = new IndexWriter(dir, config);
    }

    /**
     * Indexes a file or directory
     * 
     * @param fileName
     *            the name of a text file or a folder we wish to add to the
     *            index
     * @throws java.io.IOException
     *             when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
	// ===================================================
	// gets the list of files in a folder (if user has submitted
	// the name of a folder) or gets a single file name (is user
	// has submitted only the file name)
	// ===================================================
	addFiles(new File(fileName));

	int originalNumDocs = writer.numDocs();
	for (File f : queue) {
	    FileReader fr = null;
	    try {
		Document doc = new Document();
                
                removeTags(f);
                
		// ===================================================
		// add contents of file
		// ===================================================
		fr = new FileReader(f);
       
		doc.add(new TextField("contents", fr));
		doc.add(new StringField("path", f.getPath(), Field.Store.YES));
		doc.add(new StringField("filename", f.getName(),Field.Store.YES));

		writer.addDocument(doc);
                
		System.out.println("Added: " + f);
	    } catch (Exception e) {
		System.out.println("Could not add: " + f);
	    } finally {
		fr.close();
	    }
	}

	int newNumDocs = writer.numDocs();
	System.out.println("");
	System.out.println("************************");
	System.out
		.println((newNumDocs - originalNumDocs) + " documents added.");
	System.out.println("************************");

	queue.clear();
    }

    //Parsing "<html>" and "<pre>" tags.
    public static void  removeTags(File f) throws FileNotFoundException, IOException {
        BufferedReader br = new BufferedReader(new FileReader(f));
        org.jsoup.nodes.Document h;
        String html = "";
        String line;
        while ((line=br.readLine())!= null){
            html += line + '\n';
        }
        br.close();
        try{
            h = Jsoup.parse(html);
            html = h.text();
        }catch(Exception e){
            System.out.println("Exception " + e.getMessage());
        }
        BufferedWriter bw = new BufferedWriter(new FileWriter(f));
        bw.write(html);
        bw.close(); 
    }
    
    private void addFiles(File file) {

	if (!file.exists()) {
	    System.out.println(file + " does not exist.");
	}
	if (file.isDirectory()) {
	    for (File f : file.listFiles()) {
		addFiles(f);
	    }
	} else {
	    String filename = file.getName().toLowerCase();
	    // ===================================================
	    // Only index text files
	    // ===================================================
	    if (filename.endsWith(".htm") || filename.endsWith(".html")
		    || filename.endsWith(".xml") || filename.endsWith(".txt")) {
		queue.add(file);
	    } else {
		System.out.println("Skipped " + filename);
	    }
	}
    }

    /**
     * Close the index.
     * 
     * @throws java.io.IOException
     *             when exception closing
     */
    public void closeIndex() throws IOException {
	writer.close();
    }
}
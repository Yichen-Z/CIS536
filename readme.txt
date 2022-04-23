Readme 
Yichen Zhang
CIS 536
Spring 2022

To run the script file main.py:
    0) Download and install a compatible IDE. Some examples are listed below.
        Visual Studio Code: https://code.visualstudio.com/
        PyCharm: https://www.jetbrains.com/pycharm/
    
    1) Script directory:
        a) Create another directory, either nested within or independent of the directory above
        b) Move the .py script to this directory
            Or fork from https://github.com/Yichen-Z/CIS536
        c) Open this directory with IDE
            If using Visual Studio Code or another IDE that does not auto-create virtual env:
                Terminal:
                    python -m venv new_venv
            VS Code will have a pop-up window that helps automatically activate this venv
            (This should automatically install pip)
    
    2) In main.py
        a) Update line 9's RAW_FILES to be the directory where the raw wikipedia files are
        b) Update line 10's CLEANED_FILES to be the directory where the cleaned and separated text files should go
 
    3) Install packages via terminal from directory where script is:
        To use Pipreqs:
            Type the following:
                pipreqs
                python -m pip install -r requirements.txt
        Manual installation:
            Run this command
                python -m pip install package_name
            Replace package_name with each of these:
                pandas
                -U pip setuptools wheel
                -U spacy
    
    4) Install spaCy language model via terminal:
        python -m spacy download en_core_web_sm

Checkpoint 2 Scope
- Multiple txt files
- "Localized" inverted indices

Observations:
    Running read_chunks() on one of the files without any processing of the text:
        Testing read_chunks takes 0.781052827835083 sec
        However, ultimately this seems to hang the regex and lemmatizer
        # Read in chunks of 100 MB - slow/hanging
        # def read_chunks(file, c = CHUNK_SIZE):
        #     """
        #     uses file.read() to read in text in chunks of size CHUNK_SIZE, set here to be 100 MB
        #     and process the documents in each line
        #     :param file: string for file path
        #     :param c: int for size of chunk to read
        #     :return:
        #     """
        #     with open(file, 'r', encoding='utf-8') as f:
        #         rfile = partial(f.read, c)
        #         for text in iter(rfile, ''): # stop when the file ends
        #             if not text.endswith('\n'): # catching part of the last line that we can read
        #                 prev = text
        #             else:
        #                 if prev != '': # there's a lingering partial line
        #                     text = prev + text
        #                     prev = ''
        #                 # this is a complete line and can be processed as usual
        #                 print(process(text))
    Changed to reading line by line instead with read_file
        New issue: spaCy lemmatizer nlp pipeline is now much slower even on a smaller text file compared to Checkpoint 1
            Lemmatization time:  3.898629903793335
            Next iteration needs to return to chunking so spaCy can process as much of the text as possible
    Next approach:
        Break apart the big files and clean them at the same time
        Problem not solved: takes a very long time
        On the plus side, if the separation and cleaning ever get done, the actual dictionary and index construction do not take as long
    Still need to improve:
        Considerably speed up the reformatting and lemmatization of the raw files - impossible to do at this point at scale
        Separate the creation of the vocabulary from the creation of the inverted indices
            Kind of a chicken-and-egg problem, as the inverted indices still need the term ID, which can only be determined once the entire vocabulary is complete

From Checkpoint 1:
To run the script file checkpoint_01.py: (continued from instructions for main.py)
    5) To sample or not:
        To run the script on the first n lines of the original text file
            a) Line 31, set ROWS = n
            b) Ensure line 170's sample_text(FILEPATH) is NOT commented out - ensure it will run
        To run the script on the entire original file
            a) Line 32, set SAMPLE_FILE to the path of a copy of the original text file
            b) Ensure line 170's sample_text(FILEPATH) will NOT run - comment it out
    
    6) Double check:
        Ensure the following will run (NOT commented out)
            Line 175: change_to_lowercase(SAMPLE_FILE)
            Line 176: regex_replace()
            Line 179: lemmatize_file()
            Line 184: make_corpus_dictionary()
            Line 185: build_unigram()

Readme 
Yichen Zhang
CIS 536
Spring 2022

To run the script file checkpoint_01.py:
    0) Download and install a compatible IDE. Some examples are listed below.
        Visual Studio Code: https://code.visualstudio.com/
        PyCharm: https://www.jetbrains.com/pycharm/
    
    1) HOME & FILE paths:
        a) Create a directory. Place the Wikipedia text file you wish to use in it.
        b) Update HOME variable on line 28 to this directory's path.
        c) Update the string in FILE on line 29 to the name of the text file
    
    2) Script directory:
        a) Create another directory, either nested within or independent of the directory above
        b) Move the .py script to this directory
            Or fork from https://github.com/Yichen-Z/CIS536
        c) Open this directory with IDE
            If using Visual Studio Code or another IDE that does not auto-create virtual env:
                Terminal:
                    python -m venv new_venv
            VS Code will have a pop-up window that helps automatically activate this venv
            (This should automatically install pip)
 
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
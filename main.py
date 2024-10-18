import find_by_citation

import subprocess
import os

def run_script(script_path):
    # Get the absolute path to the script
    abs_path = os.path.abspath(script_path)
    
    # Run the script
    process = subprocess.Popen(['python', abs_path], stdout=subprocess.PIPE, 
                           stderr=subprocess.STDOUT, text=True, cwd=os.path.dirname(abs_path))

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip()) 


def run_module(script_path, *args):
    # Get the absolute path to the script
    abs_path = os.path.abspath(script_path)
    
    # Run the script
    process = subprocess.Popen(['python', '-m' , os.path.basename(script_path), *args], stdout=subprocess.PIPE, 
                           stderr=subprocess.STDOUT, text=True, cwd=os.path.dirname(abs_path))

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip()) 


###  Run the citation-based analysis

run_script(os.path.join('find_by_citation', 'find_datasets_in_dois.py'))

###  Run the pdf-contents-based analysis

run_script(os.path.join('find_by_pdf_content', 'get_article_metadata.py'))
# we set the input to be the output dir (which was output of previous step) and the output of
# the script to the output directory of [find_by_pdf_content]. Very sane and not confusing.
run_module(os.path.join('find_by_pdf_content', 'pure_text_analysis', 'pure_scraper'), 'output', '../output')

### Process results

run_script(os.path.join('process_output.py.py'))


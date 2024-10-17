# Maybe move this to a python file so there is no confusion regarding python version etc
python --version

# Run the Citation metadata based analysis
cd find_by_citation/
#python main.py
cd ..

# Run the PDF content based analysis
cd find_by_pdf_content
python get_article_metadata.py
cd pure_text_analysis
python -m pure_scraper-m find_by_pdf_content/get_article_metadata.py
cd ../..
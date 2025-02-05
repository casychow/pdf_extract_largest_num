# PDF Scraper Extract Largest Num

Goal: Find the largest number in this [large pdf document](https://www.saffm.hq.af.mil/Portals/84/documents/FY25/FY25%20Air%20Force%20Working%20Capital%20Fund.pdf?ver=sHG_i4Lg0IGZBCHxgPY01g%3d%3d). The unit is not important (could be dollars, years, pounds, etc), output the greatest numerical value in the document.

[comment]: <> (For a bonus challenge if you have time, take natural language guidance from the document into consideration. For example, where the document states that values are listed in millions, a value of 3.15 would be considered to be 3,150,000 instead of 3.15.)

## How to Run Software
1. Download and install Python.
2. Install the PyPDF2 library: `pip install PyPDF2`
3. Ensure that the pdf file is in the same directory as the python script.
4. Run the program using either method:
    - Using a terminal, change the working directory into the same directory as the python script and the pdf file, then use `python pdf_extract_largest_num.py`, or
    - Open a code editor that can run jypter notebook files and press "Run all" on the `pdf_extract_largest_num.ipynb` file.

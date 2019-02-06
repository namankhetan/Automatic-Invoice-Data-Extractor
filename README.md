# Automatic-Invoice-Data-Extractor
Making the task of accounting easy and efficient.
The python script extracts all the important data from the invoice and automatically update the database according to the data in the invoice, after getting image of the invoice as an input. It uses Pytesseract library to extract the data from that image and then recognizes the required data with the help of OpenCv and regular expressions and the formatted required data is send to the sql database. 

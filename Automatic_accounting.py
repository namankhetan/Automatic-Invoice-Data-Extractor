# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 02:17:41 2019

@author: LocalAdmin
"""

from PIL import Image
import pytesseract
import argparse
import cv2 
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)


filename = "{}.jpg".format(os.getpid())

def crop_and_fetch_data(x,y,w,h, img):
	crop_img = img[x:x+w, y:y+h]
	cv2.imwrite('crop_img.jpg', crop_img)
	img1 = cv2.imread("crop_img.jpg")
	text = pytesseract.image_to_string(Image.open('./crop_img.jpg'))
	#os.remove(filename)
	return text 

img = gray

b = img.shape[1]
l = img.shape[0]

#Descriptoins
x = int(0.3333*l) 
y = int(0.0516*b) 
h = int(0.2666*l) 
w = int(0.42*b)
des = crop_and_fetch_data(x,y,w,h,img)
d = des.split('\n')
while '' in d:
	d.remove('')
#print(d)
#print(des)

#Invoice Details
x = int(0.1125*l) 
y = int(0.157*b) 
h= int(0.0625*l) 
w = int(0.317*b)
inv_det = crop_and_fetch_data(x,y,h,w,img)
ind = inv_det.split('\n')
while '' in ind:
	ind.remove('')
#print(ind)



#print(inv_det)

#Quantity
x = int(0.333*l) 
y = int(0.581*b) 
h= int(0.2666*l) 
w = int(0.0896*b)
qty = crop_and_fetch_data(x,y,h,w,img)
q = qty.split('\n')
while '' in q:
	q.remove('')
#print(q)
#print(qty)

#Amount
x = int(0.3333*l) 
y = int(0.858*b) 
h= int(0.2666*l) 
w = int(0.1413*b)
amt = crop_and_fetch_data(x,y,w,h,img)
a = amt.split('\n')
while '' in a:
	a.remove('')
#print(a)
#print(amt)

#GTotal
x = int(0.641*l) 
y = int(0.858*b) 
h= int(0.0541*l) 
w = int(0.1413*b)
cp_img = img[x:x+h,y:y+w]
cv2.imshow("w",cp_img)
gt = crop_and_fetch_data(x,y,h,w,img)
#print(gt)

#Address
x = int(0.175*l) 
y = int(0*b) 
h= int(0.129*l) 
w = int(0.4755*b)
add = crop_and_fetch_data(x,y,h,w,img)
ad = add.split()
ad = (' '.join(ad))
#print(ad)



#print("Description \n", des)
#print("Inv_detals\n ", inv_det)
#print("Qty \n", qty)
#print("Amount \n", amt)
#rint("G_total\n ", gt)
#rint("Bill_det\n ", add)

import sqlite3 
connection = sqlite3.connect("invoice.db")
crsr = connection.cursor()
sql_command = """CREATE TABLE IF NOT EXISTS prod(
product_names VARCHAR(20), 
quantity INTEGER,
amount DECIMAL(7,2));"""

crsr.execute(sql_command)

sql_command = """CREATE TABLE IF NOT EXISTS inv( 
invoice_number VARCHAR(20),
date DATE,
total_amount DECIMAL(7,2),
customer VARCHAR(100));"""
crsr.execute(sql_command)

for i in range((len(d))):
    #print("value of d , q , a is ", d[i], q[i], a[i] )
    crsr.execute("INSERT INTO prod VALUES (?, ?, ?)", (d[i], q[i], a[i]))
    
crsr.execute("INSERT INTO inv VALUES (?, ?, ?, ?)", (ind[0] , ind[1], gt, ad))
#connection.commit()
crsr.execute("SELECT * FROM inv")
ans2= crsr.fetchall()
print("\n\n(Invoice Number, Date, GRAND Amount, Customer's Details )")
print((ans2))
print("\n\n(Product name, Quantity, Amount)")
crsr.execute("SELECT * FROM prod") 

ans1= crsr.fetchall()

i=0
for i in ans1:
	print(i)
crsr.execute("SELECT SUM(total_amount) FROM inv")
ans3=crsr.fetchall()
print("\n\nTHE GRAND TOTAL OF ALL THE BILLS IS ",(ans3))
connection.commit()
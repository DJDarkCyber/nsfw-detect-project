import random
from string import ascii_lowercase
import mysql.connector
import pandas as pd

DBHOST = "localhost"
DBNAME = "image_hosting"
DBPASS = ""
DBUSER = ""


def getAllImages():
    con = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
    cursor = con.cursor()
    cursor.execute("SELECT Img_File FROM hell_hosting")
    result = cursor.fetchall()
    imgs = pd.DataFrame(result)
    all_images = []
    for stuff in imgs.values:
        all_images.append(stuff[0])
    
    cursor.execute("SELECT Img_Desc FROM hell_hosting")
    result = cursor.fetchall()
    desc = pd.DataFrame(result)
    all_desc = []
    for stuff in desc.values:
        all_desc.append(stuff[0])

    return all_images[:25], all_desc[:25]

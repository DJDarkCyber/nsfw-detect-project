# Secure File
# Version 1.0

import random
from string import ascii_lowercase
import mysql.connector
import pandas as pd
import numpy as np
import os

DBHOST = "localhost"
DBNAME = "image_hosting"
DBPASS = ""
DBUSER = ""

def secureFile(fileName, fileHeader):
    flag = 0
    if "application/x-php" in fileHeader:
        flag = 1
        return flag
    fileName = fileName.lower()
    imageFileExt = [".png", ".jpg", ".jpeg", ".svg"]
    if fileName[-4:] == imageFileExt[0] or fileName[-4:] == imageFileExt[1] or fileName[-5:] == imageFileExt[2] or fileName[-4:] == imageFileExt[3]:
        pass
    else:
        flag = 1
        return flag
    
    
    return flag


def saveFileInDB(fileName, imgTitle):
    storedName = ""
    def genRandomFileName():
        randomName = ""
        if fileName[-5:] == ".jpeg":
            for i in range(50):
                randomName += ascii_lowercase[random.randint(0, len(ascii_lowercase)-1)]
            randomName += ".jpeg"
        else:
            for i in range(50):
                randomName += ascii_lowercase[random.randint(0, len(ascii_lowercase)-1)]
            randomName += fileName[-4:]
        return randomName
    
    con = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
    cursor = con.cursor()
    cursor.execute("SELECT Img_File from hell_hosting")
    allFiles = pd.DataFrame(cursor.fetchall(), columns=["Files"])

    randomName = ""

    while True:
        randomName = genRandomFileName()
        if randomName in allFiles:
            pass
        else:
            break
    
    storedName = randomName

    cursor.execute("INSERT INTO hell_hosting (Img_File, Img_Desc) VALUES (%s, %s)", (storedName, imgTitle))
    con.commit()
    return storedName


def detectNSFW(fileName):
    from tensorflow.keras.preprocessing import image
    from tensorflow import keras
    flag = 0
    model = keras.models.load_model("porndetect.h5")
    test_img = image.load_img("static/hostingImages/" + fileName, target_size=(256, 256))
    test_img = image.img_to_array(test_img)
    test_img = np.expand_dims(test_img, axis=0)
    result = model.predict(test_img) # 0 -> Normal, 1 -> Porn
    del model
    del keras
    del image
    
    if result == 0:
        flag = 1
        return flag
    
    return flag


def removeFile(fileName):
    os.remove("static/hostingImages/" + fileName)
    con = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
    cursor = con.cursor()
    cursor.execute("DELETE FROM hell_hosting WHERE Img_File='" + fileName + "'")
    con.commit()

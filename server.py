from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
from pyscrs.handleFile import secureFile, saveFileInDB, detectNSFW, removeFile
from pyscrs.getFiles import getAllImages

app = Flask("__name__")

app.secret_key = "437437437437"

@app.route("/", methods=["GET"])
def main():
    images, descs = getAllImages()
    return render_template("index.html", img=images, ln=len(images), desc=descs)

@app.route("/upload", methods=["GET", "POST"])
def uploadImage():
    if request.method == "POST":
        f = request.files["IMAGE"]
        imgTitle = request.form["IMGTITLE"]
        fileName = f.filename
        fileHeader = f.headers
        storedFileName = saveFileInDB(fileName, imgTitle)
        f.save( "static/hostingImages/" + secure_filename(storedFileName))
        flag = secureFile(fileName, fileHeader)
        flag2 = detectNSFW(storedFileName)
        if flag2 == 1:
            removeFile(storedFileName)
            return render_template("uploadImg.html", error=1)
        if flag == 1:
            removeFile(storedFileName)
            return render_template("uploadImg.html", error=1)
        
        
        return render_template("uploadImg.html")
    if request.method == "GET":
        return render_template("uploadImg.html")


if "__main__" == __name__:
    app.run(debug=True)
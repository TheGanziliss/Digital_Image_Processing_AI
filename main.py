import numpy as np
from PIL import ImageGrab, Image
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from textblob import TextBlob
import time
import asyncio
import cv2
import ctypes
from threading import Thread
from datetime import datetime
import pyodbc
import os

screenX = 1920
screenY = 1080

saveOnce = True

secsSignalsList1 = []
secsSignalsList2 = []
secsSignalsList3 = []
secsSignalsList4 = []
secsSignalsList5 = []
secsSignalsList6 = []
secsSignalsList7 = []
secsSignalsList8 = []
secsSignalsList9 = []

# Grab some screen 1590,665  755,665
i = 61
a = 0
b = 0
c = 1
d = 1

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #Type your Tesseract.exe file path
tesseract1 = pytesseract

def CreateFile(bedName, lineName):
    curr_time = datetime.now()

    dirName = os.path.expanduser('~/Documents')  #Type the address of the directory where you will create the files
    dirName += "/" + bedName

    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")

    dirName += "/" + str(curr_time.year)

    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")

    dirName += "/" + str(curr_time.month)

    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")

    dirName += "/" + str(curr_time.day)

    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")

    dirName += "/" + str(curr_time.hour)

    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")

    dirName += "/" + lineName

    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")

    return dirName + '/'

def picMethod1(img, name, bedName): #Function written to adjust the width and aspect ratios of the received image (you can write a separate size scaling function for each parameter)
    Changedimg = np.array(img)
    Changedimg = cv2.resize(Changedimg, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    gray_image = cv2.cvtColor(Changedimg, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    threshold_img = cv2.bitwise_not(threshold_img)
    threshold_img = cv2.blur(threshold_img, (2, 2))
    curr_time = datetime.now()
    return threshold_img

def picMethod2(img, name, bedName):
    Changedimg = np.array(img)
    gray_image = cv2.cvtColor(Changedimg, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    threshold_img = cv2.bitwise_not(threshold_img)
    threshold_img = cv2.blur(threshold_img, (2, 2))
    curr_time = datetime.now()
    path = CreateFile(bedName,name)+str(curr_time.minute)+'%%'+str(curr_time.second)+".jpg"
    cv2.imwrite(path,threshold_img);
    return threshold_img

def picMethod61(img, name, bedName):
    Changedimg = np.array(img)
    threshold_img = cv2.blur(Changedimg, (2, 2))
    curr_time = datetime.now()
    path = CreateFile(bedName,name)+str(curr_time.minute)+'%%'+str(curr_time.second)+".jpg"
    cv2.imwrite(path,threshold_img);
    return threshold_img

def picMethod31(img, name, bedName):
    Changedimg = np.array(img)
    gray_image = cv2.cvtColor(Changedimg, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    threshold_img = cv2.bitwise_not(threshold_img)
    threshold_img = cv2.blur(threshold_img, (2, 2))
    curr_time = datetime.now()
    path = CreateFile(bedName,name)+str(curr_time.minute)+'%%'+str(curr_time.second)+".jpg"
    cv2.imwrite(path,threshold_img);
    return threshold_img

def picMethod3(img, name, bedName):
    Changedimg = np.array(img)
    gray_image = cv2.cvtColor(Changedimg, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    threshold_img = cv2.bitwise_not(threshold_img)
    curr_time = datetime.now()
    return threshold_img

def picMethod4(img, name, bedName):
    Changedimg = np.array(img)
    gray_image = cv2.cvtColor(Changedimg, cv2.COLOR_BGR2GRAY)
    _, thressed1 = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    threshold_img = cv2.bitwise_not(thressed1)
    curr_time = datetime.now()
    return threshold_img

def picMethod5(img, name, bedName):
    Changedimg = np.array(img)
    gray_image = cv2.cvtColor(Changedimg, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.bitwise_not(gray_image)
    _, threshold_img = cv2.threshold(threshold_img, 128, 255, cv2.THRESH_BINARY)
    curr_time = datetime.now()
    return threshold_img

def parseTheLines(Lines_): #Function written to parse the values of parameters
    SPO2 = -61
    sys = -61
    dia = -61
    mean = -61
    rr = -61
    temp = -61

    returnedClass = HbParameters()

    for val in Lines_:
        val = val.replace(" ", "")
        if "SPO2" in val:
            values = val.split("SPO2")[1]
            if "%" in values:
                value = values.split("%")[0]
                SPO2 = ConvertDec(values)
                if SPO2 < 0 and SPO2 > 100:
                    SPO2 = -61

        elif "ART1" in val:
            values = val.split("ART1")[1]
            if ("(" in values) and (")" in values) and ("/" in values):
                sys = ConvertDec(values.split("/")[0])
                if sys < 0 and sys > 370:
                    sys = -61
                dia = ConvertDec((values.split("/")[1]).split("(")[0])
                if dia < 0 and dia > 360:
                    dia = -61
                mean = ConvertDec((values.split("(")[1]).split(")")[0])
                if mean < 0 and mean > 360:
                    mean = -61

        elif "NBP" in val:
            values = val.split("NBP")[1]
            if ("(" in values) and (")" in values) and ("/" in values):
                sys = ConvertDec(values.split("/")[0])
                if sys < 0 and sys > 370:
                    sys = -61
                dia = ConvertDec((values.split("/")[1]).split("(")[0])
                if dia < 0 and dia > 360:
                    dia = -61
                mean = ConvertDec((values.split("(")[1]).split(")")[0])
                if mean < 0 and mean > 360:
                    mean = -61

        elif "of-of" in val:
            rr = ConvertDec(val.split("of-of")[1])
            if rr < 0 and rr > 895:
                rr = -61

        elif "TP1Of" in val:
            # print(val)
            temp = ConvertDec((val.split("TP1Of")[1]).split("°C")[0])
            if temp < 0 and temp > 47:
                temp = -61

    returnedClass._SPO2 = SPO2
    returnedClass._sys = sys
    returnedClass._dia = dia
    returnedClass._mean = mean
    returnedClass._rr = rr
    returnedClass._temp = temp
    return returnedClass

def getHR(x, y, bedName): #The function written to find the size address in the image of the value that the parameters should read in the recorded image (written separately for each parameter)
    try:
        x1 = int((x + 120) * (screenX / 1920))
        y1 = int((y + 58) * (screenY / 1080))
        x = int(x * (screenX / 1920))
        y = int(y * (screenY / 1080))
        bed61Variable = ImageGrab.grab(bbox=(x, y, x1, y1))
        curr_time = datetime.now()
        threshold_img = picMethod2(bed61Variable, "HR", bedName)
        text = pytesseract.image_to_string(threshold_img, lang='eng',
                                           config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789/')
        correctedText = TextBlob(text).correct()
        return str(correctedText)
    except Exception as e:
        print(e + "1")

def getSpo2(x, y, bedName):
    try:
        x1 = int((x + 95) * (screenX / 1920))
        y1 = int((y + 24) * (screenY / 1080))
        x = int(x * (screenX / 1920))
        y = int(y * (screenY / 1080))
        bed61Variable = ImageGrab.grab(bbox=(x, y, x1, y1))
        curr_time = datetime.now()
        threshold_img = picMethod2(bed61Variable, "SPO2", bedName)
        text = pytesseract.image_to_string(threshold_img, lang='eng',
                                           config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789/')
        correctedText = TextBlob(text).correct()
        return str(correctedText)
    except Exception as e:
        print(e + "1")

def getRR(x, y, bedName):
    try:
        x1 = int((x + 95) * (screenX / 1920))
        y1 = int((y + 24) * (screenY / 1080))
        x = int(x * (screenX / 1920))
        y = int(y * (screenY / 1080))
        bed61Variable = ImageGrab.grab(bbox=(x, y, x1, y1))
        curr_time = datetime.now()
        threshold_img = picMethod2(bed61Variable, "RR", bedName)
        text = pytesseract.image_to_string(threshold_img, lang='eng',
                                           config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789/')
        correctedText = TextBlob(text).correct()
        return str(correctedText)
    except Exception as e:
        print(e + "1")

def getSYS(x, y, bedName):
    try:
        x1 = int((x + 35) * (screenX / 1920))
        y1 = int((y + 29) * (screenY / 1080))
        x = int(x * (screenX / 1920))
        y = int(y * (screenY / 1080))
        bed61Variable = ImageGrab.grab(bbox=(x, y, x1, y1))
        curr_time = datetime.now()
        threshold_img = picMethod2(bed61Variable, "SYS", bedName)
        text = pytesseract.image_to_string(threshold_img, lang='eng',
                                           config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789/()')
        correctedText = TextBlob(text).correct()
        return str(correctedText)
    except Exception as e:
        print(e + "1")

def getDIA(x, y, bedName):
    try:
        x1 = int((x + 50) * (screenX / 1920))
        y1 = int((y + 29) * (screenY / 1080))
        x = int(x * (screenX / 1920))
        y = int(y * (screenY / 1080))
        bed61Variable = ImageGrab.grab(bbox=(x, y, x1, y1))
        curr_time = datetime.now()
        threshold_img = picMethod2(bed61Variable, "DIA", bedName)
        text = pytesseract.image_to_string(threshold_img, lang='eng',
                                           config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789/()')
        correctedText = TextBlob(text).correct()
        return str(correctedText)
    except Exception as e:
        print(e + "1")

def getMEAN(x, y, bedName):
    try:
        x1 = int((x + 30) * (screenX / 1920))
        y1 = int((y + 29) * (screenY / 1080))
        x = int(x * (screenX / 1920))
        y = int(y * (screenY / 1080))
        bed61Variable = ImageGrab.grab(bbox=(x, y, x1, y1))
        curr_time = datetime.now()
        threshold_img = picMethod2(bed61Variable, "MEAN", bedName)
        text = pytesseract.image_to_string(threshold_img, lang='eng',
                                           config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789/()')
        correctedText = TextBlob(text).correct()
        return str(correctedText)
    except Exception as e:
        print(e + "1")

def getTemp(x, y, bedName):
    try:
        x1 = int((x + 120) * (screenX / 1920))
        y1 = int((y + 58) * (screenY / 1080))
        x = int(x * (screenX / 1920))
        y = int(y * (screenY / 1080))
        bed61Variable = ImageGrab.grab(bbox=(x, y, x1, y1))
        curr_time = datetime.now()
        threshold_img = picMethod2(bed61Variable, "TEMP", bedName)
        text = pytesseract.image_to_string(threshold_img, lang='eng',
                                           config='--psm 8 --oem 3 -c tessedit_char_whitelist=01234567.89/')
        correctedText = TextBlob(text).correct()

        return str(correctedText)
    except Exception as e:
        print(e + "1")

def getLinex(x, y, bedName):
    try:
        x1 = int((x + 145) * (screenX / 1920))
        y1 = int((y + 80) * (screenY / 1080))
        x = int(x * (screenX / 1920))
        y = int(y * (screenY / 1080))
        bed61Variable = ImageGrab.grab(bbox=(x, y, x1, y1))
        threshold_img = picMethod2(bed61Variable, bedName + "SUAT")
        text = pytesseract.image_to_string(threshold_img, lang='eng',
                                           config='--psm 7 --oem 3 -c tessedit_char_whitelist= TRABZONSPOR61/()-')
        correctedText = TextBlob(text).correct()
        return str(correctedText)
    except Exception as e:
        print(e + "2")

def getLine(x, y, bedName,lineName):
    try:
        x1 = int((x + 220) * (screenX / 1920))
        y1 = int((y + 25) * (screenY / 1080))
        x = int(x * (screenX / 1920))
        y = int(y * (screenY / 1080))
        bedGrab = ImageGrab.grab(bbox=(x, y, x1, y1))
        threshold_img = picMethod31(bedGrab, lineName, bedName)
        text = pytesseract.image_to_string(threshold_img, lang='eng',
                                           config='--psm 7 --oem 3 -c tessedit_char_whitelist= QWERTYUIOPASDFGHJKLZXCVBNM0123456789/()-')
        correctedText = TextBlob(text).correct()
        return str(correctedText)
    except Exception as e:
        print(e + "2")

def getValues1():
    while 1:
        try:
            bedName = "BED_1"
            HR = ConvertDec(getHR(620, 62 , bedName))
            SPO2 = ConvertDec(getSpo2(805, 62 , bedName))
            sys = ConvertDec(getSYS(615, 142 , bedName))
            dia = ConvertDec(getDIA(700, 142 , bedName))
            mean = ConvertDec(getMEAN(657, 170 , bedName))
            rr = ConvertDec(getRR(620, 218 , bedName))
            temp = ConvertDec(getTemp(805, 218 , bedName))

            output = ""
            output += "\n**********************************"
            output += "\nBED ID :" + bedName
            output += "\nHR:" + str(HR)
            output += "\nSPO2:" + str(SPO2)
            output += "\nSYS:" + str(sys)
            output += "\nDIA:" + str(dia)
            output += "\nMEAN:" + str(mean)
            output += "\nRR:" + str(rr)
            output += "\nTEMP:" + str(temp)
            output += "\n**********************************"

            print(output)
            output = ""

            bed1Parameters = HbParameters()
            bed1Parameters._hr = HR
            bed1Parameters._SPO2 = SPO2
            bed1Parameters._sys = sys
            bed1Parameters._dia = dia
            bed1Parameters._mean = mean
            bed1Parameters._rr = rr
            bed1Parameters._temp = temp
            secsSignalsList1.append(bed1Parameters)

            time.sleep(2.5);

        except Exception as e:
            print(e)

def getValues2():
    while 1:
        try:
            bedName = "BED_2"
            HR = ConvertDec(getHR(620+965, 62 , bedName))
            SPO2 = ConvertDec(getSpo2(805+965, 62 , bedName))
            sys = ConvertDec(getSYS(615+965, 142 , bedName))
            dia = ConvertDec(getDIA(700+965, 142 , bedName))
            mean = ConvertDec(getMEAN(657+965, 170 , bedName))
            rr = ConvertDec(getRR(620+965, 218 , bedName))
            temp = ConvertDec(getTemp(805+965, 218 , bedName))

            output = ""
            output += "\n**********************************"
            output += "\nBED ID :" + bedName
            output += "\nHR:" + str(HR)
            output += "\nSPO2:" + str(SPO2)
            output += "\nSYS:" + str(sys)
            output += "\nDIA:" + str(dia)
            output += "\nMEAN:" + str(mean)
            output += "\nRR:" + str(rr)
            output += "\nTEMP:" + str(temp)
            output += "\n**********************************"

            print(output)
            output = ""

            bed1Parameters = HbParameters()
            bed1Parameters._hr = HR
            bed1Parameters._SPO2 = SPO2
            bed1Parameters._sys = sys
            bed1Parameters._dia = dia
            bed1Parameters._mean = mean
            bed1Parameters._rr = rr
            bed1Parameters._temp = temp
            secsSignalsList1.append(bed1Parameters)

            time.sleep(2.5);

        except Exception as e:
            print(e)

def getValues3():
    while 1:
        try:
            bedName = "BED_3"
            HR = ConvertDec(getHR(620, 62 +240 , bedName))
            SPO2 = ConvertDec(getSpo2(805, 62+240 , bedName))
            sys = ConvertDec(getSYS(615, 142+240 , bedName))
            dia = ConvertDec(getDIA(700, 142+240, bedName))
            mean = ConvertDec(getMEAN(657, 170+240, bedName))
            rr = ConvertDec(getRR(620, 218+240, bedName))
            temp = ConvertDec(getTemp(805, 218 +240, bedName))

            output = ""
            output += "\n**********************************"
            output += "\nBED ID :" + bedName
            output += "\nHR:" + str(HR)
            output += "\nSPO2:" + str(SPO2)
            output += "\nSYS:" + str(sys)
            output += "\nDIA:" + str(dia)
            output += "\nMEAN:" + str(mean)
            output += "\nRR:" + str(rr)
            output += "\nTEMP:" + str(temp)
            output += "\n**********************************"

            print(output)
            output = ""

            bed1Parameters = HbParameters()
            bed1Parameters._hr = HR
            bed1Parameters._SPO2 = SPO2
            bed1Parameters._sys = sys
            bed1Parameters._dia = dia
            bed1Parameters._mean = mean
            bed1Parameters._rr = rr
            bed1Parameters._temp = temp
            bed1Parameters.append(bed1Parameters)

            time.sleep(2.5);

        except Exception as e:
            print(e)

def getValues4():
    while 1:
        try:
            bedName = "BED_4"
            HR = ConvertDec(getHR(620+965, 62+240 , bedName))
            SPO2 = ConvertDec(getSpo2(805+965, 62+240 , bedName))
            sys = ConvertDec(getSYS(615+965, 142+240 , bedName))
            dia = ConvertDec(getDIA(700+965, 142+240 , bedName))
            mean = ConvertDec(getMEAN(657+965, 170+240 , bedName))
            rr = ConvertDec(getRR(620+965, 218+240 , bedName))
            temp = ConvertDec(getTemp(805+965, 218+240 , bedName))

            output = ""
            output += "\n**********************************"
            output += "\nBED ID :" + bedName
            output += "\nHR:" + str(HR)
            output += "\nSPO2:" + str(SPO2)
            output += "\nSYS:" + str(sys)
            output += "\nDIA:" + str(dia)
            output += "\nMEAN:" + str(mean)
            output += "\nRR:" + str(rr)
            output += "\nTEMP:" + str(temp)
            output += "\n**********************************"

            print(output)
            output = ""

            bed1Parameters = HbParameters()
            bed1Parameters._hr = HR
            bed1Parameters._SPO2 = SPO2
            bed1Parameters._sys = sys
            bed1Parameters._dia = dia
            bed1Parameters._mean = mean
            bed1Parameters._rr = rr
            bed1Parameters._temp = temp
            secsSignalsList1.append(bed1Parameters)

            time.sleep(2.5);

        except Exception as e:
            print(e)

def getValues5():
    while 1:
        try:
            bedName = "BED_5"
            HR = ConvertDec(getHR(620, 62 +480 , bedName))
            SPO2 = ConvertDec(getSpo2(805, 62+480 , bedName))
            sys = ConvertDec(getSYS(615, 142+480 , bedName))
            dia = ConvertDec(getDIA(700, 142+480, bedName))
            mean = ConvertDec(getMEAN(657, 170+480, bedName))
            rr = ConvertDec(getRR(620, 218+480, bedName))
            temp = ConvertDec(getTemp(805, 218+480, bedName))

            output = ""
            output += "\n**********************************"
            output += "\nBED ID :" + bedName
            output += "\nHR:" + str(HR)
            output += "\nSPO2:" + str(SPO2)
            output += "\nSYS:" + str(sys)
            output += "\nDIA:" + str(dia)
            output += "\nMEAN:" + str(mean)
            output += "\nRR:" + str(rr)
            output += "\nTEMP:" + str(temp)
            output += "\n**********************************"

            print(output)
            output = ""

            bed1Parameters = HbParameters()
            bed1Parameters._hr = HR
            bed1Parameters._SPO2 = SPO2
            bed1Parameters._sys = sys
            bed1Parameters._dia = dia
            bed1Parameters._mean = mean
            bed1Parameters._rr = rr
            bed1Parameters._temp = temp
            secsSignalsList1.append(bed1Parameters)

            time.sleep(2.5);

        except Exception as e:
            print(e)

def getValues6():
    while 1:
        try:
            bedName = "BED_6"
            HR = ConvertDec(getHR(760+425, 106+480 , bedName))
            SPO2 = ConvertDec(getSpo2(75+965, 152+480, bedName))
            sys = ConvertDec(getSYS(90+965, 212+470 , bedName))
            dia = ConvertDec(getDIA(160+965, 212+470 , bedName))
            mean = ConvertDec(getMEAN(205+955, 210+475, bedName))
            rr = ConvertDec(getRR(620+965, 218+480 , bedName))
            temp = ConvertDec(getTemp(805+965, 218+480 , bedName))

            output = ""
            output += "\n**********************************"
            output += "\nBED ID :" + bedName
            output += "\nHR:" + str(HR)
            output += "\nSPO2:" + str(SPO2)
            output += "\nSYS:" + str(sys)
            output += "\nDIA:" + str(dia)
            output += "\nMEAN:" + str(mean)
            output += "\nRR:" + str(rr)
            output += "\nTEMP:" + str(temp)
            output += "\n**********************************"

            print(output)
            output = ""

            bed1Parameters = HbParameters()
            bed1Parameters._hr = HR
            bed1Parameters._SPO2 = SPO2
            bed1Parameters._sys = sys
            bed1Parameters._dia = dia
            bed1Parameters._mean = mean
            bed1Parameters._rr = rr
            bed1Parameters._temp = temp
            secsSignalsList1.append(bed1Parameters)

            time.sleep(2.5);

        except Exception as e:
            print(e)

def getValues7():
    while 1:
        try:
            bedName = "BED_7"
            HR = ConvertDec(getHR(760 + 375, 106 + 480, bedName))
            SPO2 = ConvertDec(getSpo2(1020, 62 + 580, bedName))
            sys = ConvertDec(getSYS(1121, 102 + 580, bedName))
            dia = ConvertDec(getDIA(1067, 104 + 580, bedName))
            mean = ConvertDec(getMEAN(1162, 102 + 580, bedName))
            rr = ConvertDec(getRR(1020, 62 + 580, bedName))
            temp = ConvertDec(getTemp(760 + 365, 106 + 480, bedName))

            output = ""
            output += "\n**********************************"
            output += "\nBED ID :" + bedName
            output += "\nHR:" + str(HR)
            output += "\nSPO2:" + str(SPO2)
            output += "\nSYS:" + str(sys)
            output += "\nDIA:" + str(dia)
            output += "\nMEAN:" + str(mean)
            output += "\nRR:" + str(rr)
            output += "\nTEMP:" + str(temp)
            output += "\n**********************************"

            print(output)
            output = ""

            bed1Parameters = HbParameters()
            bed1Parameters._hr = HR
            bed1Parameters._SPO2 = SPO2
            bed1Parameters._sys = sys
            bed1Parameters._dia = dia
            bed1Parameters._mean = mean
            bed1Parameters._rr = rr
            bed1Parameters._temp = temp

            secsSignalsList7.append(bed1Parameters)

            time.sleep(2.5)

        except Exception as e:
            print(e)

def getValues8():
    while 1:
        try:
            bedName = "BED_8"
            HR = ConvertDec(getHR(1150, 620 + 247, bedName))
            SPO2 = -61
            sys = -61
            dia = -61
            mean = -61
            rr = -61
            temp = -61
            line1 = getLine(1026, 914, bedName,"line1")
            line2 = getLine(1026, 938, bedName,"line2")
            line3 = getLine(1026, 962, bedName,"line3")
            line4 = getLine(1026, 986, bedName,"line4")
            line5 = getLine(1026, 1010, bedName,"line5")
            line6 = getLine(1026, 1034, bedName,"line6")

            Lines = [line1, line2, line3, line4, line5, line6]

            outputClass = parseTheLines(Lines);

            SPO2 = outputClass._SPO2
            sys = outputClass._sys
            dia = outputClass._dia
            mean = outputClass._mean
            rr = outputClass._rr
            temp = outputClass._temp

            output = ""
            output += "\n**********************************"
            output += "\nBED ID :" + bedName
            output += "\nHR:" + str(HR)
            output += "\nSPO2:" + str(SPO2)
            output += "\nSYS:" + str(sys)
            output += "\nDIA:" + str(dia)
            output += "\nMEAN:" + str(mean)
            output += "\nRR:" + str(rr)
            output += "\nTEMP:" + str(temp)
            output += "\n**********************************"

            print(output)
            output = ""

            bed8Parameters = HbParameters()
            bed8Parameters._hr = HR
            bed8Parameters._SPO2 = SPO2
            bed8Parameters._sys = sys
            bed8Parameters._dia = dia
            bed8Parameters._mean = mean
            bed8Parameters._rr = rr
            bed8Parameters._temp = temp
            secsSignalsList8.append(bed8Parameters)

            time.sleep(2.5);

        except Exception as e:
            print(e)

def getValues9():
    while 1:
        try:
            bedName = "BED_9"

            HR = ConvertDec(getHR(1150 + 638, 373 - 247, bedName))
            SPO2 = -61
            sys = -61
            dia = -61
            mean = -61
            rr = -61
            temp = -61
            line1 = getLine(1027 + 638, 669 - 493, bedName,"line1")
            line2 = getLine(1027 + 638, 693 - 493, bedName,"line2")
            line3 = getLine(1027 + 638, 717 - 493, bedName,"line3")
            line4 = getLine(1027 + 638, 741 - 493, bedName,"line4")
            line5 = getLine(1027 + 638, 765 - 493, bedName,"line5")
            line6 = getLine(1027 + 638, 789 - 493, bedName,"line6")

            Lines = [line1, line2, line3, line4, line5, line6]

            outputClass = parseTheLines(Lines);

            SPO2 = outputClass._SPO2
            sys = outputClass._sys
            dia = outputClass._dia
            mean = outputClass._mean
            rr = outputClass._rr
            temp = outputClass._temp

            output = ""
            output += "\n**********************************"
            output += "\nBED ID :" + bedName
            output += "\nHR:" + str(HR)
            output += "\nSPO2:" + str(SPO2)
            output += "\nSYS:" + str(sys)
            output += "\nDIA:" + str(dia)
            output += "\nMEAN:" + str(mean)
            output += "\nRR:" + str(rr)
            output += "\nTEMP:" + str(temp)
            output += "\n**********************************"

            print(output)
            output = ""

            bed9Parameters = HbParameters()
            bed9Parameters._hr = HR
            bed9Parameters._SPO2 = SPO2
            bed9Parameters._sys = sys
            bed9Parameters._dia = dia
            bed9Parameters._mean = mean
            bed9Parameters._rr = rr
            bed9Parameters._temp = temp
            secsSignalsList9.append(bed9Parameters)
            time.sleep(2.5);

        except Exception as e:
            print(e)

def getBedValueFromCrop(xArray,yArray,bedName):
    while 1:
        try:
            HR = ConvertDec(getHR(xArray[0],yArray[0], bedName))
            SPO2 = -61
            sys = -61
            dia = -61
            mean = -61
            rr = -61
            temp = -61
            line1 = getLine(xArray[1],yArray[1], bedName,"line1")
            line2 = getLine(xArray[2],yArray[2], bedName,"line2")
            line3 = getLine(xArray[3],yArray[3],bedName,"line3")
            line4 = getLine(xArray[4],yArray[4], bedName,"line4")
            line5 = getLine(xArray[5],yArray[5], bedName,"line5")
            line6 = getLine(xArray[6],yArray[6], bedName,"line6")

            Lines = [line1, line2, line3, line4, line5, line6]

            outputClass = parseTheLines(Lines);

            SPO2 = outputClass._SPO2
            sys = outputClass._sys
            dia = outputClass._dia
            mean = outputClass._mean
            rr = outputClass._rr
            temp = outputClass._temp

            output = ""
            output += "\n**********************************"
            output += "\nBED ID :" + bedName
            output += "\nHR:" + str(HR)
            output += "\nSPO2:" + str(SPO2)
            output += "\nSYS:" + str(sys)
            output += "\nDIA:" + str(dia)
            output += "\nMEAN:" + str(mean)
            output += "\nRR:" + str(rr)
            output += "\nTEMP:" + str(temp)
            output += "\n**********************************"

            print(output)
            output = ""

            bed9Parameters = HbParameters()
            bed9Parameters._hr = HR
            bed9Parameters._SPO2 = SPO2
            bed9Parameters._sys = sys
            bed9Parameters._dia = dia
            bed9Parameters._mean = mean
            bed9Parameters._rr = rr
            bed9Parameters._temp = temp
            secsSignalsList9.append(bed9Parameters)
            time.sleep(2.5);

        except Exception as e:
            print(e)

def ConvertDec(val):
    try:
        return float(val)
    except Exception as e:
        # print(e)
        return -61

def getAvarageOfClass(listOfClass):
    ReturnedClass = HbParameters()

    totalHr = 0
    Divider = 0

    for val in listOfClass:
        if (val._hr == -61):
            continue
        Divider += 1
        totalHr += val._hr

    try:
        ReturnedClass._hr = totalHr / Divider
    except:
        print("Exception in convert avarage")

    totalspo2 = 0
    Divider = 0

    for val in listOfClass:
        if (val._SPO2 == -61):
            continue
        Divider += 1
        totalspo2 += val._SPO2

    try:
        ReturnedClass._SPO2 = totalspo2 / Divider
    except:
        print("Exception in convert avarage")

    totalsys = 0
    Divider = 0

    for val in listOfClass:
        if (val._sys == -61):
            continue
        Divider += 1
        totalsys += val._sys

    try:
        ReturnedClass._sys = totalsys / Divider
    except:
        print("Exception in convert avarage")

    totaldia = 0
    Divider = 0

    for val in listOfClass:
        if (val._dia == -61):
            continue
        Divider += 1
        totaldia += val._dia

    try:
        ReturnedClass._dia = totaldia / Divider
    except:
        print("Exception in convert avarage")

    totalmean = 0
    Divider = 0

    for val in listOfClass:
        if (val._mean == -61):
            continue
        Divider += 1
        totalmean += val._mean

    try:
        ReturnedClass._mean = totalmean / Divider
    except:
        print("Exception in convert avarage")

    totalrr = 0
    Divider = 0

    for val in listOfClass:
        if (val._rr == -61):
            continue
        Divider += 1
        totalrr += val._rr

    try:
        ReturnedClass._rr = totalrr / Divider
    except:
        print("Exception in convert avarage")

    totaltemp = 0
    Divider = 0

    for val in listOfClass:
        if (val._temp == -61):
            continue
        Divider += 1
        totaltemp += val._temp

    try:
        ReturnedClass._temp = totaltemp / Divider
    except:
        print("Exception in convert avarage")

    return ReturnedClass

def savetoDb(bedId, signalId, value):
    try:
        if value < 0:
            return

        cursor.execute('SELECT PatientId FROM MedicalHosp.dbo.Patient where BedId = ' + bedId + ' and ReleaseDate is null')
        patientId = 0
        for i in cursor:
            patientId = i[0]
        print(patientId)
        count = cursor.execute("""
        INSERT INTO MedicalHosp.dbo.PtSignal (PatientId,SignalId,Value,Date,Time,AddDate,AddTime,ManuelMi) values(?,?,?,GETDATE(),convert(varchar(5), GETDATE(), 108),GETDATE(),convert(varchar(10), GETDATE(), 108),0)""",
                               patientId, signalId, value).rowcount
        conn.commit()
        print('Rows inserted: ' + str(count))
    except:
        print("Sql Error!")

def main():

    Thread(target=getValues1).start()
    Thread(target=getValues2).start()
    Thread(target=getValues3).start()
    Thread(target=getValues4).start()
    Thread(target=getValues5).start()
    Thread(target=getValues6).start()
    Thread(target=getValues7).start()
    Thread(target=getValues8).start()
    Thread(target=getValues9).start()

    print("This will be printed immediately")


if __name__ == "__main__":
    main()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class HbParameters:
    _hr = -61
    _SPO2 = -61
    _sys = -61
    _dia = -61
    _mean = -61
    _rr = -61
    _temp = -61

while 1:

    time.sleep(5)

    print("While Start")
    currentTime = datetime.now()
    if (((currentTime.minute % 2) == 0) and saveOnce):

        ScreenShot = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        path = CreateFile("Hospital SS LOGS", "ss") + str(currentTime.minute) + '%%' + str(currentTime.second) + ".jpg"
        ScreenShot = np.array(ScreenShot)
        cv2.imwrite(path, ScreenShot);

        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=Please write your IP address;'
                              'Database=Please write your DB name;'
                              'uid=Please write your Sql login name;'
                              'pwd=Please write your Sql password;')

        cursor = conn.cursor()

        print("Save")

        _bed1 = getAvarageOfClass(secsSignalsList1)
        secsSignalsList1.clear()

        savetoDb("1", 25, _bed1._hr);
        savetoDb("1", 0, _bed1._mean);
        savetoDb("1", 1, _bed1._dia);
        savetoDb("1", 2, _bed1._sys);
        savetoDb("1", 66, _bed1._SPO2);
        savetoDb("1", 74, _bed1._temp);
        savetoDb("1", 59, _bed1._rr);

        _bed2 = getAvarageOfClass(secsSignalsList2)
        secsSignalsList2.clear()

        savetoDb("2", 25, _bed2._hr);
        savetoDb("2", 0, _bed2._mean);
        savetoDb("2", 1, _bed2._dia);
        savetoDb("2", 2, _bed2._sys);
        savetoDb("2", 66, _bed2._SPO2);
        savetoDb("2", 74, _bed2._temp);
        savetoDb("2", 59, _bed2._rr);

        _bed3 = getAvarageOfClass(secsSignalsList3)
        secsSignalsList3.clear()

        savetoDb("3", 25, _bed3._hr);
        savetoDb("3", 0, _bed3._mean);
        savetoDb("3", 1, _bed3._dia);
        savetoDb("3", 2, _bed3._sys);
        savetoDb("3", 66, _bed3._SPO2);
        savetoDb("3", 74, _bed3._temp);
        savetoDb("3", 59, _bed3._rr);

        _bed4 = getAvarageOfClass(secsSignalsList4)
        secsSignalsList4.clear()

        savetoDb("4", 25, _bed4._hr);
        savetoDb("4", 0, _bed4._mean);
        savetoDb("4", 1, _bed4._dia);
        savetoDb("4", 2, _bed4._sys);
        savetoDb("4", 66, _bed4._SPO2);
        savetoDb("4", 74, _bed4._temp);
        savetoDb("4", 59, _bed4._rr);

        _bed5 = getAvarageOfClass(secsSignalsList5)
        secsSignalsList5.clear()

        savetoDb("5",25,_bed5._hr);
        savetoDb("5",0,_bed5._mean);
        savetoDb("5",1,_bed5._dia);
        savetoDb("5",2,_bed5._sys);
        savetoDb("5",66,_bed5._SPO2);
        savetoDb("5",74,_bed5._temp);
        savetoDb("5",59,_bed5._rr);

        _bed6 = getAvarageOfClass(secsSignalsList6)
        secsSignalsList6.clear()

        savetoDb("6",25, _bed6._hr);
        savetoDb("6",0, _bed6._mean);
        savetoDb("6",1, _bed6._dia);
        savetoDb("6",2, _bed6._sys);
        savetoDb("6",66, _bed6._SPO2);
        savetoDb("6",74, _bed6._temp);
        savetoDb("6",59, _bed6._rr);

        _bed7 = getAvarageOfClass(secsSignalsList7)
        secsSignalsList7.clear()

        savetoDb("7", 25, _bed7._hr);
        savetoDb("7", 0, _bed7._mean);
        savetoDb("7", 1, _bed7._dia);
        savetoDb("7", 2, _bed7._sys);
        savetoDb("7", 66, _bed7._SPO2);
        savetoDb("7", 74, _bed7._temp);
        savetoDb("7", 59, _bed7._rr);

        _bed8 = getAvarageOfClass(secsSignalsList8)
        secsSignalsList8.clear()

        savetoDb("8",25,_bed8._hr);
        savetoDb("8",0,_bed8._mean);
        savetoDb("8",1,_bed8._dia);
        savetoDb("8",2,_bed8._sys);
        savetoDb("8",66,_bed8._SPO2);
        savetoDb("8",74,_bed8._temp);
        savetoDb("8",59,_bed8._rr);

        _bed9 = getAvarageOfClass(secsSignalsList9)
        secsSignalsList9.clear()

        savetoDb("9", 25, _bed9._hr);
        savetoDb("9", 0, _bed9._mean);
        savetoDb("9", 1, _bed9._dia);
        savetoDb("9", 2, _bed9._sys);
        savetoDb("9", 66, _bed9._SPO2);
        savetoDb("9", 74, _bed9._temp);
        savetoDb("9", 59, _bed9._rr);

        print(
            _bed1._hr + _bed2._hr + _bed3._hr + _bed4._hr + _bed5._hr + _bed6._hr + _bed7._hr + _bed8._hr + _bed9._hr)

        cursor.close()
        conn.close()

        saveOnce = False
    elif ((currentTime.minute % 2) != 0):
        print("Wait")
        saveOnce = True
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 16:36:54 2017

@author: Harish
"""

from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup
from numpy import mean
from os.path import isfile
import re
import time



def initializeFiles():
    """
    This function Creates/Opens a CSV file to update price values
    and a TXT file that serves as a log
    """
    ## Create a CSV file or Open Existing one
    ## This file stores the observations
    if not isfile("turDalPrices.csv"):
        try:
            fileHandle = open("turDalPrices.csv","a")
            ## Create header for the CSV file
            fileHandle.write("Source, LastUpdated, LastFetched, Variety, MinPrice, MaxPrice, Price, UnitOfPrice")
            fileHandle.write("\n")
        except PermissionError:
            print("Error: Cannot open the CSV file. Please close any active instances of that file")
            exit
            
    else:
        try:
            fileHandle = open("turDalPrices.csv","a")
        except PermissionError:
            print("Error: Cannot open the CSV file. Please close any active instances of that file")
            exit
        
        
    ## Open/Create a log file
    try:
        logFileHandle = open("log.txt","w")
    except PermissionError:
        print("Error: Cannot open the LOG file. Please close any active instance of that file")
        exit
    
    logFileHandle.write("Program Initialized at {0}".format(time.strftime("%d %b %Y %H:%M")))
    logFileHandle.write("\n")
    
    try:
        return fileHandle,logFileHandle
    except NameError:
        return None, None



def URL1(lastFetched, fileHandle, logFileHandle):
    ## URL1
    logFileHandle.write("URL1 called...")
    logFileHandle.write("\n")
    ## Read data
    url1 = "http://agmarknet.nic.in/rep1Newx1_today.asp"
    try:
        rawData1 = urlopen(url1)
    except URLError:
        print("URL1: Your URL returned an error. Please check the URL")
        logFileHandle.write("URL1: Your URL returned an error. Please check the URL")
        logFileHandle.write("\n")
        
    
    ## Convert raw data into Python Object
    data1 = BeautifulSoup(rawData1.read(),"lxml")
        
    ## Grab the last updated date
    patt = re.compile(r'[0-9]+/[0-9]+/[0-9]+')
    lastUpdated = data1.find(text=patt)
    if lastUpdated==None:
        print("Warning: Last updated element not found")
        logFileHandle.write("Warning: Last updated element not found")
        logFileHandle.write("\n")
        lastUpdated = "NA"
        
    ## Look for Arhar Dal(Tur) - tentative
    targObj = data1.find(text="Arhar Dal(Tur)")
    if targObj==None:
        print("Warning: Arhar Dal(Tur Dal) Element is not found. Possibly, It wasn't updated yet or Site layout might have changed")
        logFileHandle.write("Warning: Arhar Dal(Tur Dal) Element is not found. Possibly, It wasn't updated yet or Site layout might have changed")
        logFileHandle.write("\n")
        maxPrice = "NA"
        minPrice = "NA"
        price = "NA"
    else:
        ## TODO: Think about the possible failures here and handle 'em
        maxPrice = int(targObj.find_next().get_text())
        temp = targObj.find_next("td")
        minPrice = int(temp.find_next("td").get_text())
        price = mean([maxPrice,minPrice])
    
    ## Update variables to write
    source = "agmarknet"
    variety = "Arthar Dal(Tur)"
    unitOfPrice = "Rs/Quintal"
    
    ## TODO: This could be implemented as a function
    ## Write this record to the file
    fileHandle.write(source+','+lastUpdated+','+lastFetched+','+variety+','+str(minPrice)+','+str(maxPrice)+','+str(price)+','+unitOfPrice)
    fileHandle.write("\n")
    



def URL2(lastFetched, fileHandle, logFileHandle):
    ## URL2
    logFileHandle.write("URL2 called...")
    logFileHandle.write("\n")
    ## Read data
    url2 = "https://www.commodityonline.com/mandiprices/arhar/yeotmal/1892049"
    try:
        rawData2 = urlopen(url2)
    except URLError:
        print("URL2: Your URL returned an error. Please check the URL")
        logFileHandle.write("URL2: Your URL returned an error. Please check the URL")
        logFileHandle.write("\n")
        
    ## Convert raw data into Python Object
    data2 = BeautifulSoup(rawData2.read(),"lxml")
    
    ## Grab the last updated date
    lastUpdated = data2.find(text=" Last Updated :")
    if lastUpdated==None:
        print("Warning: Attribute 'Last Updated' not found. Site layout may have been changed")
        logFileHandle.write("Warning: Attribute 'Last Updated' not found. Site layout may have been changed")
        logFileHandle.write("\n")
        lastUpdated = "NA"
    else:
        lastUpdated = lastUpdated.find_next().get_text()
    
    variety = data2.find(text="Variety")
    if variety==None:
        print("Warning: Attribute 'Variety' not found. Site layout may have been changed")
        logFileHandle.write("Warning: Attribute 'Variety' not found. Site layout may have been changed")
        logFileHandle.write("\n")
        variety = "NA"
    else:
        variety = variety.find_next().get_text()
    
    price = data2.find(text="Modal Price")
    if price==None:
        print("Warning: Attribute 'Modal Price' not found. Site layout may have been changed")
        logFileHandle.write("Warning: Attribute 'Modal Price' not found. Site layout may have been changed")
        logFileHandle.write("\n")
        price = "NA"
    else:
        price = price.find_next().get_text()
    
    unitOfPrice = data2.find(text="Unit of Price")
    if unitOfPrice==None:
        print("Warning: Attribute 'Unit Price' not found. Site layout may have been changed")
        logFileHandle.write("Warning: Attribute 'Unit Price' not found. Site layout may have been changed")
        logFileHandle.write("\n")
        unitOfPrice = "NA"
    else:
        unitOfPrice = unitOfPrice.find_next().get_text()
    
    minMax = data2.find(text="Min/Max Price")
    if minMax==None:
        print("Warning: Attribute 'Min/Max Price' not found. Site layout may have been changed")
        logFileHandle.write("Warning: Attribute 'Min/Max Price' not found. Site layout may have been changed")
        logFileHandle.write("\n")
        minPrice = "NA"
        maxPrice = "NA"
    else:
        minMax = minMax.find_next().get_text()
        minPrice = minMax.split('/')[0]
        maxPrice = minMax.split('/')[1]
        
    
    ## Update variables to write
    source = "Commodity-Online"
        
    ## Write this record to the file
    fileHandle.write(source+','+lastUpdated+','+lastFetched+','+variety+','+minPrice+','+maxPrice+','+price+','+unitOfPrice)
    fileHandle.write("\n")


##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<##

def URL3(lastFetched, fileHandle, logFileHandle):
    ## URL3
    logFileHandle.write("URL3 called...")
    logFileHandle.write("\n")
    ## Read data
    url3 = "http://www.agriwatch.com/pulses/tur-pigeon-peas/"
    try:
        rawData3 = urlopen(url3)
    except URLError:
        print("URL3: Your URL returned an error. Please check the URL")
        logFileHandle.write("URL3: Your URL returned an error. Please check the URL")
        logFileHandle.write("\n")
        
    
    data3 = BeautifulSoup(rawData3.read(),"lxml")
    
    ## When was it last updated - Get the date
    fDate = data3.find("th",{"class":"first_date"})
    if fDate==None:
        print("Warning: Attribute 'first_date' not found. Site layout may have been changed")
        logFileHandle.write("Warning: Attribute 'first_date' not found. Site layout may have been changed")
        logFileHandle.write("\n")
        lastUpdated = "NA"
    else:
        lastUpdated = fDate.get_text()
    
    ## Get the price in Mumbai
    obj = data3.find_all("td", text="Mumbai( Rs/Qtl )")
    if obj==None:
        print("Warning: Attribute 'Mumbai( Rs/Qtl )' not found. Site layout may have been changed")
        logFileHandle.write("Warning: Attribute 'Mumbai( Rs/Qtl )' not found. Site layout may have been changed")
        logFileHandle.write("\n")
        maxPrice = "NA"
        minPrice = "NA"
        price = "NA"
    tar = obj[0].find_next().contents
    try:
        variety = tar[0].get_text()
    except IndexError:
        print("Error: Index Error. Site layout may have been changed")
        logFileHandle.write("Error: Index Error. Site layout may have been changed")
        logFileHandle.write("\n")
        variety = "NA"
    
    try:
        minMax = tar[1].get_text()
        maxPrice = minMax.split('-')[1]
        minPrice = minMax.split('-')[0]
        price = mean([int(minPrice), int(maxPrice)])
    except IndexError:
        print("Error: Index Error. Site layout may have been changed")
        logFileHandle.write("Error: Index Error. Site layout may have been changed")
        logFileHandle.write("\n")
    
    unitOfPrice = "Rs/Quintal"
    source = "agriWatch"
    
    ## Write this record to the file
    fileHandle.write(source+','+lastUpdated+','+lastFetched+','+variety+','+minPrice+','+maxPrice+','+str(price)+','+unitOfPrice)
    fileHandle.write("\n")



if __name__=='__main__':
    ## Last Fetched time
    lastFetched = time.strftime("%b %d %Y")
    fileHandle, logFileHandle = initializeFiles()
    if fileHandle!=None and logFileHandle!=None:
        URL1(lastFetched, fileHandle, logFileHandle)
        URL2(lastFetched, fileHandle, logFileHandle)
        URL3(lastFetched, fileHandle, logFileHandle)
        fileHandle.close()
        logFileHandle.close()




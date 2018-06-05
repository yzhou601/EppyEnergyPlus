# EppyEnergyPlus




## Introduction

* This script could run EnergyPlus parametrically with Eppy package( [Eppy tutorial link](https://pythonhosted.org/eppy/Main_Tutorial.html)), generating new IDF files with different orientations in folder "idfs".

* This script also solves problems when automatically deploying one building IDF model to a large amount of different locations with loops of replacing the ddy information in IDFs and attaching epw files to run.

* Information in ddy file is extracted and used to replace the "sizing period" part in IDF files with Regex package([Regex Doc](https://docs.python.org/3/library/re.html)).

* All the weather files needed are initially stored in folder "weather" under the main directory. The locations need to run (weather file names without extensions) are listed in the WeatherFileNameList.csv file under "runtrial". This csv file could be written by reading the weather file name list in the weather directory with function "WriteEPWNameToCSV" or manually edited by entering the weather file name.

* The results of simulations would be stored in folders generated in "runtrial" repository.



### Variables and Paths

* The initial idf model is needed for energy simulation in different locations and generating new models parametrically.

* The paths to weather files (epw format and ddy format) are needed to deploy the building model to different locations.

* Paths in the scripts are all relative addresses.



### Functions


#### packddy(ddypath):

    This function helps pack up ddy files into blocks by recognizing blank lines as separations

    :param ddypath: This is the path to the directory where the ddy files are located

    :return: This function returns the lists of blocks which are lists of lines in ddy files



#### pickupblocks(packedlist, tar):

    This function has to be called after packddy function with an arguement of ddy block list, and this function is to pick up the blocks by a special string in the block

    :param packedlist: This is the packed ddy list with different blocks

    :param tar: This is a special string to recognize the target block

    :return: This function returns a dictionary of the picked block in which the key is the statement in ddy file after "!-"



#### updatesite(packedlist, idf):

    This function updates the site:Location information in idf file with that in ddy file, this function has to be called after packddy function with an argument of packed ddy list

    :param packedlist: This is the packed ddy list with different blocks

    :param idf: The initial input idf file

    :return: This function returns the site:location part updated idf file



#### updateddyitem(DP0, sizingperiod):

    This is the process function called by UpdateLocationInfinIDF function which updates each block of design day information

    :param DP0: This is the design period block picked from ddy file

    :param sizingperiod: This is the corresponding block in idf file

    :return: This function returns the updated block in IDF



#### UpdateLocationInfinIDF(idf1,ddyname):

    This function Automatically updates the location information as well as the design period information in an idf file

    :param idf1: the input idf file which needs to update the design day data and site information

    :param ddyname: This is the path to the directory in which the ddy files are located (relative to the working dir)

    :return: This function returns the updated idf file



### WriteEPWNameToCSV(WeatherPath, CsvPath, i):

    This function automatically writes the csv file with weather file names by reading the name list in the directory where these files stored.

    :param WeatherPath: This is the path to the directory where the weather files are stored

    :param CsvPath: This is the path to the .csv file

    :param i: This is the number of weather files written into the csv file in the loop

    :return: This function returns nothing



### ReadFileNameInCsv(dir):

    This function reads the file names stored in a .csv file

    :param dir: This is the path to the directory in which the csv files are located (relative to the working directory)

    :return: A list object in which each element is a file name as a string





# EppyEnergyPlus


## Introduction

* This script could run EnergyPlus parametrically with Eppy package( [Eppy tutorial link](https://pythonhosted.org/eppy/Main_Tutorial.html)), generating new IDF files with different orientations in folder "idfs".

* This script also solves problems when automatically deploying one building IDF model to a large amount of different locations with loops of replacing the ddy information in IDFs and attaching epw files to run.

* Information in ddy file is extracted and used to replace the "sizing period" part in IDF files with Regex package([Regex Doc](https://docs.python.org/3/library/re.html)).

* All the weather files in the database(.epw and .ddy) are downloaded and stored in folder "weather". The locations need to run (weather file names without extensions) are listed in the WeatherFileNameList.csv file under "runtrial". This csv file could be written by reading the weather file name list in the weather directory with function "WriteEPWNameToCSV" or manually edited by entering the weather file name.

* The results of simulations would be stored in folders generated in "runtrial" repository.



### Variables and Paths
* The initial idf model is needed for energy simulation in different locations and generating new models parametrically.

* The paths to weather files are relative addresses. They are not supposed to be changed if the directory is cloned with resources folder "weather". It should be updated if the local directory of weather files is used.

* The paths to idd and idf files are relative addresses as well. Please update.


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





### Heading 3
THis is where I will describe loops
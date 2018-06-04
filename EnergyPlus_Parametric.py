import csv
import os
import re
from eppy.modeleditor import IDF

##pack the file into blocks
def packddy(ddypath):
    '''
    This function helps pack up ddy files into blocks by recognizing blank lines as separations
    :param ddypath: This is the path to the directory where the ddy files are located
    :return: This function returns the lists of blocks which are lists of lines in ddy files
    '''
    start = ['  \n', ' \n', '\n']
    my_list = []    ##temporary list
    packedls = []   ##final packed list with blocks
    for line in open(ddypath,'rt').readlines():
        if line.startswith(start[0]) or line.startswith(start[1]) or line.startswith(start[2]):
            packedls.append(my_list)
            my_list = []
        else:
            my_list.append(line)
    return(packedls)

##pick up the needed blocks
def pickupblocks(packedlist, tar):
    '''
    This function has to be called after packddy function with an arguement of ddy block list, and this function is to pick up the blocks by a special string in the block
    :param packedlist: This is the packed ddy list with different blocks
    :param tar: This is a special string to recognize the target block
    :return: This function returns a dictionary of the picked block in which the key is the statement in ddy file after "!-"
    '''
    d = {}          ##store data in a dictionary

##Site:Location
    for blocks in packedlist:
        for lines in blocks:
            if tar in lines:
                for l in blocks:
                        y = l.replace(" ", "")
                        x = y.split("!-")
                        if len(x) > 1:
                            ##organize data and make the dictionary
                            regex1 = re.compile(r'{.*}\n')
                            regex2 = re.compile(r'\.*\n')
                            str1 = re.sub(regex1, '', x[1])
                            str2 = re.sub(regex2, '', str1)
                            str3 = re.sub("\d+","??", str2)
                            value = re.sub('[^A-Za-z0-9-._\s]+','',x[0])
                            ind = str3
                            d[ind] = value

    return(d)

def updatesite(packedlist, idf):
    '''
    This function updates the site:Location information in idf file with that in ddy file, this function has to be called after packddy function with an argument of packed ddy list
    :param packedlist: This is the packed ddy list with different blocks
    :param idf: The initial input idf file
    :return: This function returns the site:location part updated idf file
    '''
    idfsite = idf.idfobjects['SITE:LOCATION'][0]
    target = 'Site:Location'
    SiteInformation = pickupblocks(packedlist, target)
    idfsite.Name = SiteInformation.get('LocationName')
    idfsite.Latitude = SiteInformation.get('Latitude')
    idfsite.Longitude = SiteInformation.get('Longitude')
    idfsite.Time_Zone = SiteInformation.get('TimeZoneRelativetoGMT')
    idfsite.Elevation = SiteInformation.get('Elevation')
    return idfsite

##DDY
def updateddyitem(DP0, sizingperiod):
    '''
    This is the process function called by UpdateLocationInfinIDF function which updates each block of design day information
    :param DP0: This is the design period block picked from ddy file
    :param sizingperiod: This is the corresponding block in idf file
    :return: This function returns the updated block in IDF
    '''
    sizingperiod.Name = DP0.get('Name')
    sizingperiod.Month = DP0.get('Month')
    sizingperiod.Day_of_Month = DP0.get('DayofMonth')
    sizingperiod.Day_Type = DP0.get('DayType')
    sizingperiod.Maximum_DryBulb_Temperature = DP0.get('MaximumDry-BulbTemperature')
    sizingperiod.Daily_DryBulb_Temperature_Range = DP0.get('DailyDry-BulbTemperatureRange')
    sizingperiod.DryBulb_Temperature_Range_Modifier_Type = DP0.get('Dry-BulbTemperatureRangeModifierType')
    sizingperiod.DryBulb_Temperature_Range_Modifier_Day_Schedule_Name= DP0.get('Dry-BulbTemperatureRangeModifierScheduleName')
    sizingperiod.Humidity_Condition_Type= DP0.get('HumidityConditionType')
    if DP0.get('HumidityConditionType') == 'Wetbulb'or 'Enthalpy':
        if DP0.get('WetbulbatMaximumDry-Bulb') is None:
            sizingperiod.Wetbulb_or_DewPoint_at_Maximum_DryBulb = ''
        else:
            sizingperiod.Wetbulb_or_DewPoint_at_Maximum_DryBulb= DP0.get('WetbulbatMaximumDry-Bulb')
    if DP0.get('HumidityConditionType') == 'Dewpoint':
        sizingperiod.Wetbulb_or_DewPoint_at_Maximum_DryBulb = DP0.get('DewpointatMaximumDry-Bulb')
    sizingperiod.Humidity_Condition_Day_Schedule_Name=DP0.get('HumidityIndicatingDayScheduleName')
    sizingperiod.Humidity_Ratio_at_Maximum_DryBulb = DP0.get('HumidityRatioatMaximumDry-Bulb')
    sizingperiod.Enthalpy_at_Maximum_DryBulb = DP0.get('EnthalpyatMaximumDry-Bulb')
    sizingperiod.Daily_WetBulb_Temperature_Range = DP0.get('DailyWet-BulbTemperatureRange')
    sizingperiod.Barometric_Pressure = DP0.get('BarometricPressure')
    sizingperiod.Wind_Speed = DP0.get('WindSpeed{m/s}designconditionsvs.traditional??.??m/s(??mph)')
    sizingperiod.Wind_Direction = DP0.get('WindDirection')
    sizingperiod.Rain_Indicator = DP0.get('Rain')
    sizingperiod.Snow_Indicator = DP0.get('Snowonground')
    sizingperiod.Daylight_Saving_Time_Indicator = DP0.get('DaylightSavingsTimeIndicator')
    sizingperiod.Solar_Model_Indicator = DP0.get('SolarModelIndicator')
    sizingperiod.Beam_Solar_Day_Schedule_Name= DP0.get('BeamSolarDayScheduleName')
    sizingperiod.Diffuse_Solar_Day_Schedule_Name = DP0.get('DiffuseSolarDayScheduleName')
    sizingperiod.ASHRAE_Clear_Sky_Optical_Depth_for_Beam_Irradiance_taub = DP0.get('ASHRAEClearSkyOpticalDepthforBeamIrradiance(taub)')
    sizingperiod.ASHRAE_Clear_Sky_Optical_Depth_for_Diffuse_Irradiance_taud = DP0.get('ASHRAEClearSkyOpticalDepthforDiffuseIrradiance(taud)')
    return sizingperiod

def UpdateLocationInfinIDF(idf1,ddyname):
    '''
    This function Automatically updates the location information as well as the design period information in an idf file
    :param idf1: the input idf file which needs to update the design day data and site information
    :param ddyname: This is the path to the directory in which the ddy files are located (relative to the working dir)
    :return: This function returns the updated idf file
    '''
    DDYlist = ['Annual Cooling (DB=>MWB) .4%','Annual Cooling (DP=>MDB) .4%', 'Annual Cooling (Enthalpy=>MDB) .4%','Annual Cooling (WB=>MDB) .4%', 'Annual Heating 99.6%','Annual Heating Wind 99.6% Design Conditions WS=>MCDB','Annual Humidification 99.6% Design Conditions DP=>MCDB']
    for i in range(0, 7):
        sizingprd = idf1.idfobjects['SIZINGPERIOD:DESIGNDAY'][i]
        target = DDYlist[i]
        packedls = packddy(ddyname)
        DP = pickupblocks(packedls, target)
        ##print(DP)
        updateddyitem(DP, sizingprd)
        updatesite(packedls,idf1)
    return idf1

##write epw name into a .csv file for later use of weather file
def WriteEPWNameToCSV(WeatherPath, CsvPath, i):
    '''
    This function automatically writes the csv file with weather file names by reading the name list in the directory where these files stored.
    :param WeatherPath: This is the path to the directory where the weather files are stored
    :param CsvPath: This is the path to the .csv file
    :param i: This is the number of weather files written into the csv file in the loop
    :return: This function returns nothing
    '''
    ls = os.listdir(WeatherPath)
    print (ls)
    with open(CsvPath,'wt') as f:
        k = 0
        for epwitem in ls:
            if k < i:
                 f.writelines(os.path.splitext(epwitem)[0]+"\n")
                 k += 1

## read epw file names
def ReadFileNameInCsv(dir):
    '''
    This function reads the file names stored in a .csv file
    :param dir: This is the path to the directory in which the csv files are located (relative to the working directory)
    :return: A list object in which each element is a file name as a string
    '''
    with open(dir, 'rt') as f:
        filename_list = []
        for i in csv.reader(f):
            for j in i:
                filename_list.append(j)
                if j is None: break
            if i is None: break
        return filename_list

##set idd file
iddfile = "Energy+.idd"
IDF.setiddname(iddfile)
DirName = '../eppy_energy-'
WeatherDir = DirName+'/weather/weather_files_ddy_epw/'
epwDir = WeatherDir + 'epw/USA/'
ddyDir = WeatherDir + 'ddy/USA/'
CSVDir = DirName+'/runtrial/WeatherFileNameList.csv'
WriteEPWNameToCSV(epwDir, CSVDir , 8)
weatherfilename_list = ReadFileNameInCsv(CSVDir)

print(weatherfilename_list)

##run with different locations
for i in weatherfilename_list:
    epwname = epwDir + i +'.epw'         ##Before write the path, put weather files in EnergyPlus WeatherData folder
    ddyname = ddyDir + i +'.ddy'
    fname1 = DirName + '/runtrial/TrialKA2_Unsized.idf'
    idf1 = IDF(fname1, epwname)
    UpdateLocationInfinIDF(idf1,ddyname)
    ##idf1.printidf()
    building = idf1.idfobjects['BUILDING'][0]
    building.Name = "KA2 A Flatroof Sample Building"
    objectlist = idf1.idfobjects
    rundirname = u'../eppy_energy-/runtrial/'
    resultsdir = rundirname+'results'+i
    ##os.makedirs(resultsdir)
    idf1.saveas(DirName + "/idfs/"+i+'.idf')
    idf1.run(output_directory = resultsdir)

Axis = 0
while Axis in range(0,360):
    building.North_Axis = Axis
    ##idf1.saveas(DirName+'/idfs/Axises/'+str(Axis)+".idf")
    resultsdirAxis= rundirname+'results'+i+'Axis'+str(Axis)
    ##os.makedirs(resultsdirAxis)
    ##idf1.run(output_directory = resultsdirAxis)
    Axis += 45
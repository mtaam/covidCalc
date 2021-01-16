#!/usr/bin/python

import csv
import urllib.request
from io import StringIO

source = "c:/users\milt\downloads\covid_confirmed_usafacts (5).csv"
fnameSuffix = "n100k.csv"
popSrc = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_county_population_usafacts.csv"
popData=urllib.request.urlopen( popSrc ).read().decode('ascii', 'ignore')
pop = StringIO(popData)

caseSrc = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv"
caseData=urllib.request.urlopen( caseSrc ).read().decode('ascii', 'ignore')
cases = StringIO(caseData)

outFolder = "d:/temp/covidCases/"
usaFile = open( outFolder+"usa-"+fnameSuffix, 'w' )

#content = open( source )
with pop as popCsvfile, cases as casesCsvfile:
     popCsv = csv.reader(popCsvfile, delimiter=',')
     casesCsv = csv.reader(casesCsvfile, delimiter=',')
     i = 0
     for row, popRow in zip( casesCsv, popCsv ) :
         
         i += 1
         if i==1:
             date = row[len(row)-1]
             print( date )
             exit
         else :
             population = float( popRow[3] )
             if population == 0 :
                 norm100k = 0
             else :
                 norm100k = 1e5/ population
             county = row[1]
             #remove the last word in string, typically county but may be parish, etc
             county.replace("City and County", '' )
             county.replace( "County", '')
             county.replace( "Parish", '')
             
             split = county.split()
             split.pop()
             county = ''.join( split ).lower()
             #county = county[0:len(county)-7]
             #if county != "Tompkins" and  county != "Kings" :
             #    continue
             print( popRow[1], population, norm100k )
             for c in ['.', ' ', '/']:
                  county = county.replace( c, "_" )
             state = row[2]
             filename = str.format( outFolder+"{}-{}-"+fnameSuffix, state, county ).lower()
             print( filename )
             countyFile = open( filename, 'w' )
             s = str.format( "{}, {}", date, int(population) )
             for i in range( 1, 3) :
                 s =  s+str.format( ", {}", row[i] )
            #skip 3, state code
             numDays = 30
             for i in range( len(row)-numDays, len(row) ):
                 cases = int(row[i]);
                 #if cases > 0 :
                 s =  s+str.format( ", {:.0f}", cases*norm100k )
             #print( s  )
             usaFile.write( s + "\n" );
             countyFile.write( s )
             countyFile.close()
             #print(', '.join(row))
popCsvfile.close()
usaFile.close()

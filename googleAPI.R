library(RJSONIO)
library(rPython)
python.load("queMysql2GoogleAPI_simplied.py")

theresult <- python.get("Resultset_Geocoding_List")

head(theresult)




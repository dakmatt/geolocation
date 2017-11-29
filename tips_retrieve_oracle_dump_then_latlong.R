library(DBI)
library(RMySQL)
library(shiny)
library(RJDBC)
library(rPython)

# ahmad 
# 20 september 2016 
# 
# hang kena follow the sequence below 

# 1- build the connection 
drv <- JDBC("oracle.jdbc.OracleDriver",classPath="C:/app/TM33902/product/11.2.0/client_1/sqldeveloper/jdbc/lib/ojdbc5.jar", " ")
# Connect to the database
con <- dbConnect(drv, "jdbc:oracle:thin:@YOURURL:1521/YOURSCHEMA", "YOURID", "YOURPASSWORD")

# 2- get the data from oracle 
query <- sprintf("select A.ORDER_ID,A.ORDER_TYPE,B.PACKAGE_NAME,A.CREATED_DT,B.ADDR_NUM || ',' || B.STREET_TYPE || ',' || B.FLOOR_LEVEL_CODE || ',' || B.BUILDING_NAME || ',' || B.STREET_NAME || ',' || B.SECTION_NAME || ',' || B.POSTCODE || ',' || B.CITY AS ADDRESS,B.ZONE from crispadm.nova_service_order A inner join crispadm.nova_main_order_line_item B on A.NOVA_ORDER_ROW_ID=B.NOVA_ORDER_ROW_ID where A.APPLICATION_DT  > (CURRENT_DATE -7) and A.ORDER_TYPE='Terminate' and A.ZONE='ZONE KERAMAT'")
oradata <- dbGetQuery(con, query)
View(oradata)
oradata$ORDER_ID[1]
oradata$ORDER_TYPE[1]
length(oradata) # length of columns
nrow(oradata) # number of records 

oradata$ADDRESS[49]

oradata$ADDRESS <- gsub("'","",oradata$ADDRESS)

# 3- insert into mysql 
mydb = dbConnect(MySQL(), user='root', password='YOURPASSOWRD', dbname='YOURDB', host='YOURIP')
# clean up
oradata$ADDRESS <- gsub("'","",oradata$ADDRESS)
# masukkan
while (count <= nrow(oradata)){
  myquery <- paste("insert into circledonfly_orders(order_id,order_type,package_name,created_dt,address,zone) values ('",oradata$ORDER_ID[count],"','",oradata$ORDER_TYPE[count],"','",oradata$PACKAGE_NAME[count],"','",oradata$CREATED_DT[count],"','",oradata$ADDRESS[count],"','",oradata$ZONE[count],"')")
  myquery
  myresultset <- dbSendQuery(mydb,myquery)
  count <- count +1 
}

# then retrieving for google API 
# python
python.load("queMysql2GoogleAPI_simplied.py")


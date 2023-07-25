###DATA CLEANING & TRANSFORMATION

import pandas as pd

DATA_PATH = "archive/players_21.csv";
df = pd.read_csv(DATA_PATH);

# Descripcion de los datos
# print(df.describe());


#1.-The height should be in Meters(Float64) and the weight in pounds(Int)
print("-------------- Question 1 --------------");

print(df["height_cm"]);

print(df["short_name"]);

#Acceder a una fila con un valor especifico en una columna
print(df.loc[df["short_name"] == "Cristiano Ronaldo"]["height_cm"]);

#Tipo de valor de una columna en especifica
print(df["height_cm"].dtype);

#Tipo de valor de varias columnas
print(df.dtypes);

'''
    Valor enteros -> int64 
    Valor flotantes -> float64
    Valor texto -> object
'''

# print(df["weight_kg"].dtype);

#Transforming Height into Meters 
df.rename(columns={"height_cm":"height_mt"},inplace=True);
df["height_mt"] = df["height_mt"] / 100;

#Transforming Weight into pounds 
df.rename(columns={"weight_kg":"weight_lbs"},inplace=True);
df["weight_lbs"] = df["weight_lbs"] * 2.20462;

print(df["weight_lbs"]);


#2 Yes, separate the column "joined" into 3 columns "year","month","day"

print("-------------- Question 2 --------------");

'''
.str is a df method in pandas that is used to get access 
into the functionalities of manipulate strings

Method of dataFrame that returns 
"pandas.core"string.StringMethods" which is an object
that have a lot of useful methods to manipulate strings.

.split is a df method in pandas that is used to divide
one column which contains strings into substrings using a 
specific delimeter
'''

NEW_COLUMNS = ["year","month","day"];

df[NEW_COLUMNS] = df["joined"].str.split("-",expand=True);

# Delete the "joined column"
df.drop(columns=["joined"],inplace=True);

#Delete rows with NaN in the columns = Year,Month,Day 
df.dropna(subset=["year","month","day"],inplace=True);

for column in NEW_COLUMNS:
     df[column] = df[column].astype(int);

print(df[["year","month","day"]].dtypes);


#3.- Clean and transform wage_eur, release_clause_eur
print("-------------- Question 3 --------------");
#Patron para buscar columnas que contengan la palabra en comun
print(df.filter(regex="wage_eur"));
print(df.filter(regex="release_clause_eur"));

#Verify if there's Null values in the columns
df["release_clause_eur"].isnull().any(); # -> True 
df.dropna(subset=["release_clause_eur"],inplace=True);

#Transforming wage_eur into int64 column
df["wage_eur"].astype(int);


#4.-Remove "newlines" characters from Hits column

print("-------------------------Question 4-----------------");
for column in df.columns:
     print(column);
# print(df.filter(regex="hits"));






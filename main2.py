
import pandas as pd

#1.- Answer: No it should have float64 and int64 type instead
DATA_PATH = "fifa21v2.csv";

df = pd.read_csv(DATA_PATH);

print(df[["Height","Weight"]]);


# df["Height"] = df["Height"].str.replace("cm","").str.replace('\'', '');

#Convert column into float type
# df["Height"] = df["Height"].astype(float) / 100;
# print(df["Height"]);

# df["Weight"] = df["Weight"].str.replace("kg","").astype(int);

# Función para convertir pies y pulgadas a centímetros
def inches_to_meters(height_str):
    try:
        if "'" in height_str and '"' in height_str:
            pies, pulgadas = height_str.split("'")
            pulgadas = pulgadas.replace('"', '')
            altura_cm = int(pies) * 30.48 + float(pulgadas) * 2.54
            return altura_cm / 100;
        elif "cm" in height_str:
            return float(height_str.replace('cm', '')) /100;
        else:
            return float(height_str) / 100;
    except ValueError:
        return height_str / 100;

def pounds_to_kg(weight_str):
    try:
        if "lbs" in weight_str:
            pounds,lbs = weight_str.split("lbs");
            weight_kg = int(pounds) * 0.4535;
            return float(weight_kg);
        elif "kg" in weight_str:
            return float(weight_str.replace("kg",""));
        else:
            return weight_kg;

    except ValueError:
        return weight_str;
    

# Apply function to the column "Height"
df['Height'] = df['Height'].apply(inches_to_meters)

# Changing name of column Height to Height_mt
df.rename(columns={"Height":"Height_mt"},inplace=True);

print(df["Height_mt"]);

#Apply function to the column Weight
df["Weight"] = df["Weight"].apply(pounds_to_kg);

#Changing the name of column Weight to Weight_kg
df.rename(columns={"Weight":"Weight_kg"},inplace=True);
print(df["Weight_kg"]);


#2

print("------------- Question 2 --------------");

# print(df["Joined"].str.split(" ",expand=True));
#Creating 3 new columns into the dataFrame 
df[["month","day","year"]] = df["Joined"].str.split(" ",expand=True);

df["day"] = df["day"].str.replace(",","");

'''
expand argument takes all the elements from the array 
that the split method returns and convers all the items
into columns , it will ignore blank elements like ""
or spaces
'''
df["day"] = df["day"].astype(int);
df["year"] = df["year"].astype(int);
print(df[["day","year"]].dtypes);

#3 Wage, release 
print("------------- Question 3 --------------");

QUESTION_3_COLUMNS = ["Wage","Release Clause"];

def euros_to_dolars(wage_str):
    DOLAR_VALUE = 1.11;
    euros = str(wage_str);

    if "€" in euros:
        euros = euros.split("€")[1];
        
    #If the amount of money have "K" we're going to separate and transform to correct digits
    if "K" in euros:
        euros = float(euros.split("K")[0]);
        euros = euros * 1000;
    
    elif "M" in euros:
        euros = float(euros.split("M")[0]);
        euros = euros * 1000000;

    #Change euros to dolars
    dolars = float(euros) * DOLAR_VALUE;
    return dolars;

    
# df[QUESTION_3_COLUMNS] = df[QUESTION_3_COLUMNS].apply(euros_to_dolars);
# df.rename(columns={"Wage":"Wage_dolars","Release Clause":"Release_Clause_dolars"},inplace=True);

df["Wage"] = df["Wage"].apply(euros_to_dolars);
df["Release Clause"] = df["Release Clause"].apply(euros_to_dolars);
print(df[QUESTION_3_COLUMNS]);


#4 Remove "Newlines characters from the "Hits" column

print("------------- Question 4 --------------");


#Column Hits have NaN values
#El SimpleImputer de sklearn es una clase proporcionada por la biblioteca scikit-learn (también conocida como sklearn) que se utiliza para imputar o rellenar valores faltantes en un conjunto de datos. La imputación es una técnica común para tratar con valores faltantes en un conjunto de datos antes de aplicar algoritmos de aprendizaje automático.
print(df["Hits"]);

from sklearn.impute import SimpleImputer

#Creating the new Imputer with Mean strategic
imputer = SimpleImputer(strategy="most_frequent");

#Ajusting and transforming the SimpleImputer with Dataset
df["Hits"] = imputer.fit_transform(df[["Hits"]]); #Valores faltantes 


df["Hits"] = df["Hits"].apply(euros_to_dolars);
print(df["Hits"]);


#5 Separate Team & Contract Column into separate columns
print("------------- Question 5 --------------");


def remove_characters(club_str):

    caracters = club_str.split("\n");
    return caracters[-1]; 

# df["Club"] = df["Club"].apply(remove_characters);
df["Club"] = df["Club"].str.split("\n").str[-1];

print(df["Club"]);

#Separating the Contract column into Contract start and Contract end column

def separate_contract_columns(contract_str:str):

    meses_abreviados = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    if contract_str.split()[0] in meses_abreviados:
        month,day,year,_,city = contract_str.split();
        return pd.Series([f"{day}/{month}/{year}","0"]);

    elif "~" in contract_str:
        start_date,end_date = contract_str.split("~");
        return pd.Series([start_date,end_date]);
        
    else:
        return pd.Series(["",""]);

# df[["Contract_Start","Contract_end"]] = df["Contract"].str.split("~",expand=True);
df[["Contract_Start","Contract_End"]] = df["Contract"].apply(separate_contract_columns);
'''
    Formas de eliminar columnas en pandas

    #Drop method
    df = df.drop("Columna_a_eliminar",axis=1);

    #del keyword
    del df["Columna_a_eliminar"];

    #Pop method
    columna_eliminadas = df.pop("Columna_a_eliminar");
'''
del df["Contract"];
print(df[["Contract_Start","Contract_End"]]);

# Guardar CSV limpio!
df_reducido = df[["Contract_Start","Contract_End"]];
df_reducido.to_csv("archivo.csv",index=False);





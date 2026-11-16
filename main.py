import pandas as pd

df = pd.read_csv("data/bank-additional-full.csv", sep=";")

pd.set_option("display.max_columns", None)

#Cleans the data
df_clean = df.drop_duplicates().copy()
df_clean = df_clean.drop(columns=["duration", "campaign", "pdays"])
df_clean["y"] = (df_clean["y"] == "yes").astype(int) #Convert t/f to 1/0

print(df_clean.shape)
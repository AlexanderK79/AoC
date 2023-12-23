# importing pandas module 
import pandas as pd  

strFileName = 'AoC2020\\01-Alexander-input.txt'
#dctFileContent = (open(strFileName)).readlines()
#for line in dctFileContent:
#    line = line.replace('\n', '').replace('\r', '')



# Define a dictionary with column A 
data1 = {'A': [1, 2]}  
#data1 = {'A': [dctFileContent]}  
     
# Define another dictionary with column B 
data2 = {'B': ['a', 'b', 'c']}   
#data2 = {'B': [dctFileContent]}   
   
# Convert the dictionary into DataFrame   
#df = pd.DataFrame(data1, index =[0, 1]) 
df = pd.read_fwf(strFileName, names=["A"])

# Convert the dictionary into DataFrame   
#df1 = pd.DataFrame(data2, index =[2, 3, 4])  
df1 = pd.read_fwf(strFileName,  names=["B"])
df2 = pd.read_fwf(strFileName,  names=["C"])

# Now to perform cross join, we will create 
# a key column in both the DataFrames to  
# merge on that key. 
df['key'] = 1
df1['key'] = 1
df2['key'] = 1
  
# to obtain the cross join we will merge  
# on the key and drop it. 
result = pd.merge(df, df1, on ='key').drop("key", 1) 
result['key'] = 1
result2 = pd.merge(result, df2, on ='key').drop("key", 1) 

result['sum'] = result.A + result.B
result['product'] = result.A * result.B
rslt_df = result[result.A + result.B == 2020]
rslt_df = result[result['sum'] == 2020]

rslt2_df = result2[result2.A + result2.B  + result2.C == 2020]

print (rslt2_df, rslt2_df.A * rslt2_df.B * rslt2_df.C)
result
# add 
  
result 
from ucimlrepo import fetch_ucirepo 
  
# fetch dataset 
liver_disorders = fetch_ucirepo(id=60) 
  
# data (as pandas dataframes) 
X = liver_disorders.data.features 
y = liver_disorders.data.targets 
  
# # metadata 
# print(liver_disorders.metadata) 
  
# # variable information 
# print(liver_disorders.variables)

print(X)
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['figure.figsize'] = (16, 9)



df = pd.read_csv('abfs[s]://filesystem@accentureazure.dfs.core.windows.net/HRDataset_v14.csv')


df.dropna(how='all',inplace=True)
df.head()



# Missing Values
missings = df.isnull().sum()
df['DaysLateLast30'] = df['DaysLateLast30'].fillna(-1)

df['DateofHire'] = pd.to_datetime(df['DateofHire'], dayfirst = False)
df['DOB'] = pd.to_datetime(df['DOB'], dayfirst = False)
df['DateofTermination'] = pd.to_datetime(df['DateofTermination'], dayfirst = False)
df['LastPerformanceReview_Date'] = pd.to_datetime(df['LastPerformanceReview_Date'], dayfirst = False)
 
#df['Last_Name'] = df['Employee_Name'].apply(lambda name: name.split(',')[0].strip())
#df['first_Name'] = df['Employee_Name'].apply(lambda name: name.split(',')[1].strip() if ("," in name) else "")

df["Sex"] = df["Sex"].str.strip()

bins = [10,20,30,40,50,60,70,80,90]
labels = [10,20,30,40,50,60,70,80]
df["SalaryBin10"] = pd.cut(df["Salary"], bins)



df['LastDayWorked'] = df['DateofTermination']
df['LastDayWorked'].fillna(df['LastPerformanceReview_Date'].max(),inplace=True)
df['NbrDayWorked'] = (df['LastDayWorked']-df['DateofHire'])//np.timedelta64(1,'D')
del df['LastDayWorked']
print(df['NbrDayWorked'].max(),df['NbrDayWorked'].min())


df["SalaryMedianPosition"] = df.groupby(['Position'])["Salary"].transform('median')
df["SalaryEcart"] = df["Salary"] - df["SalaryMedianPosition"]


keepColId = ['MarriedID', 'FromDiversityJobFairID','Termd']
keepColNum = ['NbrDayWorked','SalaryEcart', 'EngagementSurvey', 'EmpSatisfaction','SpecialProjectsCount']
keepColCat = ['Sex', 'MaritalDesc', 'CitizenDesc','Department', 'PerformanceScore']


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaledData = scaler.fit_transform(df[keepColNum])
scaledData=pd.DataFrame(scaledData,columns=keepColNum)


data = pd.concat([scaledData,df[keepColId], pd.get_dummies(df[keepColCat]),df['EmploymentStatus']], axis=1)

X=data.loc[data['EmploymentStatus'].isin(['Active','Voluntarily Terminated'])].copy()
# Target
y=X['Termd']

X.drop(["Termd",'EmploymentStatus'], axis=1, inplace=True)


data.to_csv('../data/HRDataset_v14_processed.csv')

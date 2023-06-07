import pandas as pd

PATH = "./HR/data/HRDataset_v14.csv"
dataSetTwo = pd.read_csv(PATH)

# primaryKey = carData['Model']

# dataSetOne = carData.loc[:, ['Model', 'Company',
#                          'Horsepower', 'Torque', 'Transmission Type', 'Drivetrain']]
# dataSetTwo = carData.loc[:, ['Model', 'Fuel Economy',
#                          'Number of Doors', 'Price', 'Model Year Range', 'Number of Cylinders']]

# dataSetOne.to_csv('./HR/Data/dataSetOne.csv', sep=',',
#                   index=False, encoding='utf-8')
# dataSetTwo.to_csv('./HR/Data/dataSetTwo.csv', sep=',',
#                   index=False, encoding='utf-8')


testDataset = dataSetTwo.tail(4)
testDataset.to_csv('./HR/Data/testDatasetHRTwo.csv',
                   sep=',', index=False, encoding='utf-8')

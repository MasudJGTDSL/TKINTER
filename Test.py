import pandas as pd
import numpy as np


jg_employee_dt = pd.read_csv("JGTDSL_Employee.csv")
selected_column = [
    "JGID",
    "PersonName",
    "FathersName",
    "DateOfBirth",
    "CurrentBasicPay",
    "Email",
    "Mobile",
]
selected_column_df = jg_employee_dt[selected_column]

data_dict_df = selected_column_df.T.to_dict()
data = [[x for x in val.values()] for val in data_dict_df.values()]
# print(selected_column_df.T.to_dict('list')) # Here is T for Transform (Row to Column)
# print(selected_column_df.to_dict('index'))

# Boath works =========================================================
#! print([[y for y in x.values()] for x in selected_column_df.to_dict('index').values()])
#! print([x for x in selected_column_df.T.to_dict('list').values()])

df = pd.DataFrame([x for x in selected_column_df.T.to_dict('list').values()])
df.columns = [selected_column]
# df.to_csv('jg_employee_selected_column.csv', index=False)
nmpy_dt = np.array(df)

np.savetxt('np.txt', nmpy_dt, selected_column)
print(nmpy_dt)
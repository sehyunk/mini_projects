# 'user_id', 'date'를 넣으면 코호트 또는 리텐션을 출력해주는 함수입니다.

import pandas as pd
from datetime import timedelta

def get_cohort_table(df):
    df = pd.merge(df,df.groupby(['user_id'])[['date']].min(), on ='user_id', how = 'inner')
    df.columns = ['user_id', 'date', 'first_date']
    first_order_month = pd.to_datetime(df['first_date']).dt.year*12 + pd.to_datetime(df['first_date']).dt.month
    order_month = pd.to_datetime(df['date']).dt.year*12 + pd.to_datetime(df['date']).dt.month
    df['cohort'] = order_month - first_order_month 
    df['first_month'] = df['first_date'].str[:7]
    return df

def get_cohort(df):
    df = get_cohort_table(df)
    cohort = df.groupby(['first_month','cohort'])[['user_id']].nunique().reset_index()
    cohort = cohort.pivot(index = 'first_month', columns = 'cohort' , values = 'user_id')
    cohort = (cohort.T/cohort[0]).T*100
    return cohort

def get_retention(df):
    cohort = get_cohort(df)
    retention = pd.DataFrame(cohort.mean(), columns = ['retention']).T
    return retention


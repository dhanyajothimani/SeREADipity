# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 16:37:55 2019

@author: Jothimani
"""

import pandas as pd
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#import plotly.plotly as py
import matplotlib.pyplot as plt
from matplotlib import pyplot
import plotly.graph_objs as go
import os 
import json
init_notebook_mode(connected=True)


os.chdir("C:\\Users\\Jothimani\\Documents\\TS")
time_series_df=pd.read_csv('FB.csv')
time_series_df.head()



time_series_df.Date = pd.to_datetime(time_series_df.Date, format='%Y-%m-%d')
time_series_df = time_series_df.sort_values(by="Date")
time_series_df = time_series_df.reset_index(drop=True)
time_series_df.head()
time_series_df.shape

actual_vals = time_series_df.AdjClose
actual_log = np.log10(actual_vals)


#SARIMA
import math
import statsmodels.api as sm
import statsmodels.tsa.api as smt
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.tools as tls
#import plotly.express as px
#train, test = actual_vals[0:3450], actual_vals[3450:]
xy = round(0.80*len(actual_vals))
train, test = actual_vals[0:xy], actual_vals[xy:]
train_log, test_log = np.log10(train), np.log10(test)
my_order = (1, 1, 3)
my_seasonal_order = (0, 1, 1, 7)



history = [x for x in train_log]
predictions = list()
predict_log=list()
#test_log = list(test_log)
#for t in range(len(test_log)):
for index, value in test_log.items():
    model = sm.tsa.SARIMAX(history, order=my_order, seasonal_order=my_seasonal_order,enforce_stationarity=False,enforce_invertibility=False)
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    predict_log.append(output[0])
    yhat = 10**output[0]
    print(yhat)
    predictions.append(yhat)
    #print(predictions)
    obs = test_log[index]
    history.append(obs)
    print(len(history))


error = math.sqrt(mean_squared_error(test_log, predict_log))
print('Test rmse: %.3f' % error)

figsize=(12, 7)
plt.figure(figsize=figsize)
test = list(test)
pyplot.plot(test,label='Actuals')
pyplot.plot(predictions, color='red',label='Predicted')
pyplot.legend(loc='upper right')
pyplot.show()


import numpy as np
def detect_classify_anomalies(df,window):
    df.replace([np.inf, -np.inf], np.NaN, inplace=True)
    df.fillna(0,inplace=True)
    df['error']=df['actuals']-df['predicted']
    df['percentage_change'] = ((df['actuals'] - df['predicted']) / df['actuals']) * 100
    df['meanval'] = df['error'].rolling(window=window).mean()
    df['deviation'] = df['error'].rolling(window=window).std()
    df['-3s'] = df['meanval'] - (2 * df['deviation'])
    df['3s'] = df['meanval'] + (2 * df['deviation'])
    df['-2s'] = df['meanval'] - (1.75 * df['deviation'])
    df['2s'] = df['meanval'] + (1.75 * df['deviation'])
    df['-1s'] = df['meanval'] - (1.5 * df['deviation'])
    df['1s'] = df['meanval'] + (1.5 * df['deviation'])
    cut_list = df[['error', '-3s', '-2s', '-1s', 'meanval', '1s', '2s', '3s']]
    cut_values = cut_list.values
    cut_sort = np.sort(cut_values)
    df['impact'] = [(lambda x: np.where(cut_sort == df['error'][x])[1][0])(x) for x in
                               range(len(df['error']))]
    severity = {0: 3, 1: 2, 2: 1, 3: 0, 4: 0, 5: 1, 6: 2, 7: 3}
    region = {0: "NEGATIVE", 1: "NEGATIVE", 2: "NEGATIVE", 3: "NEGATIVE", 4: "POSITIVE", 5: "POSITIVE", 6: "POSITIVE",
              7: "POSITIVE"}
    df['color'] =  df['impact'].map(severity)
    df['region'] = df['impact'].map(region)
    df['anomaly_points'] = np.where(df['color'] == 3, df['error'], np.nan)
    df = df.sort_values(by='Date', ascending=False)
    df.Date = pd.to_datetime(df['Date'].astype(str), format="%Y-%m-%d")
    print(df)
    return df




#predicted_df <- pd.read_csv(")
#classify_df=detect_classify_anomalies(predicted_df,7)



def plot_anomaly(df,metric_name):
    dates = df.Date
    bool_array = (abs(df['anomaly_points']) > 0)
    actuals = df["actuals"][-len(bool_array):]
    anomaly_points = bool_array * actuals
    anomaly_points[anomaly_points == 0] = np.nan
    color_map= {0: "rgba(228, 222, 249, 0.65)", 1: "yellow", 2: "orange", 3: "red"}
    table = go.Table(
            domain=dict(x=[0, 1], y=[0, 0.3]),
            columnwidth=[1, 2 ],
            header = dict(height = 20,
            values = [['<b>Date</b>'],['<b>Actual Values </b>'],
                     ['<b>Predicted</b>'], ['<b>% Difference</b>'],['<b>Severity (0-3)</b>']],
            font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
            fill = dict(color='#d562be')),
            cells = dict(values = [df.round(3)[k].tolist() for k in ['Date', 'actuals', 'predicted', 'percentage_change','color']],
            line = dict(color='#506784'),
            align = ['center'] * 5,
            font = dict(color=['rgb(40, 40, 40)'] * 5, size=12),
            suffix=[None] + [''] + [''] + ['%'] + [''],
            height = 27,
            fill=dict(color= [df['color'].map(color_map)],)
                )
            )
    anomalies = go.Scatter(name="Anomaly", x=dates, xaxis='x1', yaxis='y1',
                           y=df['anomaly_points'], mode='markers',
                           marker = dict(color ='red',
                                         size = 11,line = dict(
                                                 color = "red",
                                                 width = 2)
                                         )
                                )
    upper_bound = go.Scatter(hoverinfo="skip",
                         x=dates,
                         showlegend =False,
                         xaxis='x1',
                         yaxis='y1',
                         y=df['3s'],
                         marker=dict(color="#444"),
                         line=dict(
                             color=('rgb(23, 96, 167)'),
                             width=2,
                             dash='dash'),
                         fillcolor='rgba(68, 68, 68, 0.3)',
                         fill='tonexty')
    lower_bound = go.Scatter(name='Confidence Interval',
                          x=dates,
                         xaxis='x1',
                         yaxis='y1',
                          y=df['-3s'],
                          marker=dict(color="#444"),
                          line=dict(
                              color=('rgb(23, 96, 167)'),
                              width=2,
                              dash='dash'),
                          fillcolor='rgba(68, 68, 68, 0.3)',
                          fill='tonexty')
    Actuals = go.Scatter(name= 'Actuals',
                     x= dates,
                     y= df['actuals'],
                    xaxis='x2', yaxis='y2',
                     mode='line',
                     marker=dict(size=12,
                                 line=dict(width=1),
                                 color="blue")
                     )
#    Predicted = go.Scatter(name = 'Predected',
#                          x = dates, 
#                          y = df['predicted'],
#                          xaxis = 'x2', 
#                          yaxis = 'y2',
#                          mode = 'line',
#                          marker = dict(size = 12, 
#                                        line = dict(width = 1),
#                                        color = "orange"
#                                  )
#                          )
    Predicted = go.Scatter(name= 'Predicted',
                     x= dates,
                     y= df['predicted'],
                     xaxis='x2', yaxis='y2',
                     mode='line',
                     marker=dict(size=12,
                                 line=dict(width=1),
                                 color="orange"
                                ),
		     error_y = dict(type = 'percent',
                                    value=df['predicted'].std(),
                                    thickness = 1,
				    width = 0,
                                    color='#444',
                                    opacity=0.8
                                    )
			     )
    Error = go.Scatter(name="Error",
                   x=dates, y=df['error'],
                   xaxis='x1',
                   yaxis='y1',
                   mode='line',
                   marker=dict(size=12,
                               line=dict(width=1),
                               color="red"),
                   text="Error")
    anomalies_map = go.Scatter(name = "anomaly actual",
                                   showlegend=False,
                                   x=dates,
                                   y=anomaly_points,
                                   mode='markers',
                                   xaxis='x2',
                                   yaxis='y2',
                                    marker = dict(color ="red",
                                  size = 11,
                                 line = dict(
                                     color = "red",
                                     width = 2)
                                     )
                                 )
    Mvingavrg = go.Scatter(name="Moving Average",
                           x=dates,
                           y=df['meanval'],
                           mode='line',
                           xaxis='x1',
                           yaxis='y1',
                           marker=dict(size=12,
                                       line=dict(width=1),
                                       color="green"),
                                       text="Moving average")
    axis=dict(showline=True,
              zeroline=False,
              showgrid=True,
              mirror=True,
              ticklen=4,
              gridcolor='#ffffff',
              tickfont=dict(size=10))
    layout = dict(width=1000,
                  height=865,
                  autosize=False,
                  title= metric_name,
                  margin = dict(t=75),
                  showlegend=True,
                  xaxis1=dict(axis, **dict(domain=[0, 1], anchor='y1', showticklabels=True)),
                  xaxis2=dict(axis, **dict(domain=[0, 1], anchor='y2', showticklabels=True)),
                  yaxis1=dict(axis, **dict(domain=[2 * 0.21 + 0.20 + 0.09, 1], anchor='x1', hoverformat='.2f')),
                  yaxis2=dict(axis, **dict(domain=[0.21 + 0.12, 2 * 0.31 + 0.02], anchor='x2', hoverformat='.2f')))
    fig = go.Figure(data = [table,anomalies,anomalies_map,
                        upper_bound,lower_bound,Actuals,Predicted,
                        Mvingavrg,Error], layout = layout)
    plot(fig)
    pyplot.show()
    #plt.savefig(fig, format="png")

predicted_df=pd.DataFrame()
predicted_df['Date']=time_series_df['Date'][xy:]
predicted_df['actuals']=test
predicted_df['predicted']=predictions
predicted_df.reset_index(inplace=True)
del predicted_df['index']
predicted_df.head()

classify_df=detect_classify_anomalies(predicted_df,7)
classify_df.reset_index(inplace=True)
del classify_df['index']
plot_anomaly(classify_df,"metric_name")

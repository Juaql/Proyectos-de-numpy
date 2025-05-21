import pandas as pd
import yfinance as yf
import datetime as dt
import numpy as np

tickers = ["YPFD.BA","ALUA.BA","BMA.BA"]

start = dt.datetime.today() - dt.timedelta(60)
end = dt.datetime.today()

def contar_fechas(data):
    data['prev_date'] = data['date'].shift(1)
    data['diff'] = (data['date'] - data['prev_date']).dt.days
    data['reset'] = data['diff'] > 2
    data['group'] = data['reset'].cumsum()
    data['day_count'] = data.groupby('group').cumcount() + 1
    data.drop(columns=['prev_date', 'diff', 'reset'], axis=1, inplace=True)

    return data

for ticker in tickers:
    yfinance_information = yf.download(ticker, start=start, end=end, interval="1d", auto_adjust=True)
    data = pd.DataFrame(yfinance_information)

    data.columns = ['Close', 'High', 'Low', 'Open', 'Vol']
    data['Ticker'] = ticker
    data["date"] = data.index

    data = contar_fechas(data)
    print(data)

    t = np.arange(len(data['Close']))
    print("Promedio ponderado: ",np.average(data['Close'], weights=t))
    print("Promedio: ",np.mean(data['Close']))
    print("Minimo: ",np.min(data['Close']))
    print("Maximo: ",np.max(data['Close']))
    print("Spread: ",np.ptp(data['Close']))
    print("Mediana: ",np.median(data['Close']))
    print("Varianza: ",np.var(data['Close']))

    retornos = np.diff(data['Close']) / data['Close'][:-1]
    print("Deviacion estandar: ", np.std(retornos))

    volatilidad = np.std(np.diff(np.log(data['Close']))) / np.mean(np.diff(np.log(data['Close'])))
    volatilidad = volatilidad / np.sqrt(1./60.)
    print("Volatilidad: ",volatilidad)

    averages = np.zeros(5)

    for i, grupo in data.groupby("group"):
        precios = grupo["Close"]
        avg = precios.mean()
        print(f"Semana {i}, Precios: {precios.values}, Promedio: {avg}")
import pandas as pd
import yfinance as yf
import datetime as dt
import numpy as np

tickers = ["YPFD.BA","ALUA.BA","BMA.BA"]

start = dt.datetime.today() - dt.timedelta(60)
end = dt.datetime.today()

for ticker in tickers:
    yfinance_information = yf.download(ticker, start=start, end=end, interval="1d", auto_adjust=True)
    data = pd.DataFrame(yfinance_information)

    data.columns = ['Close', 'High', 'Low', 'Open', 'Vol']
    data['Ticker'] = ticker
    data["date"] = data.index

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

    print("Retornos logaritmicos: ", np.diff(np.log(data['Close'])))

    volatilidad = np.std(np.diff(np.log(data['Close']))) / np.mean(np.diff(np.log(data['Close'])))
    volatilidad = volatilidad / np.sqrt(1./60.)
    print(volatilidad)


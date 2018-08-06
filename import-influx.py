import csv
import socket

import moment
import pandas as pd
import numpy as np
from influxdb import DataFrameClient


def import_csv(stock):
    # open the socket
    # resp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # resp_socket.connect(socket.getaddrinfo('localhost', 8282)[0][-1])

    host = 'localhost'
    port = 8086
    user = 'root'
    password = ''
    dbname = 'mydb'
    protocol = 'json'

    client = DataFrameClient(host, port, user, password, dbname)
    df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])

    # prepare the file
    with open('{}'.format('data/{}.csv'.format(stock)), 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            quote_date = moment.date(row['Date'], '%Y-%m-%d')
            open_price = row['Open']
            high_price = row['High']
            low_price = row['Low']
            close_price = row['Close']
            adj_close = row['Adj Close']
            volume = row['Volume']

            if not open_price.replace('.', '', 1).isdigit():
                continue

            current_series = pd.Series({
                'Open': float(open_price),
                'High': float(high_price),
                'Low': float(low_price),
                'Close': float(close_price),
                'Volume': int(volume),
            }, name=quote_date.date)

            df = df.append(current_series)

        print(df)

        client.write_points(df, 'price', {'stock': stock})


def main():
    for stock in ['0001.HK', '0005.HK']:
        import_csv(stock)


if __name__ == "__main__":
    main()

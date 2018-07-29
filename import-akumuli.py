import socket
import select
import csv
import moment


def import_csv(stock):
    # open the socket
    resp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    resp_socket.connect(socket.getaddrinfo('localhost', 8282)[0][-1])

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

            if not open_price.replace('.','',1).isdigit():
                continue

            msg_to_send = "+price.{0}.open|price.{0}.high|price.{0}.low|price.{0}.close|price.{0}.volume ticker={0}\r\n+{1}\r\n*5\r\n+{2}\r\n+{3}\r\n+{4}\r\n+{5}\r\n+{6}\r\n".format(stock, quote_date.format("YYYYMMDDT000000"), open_price, high_price, low_price, close_price, volume)

            print(msg_to_send)

            # print('+price.{0}.close'.format(stock))
            # print('+{0}'.format(quote_date.isoformat()))
            # print(':{0}\r\n'.format(close_price).encode())

            # resp_socket.sendall('+price.{0}.close '.format(stock).encode())
            # resp_socket.sendall('+{0}'.format(quote_date.format("%Y-%m-%dT000000")).encode())
            # resp_socket.sendall(':{0}'.format(close_price).encode())

            resp_socket.sendall(msg_to_send.encode())
            # response = resp_socket.recv(1024)

            # print(response)
    resp_socket.close()

def main():
    for stock in ['0001.HK', '0005.HK']:
        import_csv(stock)


if __name__ == "__main__":
    main()

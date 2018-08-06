from influxdb import DataFrameClient


def do_query():
    host = 'localhost'
    port = 8086
    user = 'root'
    password = ''
    dbname = 'mydb'
    protocol = 'json'

    client = DataFrameClient(host, port, user, password, dbname)

    # df = client.query("""
    #     SELECT mean("Close") AS "mean_Close" FROM "mydb"."autogen"."price"
    #     WHERE time > '2015-01-01T05:48:00.000Z' AND time < '2018-08-06T05:48:00.000Z'
    #     GROUP BY time(1d), stock FILL(previous)
    # """)

    df = client.query("""
        SELECT mean("Close") AS "mean_Close", max("High") AS "max_High", min("Low") AS "min_Low" 
        FROM "mydb"."autogen"."price" 
        WHERE time > '2015-01-01T05:48:00.000Z' AND time < '2018-08-06T05:48:00.000Z' 
        AND "stock"='0001.HK' 
        GROUP BY time(4w) FILL(previous)
    """)
    print(df)


def main():
    do_query()


if __name__ == "__main__":
    main()

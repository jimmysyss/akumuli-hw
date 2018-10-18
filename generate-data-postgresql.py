import psycopg2
import uuid


def main():
    conn = psycopg2.connect(host="localhost", database="clicktrade", user="clicktrade", password="wong2903", port="5432")
    cur = conn.cursor()

    # insert records
    # 1000 x 1000
    for i1 in range(1000):
        data_list = [[uuid.uuid4().hex, uuid.uuid4().hex * 10, uuid.uuid4().hex * 100] for i2 in range(1000)]
        cur.executemany("INSERT INTO large_like_search_table VALUES (%s, %s, %s)", data_list)
        conn.commit()

    cur.close()


if __name__ == "__main__":
    main()

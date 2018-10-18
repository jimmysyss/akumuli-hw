# https://www.kaggle.com/rmisra/news-category-dataset#News_Category_Dataset.json

import psycopg2
import uuid
import json


def main():
    conn = psycopg2.connect(host="localhost", database="clicktrade", user="clicktrade", password="wong2903", port="5432")
    cur = conn.cursor()

    data_list = []
    count = 0
    with open('Dataset.json', 'r') as file:
        # Read line and Parse the json
        # Commit per 100 lines
        for line in file:
            dict = json.loads(line)
            data_list.append([uuid.uuid4().hex, dict["short_description"][:500], dict["headline"][:500], dict["date"], dict["link"][:500],
                             dict["category"], dict["authors"].split(', ')])

            count += 1

            if count % 1000 == 0 :
                print(count)
                cur.executemany("INSERT INTO news_cat_dataset VALUES (%s, %s, %s, %s, %s, %s, %s)", data_list)
                conn.commit()
                data_list = []
    cur.close()
    file.close()

    # insert records
    # 1000 x 1000
    # for i1 in range(1000):
    #     data_list = [[uuid.uuid4().hex, uuid.uuid4().hex * 10, uuid.uuid4().hex * 100] for i2 in range(1000)]
    #     cur.executemany("INSERT INTO large_like_search_table VALUES (%s, %s, %s)", data_list)
    #     conn.commit()


if __name__ == "__main__":
    main()

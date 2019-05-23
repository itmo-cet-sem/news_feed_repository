import json
import sys
import re


def main():
    key_word = sys.argv[1]
    file_name = sys.argv[2]

    # print(key_word, file_name)

    with open(file_name, 'r') as fp:
        news_list = json.load(fp)

    filtered_news_list = []
    for index, news_item in enumerate(news_list):
        if re.search(key_word, news_item['title'], re.IGNORECASE) \
                or re.search(key_word, news_item['description'], re.IGNORECASE) \
                or re.search(key_word, news_item['section'], re.IGNORECASE) \
                or re.search(key_word, news_item['text'], re.IGNORECASE):
            filtered_news_list.append(index)
            # print(news_item)
            # print("____________________________________________________________________")

    print(filtered_news_list)


if __name__ == '__main__':
    main()

import json

if __name__ == "__main__":
    url_index = json.loads(open("url_index.json").read())
    print(url_index[41])


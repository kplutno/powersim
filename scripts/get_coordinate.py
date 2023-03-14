import os

if __name__ == "__main__":
    api_key = os.environ["METEO_API_KEY"]
    headers = {"Authorization": "Token {}".format(api_key)}

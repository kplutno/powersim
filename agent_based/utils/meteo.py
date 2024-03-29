from math import sqrt
from dotenv import load_dotenv
import os
import datetime
import requests
import pandas as pd


def fetch_meteo_um_data(config, time, meteo_token, coordinates):
    model: list = "um"
    fields: list = config.meteo.fields
    time_format: str = config.meteo.api.time_format
    date: str = time.strftime(time_format)
    url_template = config.meteo.api.url
    length_of_forecast = config.meteo.length_of_forecast

    headers = {"Authorization": f"Token {meteo_token}"}

    weather = dict()
    times = dict()

    for key, field in fields.items():
        url = url_template.format(
            model=model,
            grid=field.grid,
            coordinates=coordinates[field.grid],
            field=field.code,
            date=date,
        )
        request = requests.post(url, headers=headers)
        times[key] = request.json()["times"][:length_of_forecast]
        weather[key] = request.json()["data"][:length_of_forecast]

    # Calculate wind velocity - to use in PV, don't need vector, just length
    weather["wind_speed"] = [
        sqrt(x**2 + y**2) for x, y in zip(weather["u_10"], weather["v_10"])
    ]

    # Using times
    index = pd.date_range(
        start=time,
        end=((config.meteo.length_of_forecast - 1) * datetime.timedelta(minutes=15))
        + time,
        freq=datetime.timedelta(minutes=15),
    )

    pressure_index = pd.date_range(
        start=time,
        end=(config.meteo.length_of_forecast * datetime.timedelta(minutes=15)) + time,
        freq=datetime.timedelta(hours=1),
    )

    # Due to the different frequency, there is a need to adapt the pressure index
    pressure_df = pd.DataFrame(data=weather["pressure"], index=pressure_index)

    pressure_df = (
        pressure_df.reindex(pressure_df.index.union(index))
        .interpolate(config.meteo.fields.pressure.interpolate_method)
        .reindex(index)
    )
    pressure_df.columns = ["pressure"]

    del weather["pressure"]

    weather_df = pd.DataFrame(data=weather, index=index).join(pressure_df)

    store_name = config.meteo.db.um.store_template.format(
        date=time.strftime(config.meteo.save_time_format),
        coordinates_P5=coordinates["P5"],
        coordinates_p5=coordinates["p5"]
    )
    
    save_path = os.path.join(config.meteo.db.um.path, store_name) + config.meteo.db.um.store_file_extension

    weather_df.to_parquet(save_path)

    return weather_df


def load_db_store(config) -> set:
    meteo_db = os.listdir(config.meteo.db.um.path)
    meteo_db = {os.path.splitext(date)[0] for date in meteo_db}
    
    return meteo_db
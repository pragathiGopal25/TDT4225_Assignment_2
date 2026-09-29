import pandas as pd
import haversine as hs

df = pd.read_csv("porto.csv")
taxi_dict = {}
trips_dict ={}

def getTime():
    timestamp = df["TIMESTAMP"]
    start_time_list = []

    for index, row in timestamp.items():
        start_time_list.append(pd.to_datetime(row, unit="s").strftime("%Y-%m-%d %H:%M:%S"))

    trips_dict["start_time"] = start_time_list

    print(trips_dict["start_time"])

def main():
    getTime()
    # print(df)

if __name__ == "__main__":
    main()
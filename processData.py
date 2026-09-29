import pandas as pd
import haversine as hs
import ast

df = pd.read_csv("porto.csv")
taxi_dict = {}
trips_dict ={}

# Deleting rows where MISSING_DATA is true 
def refine_data():
    global df
    df = df[df["MISSING_DATA"] != True]


# Calculate duration of trip
def get_duration():
    durations = ((df["POLYLINE"].str.count(r"\[") - 1) * 15).tolist() # polyline stored as string, so have to count accordingly
    
    trips_dict["duration"] = durations
    print(trips_dict["duration"][:5])


# Following two functions calculate the start and end times respectively.
def get_start_time():
    start_time_list = (
        pd.to_datetime(df["TIMESTAMP"], unit="s")
        .dt.strftime("%Y-%m-%d %H:%M:%S")
        .tolist()
    )

    trips_dict["start_time"] = start_time_list

    print(trips_dict["start_time"][:5])


def get_end_time():
    
    end_time_list = (
        (pd.to_datetime(df["TIMESTAMP"], unit="s") + 
        pd.to_timedelta(trips_dict["duration"], unit="s"))
        .dt.strftime("%Y-%m-%d %H:%M:%S")
        .tolist()
    )

    trips_dict["end_time"] = end_time_list

    print(trips_dict["end_time"][:5])


def main():
    print("CSV loaded")

    refine_data()
    print("Data refined")

    get_duration()
    print("Duration calculated")

    get_start_time()
    print("Start times calculated")

    get_end_time()
    print("End times calculated")
    # refine_data()
    # get_duration()
    # get_start_time()
    # get_end_time()
 

if __name__ == "__main__":
    main()
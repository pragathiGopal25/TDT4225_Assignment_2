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
    durations = []
    
    for coords in trips_dict["coordinates"]:
      durations.append(len(coords - 1) * 15)
    # polyline stored as string, so have to count accordingly
    
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

def getCoordinates():
    polyline = df["POLYLINE"]
    coordinates_list = []

    for index, row in polyline.items():
        row = row[1:-1]

        if row == "":
            coordinates_list.append([])
        else:
            coordinates = row.split("],[")
            trip_coordinates = []

            for coordinate in coordinates:
                coordinate = coordinate.replace("[", "").replace("]", "").split(",")

                longitude = float(coordinate[0])
                latitude = float(coordinate[1])

                trip_coordinates.append((latitude, longitude))

            coordinates_list.append(trip_coordinates)

    trips_dict["coordinates"] = coordinates_list

def checkValidity():
    validity_list = []

    for coordinates in trips_dict["coordinates"]:
        validity_list.append(len(coordinates) >= 3)

    trips_dict["valid"] = validity_list


def calculateDistance():
    distance_list = []

    for coordinates in trips_dict["coordinates"]:
        trip_distance = 0

        for i in range(len(coordinates) - 1):
            distance = hs.haversine(
                coordinates[i],
                coordinates[i + 1]
            )

            trip_distance += distance

        distance_list.append(trip_distance)

    trips_dict["distance"] = distance_list
    

def main():
    refine_data()
    getCoordinates()
    checkValidity()
    calculateDistance()
    get_duration()
    get_start_time()
    get_end_time()
    

    print(trips_dict["start_time"], trips_dict["valid"],trips_dict["distance"])

    false_count = trips_dict["valid"].count(False)
    print(false_count)

    # print(df)

if __name__ == "__main__":
    main()
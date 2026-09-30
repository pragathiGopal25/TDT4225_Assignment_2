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

    #print(trips_dict["start_time"])

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
    getTime()
    getCoordinates()
    checkValidity()
    calculateDistance()

    print(trips_dict["start_time"], trips_dict["valid"],trips_dict["distance"])

    false_count = trips_dict["valid"].count(False)
    print(false_count)

    # print(df)

if __name__ == "__main__":
    main()
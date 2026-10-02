import pandas as pd
import haversine as hs

class ProcessData:

    def __init__(self, filename):
        self.df = pd.read_csv(filename)
        self.taxi_dict = {}
        self.trips_dict = {}
        self.coordinates = {}
    
    # Deleting rows where MISSING_DATA is true 
    # Deleting rows with empty polylines
    # Deleting duplicate trips
    # Resetting indexes
    def refine_data(self):

        self.df = self.df[self.df["MISSING_DATA"] != True]
        self.df = self.df[self.df["POLYLINE"] != "[]"]
        self.df = self.df.drop_duplicates()
        self.df = self.df.reset_index(drop=True)

        #print("Number of rows after cleaning:", len(df))

    # Calculate duration of trip
    def get_duration(self):
        durations = []
        
        for coords in self.coordinates["coordinates"]:
            durations.append((len(coords) - 1) * 15)
        
        self.trips_dict["duration"] = durations
        print(self.trips_dict["duration"][:5])


    # Following two functions calculate the start and end times respectively.
    def get_start_time(self):
        start_time_list = (
            pd.to_datetime(self.df["TIMESTAMP"], unit="s")
            .dt.strftime("%Y-%m-%d %H:%M:%S")
            .tolist()
        )

        self.trips_dict["start_time"] = start_time_list

        print(self.trips_dict["start_time"][:5])


    def get_end_time(self):
        
        end_time_list = (
            (pd.to_datetime(self.df["TIMESTAMP"], unit="s") + 
            pd.to_timedelta(self.trips_dict["duration"], unit="s"))
            .dt.strftime("%Y-%m-%d %H:%M:%S")
            .tolist()
        )

        self.trips_dict["end_time"] = end_time_list

        print(self.trips_dict["end_time"][:5])

    def getCoordinates(self):
        polyline = self.df["POLYLINE"]
        coordinates_list = []

        for index, row in polyline.items():
            row = row[1:-1]

            coordinates = row.split("],[")
            trip_coordinates = []

            for coordinate in coordinates:
                coordinate = coordinate.replace("[", "").replace("]", "").split(",")

                longitude = float(coordinate[0])
                latitude = float(coordinate[1])

                trip_coordinates.append((latitude, longitude))

            coordinates_list.append(trip_coordinates)

        self.coordinates["coordinates"] = coordinates_list

    def checkValidity(self):
        validity_list = []

        for coordinates in self.coordinates["coordinates"]:
            validity_list.append(len(coordinates) >= 3)

        self.trips_dict["valid"] = validity_list


    def calculateDistance(self):
        distance_list = []

        for coordinates in self.coordinates["coordinates"]:
            trip_distance = 0

            for i in range(len(coordinates) - 1):
                distance = hs.haversine(
                    coordinates[i],
                    coordinates[i + 1]
                )

                trip_distance += distance

            distance_list.append(trip_distance)

        self.trips_dict["distance"] = distance_list
    

    def set_call_type(self):
        self.trips_dict["call_type"] = self.df["CALL_TYPE"].tolist()

    def set_id(self):
        self.taxi_dict["taxi_id"] = self.df["TAXI_ID"].unique().tolist()

        self.trips_dict["trip_id"] = self.df["TRIP_ID"].unique().tolist()
        self.trips_dict["taxi_id"] = self.df["TAXI_ID"].tolist()
        

    def run(self):
        print("CSV loaded")

        self.refine_data()
        print("Data refined")

        self.set_id()
        print("id set")

        self.getCoordinates()
        print("Coords calculated")

        self.get_duration()
        print("Duration calculated")

        self.get_start_time()
        print("Start times calculated")

        self.get_end_time()
        print("End times calculated")

        self.calculateDistance()
        print("Distance calculated")

        self.checkValidity()
        print("Validity checked")

        self.set_call_type()
        print("call type set")


    def get_table(self, table_name):
        if table_name == "Taxi":
            return self.taxi_dict
        else:
            return self.trips_dict


def main():
    p = ProcessData("porto.csv")
    p.run()
 
if __name__ == "__main__":
    main()
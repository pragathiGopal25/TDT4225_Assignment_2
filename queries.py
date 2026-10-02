from DbConnector import DbConnector
from tabulate import tabulate 


class Queryprogram:
    def __init__(self):
        self.connection = DbConnector
        self.cursor = self.connection.cursor
        
    def question_1(self):
        query = """"
            SELECT (SELECT COUNT(*) FROM Taxi) AS taxis, 
            COUNT(*) AS trips, 
            SUM(JSON_LENGTH(Polyline)) as GPS_points 
            FROM Trips 
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=self.cursor.column_names))
        
    def question_2(self):
        query = """
            SELECT AVG(Num_Trips) AS average_trips_per_taxi
            FROM Taxi
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=self.cursor.column_names))
        
    def question_3(self):
        query = """
            SELECT Taxi_ID, Num_Trips
            FROM Taxi
            ORDER BY Num_Trips DESC
            LIMIT 20
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=self.cursor.column_names))
        
        
    def question_4a(self):
        
        query = """
            WITH call_counts AS (
                SELECT Taxi_ID, Call_Type, COUNT(*) AS trip_count
                FROM Trips
                GROUP BY Taxi_ID, Call_Type
            ),
            ranked AS (
                SELECT
                    Taxi_ID,
                    Call_Type,
                    trip_count,
                    RANK() OVER (
                        PARTITION BY Taxi_ID
                        ORDER BY trip_count DESC
                    ) AS ranking
                FROM call_counts
            )
            SELECT Taxi_ID, Call_Type, trip_count
            FROM ranked
            WHERE ranking = 1
            ORDER BY Taxi_ID, Call_Type
            """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=self.cursor.column_names))
        
    def question_4b(self):
        query = """
            SELECT
                Call_Type,
                AVG(Duration) AS avg_duration,
                AVG(Distance) AS avg_distance,
                ROUND(100.0 * AVG(HOUR(Start_Time) >= 0
                                AND HOUR(Start_Time) < 6), 2) AS pct_00_06,
                ROUND(100.0 * AVG(HOUR(Start_Time) >= 6
                                AND HOUR(Start_Time) < 12), 2) AS pct_06_12,
                ROUND(100.0 * AVG(HOUR(Start_Time) >= 12
                                AND HOUR(Start_Time) < 18), 2) AS pct_12_18,
                ROUND(100.0 * AVG(HOUR(Start_Time) >= 18
                                AND HOUR(Start_Time) < 24), 2) AS pct_18_24
            FROM Trips
            GROUP BY Call_Type
            ORDER BY Call_Type
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=self.cursor.column_names))

    #går ut i fra at tid i duration lagres som sekunder? 
    def question_5(self):
        query = """
            SELECT
                Taxi_ID,
                ROUND(Total_Duration / 3600, 2) AS total_hours,
                Total_Distance AS total_distance
            FROM Taxi
            ORDER BY total_hours DESC, total_distance DESC
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=self.cursor.column_names))
    
    
    def question_6(self):
        query = """
            SELECT
                t.Trip_ID,
                ROUND(
                    MIN(
                        ST_Distance_Sphere(
                            POINT(p.longitude, p.latitude),
                            POINT(-8.62911, 41.15794)
                        )
                    ), 2
                ) AS closest_distance_m
            FROM Trips AS t
            JOIN JSON_TABLE(
                t.Polyline,
                '$[*]' COLUMNS (
                    longitude DOUBLE PATH '$[0]',
                    latitude  DOUBLE PATH '$[1]'
                )
            ) AS p
            GROUP BY t.Trip_ID
            HAVING closest_distance_m <= 100
            ORDER BY closest_distance_m
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=self.cursor.column_names))


if __name__ == "__main__":
    program = Queryprogram()
    program.question_1()
    program.question_2()
    program.question_3()
    program.question_4a()
    program.question_4b()
    program.question_5()
    program.question_6()
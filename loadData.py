from DbConnector import DbConnector


# use this class to load and explore the data
class LoadData:

    def __init__(self, filename):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor
        self.filename = filename


    def create_table(self, table_name, columns):
        column_string = ""

        for column, type in columns.items():
            column_string += column + " " + type + ","
        
        column_string = column_string.rstrip(",")

        query = f"""CREATE TABLE IF NOT EXISTS {table_name} ({column_string})"""

        self.cursor.execute(query)
        self.db_connection.commit()

    def create_taxi_table(self):
        columns = {
            "Taxi_ID": "INT NOT NULL PRIMARY KEY",
            "Num_Trips": "INT NOT NULL DEFAULT 0",
            "Total_Distance": "DOUBLE NOT NULL DEFAULT 0",
            "Total_Duration": "BIGINT NOT NULL DEFAULT 0"
        }
        self.create_table("Taxi", columns)

    def populate_taxi_table(self):
        query = """
            INSERT INTO Taxi (Taxi_ID, Num_Trips, Total_Distance, Total_Duration)
            SELECT Taxi_ID, COUNT(*), SUM(Distance), SUM(Duration)
            FROM Trips
            WHERE Validity = 1
            GROUP BY Taxi_ID
        """
        self.cursor.execute(query)
        self.db_connection.commit()

    # df = pd.read_csv(filename)

def main():
    program = LoadData("porto/porto.csv")
    try:
        program.create_taxi_table()
    finally:
        program.connection.close_connection()

if __name__ == "__main__":
    main()
from DbConnector import DbConnector
from processData import ProcessData

# use this class to load and explore the data
class LoadData:

    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor

    def create_table(self, table_name, columns):
        column_string = ""

        for column, type in columns.items():
            column_string += column + " " + type + ","
        
        column_string = column_string.rstrip(",")

        query = f"""CREATE TABLE IF NOT EXISTS {table_name} ({column_string})"""

        self.cursor.execute(query)
        self.db_connection.commit()
    
    def load_data(self, table_name, data_dict):
        columns = ""
        placeholders = ""

        for index, column in enumerate(data_dict):
            if index == len(data_dict) - 1:
                columns += column
                placeholders += "%s"
            else:
                columns += column + ","
                placeholders += "%s,"
            index += 1

        # inserts data row by row
        query = f"""INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"""

        num_rows = len(list(data_dict.values())[0])

        for i in range(num_rows):
            row = []

            for column in data_dict:
                row.append(data_dict[column][i])

            self.cursor.execute(query, row)

        self.db_connection.commit()

def main():
    p = ProcessData("porto.csv")
    p.run()

    # Testing columns:
    l = LoadData()
    
    # Deleting old table, more for testing purposes
    l.cursor.execute("DROP TABLE IF EXISTS Trips")
    l.cursor.execute("DROP TABLE IF EXISTS Taxi")
    l.db_connection.commit()

    l.create_table("Taxi", {"taxi_id": "INT PRIMARY KEY"})
    l.load_data("Taxi", p.get_table("Taxi"))

    l.create_table("Trips", {
        "trip_id": "BIGINT PRIMARY KEY",
        "taxi_id": "INT",
        "start_time": "VARCHAR(255)",
        "end_time": "VARCHAR(255)",
        "duration": "INT",
        "distance": "DOUBLE",
        "valid": "BOOLEAN",
        "call_type": "VARCHAR(255)",
        "circular": "BOOLEAN"
        "FOREIGN KEY (taxi_id)": "REFERENCES Taxi(taxi_id)",
    })

    l.load_data("Trips", p.get_table("Trips"))

if __name__ == "__main__":
    main()
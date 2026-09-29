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
            column_string += column + "" + type + ","
        
        column_string = column_string.rstrip(",")

        query = f"""CREATE TABLE IF NOT EXISTS {table_name} ({column_string})"""

        self.cursor.execute(query)
        self.db_connection.commit()

    # df = pd.read_csv(filename)

def main():
    LoadData()

if __name__ == "__main__":
    main()
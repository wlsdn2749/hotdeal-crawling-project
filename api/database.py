import duckdb
from duckdb import DuckDBPyConnection


class DuckDBManager():
    def __init__(self):
        self.conn = duckdb.connect(database=':memory:', read_only=False)
        self.update_table()
        
    def get_connection(self) -> DuckDBPyConnection:
        return self.conn
    
    def update_table(self) -> None:
        # todo if exist, drop table
        self.conn.execute("CREATE TABLE fm AS SELECT * FROM read_csv_auto('./api/static/hotdeal_fm.csv')")
    
db = DuckDBManager()
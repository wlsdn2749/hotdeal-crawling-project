import duckdb
from duckdb import DuckDBPyConnection


class DuckDBManager():
    def __init__(self):
        self.conn = duckdb.connect(database=':memory:', read_only=False)
        self.available_sites = ["fm", "arca", "qz"]
        self.update_tables()
        self.merge_tables("merged")
        
    def get_connection(self) -> DuckDBPyConnection:
        return self.conn
    
    def update_tables(self) -> None:
        for site in self.available_sites:
            self.update_site_table(site)
        
    def update_site_table(self, site: str) -> None:
        self.drop_table_if_exists(site)
        self.create_table_from_csv(site, f'./app/static/{site}_hotdeal.csv')
        self.create_table_from_csv(f'{site}_detail', f'./app/static/{site}_hotdeal_board.csv', auto=True)
    
    def drop_table_if_exists(self, site: str) -> None:
        self.conn.execute(f"DROP TABLE IF EXISTS {site}")
    
    def create_table_from_csv(self, site: str, csv_path: str, auto: bool = False) -> None:
        read_csv_function = f"read_csv_auto('{csv_path}')" if auto else f"read_csv('{csv_path}', timestampformat='%Y-%m-%d %H:%M')"
        self.conn.execute(f"""
            CREATE TABLE {site} AS 
            SELECT * 
            FROM {read_csv_function}
        """)
        
    def merge_tables(self, new_table_name: str = "merged") -> None:
        
        self.drop_table_if_exists(new_table_name)
        union_query = " UNION ALL ".join([f"SELECT * FROM {site}" for site in self.available_sites])
        create_query = f"CREATE TABLE {new_table_name} AS {union_query}"
        self.conn.execute(create_query)
        
        self.drop_table_if_exists(new_table_name + "_detail")
        union_query = " UNION ALL ".join([f"SELECT * FROM {site}_detail" for site in self.available_sites])
        create_query = f"CREATE TABLE {new_table_name}_detail AS {union_query}"
        self.conn.execute(create_query)
        
    
db = DuckDBManager()

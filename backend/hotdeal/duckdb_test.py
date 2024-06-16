import duckdb
# rel = duckdb.sql('select * from read_csv("hotdeel.csv") limit 10 offset 10').fetchall()

flag = True
con = duckdb.connect(database=":memory:", read_only=False)

def make_connection():
    global con
    if flag:
        con = duckdb.connect(database=":memory:", read_only=False)
        con.execute("CREATE TABLE table1 AS SELECT * FROM read_csv_auto('./hotdeal/hotdeal_fm.csv')")
        
    return con

con = make_connection()
# con = duckdb.connect()
query = """
    SELECT *
    FROM table1
    LIMIT 10
    OFFSET 10
""" 
result = con.execute(query).fetchall()

print(result)
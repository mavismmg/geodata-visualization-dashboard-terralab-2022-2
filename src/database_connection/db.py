import psycopg2

class Connection:
    def __init__(self, dbname='SGM', user='postgres', host='ec2-3-95-135-96.compute-1.amazonaws.com', password='trlab2021'):
        self.dbname = dbname
        self.user = user
        self.host = host
        self.password = password

    def connection(self):
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            host=self.host,
            password=self.password
        )

        return conn

    def table_names(self, conn):
        cur = conn.cursor()

        cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

        print(cur.fetchall())

    def table_exists(self, conn, table_str):
        exists = False

        try:
            cur = conn.cursor()
            cur.execute("select exists(select relname from pg_class where relname='" + table_str + "')")
            exists = cur.fetchone()[0]
            print(exists)
            cur.close()

        except psycopg2.Error as e:
            print(e)

        return exists

    def get_table_col_names(self, conn, table_str):
        col_names = []

        try:
            cur = conn.cursor()
            cur.execute("select * from " + table_str + " LIMIT 0")

            for desc in cur.description:
                col_names.append(desc[0])

            cur.close()

        except psycopg2.Error as e:
            print(e)

        return col_names
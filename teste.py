import psycopg2

#te
conn = psycopg2.connect(
            user="postgres",
            password="kinnikuman", #senha da database
            host="localhost",
            port="5432",
            database="avalicoes2" #nome da database que vai usar
        )
print(conn.encoding)

cursor = conn.cursor()

cursor.execute("SELECT * from aluno")

data = cursor.fetchall()

for d in data:
    print(d)

conn.close()

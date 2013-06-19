# psql: \conninfo
# You are connected to database "cicero" as user "cicero" via socket in "/tmp" at port "5432".

import psycopg2

conn = psycopg2.connect(
  database="eventsdb",
  user="cicero",
  host="/tmp",
  password="123"
)
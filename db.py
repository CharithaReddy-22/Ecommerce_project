import psycopg2

conn = psycopg2.connect(
    host="db.irozakpwlqkthddebkzh.supabase.co",
    database="postgres",
    user="postgres",
    password="my1stpro@22",
    port="5432"
)

cursor = conn.cursor()
import ftplib
from pathlib import Path
import rarfile as rarfile
from settings import HOST, USER, PASSWORD, FILE, HOME_URL, DATABASES, RESULT_FILE
from sql_code import create_csv_file
import psycopg2

# Connect to FTP server
ftp = ftplib.FTP(HOST, USER, PASSWORD)
ftp.encoding = "utf-8"

folder_task_data = (Path.home() / HOME_URL)

# Download file task.rar
with open(FILE, "wb") as f:
    ftp.retrbinary(f"RETR {FILE}", f.write)

# Unpack file task.rar
rarfile.RarFile(FILE).extractall(Path(folder_task_data, 'task_data'))

# Connect to DB PostgreSQL
with psycopg2.connect(
        database=DATABASES['NAME'],
        user=DATABASES['USER'],
        password=DATABASES['PASSWORD'],
) as conn:
    with conn.cursor() as cur:
        conn.autocommit = True

        cur.execute(create_csv_file)


ftp.cwd('/complete/Serhii_Honcharov')

# Upload file result.csv
with open(RESULT_FILE, "rb") as f:
    ftp.storbinary(f"STOR {RESULT_FILE}", f)

ftp.quit()



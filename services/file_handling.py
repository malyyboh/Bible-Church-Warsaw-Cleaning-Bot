import os
import sys
import csv
from datetime import date

CSV_FILE_PATH = 'csv_files/schedule_cleaning.csv'
SYS_CSV_FILE_PATH = os.path.join(sys.path[1], os.path.normpath(CSV_FILE_PATH))


def prepare_data_person(name: str) -> str:
    with open(SYS_CSV_FILE_PATH) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')

        if name.strip():
            name = ' '.join(name.split())
            data_person_list = []
            next(reader, None)
            for row in reader:
                if name.lower() in row[0].lower():
                    data_person_list.append(' '.join(row))
            data_person_str = '\n'.join(data_person_list)

            return data_person_str


def prepare_saturday_data_persons() -> str:
    today = date.today()
    with open(SYS_CSV_FILE_PATH) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        sunday_list = []
        next(reader, None)
        for row in reversed(list(reader)):
            row_lst = row[1].split('.')
            row_date = date(int(row_lst[2]), int(row_lst[1]), int(row_lst[0]))
            if today <= row_date and len(sunday_list) < 4:
                sunday_list.append(' '.join(row))
        saturday_data_persons = '\n'.join(sunday_list)

    return saturday_data_persons

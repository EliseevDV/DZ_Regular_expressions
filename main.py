from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding='utf8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
def fix_address_book(contacts_list):
    fixed_rows = []
    for row in contacts_list:
        name_parts = re.split('\s+', row[0])
        lastname = name_parts[0]
        firstname = name_parts[1] if len(name_parts) > 1 else ''
        surname = name_parts[2] if len(name_parts) > 2 else ''
        phone = re.sub(r'\D', '', row[5])
        phone = '+7({}) {}-{}-{}'.format(phone[1:4], phone[4:7], phone[7:9], phone[9:11])
        if len(phone) > 11:
            phone += ' доб.{}'.format(phone[11:])
        email = row[6] if row[6] else ''
        for c in fixed_rows:
            if c[0] == lastname and c[1] == firstname:
                c[2] = surname if surname else c[2]
                c[5] = phone if phone else c[5]
                c[6] = email if email else c[6]
                break
        else:
            fixed_rows.append([lastname, firstname, surname, row[3], row[4], phone, email])
    return fixed_rows


fixed_rows = fix_address_book(contacts_list)
header = ["lastname", "firstname", "surname", "organization", "position", "phone", "email"]
fixed_rows.insert(0, header)



# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("fixed_contacts.csv", "w", newline="", encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerows(fixed_rows)


import csv
import re

with open("phonebook_raw.csv", encoding='utf8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

def merge_duplicates(contacts_list):
    unique_data = {}
    for item in contacts_list:
        name = item[0]

        if name in unique_data:
            unique_item = unique_data[name]
            for key, value in item.items():
                if key != 'Name' and value and not unique_item.get(key):
                    unique_item[key] = value
        else:
            unique_data[name] = item
    return list(unique_data.values())


def repair_book(contacts_list):
    contacts_list = merge_duplicates(contacts_list)
    repaired_book = []
    seen_contacts = set()
    for row in contacts_list:
        full_name = re.sub(r'\s+', ' ', row[0].strip())
        last_name, first_name, surname = re.split(r'\s+', full_name, maxsplit=2) + [None, None, None][len(re.split(r'\s+', full_name,maxsplit=2)):]
        phone = re.sub(r'\D', '', row[5])
        phone = '+7({}) {}-{}-{}'.format(phone[1:4], phone[4:7], phone[7:9], phone[9:11])
        if len(row[5]) > 11:
            phone += ' доб.' + row[5][11:]
            email = row[6].lower()
            position = row[4].strip().lower()
            contact_info = (last_name, first_name, surname, email, phone, position)
            if contact_info in seen_contacts:
                continue
            seen_contacts.add(contact_info)
            repaired_book.append([last_name, first_name, surname] + row[1:5] + [phone, email])
    return repaired_book


fixed_rows = repair_book(contacts_list)

with open("fixed_contacts.csv", "w", newline="", encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerows(fixed_rows)




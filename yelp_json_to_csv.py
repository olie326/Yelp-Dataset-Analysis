import csv
import json


def get_columns(line, parent_key=''):

    columns = []
    for key, value in line.items():
        column_name = f'{parent_key}.{key}' if parent_key else key
        if type(value) is dict:
            columns.extend( 
                get_columns(value, column_name)
                    )
        elif value is None:
            continue
        else:
            columns.append(column_name)

    
    return columns


def get_headers(data_file_path):

    headers = set()
    with open(data_file_path, encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            headers.update(
                set(get_columns(data, ''))
            )
    
    return headers


def get_value(line, nested_key):

    val = line
    for key in nested_key.split('.'):
        if val is None:
            return None
        elif key in val:
            val = val[key]
        else:
            return None
    
    return val


def get_row(line, columns):

    row = []
    for column in columns:
        val = get_value(line, column)
        if val is not None:
            row.append(get_value(line, column))
        else:
            row.append('')

    return row


def write_to_csv(data_file_path, csv_file_path, columns):
    
    with open(csv_file_path, 'w+', newline='', encoding='utf-8') as csv_out:

        writer = csv.writer(csv_out)
        writer.writerow(columns)

        with open(data_file_path, encoding='utf-8') as data_file:

            for line in data_file:
                line_data = json.loads(line)
                row = get_row(line_data, columns)
                writer.writerow(row)


paths = ['yelp_academic_dataset_business.json', 'yelp_academic_dataset_checkin.json', 'yelp_academic_dataset_review.json', 
         'yelp_academic_dataset_tip.json', 'yelp_academic_dataset_user.json'
         ]

for path in paths:
    json_path = f'yelp_dataset/{path}'
    headers = list(get_headers(json_path))
    headers.sort()
    
    file_name = f'{path.removesuffix('.json')}.csv'

    write_to_csv(json_path, f'yelp_csv/{file_name}', headers)

print('success!')

# test_json = {"business_id":"UJsufbvfyfONHeWdvAHKjA","name":"Marshalls","address":"21705 Village Lakes Sc Dr","city":"Land O' Lakes","state":"FL","postal_code":"34639","latitude":28.1904587953,"longitude":-82.4573802199,"stars":3.5,"review_count":6,"is_open":1,"attributes":{"RestaurantsPriceRange2":"2","BikeParking":"True","BusinessAcceptsCreditCards":"True","BusinessParking":"{'garage': False, 'street': False, 'validated': False, 'lot': False, 'valet': False}"},"categories":"Department Stores, Shopping, Fashion","hours":{"Monday":"9:30-21:30","Tuesday":"9:30-21:30","Wednesday":"9:30-21:30","Thursday":"9:30-21:30","Friday":"9:30-21:30","Saturday":"9:30-21:30","Sunday":"10:0-20:0"}}


# print(get_columns(test_json))
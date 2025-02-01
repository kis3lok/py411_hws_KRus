from file_classes import *
data = [
    {"name": "John", "age": 30, "city": "New York"}, 
    {"name": "Alice", "age": 25, "city": "San Francisco"}, 
    {"name": "Bob", "age": 35, "city": "Los Angeles"},
        ]

new_data = [
    {"name": "Abraham", "age": 30, "city": "New York"}, 
    {"name": "Isaac", "age": 25, "city": "San Francisco"}, 
    {"name": "Isallah", "age": 35, "city": "Los Angeles"},
    {"name": "Lazarus", "age": 30, "city": "New York"},
    ]

if __name__ == "__main__":
    json_file = JsonFile("data.json")
    json_file.write(*data)
    json_file.append(*new_data)

    txt_file = TxtFile("data.txt")
    txt_file.write("Hello", "World")
    txt_file.append("H213123ello", "W32123orld")

    csv_file = CsvFile("data.csv")
    csv_file.write(*data)
    csv_file.append(*new_data)
    print(csv_file.read())

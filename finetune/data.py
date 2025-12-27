import csv

def generate_stock_json(csv_file):
    json_data = []

    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first header row
        next(reader)  # Skip the second bad row

        for row in reader:
            if len(row) < 5:  # Ensure the row has enough columns
                continue
            
            date = row[0].strip()
            try:
                stock_price = float(row[4].strip())  # Close price is in the 5th column (index 4)
                json_data.append({"month": date, "stock_price": stock_price})
            except ValueError:
                continue  # Skip rows where conversion fails

    return json_data



print(generate_stock_json("stock_data.csv"))
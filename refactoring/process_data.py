
#
# One big function doing everything
#

def process_data_bad(data):
    cleaned = [x.strip() for x in data if x]
    numbers = [int(x) for x in cleaned if x.isdigit()]
    average = sum(numbers) / len(numbers)
    print(f"Average is {average}")


#
# Refactored version
#

def clean_data(data):
    return [x.strip() for x in data if x]

def extract_numbers(data):
    return [int(x) for x in data if x.isdigit()]

def process_data(data):
    cleaned = clean_data(data)
    numbers = extract_numbers(cleaned)
    average = sum(numbers) / len(numbers)
    print(f"Average is {average}")

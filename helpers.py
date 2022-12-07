def get_data(day, suffix="1"):
    with open(f"./data/{day}-{suffix}.txt") as infile:
        return infile.readlines()


def chunk_list(values, chunk_size):
    return [values[i:(i + chunk_size)] for i in range(0, len(values), chunk_size)]

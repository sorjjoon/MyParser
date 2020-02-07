

with open('input', 'rb') as in_file:
    with open('runtime.txt', 'wb') as out_file:
        out_file.write(in_file.read()[:-1])


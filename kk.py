import zipfile

with zipfile.ZipFile("data.tb", "w") as zf:
    with zf.open("data1.json", "w") as f:
        f.write(b'{"message": "First write"}')
    
    with zf.open("data2.json", "w") as f:
        f.write(b'{"message": "Second write"}')
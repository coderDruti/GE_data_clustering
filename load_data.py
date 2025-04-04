import pandas as pd
def load_data(file):
    
    cols = file.split("\t").pop(0)
    print(cols)
    print(len(cols))

    data = []
    # for x in file:
    #     print(x+"\n")
    # print(file)
    y = []
    for i in range(0, len(file)):
        data.append(file[i].split("\t"))
        y.append(data[i].pop(0))

    # # for i in range(0, len(data)):
    # y.append(data[0][0])
    # print(data[0])
    # content = []
    # for i in range(0, len(data)):
    #     content.append(data[i])
    # print(len(content))
    # print(content)
    # print(y)
    df = pd.DataFrame(data,index=y, columns = cols)
    return df

def get_data_and_labels(num):
    result_data = []
    result_labels = []
    i = 0
    with open("txt/corpus.txt", 'r') as f:
        for line in f:
            if i < num:
                data = line.strip().split()
                result_data.append(data[1:])
                if data[0] == 'pos':
                    result_labels.append(1)
                else:
                    result_labels.append(0)
                i += 1
    return result_data, result_labels
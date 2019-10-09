import ga

def parser(file_name):
    file = open("../data/"+file_name, 'r')
    Name = file.readline().strip().split()[2]
    FileType = file.readline().strip().split()[2]
    Comment = file.readline().strip().split()[2]
    Dimension = file.readline().strip().split()[2]
    EdgeWeightType = file.readline().strip().split()[2]

    city_list = []

    file.readline()

    for i in range(0, int(Dimension)):
        x, y = file.readline().strip().split()[1:]
        city_list.append(ga.City(float(x), float(y)))

    file.close()

    return city_list

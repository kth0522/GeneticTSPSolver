import ga
from tqdm import tqdm

def parser(file_name):
    file = open("../data/"+file_name, 'r')
    Name = file.readline().strip().split()[2]
    FileType = file.readline().strip().split()[2]
    Comment = file.readline().strip().split()[2]
    Dimension = file.readline().strip().split()[2]
    EdgeWeightType = file.readline().strip().split()[2]

    city_list = []

    file.readline() #NODE_COORD_SECTION

    for i in tqdm(range(0, int(Dimension)), desc="data parsing now..."):
        x, y = file.readline().strip().split()[1:]
        city_list.append(ga.City(float(x), float(y), i))

    file.close()

    return city_list

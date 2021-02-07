from convert import extract_lat_lng
from ga import Node, geneticAlgorithm, geneticAlgorithmPlot
from delivery import distribute, distributeShow

# 讀取 input
f = open(r'input.csv', encoding="utf-8")
raw_data = []
for line in f:
    line = line.encode("utf-8").decode("utf-8-sig").strip()
    raw_data.append(line.split(","))
f.close()

# 地址轉成在 list 中的 index + 經緯度
coordinate = {}
for i in range(1, len(raw_data)):
    lat_lng = extract_lat_lng(raw_data[i][0])
    coordinate[i] = lat_lng

# Running the genetic algorithm
nodeList = []
for i in range(1, len(coordinate)):
    nodeList.append(Node(coordinate[i][0], coordinate[i][1]))

# route = geneticAlgorithm(population=nodeList, popSize=100, eliteSize=20, mutationRate=0.01, generations=10)
route = geneticAlgorithmPlot(population=nodeList, popSize=100, eliteSize=20, mutationRate=0.01, generations=90)

# 接收和分配的狀況
# db = distribute(rawData=raw_data, coordinate=coordinate, route=route) # 得到 dict
db = distributeShow(rawData=raw_data, coordinate=coordinate, route=route)

addressList = []
for node in db:
    addressList.append(db[node]['address'])
import json
addressList = json.dumps(addressList)
print(addressList + "\n")

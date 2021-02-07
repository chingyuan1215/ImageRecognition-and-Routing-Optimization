# 安全存貨
SPE_NUM = 0
NOR_NUM = 0
NUT_NUM = 5
RAW_NUM = 0

# 各種 index in rawData
ADDRESS_IDX = 0
SPE_IDX = 1
NOR_IDX = 2
NUT_IDX = 3
RAW_IDX = 4

SPE_DS = 1
NUT_DS = 2


class Vehicle:
    def __init__(self, special=SPE_NUM, normal=NOR_NUM, nutri=NUT_NUM, raw=RAW_NUM):
        self.special = special
        self.normal = normal
        self.nutri = nutri
        self.raw = raw
    
    def __repr__(self):
        content = {'special': self.special, 'normal': self.normal,
         'nutri': self.nutri, 'raw': self.raw}
        return str(content)

    def __str__(self):
        content = {'special': self.special, 'normal': self.normal,
         'nutrient': self.nutri, 'raw': self.raw}
        return str(content)

    def isEmpty(self):
        if (self.special == 0 and self.normal == 0 and self.nutri == 0 and self.raw == 0):
            return True
        else:
            return False
    
    def auto_select(self):
        category = 'normal'
        num = self.normal

        if (self.special > num):
            category = 'special'
            num = self.special
        if (self.nutri > num):
            category = 'nutri'
            num = self.nutri

        if (num == 0 and self.raw == 0):
            print("ERROR!")
            return None

        if (num == 0):
            self.raw -= 1
            return 'raw'

        if (category == 'normal'):
            self.normal -= 1
        elif (category == 'special'):
            self.special -= 1
        else: 
            self.nutri -= 1
        
        return category

def creatDB(rawData, coordinate, route):

    db = {}
    # db[0] 和 route_id 0 是咖啡館
    # db[0] = {'route_id': 0, 'address': '新北市永和區文化路155號', 'coordinate': (25.0163149, 121.510413), 'type': 'supply'}

    for i in range(len(route)):
        for key, value in coordinate.items():
            if (route[i] == value):
                db[key] = {'route_id': i, 'address': rawData[key][ADDRESS_IDX], 'coordinate': route[i]}
                # db[key] = {'route_id': i + 1, 'address': rawData[key][ADDRESS_IDX], 'coordinate': route[i]}

                if (rawData[key][-1] != ''):
                    db[key]['type'] = 'supply'
                    db[key]['special'] = int(rawData[key][SPE_IDX])
                    db[key]['normal'] = int(rawData[key][NOR_IDX])
                    db[key]['nutri'] = int(rawData[key][NUT_IDX])
                    db[key]['raw'] = int(rawData[key][RAW_IDX])

                else:
                    db[key]['type'] = 'demand'
                    db[key]['special_demand'] = int(rawData[key][SPE_DS])
                    db[key]['nutri_demand'] = int(rawData[key][NUT_DS])
                    db[key]['special'] = 0
                    db[key]['normal'] = 0
                    db[key]['nutri'] = 0
                    db[key]['raw'] = 0                

    return db

def compute(init_db, order, rawData):
    vehicle = Vehicle(special=SPE_NUM, normal=NOR_NUM, nutri=NUT_NUM, raw=RAW_NUM)
    db = init_db
    for key in order:
        person = db[key]
        if person['type'] == 'supply':
            if (person['special'] != 0):
                vehicle.special += person['special']
            if (person['normal'] != 0):
                vehicle.normal += person['normal']
            if (person['nutri'] != 0):
                vehicle.nutri += person['nutri']
            if (person['raw'] != 0):
                vehicle.raw += person['raw']            
        else:
            if (vehicle.isEmpty()):
                print("Nothing can give. Sorry To " + str(key))
            elif (person['nutri_demand'] >= 5 and vehicle.nutri > 0):
                vehicle.nutri -= 1
                person['nutri'] += 1
            elif (person['special_demand'] >= 5 and vehicle.special > 0):
                vehicle.special -= 1
                person['special'] += 1
            else:
                category = vehicle.auto_select()
                person[category] += 1     
    return db

def computeShow(init_db, order, rawData):
    vehicle = Vehicle(special=SPE_NUM, normal=NOR_NUM, nutri=NUT_NUM, raw=RAW_NUM)
    print("Initial vehicle status: " + str(vehicle) + "\n")

    db = init_db
    for key in order:
        print("Go to node " + str(key), end=' ')
        person = db[key]
        if person['type'] == 'supply':
            print("【Supply】")
            if (person['special'] != 0):
                vehicle.special += person['special']
                print("\tGet " + str(person['special']) + " special food")
                print("\tVehicle status now: " + str(vehicle))
            if (person['normal'] != 0):
                vehicle.normal += person['normal']
                print("\tGet " + str(person['normal']) + " normal food")
                print("\tVehicle status now: " + str(vehicle))
            if (person['nutri'] != 0):
                vehicle.nutri += person['nutri']
                print("\tGet " + str(person['nutri']) + " nutrient food")
                print("\tVehicle status now: " + str(vehicle))
            if (person['raw'] != 0):
                vehicle.raw += person['raw']
                print("\tGet " + str(person['raw']) + " raw material food")
                print("\tVehicle status now: " + str(vehicle)) 
        else:
            print("【Demand】")
            if (vehicle.isEmpty()):
                print("\tWarning: nothing can give to node " + str(key))
            elif (person['nutri_demand'] >= 5 and vehicle.nutri > 0):
                vehicle.nutri -= 1
                person['nutri'] += 1
                print("\tGive 1 nutrient food")
                print("\tVehicle status now: " + str(vehicle))
            elif (person['special_demand'] >= 5 and vehicle.special > 0):
                vehicle.special -= 1
                person['special'] += 1
                print("\tGive 1 special food")
                print("\tVehicle status now: " + str(vehicle))
            else:
                category = vehicle.auto_select()
                person[category] += 1
                if (category == 'nutri'):
                    category = 'nutrient'
                elif (category == 'raw'):
                    category = 'raw material'
                print("\tGive 1 " + category + " food")
                print("\tVehicle status now: " + str(vehicle))
    print("\nReturn to center\n")

    print("Assignment successful.\n")

    return db

def exportDB(db, file_name):
    import json
    # 輸出 output json 檔
    with open(file_name, 'w') as file_object:
        json.dump(db, file_object)

def exportDBShow(db, file_name):
    import json
    # 輸出 output json 檔
    with open(file_name, 'w') as file_object:
        json.dump(db, file_object)
        print("The file: " + file_name + " has been exported\n")

def upload(json_name):
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    #Login to Google Drive and create drive object
    g_login = GoogleAuth()
    g_login.LocalWebserverAuth()
    drive = GoogleDrive(g_login)
    # Importing os and glob to find all PDFs inside subfolder
    import glob, os
    for file in glob.glob(json_name):
        with open(file,"r") as f:
            fn = os.path.basename(f.name)
            file_drive = drive.CreateFile({'title': fn })  
            file_drive.SetContentString(f.read()) 
            file_drive.Upload()        
            permission = file_drive.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
    for file in glob.glob("*.jpg"):
        file_drive = drive.CreateFile()  
        file_drive.SetContentFile(file) 
        file_drive.Upload()
        permission = file_drive.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})

def uploadShow(json_name):
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    #Login to Google Drive and create drive object
    g_login = GoogleAuth()
    g_login.LocalWebserverAuth()
    drive = GoogleDrive(g_login)
    print("")
    import glob, os
    for file in glob.glob(json_name):
        with open(file,"r") as f:
            fn = os.path.basename(f.name)
            file_drive = drive.CreateFile({'title': fn })  
            file_drive.SetContentString(f.read()) 
            file_drive.Upload()        
            print("The file: " + fn + " has been uploaded")
            # Insert the permission.
            permission = file_drive.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
            print(file_drive['alternateLink'])
    # for file in glob.glob("*.jpg"):
    #     file_drive = drive.CreateFile()  
    #     file_drive.SetContentFile(file) 
    #     file_drive.Upload()
    #     print("The file: " + file + " has been uploaded")
    #     permission = file_drive.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
    #     print(file_drive['alternateLink'])
    print("\nExport and Upload successful.\n")

def distribute(rawData, coordinate, route):
    init = creatDB(rawData=rawData, coordinate=coordinate, route=route)
    order = list(init.keys())
    db = compute(init_db=init, order=order, rawData=rawData)
    exportDB(db, file_name='routing.json')
    upload(json_name='routing.json')
    return db

def distributeShow(rawData, coordinate, route):
    init = creatDB(rawData=rawData, coordinate=coordinate, route=route)
    order = list(init.keys())
    db = computeShow(init_db=init, order=order, rawData=rawData)
    # exportDBShow(db, file_name='routing.json')
    # uploadShow(json_name='routing.json')
    return db
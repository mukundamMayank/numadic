import csv
import datetime
import calendar
import os
from math import radians, cos, sin, asin, sqrt
import xlsxwriter
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def calc_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371
    return c * r

def findTheVehicles(st_time, end_time):
    
    vehicles=set()
    number_of_trips={}
    transporter_name={}

    with open('Trip-info.csv',mode='r') as file:
        csvfile = csv.reader(file)
        flag = 0
        for lines in csvfile:
            if flag==0:
                flag+=1
                continue
            year=int(lines[4][0:4])
            month=int(lines[4][4:6])
            day=int(lines[4][6:8])
            hour=int(lines[4][8:10])
            min=int(lines[4][10:12])
            second=int(lines[4][12:14])
            t=datetime.datetime(year, month, day, hour, min, second)
            epoch_time = calendar.timegm(t.timetuple())
            if epoch_time>=st_time and epoch_time<=end_time:
                if lines[3] in number_of_trips.keys():
                    number_of_trips[lines[3]]+=1
                else:
                    number_of_trips[lines[3]] = 1

                vehicles.add(lines[3])
                transporter_name[lines[3]] = lines[1]
    
    if len(vehicles)==0:
        return "No vehicles exist in the given time frame"

    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet("My sheet")
    row = 0
    col = 0

    worksheet.write(row,col, "License Number")
    worksheet.write(row,col+1, "Distance")
    worksheet.write(row,col+2, "Number of Trips Completed")
    worksheet.write(row,col+3, "Average Speed")
    worksheet.write(row,col+4, "Transporter Name")
    worksheet.write(row,col+5, "Number of Speed Violations")
    worksheet.autofit()
    row+=1
    cnt = 0

    for i in vehicles:
        cnt+=1
        distance = 0
        average_speed = 0
        speed_violations = 0
        if os.path.exists('NU-raw-location-dump\EOL-dump/'+i+'.csv'):
            with open('NU-raw-location-dump\EOL-dump/'+i+'.csv',mode='r', encoding="utf-8") as file:
                csvfile = csv.reader(file)
                flag=0
                prev_lat=0
                prev_lan=0
                for lines in csvfile:
                    if flag==0:
                        flag+=1
                        continue
                    if int(lines[11])>=st_time and int(lines[11])<=end_time:
                        if lines[8]:
                            speed_violations+=1
                        if prev_lat != 0 and prev_lan !=0:
                            if lines[7]!='' and lines[5]!='':
                                distance+=calc_distance(float(prev_lan), float(prev_lat), float(lines[7]), float(lines[5]))
                                prev_lat = float(lines[5])
                                prev_lan = float(lines[7])
                        else:
                            if lines[7]!='' and lines[5]!='':
                                prev_lat = float(lines[5])
                                prev_lan = float(lines[7])
                average_speed = (float(distance))/(float(end_time-st_time))

        final_params = [i, distance, number_of_trips[i], average_speed, transporter_name[i], speed_violations]
        for j in range(6):
            worksheet.write(row, j, final_params[j])
            worksheet.autofit()
                
        row+=1
        if cnt == len(vehicles):
            workbook.close()
    return "Excel output file created successfully"

@app.route("/getVehicleInfo", methods=['GET'])
def getVehicleInfo():
    
    data = request.args
    
    st_time = data.get('st_time')
    end_time = data.get('end_time')
    res = {"result": findTheVehicles(int(st_time), int(end_time))}
    return jsonify(result=res)

@app.route("/")
def start_app():
    return render_template('index.html')
    

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)

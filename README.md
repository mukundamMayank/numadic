How to run?
	-> Load all the csv like "The trip info" & "NU-raw-location-dump" in the same folder as project.
	-> Run app.py using python3 app.py, this will work as a server & index.html in templates folder will run. You can hit the local host & check for the index.html page.
	-> On this page you will see 2 input fields start time & end time , enter the query values here & press submit.
	-> Once you press submit 'getVehicleInfo' api will be called & required action of generating excel report will be done.
	-> Name of the excel file is 'output.xlsx'
	-> Right now I have kept 'output.xlsx' file, if you want you can delete it too before running the project.

Calculations:
	-> Number of trips completed is calculated by keeping count of the number of times a vehicle has started in trip during the queried time interval via 'Trip_info.csv'.
	-> Distance is calculated by using haversine formula on previous lattitude & longitude & current lattitude & longitud. This is done for each vehicle found in 'Trip_info.csv' while calculating number of trips.

Assumptions & Future Scope:
	-> I have assumed for any vehicle if we able to find some non zero number of trips via 'Trip_info.csv' but its csv is not available in the large data dump then distance is zero for that vehicle.
	-> This is done intentionally as marking it errorneous can affect calculations in the future.
	-> Rather we can K-NN for each distance marked zero & make its distance equal to closest neighbour having similar number of trips.

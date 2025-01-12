def riders(stations, station_x):
    riders = 1
    way_length = 0
    
    if station_x < 2:
        raise ValueError('Station_x is not valid')

    for i in range (len(stations)):
        if stations[i] < 0:
            raise ValueError('Stations is not valid')
        if way_length + stations[i] <= 100:
            if i == (station_x - 2):
                riders += 1
                if stations[i]*2 <= 100:
                    way_length = stations[i]*2
                else:
                    way_length = stations[i]
                    riders += 1
            else:
                way_length += stations[i]
        else:
            riders += 1
            if i == (station_x - 2):
                riders += 1
                if stations[i]*2 <= 100:
                    way_length = stations[i]*2
                else:
                    way_length = stations[i]
                    riders += 1
            else:
                way_length = stations[i]        
            
    return riders

    
def int_to_datetime(seconds):
    s = seconds%60
    m = seconds//60%60
    h = seconds//60//60
    return '{:02}:{:02}:{:02}'.format(h,m,s)

print (int_to_datetime(12))
print (int_to_datetime(61))
print (int_to_datetime(35999))
print (int_to_datetime(359999))
print (int_to_datetime(360000))

print ('{:02}:{:03}:{:02X}'.format(5,26,10))

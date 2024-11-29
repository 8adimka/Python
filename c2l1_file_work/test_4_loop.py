
rows = input ('rows')
columns = input('columns')

my_lst = []
for x in range (int (rows)):
    my_lst.append ([None for y in range(int (columns))])
    my_lst.append ('\n')
print (my_lst)

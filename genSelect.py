#aux function for printing a long string
for i in range(1,129):
    if i%4:
        d=' + '
    else:
        d=' + \n'
    print('POW(tpl{:03}-%s,2)'.format(i),end=d)


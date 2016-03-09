__author__ = 'sunary'


import os


def voz():
    for i in range(1, 9):
        s = ''
        for j in range(i, 3*i - 1):
            if j < 2*i:
                s += str(j%10) + ' '
            else:
                s += str((4*i - j - 2)%10) + ' '

        print s


files_number = []
for i in range(10):
    files_number.append(os.path.join(os.path.dirname(__file__) + '/../resources/no_%s.jpg' % str(i)))


print files_number
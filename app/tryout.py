from db import Db

'''
call the functions with any database name and it will be created on the fly
was supposed to incorporate in in app factory but time strapped
'''
a = Db('level').savesimcard('mike', 56, 66, 'mtn', 12, True)
b = Db('level').get_count('simcards')
c = Db('level').savesimcard('miiike', 50, 76, 'mtn', 12, True)
d = Db('level').get_count('simcards')
e = Db('level').savesimcard('mke', 55, 56, 'mtn', 11, True)
f = Db('level').get_count('simcards')
g = Db('level').get_simcard(1)
h = Db('level').update_simcard('moses', 1, 'name')
i = Db('level').get_simcards()
j = Db('level').get_human_simcards(12)
k = Db('level').delete_simcard(3)
l = Db('level').get_count('simcards')

for i in (a, b, c, d, e, f, g, h, i, j, k, l):
    print(i)


#similar for human

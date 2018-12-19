from db import Db

'''
call the functions with any database name and it will be created on the fly
was supposed to incorporate in in app factory but time strapped
'''
a = Db('levelup').savesimcard('mike', 56, 66, 'mtn', 12, True)
b = Db('levelup').savesimcard('miiike', 50, 76, 'mtn', 12, True)
c = Db('levelup').savesimcard('mke', 55, 56, 'mtn', 11, True)
d = Db('levelup').get_simcard(1)
e=Db('levelup').update_simcard('moses', 1, 'name')
g = Db('levelup').get_simcards()
f = Db('levelup').get_human_simcards(12)
g = Db('levelup').delete_simcard(3)

for i in (a, b, c, d, e, f, g):
    print(i)


#similar for human

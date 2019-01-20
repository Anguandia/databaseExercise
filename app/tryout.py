from db import Db

'''
call the functions with any database name and it will be created on the fly
was supposed to incorporate in in app factory but time strapped
'''
#a = Db('miba').savesimcard('mike', 56, 66, 'mtn', 12, True)
#b = Db('miba').get_count('simcards')
#c = Db('miba').savesimcard('miiike', 50, 76, 'mtn', 12, True)
#d = Db('miba').get_count('simcards')
#e = Db('miba').savesimcard('mke', 55, 56, 'mtn', 11, True)
#f = Db('miba').get_count('simcards')
#g = Db('miba').get_simcard(1)
#h = Db('miba').update_simcard('moses', 1, 'name')
#i = Db('miba').get_simcards()
#j = Db('miba').get_human_simcards(12)
#k = Db('miba').delete_simcard(3)
#l = Db('miba').get_count('simcards')
#
#for i in (a, b, c, d, e, f, g, h, i, j, k, l):
#    print(i)
#print(Db('mibaup').get_humans())

#similar for human

#Db('miba').create('me', 'here', 23)
print(Db('twice').get_humans())

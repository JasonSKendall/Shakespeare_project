#!python

import re
import urllib.request, urllib.parse, urllib.error


list_of_plays = [ 'othello', 'much_ado', 'lear', 'midsummer', 'merry_wives', 'twelfth_night', 'titus',
                 'allswell', 'asyoulikeit', 'cymbeline', 'lll', 'measure', 'merchant', 'pericles', 'taming_shrew',
                 'tempest', 'troilus_cressida', 'two_gentlemen', 'winters_tale', '1henryiv', '2henryiv', 'henryv',
                 '1henryvi', '2henryvi', '3henryvi', 'henryviii', 'john', 'richardii', 'richardiii', 'cleopatra',
                 'coriolanus', 'hamlet', 'julius_caesar', 'macbeth', 'romeo_juliet', 'timon', 'comedy_errors' ]


play = list_of_plays[17]
print(play)




url_to_grab = 'http://shakespeare.mit.edu/' + play + '/full.html'
fhand = urllib.request.urlopen(url_to_grab)

play = 'julius_caesar'
fhand = open('/Users/jasonkendall/Desktop/shakespeare/' + play + '/full.html')

casting = dict()
list_of_scenes = []
list_of_roles = []

def read_in_play_data():

  theact = 'Induction'
  thescene = 'Prologue'

  for rawline in fhand:
    # j = rawline.decode().rstrip()
    j = rawline.rstrip()

    Divider_act = "H3>ACT "
    isact = j.find(Divider_act)
    if isact != -1:
      theact = re.split('[<> ]',j)[3]
      continue

    Divider_scene = "h3>SCENE "
    isscene = j.find(Divider_scene)
    if isscene != -1:
      thescene= re.split('[<> \.]',j)[3]
      act_and_scene = theact + '.' + thescene
      list_of_scenes.append(act_and_scene)
      continue

    Divider_scene_prologue = "h3>PROLOGUE" 
    isscene_prologue = j.find(Divider_scene_prologue)
    if isscene_prologue != -1:
      act_and_scene = theact + '.Prologue'  
      list_of_scenes.append(act_and_scene)
      print(act_and_scene)
      continue

    Divider_role = "NAME=speech"
    isrole = j.find(Divider_role) 
    if isrole != -1: 
      role = fix_role_name (  re.sub( ' ' , '_' ,   re.split('[\<|\>]', j)[4]  ) )
      if role not in list_of_roles:
        list_of_roles.append(role)
      key_role = (role, act_and_scene)
      if key_role in casting:
        casting[key_role] += 1
      else:
        casting[key_role] = 1




def fix_role_name(i):
  role_fixes = { 'First_': '_1', 'Second_': '_2', 'Third_': '_3', 'Fourth_': '_4'}
  for j in role_fixes.keys():
    if i.find(j, 0, ) != -1:
      i = i.replace(j, '') + role_fixes[j]
  return i




read_in_play_data()

breakdown_2_data = {}
breakdown_2 = {}
scenelist = []

for i in list_of_scenes:
  scenelist.append(i)
breakdown_2_data['Role'] = scenelist

for i in list_of_roles:
  scenelist = []
  for j in list_of_scenes:
    key = (i,j)
    if key in casting:
      speech_counts = casting[key]
    else:
      speech_counts = 0
    scenelist.append(speech_counts)
  breakdown_2[i] = scenelist
  





print('Role' , ' : ' ,breakdown_2_data['Role'])
for key in sorted(breakdown_2.keys()):
  print(key, ' : ' , breakdown_2[key] )
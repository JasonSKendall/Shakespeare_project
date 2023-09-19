#!python

import re
import urllib.request, urllib.parse, urllib.error


list_of_plays = [ 'othello', 'much_ado', 'lear', 'midsummer', 'merry_wives', 'twelfth_night', 'titus', 'allswell', 'asyoulikeit', 'cymbeline', 'lll', 'measure', 'merchant', 'pericles', 'taming_shrew', 'tempest', 'troilus_cressida', 'two_gentlemen', 'winters_tale', '1henryiv', '2henryiv', 'henryv', '1henryvi', '2henryvi', '3henryvi', 'henryviii', 'john', 'richardii', 'richardiii', 'cleopatra', 'coriolanus', 'hamlet', 'julius_caesar', 'macbeth', 'romeo_juliet', 'timon', 'comedy_errors' ]


play = list_of_plays[17]
print(play)

url_to_grab = 'http://shakespeare.mit.edu/' 
fhand = urllib.request.urlopen(url_to_grab)



def get_list_of_plays():
  for rawline in fhand:
    j = rawline.decode().rstrip()
    playpage = '/index.html'
    isplay = j.find(playpage)
    if isplay != -1:
      theplay = re.split('[<>"]',j)[4]
      print(theplay)
      continue


# get_list_of_plays()

# quit()


role_fixes = { 'First_': '_1', 'Second_': '_2', 'Third_': '_3', 'Fourth_': '_4'}

list_of_excluded_roles = [ 'Here_stand_I' , # LLL \
                          'As_long_as_you_or_I' , # M4M \
                          'This_way_will_I' # JC
                          ]

casting = dict()
list_of_scenes = []
list_of_roles = []

Divider_act = "H3>ACT "
Divider_scene = "h3>SCENE "
Divider_scene_prologue = "h3>PROLOGUE" 
Divider_role = "NAME=speech"

url_to_grab = 'http://shakespeare.mit.edu/' + play + '/full.html'
fhand = urllib.request.urlopen(url_to_grab)

# play = 'comedy_errors'
fhand = open('/Users/jasonkendall/Desktop/shakespeare/' + play + '/full.html')


def read_in_play_data():
  for rawline in fhand:
    # j = rawline.decode().rstrip()
    j = rawline.rstrip()
    isact = j.find(Divider_act)
    if isact != -1:
      theact = re.split('[<> ]',j)[3]
      continue
    isscene = j.find(Divider_scene)
    if isscene != -1:
      thescene= re.split('[<> \.]',j)[3]
      act_and_scene = theact + '.' + thescene
      list_of_scenes.append(act_and_scene)
      continue

    isscene_prologue = j.find(Divider_scene_prologue)
    if isscene_prologue != -1:
      act_and_scene = theact + '.Prologue'  
      list_of_scenes.append(act_and_scene)
      print(act_and_scene)
      continue

    isrole = j.find(Divider_role) 
    if isrole != -1: 
      role = fix_role_name (  re.sub( ' ' , '_' ,   re.split('[\<|\>]', j)[4]  ) )
      if role  not in list_of_roles and role not in list_of_excluded_roles:
        list_of_roles.append(role)
      key_role = (role, act_and_scene)
      if key_role in casting:
        casting[key_role] += 1
      else:
        casting[key_role] = 1


# def fix_role_name_prefix(role, prefix, suffix):
#   if role.find(prefix, 0, ) != -1:
#     role = role.replace(prefix, '') + suffix
#     return role
#   else:
#     return


def fix_role_name(i):
  for j in role_fixes.keys():
    if i.find(j, 0, ) != -1:
      i = i.replace(j, '') + role_fixes[j]
  return i



# def print_out_breakdown_1():  
#   print("Role" , end=',')
#   for l in list_of_scenes:
#     print(l , end=",")
#   print()
# 
#   num_actors_in_scene = dict.fromkeys(list_of_scenes , 0)
#   for i in sorted(list_of_roles):
#     ii = i + ','
#   print(ii, end='')
#   for j in list_of_scenes:
#     key=(i,j)
#     if key in casting:
#     # print(key)
#       print(casting[key], end=',')
#       num_actors_in_scene[j] += 1
#     else:
#       print('', end=',')
#     print()
#   print("Number_of_actors" , end=',')
#   for j in list_of_scenes:
#     print(num_actors_in_scene[j], end=',')
#   print()




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
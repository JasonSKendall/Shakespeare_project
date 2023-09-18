#!python

import re
import urllib.request, urllib.parse, urllib.error


# play = 'othello'
# play = 'much_ado'
# play = 'lear'
# play = 'midsummer'
# play = 'merry_wives'
# play = 'twelfth_night'
play = 'titus'
play = 'allswell'
play = 'asyoulikeit'
play = 'comedy_errors' # has big issues...
play = 'cymbeline'
play = 'lll'
play = 'measure'
play = 'merchant'
play = 'pericles'
play = 'taming_shrew' # has Induction, so ACT 0
play = 'tempest'
play = 'troilus_cressida'
play = 'two_gentlemen'
play = 'winters_tale'
play = '1henryiv'
play = '2henryiv' # hal induction, act 0
play = 'henryv' # has prologue
play = '1henryvi' # hal OF_charname isssues
play = '2henryvi'
play = '3henryvi'
play = 'henryviii'
play = 'john'
play = 'richardii'
play = 'richardiii' # many janky _of_ characters
play = 'cleopatra'
play = 'coriolanus'
play = 'hamlet'
play = 'julius_caesar'
play = 'macbeth'
play = 'romeo_juliet'
play = 'timon'


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


get_list_of_plays()

quit()


role_fixes = { 'First_': '_1', 'Second_': '_2', 'Third_': '_3', 'Fourth_': '_4'}
role_misspell = { 'HERNIA': 'HERMIA', \
                 'LEAR': 'KING_LEAR', \
                  'Gentlemen_2': 'Gentleman_2', \
                    'BOTH': 'Both', \
                      'A_Lord': 'Lord', \
                        'OF_SYRACUSE': 'ANTIPHOLUS_OF_SYRACUSE', \
                          'OF_EPHESUS': 'ANTIPHOLUS_OF_EPHESUS', \
                            'Posthumus_Leonatus' : 'POSTHUMUS_LEONATUS' , \
                              'POMPHEY' : 'POMPEY' ,\
                              'SU_FFOLK' : 'SUFFOLK' ,\
                              'Murder_1' : 'Murderer_1', \
                              'murderer_2' : 'Murderer_2' , \
                              'GUILDENSTERN:' : 'GUILDENSTERN' , \
                              'ROSENCRANTZ:' : 'ROSENCRANTZ' , \
                              'Nurse' : 'NURSE' , \
                              'Senator__1' : 'Senator_1'
}

list_of_excluded_roles = [ 'Here_stand_I' , # LLL \
                          'As_long_as_you_or_I' , # M4M \
                          'This_way_will_I' # JC
                          ]

casting = dict()
list_of_scenes = []
list_of_roles = []

Divider_act = "H3>ACT "
Divider_scene = "h3>SCENE "
Divider_scene_bad_format = "<b>Scene " # found in Cymbeline II.III
Divider_role = "NAME=speech"

url_to_grab = 'http://shakespeare.mit.edu/' + play + '/full.html'
fhand = urllib.request.urlopen(url_to_grab)


def read_in_play_data():
  for rawline in fhand:
    j = rawline.decode().rstrip()
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

    isscene_bad_format = j.find(Divider_scene_bad_format)
    if isscene_bad_format != -1:
      thescene = re.split('[<>]',(re.split(Divider_scene_bad_format,j)[1]))[0]
      act_and_scene = theact + '.' + thescene
      list_of_scenes.append(act_and_scene)
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
  for j in role_misspell.keys():
    if i == j:
      i = i.replace(j, '') + role_misspell[j]
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
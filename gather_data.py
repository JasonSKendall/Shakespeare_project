#!python

import re
import urllib.request, urllib.parse, urllib.error

location_of_source = 'mac'
play = 'romeo_juliet'

def choose_play(loc, play):
  list_of_plays = [ 'othello', 'much_ado', 'lear', 'midsummer', 'merry_wives', 'twelfth_night', 'titus',
                 'allswell', 'asyoulikeit', 'cymbeline', 'lll', 'measure', 'merchant', 'pericles', 'taming_shrew',
                 'tempest', 'troilus_cressida', 'two_gentlemen', 'winters_tale', '1henryiv', '2henryiv', 'henryv',
                 '1henryvi', '2henryvi', '3henryvi', 'henryviii', 'john', 'richardii', 'richardiii', 'cleopatra',
                 'coriolanus', 'hamlet', 'julius_caesar', 'macbeth', 'romeo_juliet', 'timon', 'comedy_errors' ]
  if play == None:
    play = list_of_plays[17]
  print(play)
  if loc == 'web':
    url_to_grab = 'http://shakespeare.mit.edu/' + play + '/full.html'
    return urllib.request.urlopen(url_to_grab)
  else:
    return open('/Users/jasonkendall/Desktop/shakespeare/' + play + '/full.html')

def read_in_play_data():

  theact = 'Induction'
  thescene = 'Prologue'

  for rawline in fhand:
    if location_of_source == 'web':
      j = rawline.decode().rstrip()
    else:
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

def create_role_scene_list():
  for i in list_of_scenes:
    scenelist.append(i)
  breakdown_data['Role'] = scenelist

def create_list_of_scenes_per_role():
  for i in list_of_roles:
    scenelist = []
    for j in list_of_scenes:
      key = (i,j)
      if key in casting:
        speech_counts = casting[key]
      else:
        speech_counts = 0
      scenelist.append(speech_counts)
    breakdown[i] = scenelist
  
def print_out_breakdown():
  print('Role' , ' : ' ,breakdown_data['Role'])
  for key in sorted(breakdown.keys()):
    print(key, ' : ' , breakdown[key] )

fhand = choose_play(location_of_source, play)
casting = dict()
list_of_scenes = []
list_of_roles = []
breakdown_data = {}
breakdown = {}
scenelist = []

read_in_play_data()
create_role_scene_list()
create_list_of_scenes_per_role()
print_out_breakdown()




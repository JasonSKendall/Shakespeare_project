#!python

import re
import urllib.request, urllib.parse, urllib.error

class Breakdown:
  def __init__(self, play='othello', list_of_scenes=[], list_of_roles = [], casting={}, breakdown={}) -> None:
    self.play = play
    self.list_of_scenes = list_of_scenes
    self.list_of_roles = list_of_roles
    self.casting = casting
    self.breakdown = breakdown

  def list_of_plays(): 
    current_list = [ 'othello', 'much_ado', 'lear', 'midsummer', 'merry_wives', 'twelfth_night', 'titus',
                 'allswell', 'asyoulikeit', 'cymbeline', 'lll', 'measure', 'merchant', 'pericles', 'taming_shrew',
                 'tempest', 'troilus_cressida', 'two_gentlemen', 'winters_tale', '1henryiv', '2henryiv', 'henryv',
                 '1henryvi', '2henryvi', '3henryvi', 'henryviii', 'john', 'richardii', 'richardiii', 'cleopatra',
                 'coriolanus', 'hamlet', 'julius_caesar', 'macbeth', 'romeo_juliet', 'timon', 'comedy_errors' ] 
    return(current_list)

  def create_list_of_scenes_per_role(self):
    for i in self.list_of_roles:
      scenelist = []
      for j in self.list_of_scenes:
        key = (i,j)
        if key in self.casting:
          speech_counts = self.casting[key]
        else:
          speech_counts = 0
        scenelist.append(speech_counts)
      self.breakdown[i] = scenelist
    return (self.breakdown)

  def print_out_breakdown(self):
    self.create_list_of_scenes_per_role()
    print('Role' , ' : ' ,self.list_of_scenes)
    for key in sorted(p1.breakdown.keys()):
      print(key, ' : ' , self.breakdown[key] )

p1 = Breakdown()

location_of_source = 'mac'
play = p1.play

def choose_play(loc, play):
  if play == None:
    play = p1.play
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
      p1.list_of_scenes.append(act_and_scene)
      continue

    Divider_scene_prologue = "h3>PROLOGUE" 
    isscene_prologue = j.find(Divider_scene_prologue)
    if isscene_prologue != -1:
      act_and_scene = theact + '.Prologue'  
      p1.list_of_scenes.append(act_and_scene)
      continue

    Divider_role = "NAME=speech"
    isrole = j.find(Divider_role) 
    if isrole != -1: 
      role = fix_role_name (  re.sub( ' ' , '_' ,   re.split('[\<|\>]', j)[4]  ) )
      if role not in p1.list_of_roles:
        p1.list_of_roles.append(role)
      key_role = (role, act_and_scene)
      if key_role in p1.casting:
        p1.casting[key_role] += 1
      else:
        p1.casting[key_role] = 1

def fix_role_name(i):
  role_fixes = { 'First_': '_1', 'Second_': '_2', 'Third_': '_3', 'Fourth_': '_4'}
  for j in role_fixes.keys():
    if i.find(j, 0, ) != -1:
      i = i.replace(j, '') + role_fixes[j]
  return i




  

fhand = choose_play(location_of_source, play)


#read_in_play_data()
#p1.print_out_breakdown()


def accum(s):
  x = set(s.lower())
  counter = 0
  for i in x:
    if s.lower().count(i) > 1:
      counter += 1
  print(s, x , counter)



accum("abcAdcc") #-> "A-Bb-Ccc-Dddd"
accum("RqaEzteyyy") #-> "R-Qq-Aaa-Eeee-Zzzzz-Tttttt-Yyyyyyy"
accum("cwAt") #-> "C-Ww-Aaa-Tttt"

#!python

import re
import urllib.request, urllib.parse, urllib.error

class Breakdown:
  def __init__(self, play=None, loc=None, list_of_scenes=[], list_of_roles = [], casting={}, breakdown={}) -> None:
    self.play = play
    self.loc = loc
    self.list_of_scenes = list_of_scenes
    self.list_of_roles = list_of_roles
    self.casting = casting
    self.breakdown = breakdown

  def dict_of_plays(): 
    current_dict = { 'othello': "Othello",
                    'much_ado': "Much Ado About Nothing",
                    'lear': "King Lear",
                    'midsummer': "A Midsummer Night's Dream",
                    'merry_wives' : "The Merry Wives of Windsor",
                    'twelfth_night': "Twelfth Night",
                    'titus': "Titus Andronicus",
                    'allswell' : "All's Well That Ends Well",
                    'asyoulikeit': "As You Like It",
                    'cymbeline': "Cymbeline",
                    'lll': "Love's Labours Lost",
                    'measure': "Measure for Measure",
                    'merchant': "The Merchant of Venice",
                    'pericles': "Pericles, Prince of Tyre",
                    'taming_shrew': "Taming of the Shrew",
                    'tempest': "The Tempest",
                    'troilus_cressida': "Troilus and Cressida",
                    'two_gentlemen': "The Two Gentlemen of Verona",
                    'winters_tale': "The Winter's Tale",
                    '1henryiv' : "King Henry the IV, Part 1",
                    '2henryiv' : "King Henry the IV, Part 2",
                    'henryv' : "King Henry the V",
                    '1henryvi' : "King Henry the VI, Part 1",
                    '2henryvi' : "King Henry the VI, Part 2",
                    '3henryvi' : "King Henry the VI, Part 3",
                    'henryviii' : "King Henry the VIII",
                    'john' : "King John",
                    'richardii' : "King Richard II",
                    'richardiii': "King Richard the III",
                    'cleopatra': "Cleopatra",
                    'coriolanus': "Coriolanus",
                    'hamlet': "Hamlet",
                    'julius_caesar': "Julius Caesar",
                    'macbeth' : "Macbeth",
                    'romeo_juliet': "Romeo and Juliet",
                    'timon': "Timon of Athens",
                    'comedy_errors': "The Comedy of Errors" } 
    return(current_dict)

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
    for key in sorted(self.breakdown.keys()):
      print(key, ' : ' , self.breakdown[key] )

  def choose_play(self):
    if self.loc == 'web':
      # url_to_grab = 'http://shakespeare.mit.edu/' + play + '/full.html'
      url_to_grab = 'http://www.jasonkendall.com/shakespeare_plays/' + self.play + '.html'
      return urllib.request.urlopen(url_to_grab)
    else:
      return open('/Users/jasonkendall/Desktop/shakespeare/' + self.play + '/full.html', mode='r')


  def fix_role_name(self, rolename=None):
    self.rolename = rolename
    role_fixes = { 'First_': '_1', 'Second_': '_2', 'Third_': '_3', 'Fourth_': '_4' , 'Fifth_': '_5' , 'Sixth_': '_6' , 'Seventh_': '_7' }
    for j in role_fixes.keys():
      if rolename.find(j, 0, ) != -1:
        rolename = rolename.replace(j, '') + role_fixes[j]
    return rolename

  
  def read_in_play_data(self):
    fhand = self.choose_play()
    theact = 'Induction'
    thescene = 'Prologue'
    for rawline in fhand:
      if self.loc == 'web':
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
        self.list_of_scenes.append(act_and_scene)
        continue
      Divider_scene_prologue = "h3>PROLOGUE" 
      isscene_prologue = j.find(Divider_scene_prologue)
      if isscene_prologue != -1:
        act_and_scene = theact + '.Prologue'  
        self.list_of_scenes.append(act_and_scene)
        continue
      Divider_role = "NAME=speech"
      isrole = j.find(Divider_role) 
      if isrole != -1: 
        role = self.fix_role_name(  re.sub( ' ' , '_' ,   re.split('[\<|\>]', j)[4]  ) )
        if role not in self.list_of_roles:
          self.list_of_roles.append(role)
        key_role = (role, act_and_scene)
        if key_role in self.casting:
          self.casting[key_role] += 1
        else:
          self.casting[key_role] = 1

  def print_out_breakdown_html(self):
    self.create_list_of_scenes_per_role()
    colspan = str(len(self.create_list_of_scenes_per_role()) + 1)
    curline = '<table cellpadding="5" border="1" bgcolor="white">'
    print(curline)
    curline = '<TH colspan="' + colspan + '">Casting Breakdown</TH>'
    print(curline)
    curline = "<TR><TD>Role</TD>"
    for i in self.list_of_scenes:
      i = '<TD>' + i + '</TD>'
      curline += i
    curline += '</TR>'
    print(curline)
    for key in sorted(self.breakdown.keys()):
      curline = "<TR><TD>" + key + "</TD>"
      for i in self.breakdown[key]:
        curline += '<TD>' + str(i) + '</TD>'
      curline += '</TR>'
      print(curline)
    print('</table>')







p1 = Breakdown("midsummer", "web")
p1.read_in_play_data()
p1.print_out_breakdown_html()

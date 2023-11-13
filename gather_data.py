#!python

import re
import csv
import urllib.request, urllib.parse, urllib.error

class Breakdown:
  def __init__(self, play=None, loc='web', list_of_scenes=[], list_of_roles = [], casting={}, breakdown={}) -> None:
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


  def choose_play(self):
    if self.loc == 'mac':
      return open('/Users/jasonkendall/Desktop/shakespeare/' + self.play + '/full.html', mode='r')
    else:
      # url_to_grab = 'http://shakespeare.mit.edu/' + play + '/full.html'
      url_to_grab = 'http://www.jasonkendall.com/shakespeare_plays/' + self.play + '.html'
      return urllib.request.urlopen(url_to_grab)


  def fix_role_name(self, rolename=None):
    self.rolename = rolename
    role_fixes = { 'First_': '_1', 'Second_': '_2', 'Third_': '_3', 'Fourth_': '_4' , 'Fifth_': '_5' , 'Sixth_': '_6' , 'Seventh_': '_7' }
    for j in role_fixes.keys():
      if j in rolename:
        rolename = rolename.replace(j, '') + role_fixes[j]
    return rolename

  
  def read_in_play_data(self):
    fhand = self.choose_play()
    theact = 'Induction'
    thescene = 'Prologue'
    for rawline in fhand:
      if self.loc == 'web':
        current_line = rawline.decode().rstrip()
      else:
        current_line = rawline.rstrip()
      if "<H3>ACT " in current_line:
        theact = re.split('[<> ]',current_line)[3]
        continue
      if "<h3>SCENE " in current_line:
        thescene= re.split('[<> \.]',current_line)[3]
        act_and_scene = theact + '.' + thescene
        self.list_of_scenes.append(act_and_scene)
        continue
      if "<h3>PROLOGUE" in current_line:
        act_and_scene = theact + '.Prologue'  
        self.list_of_scenes.append(act_and_scene)
        continue
      if "NAME=speech" in current_line:
        role = self.fix_role_name(  re.sub( ' ' , '_' ,   re.split('[\<|\>]', current_line)[4]  ) )
        if role not in self.list_of_roles:
          self.list_of_roles.append(role)
        key_role = (role, act_and_scene)
        if key_role in self.casting:
          self.casting[key_role] += 1
        else:
          self.casting[key_role] = 1

  def create_breakdown_list(self):
    bd_full_list = []
    cur_role = []
    self.create_list_of_scenes_per_role()
    cur_role.append( "Role")
    for i in self.list_of_scenes:
      cur_role.append(i)
    bd_full_list.append(cur_role)
    cur_role = []
    for key in sorted(self.breakdown.keys()):
      cur_role.append(key)
      for i in self.breakdown[key]:
        cur_role.append(str(i))
      bd_full_list.append(cur_role)
      cur_role = []
    return(bd_full_list)

  def print_out_breakdown(self):
    self.read_in_play_data()
    this_play_bd = self.create_breakdown_list()
    for i in this_play_bd:
      print(i)


  def print_out_breakdown_csv(self):
    self.read_in_play_data()
    this_play_bd = self.create_breakdown_list()
    with open( self.play + '.csv' , 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerows(this_play_bd)


  def print_out_breakdown_html(self):
    self.read_in_play_data()
    this_play_bd = self.create_breakdown_list()
    html_filename = self.play + '.html'
    with open(html_filename , 'w', newline='') as writer:
      colspan = str(len(this_play_bd[0]))
      curline = '<table cellpadding="5" border="1" bgcolor="white"><TH colspan="' + colspan + '">Casting Breakdown</TH>\n'
      writer.write(curline)
      for i in this_play_bd:
        curline = f"<TR><TD>{'</TD><TD>'.join(i)}</TD></TR>\n"
        writer.write(curline)
      writer.write('</table>')





p1 = Breakdown("midsummer")
p1.print_out_breakdown()
p1.print_out_breakdown_html()
p1.print_out_breakdown_csv()

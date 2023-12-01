#!python

import re
import csv
import urllib.request, urllib.parse, urllib.error
import pysftp
import ftplib


class Breakdown:
  def __init__(self,
               play=None,
               loc='web',
               bd_full_list=[] ,
               list_of_scenes=[]) -> None:
    self.play = play
    self.loc = loc
    self.bd_full_list = bd_full_list
    self.list_of_scenes = list_of_scenes

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



  def get_list_of_plays_sftp(self):
    myHostname = "XXXX"
    myUsername = "XXXXX"
    myPassword = "XXXXX"
    myDir = '/htdocs/shakespeare_plays/'
    try:
      with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
        print("Connection succesfully stablished ... ")
        sftp.cwd(myDir)
        directory_structure = sftp.listdir_attr()
        for attr in directory_structure:
          print(attr.filename, attr)
    except:
      print('cant connect')



  def get_list_of_plays(self):
    myHostname = "XXXXX"
    myUsername = "XXXXX"
    myPassword = "XXXXXX"
    myDir = '/htdocs/shakespeare_plays/'
    try:
      ftp = ftplib.FTP(myHostname)
      ftp.login(myUsername, myPassword)
      ftp.cwd(myDir)
      data = []
      ftp.dir(data.append)
      ftp.quit()
      for line in data:
        print("-", line)
    except:
      print("cant log in")



  def choose_play(self):
    if self.loc == 'mac':
      return open('/Users/jasonkendall/Desktop/shakespeare/' + self.play + '/full.html', mode='r')
    else:
      # url_to_grab = 'http://shakespeare.mit.edu/' + play + '/full.html'
      url_to_grab = 'http://www.jasonkendall.com/shakespeare_plays/' + self.play + '.html'
      return urllib.request.urlopen(url_to_grab)




  def fix_role_name(self, rolename=None):
    self.rolename = rolename
    role_fixes = { 'First_': '_1',
                  'Second_': '_2',
                  'Third_': '_3',
                  'Fourth_': '_4',
                  'Fifth_': '_5',
                  'Sixth_': '_6',
                  'Seventh_': '_7' }
    for j in role_fixes.keys():
      if j in rolename:
        rolename = rolename.replace(j, '') + role_fixes[j]
    return rolename




  
  def read_in_play_data(self):
    fhand = self.choose_play()
    breakdown_dict = dict()
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
        if role not in breakdown_dict.keys():
          breakdown_dict[role] = dict()
        if act_and_scene not in breakdown_dict[role].keys():
          breakdown_dict[role][act_and_scene] = 0
        breakdown_dict[role][act_and_scene] += 1
    for role in breakdown_dict.keys():
      for act_and_scene in self.list_of_scenes:
        if act_and_scene not in breakdown_dict[role].keys():
          breakdown_dict[role][act_and_scene] = 0
    top_row = ['ROLE'] + self.list_of_scenes
    self.bd_full_list.append(top_row)
    for role in sorted( breakdown_dict.keys()):
      current_role_list = [ role ]
      for current_scene in self.list_of_scenes:
        if current_scene in breakdown_dict[role].keys():
          count = str( breakdown_dict[role][current_scene] )
          current_role_list.append(count)
        else:
          current_role_list.append('0')
      self.bd_full_list.append(current_role_list)
      current_role_list = []



  def create_breakdown_list_new_way(self):
    self.read_in_play_data()

  def print_out_breakdown(self):
    for i in self.bd_full_list:
      print(i)


  def print_out_breakdown_csv(self):
    with open( self.play + '.csv' , 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerows(self.bd_full_list)


  def print_out_breakdown_html(self):
    html_filename = self.play + '.html'
    with open(html_filename , 'w', newline='') as writer:
      colspan = str(len(self.bd_full_list[0]))
      curline = '<table cellpadding="5" border="1" bgcolor="white"><TH colspan="' + colspan + '">Casting Breakdown</TH>\n'
      writer.write(curline)
      for i in self.bd_full_list:
        curline = f"<TR><TD>{'</TD><TD>'.join(i)}</TD></TR>\n"
        writer.write(curline)
      writer.write('</table>')






p1 = Breakdown("midsummer")
#p1.get_list_of_plays()
p1.create_breakdown_list_new_way()
#p1.print_out_breakdown()
#p1.print_out_breakdown_html()
p1.print_out_breakdown_csv()

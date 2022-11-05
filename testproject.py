import fake_useragent
import requests
import time
import sys
from bs4 import BeautifulSoup
from PIL import Image
import os

def none_check(object): #экономит драгоценные строчки кода
    if object != None:
        return object.get_text()
    return None
def delete_smth(spisok,el):
    del(spisok[el])
    return spisok
def none_write(object):
    if object == None:
        return 'None'
    return object
def data_check(object, headers):
    try:
        requests.get(url=object, headers=headers)
        return object
    except requests.exceptions.InvalidSchema:
        return pageimg.find('a', title='{}'.format(hero)).img['data-src']
def dot_change(object):
    object = list(object)
    index = 0
    for x in range(0, object.count('.')):
        index = object.index('.', index)
        try:
            int(object[index-1])
            int(object[index+1])
            object[index] = ','
        except ValueError:
            continue
        except IndexError:
            continue
    return ''.join(object)


ua = fake_useragent.UserAgent()
headers = {'User-Agent': ua.random}

r = requests.get('https://dota2.fandom.com/ru/wiki/Герои', headers=headers)

with open('imgtest.html', 'w', encoding='utf=8') as file:
    file.write(r.text)
with open('imgtest.html', 'r', encoding='utf=8') as file:
    pageimg = BeautifulSoup(file, 'lxml')

heroes_raw = pageimg.find_all('span', style="font-size:17px; color:white; text-shadow:-1px 0 0.2em black, 0 1px 0.2em black, 1px 0 0.2em black, 0 -1px 0.2em black;")
heroes_new = []
for hero in heroes_raw:
    heroes_new.append(hero.get_text())
heroes_str = []
heroes_agi = []
heroes_int = []
for hero in heroes_new:
    if heroes_new.index(hero) < heroes_new.index('Anti-Mage'):
        heroes_str.append(hero)
    elif heroes_new.index(hero) >= heroes_new.index('Anti-Mage') and heroes_new.index(hero) < heroes_new.index('Ancient Apparition'):
        heroes_agi.append(hero)
    elif heroes_new.index(hero) >= heroes_new.index('Ancient Apparition'):
        heroes_int.append(hero)

print(heroes_str)
print(heroes_agi)
print(heroes_int)

#################################################################################### HTML HERO TOGETHER

with open(r"D:\coding\htmlcode\html pd\heroes\heroestogether.html", 'w', encoding='utf=8') as file:
    file.write("""<html>
<head>
<meta charset="UTF-8">
<title>
Все герои
</title>
</head>
<body background="fon.jpg" text="#DDDDDD">
<h1 align="left">
Герои
<a href= "index.html" border="0"> <img src= "goback.png" align="right"> </a>
</h1>
<h2 align="center">
<table align="center">""")
    file.write("""
    <tr align="center">
    <td> <h2> Сила </h2> </td> </tr>
    <tr align="center"> 
    <td>""")
    n=0
    for hero in heroes_str:
        if n<=7:
            file.write(f'<a href="{hero}.html" border="0"> <img src="{hero}IMAGE.jpg" align="bottom"> </a>')
            n+=1
        else:
            n=0
            file.write('</td></tr><tr align="center"><td>')
    file.write("""
        <tr align="center">
        <td> <h2> Ловкость </h2> </td> </tr>
        <tr align="center"> 
        <td>""")
    n = 0
    for hero in heroes_agi:
        if n <= 7:
            file.write(f'<a href="{hero}.html" border="0"> <img src="{hero}IMAGE.jpg" align="bottom"> </a>')
            n += 1
        else:
            n = 0
            file.write('</td></tr><tr align="center"><td>')
    file.write("""
        <tr align="center">
        <td> <h2> Интеллект </h2> </td> </tr>
        <tr align="center"> 
        <td>""")
    n = 0
    for hero in heroes_int:
        if n <= 7:
            file.write(f'<a href="{hero}.html" border="0"> <img src="{hero}IMAGE.jpg" align="bottom"> </a>')
            n += 1
        else:
            n = 0
            file.write('</td></tr><tr align="center"><td>')
    file.write('</td></tr></table> </h2> </body></html>')


####################################################################################

for hero in heroes_new:
    #print(hero)

    if hero == 'Anti-Mage':
        herodb = 'anti-mage'
    elif hero == 'Keeper of the Light':
        herodb = 'keeper-of-the-light'
    elif hero == "Nature's Prophet":
        herodb = 'natures-prophet'
    elif hero == 'Queen of Pain':
        herodb = 'queen-of-pain'
    elif ' ' in hero:
        herodb = list(hero)
        herodb[0] = herodb[0].lower()
        herodb[herodb.index(' ')+1] = herodb[herodb.index(' ')+1].lower()
        herodb = ''.join(herodb).replace(' ','-')
    else:
        herodb = list(hero)
        herodb[0] = herodb[0].lower()
        herodb = ''.join(herodb)
    print(herodb)
    url='https://ru.dotabuff.com/heroes/{}/abilities'.format(herodb)

    r = requests.get(url=url, headers=headers)

    with open('dbpage.html', 'w', encoding='utf=8') as file:
        file.write(r.text)
    #bs 4 moment
    with open('dbpage.html', 'r', encoding='utf=8') as file:
        page = BeautifulSoup(file, 'lxml')

    #HERO STAT
        hstatslist = ['Сила', page.find('section', class_='hero_attributes').find_all('td', class_='str')[1].get_text(),'Ловкость', page.find('section', class_='hero_attributes').find_all('td', class_='agi')[1].get_text(),'Интеллект', page.find('section', class_='hero_attributes').find_all('td', class_='int')[1].get_text()]
    for stat in page.find('section', class_='hero_attributes').find('table', class_='other').find_all('td'):
        hstatslist.append(stat.get_text())

    #SKILLS
    abilities = []
    for skill in page.find_all('div', class_='skill-tooltip reborn-tooltip'):
        container = []
        container.append(skill.find('img').get('alt')) #name
        container.append([feaut.get_text() for feaut in skill.find('div', class_='effects').find_all('p')]) #ftrs
        container.append([none_check(skill.find('div', class_='description')), none_check(skill.find('div', class_='notes'))]) #dsc and notes
        container.append([sfeaut.get_text().replace("\n", '') for sfeaut in skill.find_all('div', class_='stat effect')]) #skill features
        container.append([none_check(skill.find('div', class_='cooldown align-icon')), none_check(skill.find('div', class_='manacost align-icon'))]) #manacost and cd
        container.append(none_check(skill.find('div', class_='lore'))) #lore of skill
        abilities.append(container) #overall

    #TALENT'S TREE
    tree = []

    for strings in delete_smth(page.find('div', style = 'display: none').find_all('tr'), 0):
        container = []
        container.append(strings.find('td', class_='talent-level').find('div').get_text())
        container.append([talent.get_text().replace('–-', '-') for talent in strings.find_all('td', class_='talent-cell')])
        tree.append(container)
    #LORE
    if ' ' in hero:
        herodw = hero.replace(' ', '_')
    else:
        herodw = hero
    url = 'https://dota2.fandom.com/ru/wiki/{}'.format(herodw)
    r = requests.get(url=url, headers=headers)

    with open('dwpage.html','w', encoding='utf=8') as file:
        file.write(r.text)
    #bs4
    with open('dwpage.html', 'r', encoding='utf=8') as file:
        page = BeautifulSoup(file, 'lxml')

    lore = [page.find('div', style='display: table-cell; font-weight: bold;').find_next_sibling().get_text()]

    #IMG
    image = data_check(pageimg.find('a', title='{}'.format(hero)).img['src'], headers)
    r = requests.get(url = image, headers=headers)

    with open(r'D:\coding\htmlcode\html pd\heroes\{}IMAGE.jpeg'.format(hero), 'wb') as file:
        file.write(r.content)

    # img = Image.open(r'D:\coding\htmlcode\html pd\heroes\{}IMAGE.jpeg'.format(hero))
    with Image.open(r'D:\coding\htmlcode\html pd\heroes\{}IMAGE.jpeg'.format(hero)) as img:
        img = img.convert('RGB')
        img.save(r'D:\coding\htmlcode\html pd\heroes\{}IMAGE.jpg'.format(hero))
    os.remove(r'D:\coding\htmlcode\html pd\heroes\{}IMAGE.jpeg'.format(hero))


    # print(image, hstatslist, lore, abilities, tree)
################################################################################################### HTML HERO PAGE ЁПТА

    with open(r"D:\coding\htmlcode\html pd\heroes\{}.html".format(hero), 'w', encoding='utf=8') as file:
        file.write(
        """
        <html>
        <head>
        <meta charset="UTF-8">
        <title>
        Герой → {hero}
        </title>
        </head>
                                                        <body leftmargin='0' topmargin='0' background="fon.jpg" text="#DDDDDD" >
        <h1>
        <img src='{hero}IMAGE.jpg' align='top'> {hero} <a href= 'index.html' border='0'> <img src= "goback.png" align='right'> </a>
        </h1>
        """.format(hero=hero)
        )
        #STATS
        file.write("<p align='center'>")
        file.write("<table align='center' bgcolor='#696F87' border='3' bordercolor='#8188A6'><tr align='center'>")
        file.write("<td align='center'> Базовые характеристики </td><td align='center'> Дерево талантов </td></tr>")
        file.write("<tr> <td> <table bgcolor='#414554' border='5' bordercolor='#5B6075'>")
        n=0
        file.write('<tr>')
        for stat in hstatslist:
            if n%2 == 0:
                file.write("<td align='center' valign='middle'> {} </td>".format(stat))
            n+=1
        file.write('</tr><tr>')
        for statv in hstatslist:
            if n%2 == 1:
                file.write("<td align='center' valign='middle'> {} </td>".format(statv))
            n+=1
        file.write("</tr></table></td>")
        file.write("<td><table bgcolor='#414554' border='5' bordercolor='#5B6075' >")
        for branch in tree:
            file.write(f"<tr><td> {branch[1][0]} </td> <td align='center'> {branch[0]} </td> <td align='right'> {branch[1][0]} </td> </tr> ")
        file.write("</table> </td> </tr> </table> </p>")



        #SKILLS
        file.write("<p align='center'> <table background='fon.jpg' border='0'><tr valign='top'>") #TABLE OF ALL SKILLS
        for skill in abilities:
            file.write("<td align='center'>") #CELL
            file.write("<table bgcolor='#696F87' border='3' bordercolor='#8188A6'>") #MAIN CELL/TABLE
            file.write(f"<tr> <td align='center' valign='middle' bgcolor='#5B6075'> {skill[0]} </td> </tr>") #SKILL NAME
            file.write("<tr> <td align='left' valign='middle'>")
            for skillfeauter in skill[1]:
                file.write(f"<p align='left'> {skillfeauter.replace('Unit Target', 'Направленная на героя').replace('Enemy Units', 'на вражеских Героев').replace('Point Target', 'Направленная на точку').replace('Enemy Heroes','на вражеских Героев').replace('Creeps', 'на Крипов').replace('Heroes', 'на Героев').replace('Passive', 'Пассивная').replace('No Target', 'Ненаправленная').replace('No', 'Нет').replace('Yes', 'Да').replace('Allied Units', 'на союзников').replace(':',': ')} </p>") #SKILL FEAUTERS
            file.write("</td> </tr>")
            file.write("<tr> <td align='center' valign='middle'>")
            file.write(f"<p align='left'> {skill[2][0]} </p>") #SKILL DESCRIPTION
            file.write("</td> </tr>")
            if skill[2][1] != None:
                file.write("<tr> <td align='center' bgcolor='#5B6075' valign='middle'>")
                file.write('<p align="left"> {} </p>'.format(dot_change(skill[2][1]).replace(".",".</p> <p align='left'>")))  # SKILL NOTES
                file.write("</td> </tr>")
            file.write("<tr> <td align='center' valign='middle'>")
            if skill[3] != []:
                for skillinfo in skill[3]:
                    file.write(f"<p align='left'> {skillinfo} </p>")
                file.write("</td> </tr>")
            if skill [4][0] != None or skill[4][1] != None:
                file.write("<tr><td>")
                if skill[4][0] != None:
                    file.write(f"<p>Перезарядка: {skill[4][0]}  </p> ")
                if skill[4][1] != None:
                    file.write(f"<p> Стоймость маны: {skill[4][1]} </p>")
                file.write("</td></tr>")
            file.write("<tr><td bgcolor='#5B6075'>")
            if skill[5] != None:
                file.write(f"{skill[5]}")
            file.write("</td></tr>")

            file.write("</table>") #MAIN CELL/TABLE END
            file.write("</td>") #CELL END
        file.write("</tr> </table> </p>")
        file.write("<h3 align='center'> ↓ История (биография) персонажа ↓ </h3>")
        file.write(f"<p align='center'> {lore[0]} </p>")
        file.write("</body></html>")
    with open(r"D:\coding\htmlcode\html pd\heroes\{}.html".format(hero), 'r', encoding='utf=8') as file:
        string = file.read().replace("'",'"')
    with open(r"D:\coding\htmlcode\html pd\heroes\{}.html".format(hero), 'w', encoding='utf=8') as file:
        file.write(string)

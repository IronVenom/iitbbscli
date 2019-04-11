import click
import requests
import bs4
from prettytable import PrettyTable
import mechanize

@click.group()
def main():
	pass

@main.command(help = "Gives a list of holidays")
def holidays():
	
	#Getting Data from website using net scraping.
	hols_html = requests.get('http://www.iitbbs.ac.in/holidays-list.php')
	holidays = bs4.BeautifulSoup(hols_html.text, 'lxml')
	year = holidays.select('h1')
	holidays = holidays.select('tr')
	hols = [holidays[x].getText().split('\n') for x in range(1,len(holidays)-1)]
	hols = [' '.join(x[1:(len(x)-1)]) for x in hols]
	hols = [x.split(' ') for x in hols]
	final_hols=[]
	for x in hols:
		x = [i.replace(' ','') for i in x]
		y=[]
		for i in range(len(x)):
			if x[i] == '':
				continue
			else:
				y.append(x[i])
		final_hols.append(y)

	#Making a proper list of the holidays.
	Months = ['January','February','March','April','May','June','July','August','September','October','November','December']
	Holidays = []
	for x in final_hols:
		l=[]
		l.append(x[0])
		for j in range(len(x)):
			if x[j] in Months:
				l.append(' '.join(x[1:j]))
				for m in range(j,len(x)):
					l.append(x[m])
				break
		Holidays.append(l)

	#Printing out the holidays in the form of a table.
	table_hol = PrettyTable(['S.no','Holiday','Month','Date','Day'])
	print('\n',year[1].getText(),'\n')
	for x in Holidays:
		table_hol.add_row(x)
	print(table_hol)

@main.command(help = "Headlines")
def headlines():

	raw = (bs4.BeautifulSoup((requests.get('http://www.iitbbs.ac.in/news.php')).text,'lxml')).select('ol a b')
	headlines = [raw[x].getText().split('\n') for x in range(1,len(raw)-1)]
	news_table = PrettyTable(['S.no','Headlines'])
	for sn,x in enumerate(headlines):
		news_table.add_row([sn+1,x[0]])
	print(news_table)

@main.command(help = "Gives attendance")
def attendance():

	username = input('Enter username\n')
	password = input('Enter password\n')

	br = mechanize.Browser()
	br.open("http://erp.iitbbs.ac.in/")
	br.select_form(nr=0)
	br['email'] = username
	br['password'] = password
	br.submit()
	result = br.response()
	html=result.read()
	br.open('http://erp.iitbbs.ac.in//biometric/list_students.php')

	result = br.response()
	html=result.read()
	f = open('s.txt','wb')
	f.write(html)

	contents = open("s.txt","r")
	with open("s.html", "w") as e:
	    for lines in contents.readlines():
	        e.write(lines + "\n")

	s = bs4.BeautifulSoup(open('s.html'),'lxml')
	p = s.find('table',{'class':'table'})
	q = p.find_all('td')
	q = [str(i) for i in q]
	q = [i.replace(" ", "") for i in q]
	r = [i.split('\n')[2] for i in q]
	r = [i.split('\t')[0] for i in r]
	ids = r[0::5]
	courses = r[1::5]
	present = r[2::5]
	total = r[3::5]
	percentage = r[4::5]
	percentage = [i+'%' for i in percentage]
	biometric_attendance = PrettyTable(['Course ID','Course Name','Present','Total','Percenage'])
	attendance = []
	for i in range(len(ids)):
		attendance.append([ids[i],courses[i],present[i],total[i],percentage[i],])

	for x in attendance:
			biometric_attendance.add_row(x)

	print(biometric_attendance)

if __name__ == '__main__':
	main()

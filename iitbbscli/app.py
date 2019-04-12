import click
import requests
import bs4
from prettytable import PrettyTable
import mechanize
import getpass

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

	username = input('Enter Username:\n')
	password = getpass.getpass("Enter Password:\n")

	br = mechanize.Browser()
	br.open("http://erp.iitbbs.ac.in/")
	br.select_form(nr=0)
	br['email'] = username
	br['password'] = password
	br.submit()
	result = br.response()
	br.open('http://erp.iitbbs.ac.in//biometric/list_students.php')
	result = br.response().read()
	s = bs4.BeautifulSoup(result, 'html.parser')
	p = s.find('table',{'class':'table'})
	q = p.find_all('td')
	q = [str(i) for i in q]
	r = [i.split('\t')[0].split('\n')[1].lstrip() for i in q]
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

@main.command(help = "Queries Related to results.")
def result():
	
	Roll_No = input('Enter Roll No.:\n')
	Date_of_birth = getpass.getpass("Enter Date of Birth (YYYY-MM-DD) :\n")
	query = input('For SGPAs enter 1, for entire report card enter 2 and for CGPA enter 3.\n')

	br = mechanize.Browser()
	br.open("http://14.139.195.241/Result/login.php")
	br.select_form(nr=0)
	br['regno'] = Roll_No
	br['dob'] = Date_of_birth
	br.submit()
	result = br.response()
	br.open('http://14.139.195.241/Result/result.php')
	result = br.response().read()
	s = bs4.BeautifulSoup(result, 'html.parser')

	# Getting stuff

	semesters = s.findAll('td',colspan = "5")
	ids = s.findAll('td',align = "center", width = "20%")
	subjects = s.findAll('td',style = "padding-left: 10px", width = "50%")
	ltps = s.findAll('td',align = "center", width = "10%")
	cgpas=s.findAll('td',align = "right", colspan = "3")
	sgpas=s.findAll('td',align = "left", colspan = "2")

	# Removing Tags

	semesters = [str(i).split('<h3 class="sem-heading-page-center">')[1].split('</h3')[0] for i in semesters]
	ids = [str(i).split('<b>')[1].split('</b>')[0] for i in ids]
	subjects = [str(i).split('<td style="padding-left: 10px" width="50%">')[1].split('</td>')[0] for i in subjects]
	ltps = [str(i).split('<b>')[1].split('</b>')[0] for i in ltps]
	ltp = ltps[0::3]
	grades = ltps[2::3]
	credits = ltps[1::3]
	cgpas = [str(i).split('<b>')[1].split('</b>')[0].split(" ")[0] for i in cgpas]
	sgpas = [str(i).split('<b>')[1].split('</b>')[0].split(" ")[1] for i in sgpas]

	if query == '1':

		gpas = PrettyTable(['Semester','SGPA'])
		gpa_l = []
		for i in range(len(semesters)):
			gpa_l.append([semesters[i],sgpas[i]])
		for x in gpa_l:
			gpas.add_row(x)
		print('\n')
		print(gpas)

	elif query == '2':

		report_Card = PrettyTable(['ID','Subject','L-T-P','Credits','Grade'])
		rc = []
		for i in range(len(ids)):
			rc.append([ids[i],subjects[i],ltp[i],credits[i],grades[i]])
		for x in rc:
			report_Card.add_row(x)
		print('\n')
		print(report_Card)

	elif query == '3':
		
		print('\n')
		print(cgpas[-1])

	else:

		print('Please try again.')

if __name__ == '__main__':
	main()

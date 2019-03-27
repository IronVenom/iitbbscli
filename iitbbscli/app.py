import click
import requests
import bs4
from prettytable import PrettyTable

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

if __name__ == '__main__':
	main()

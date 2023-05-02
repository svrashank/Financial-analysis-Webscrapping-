from bs4 import BeautifulSoup
import requests 
import csv
import pandas as pd 

#Setup Beautiful soup 
headers = {"User-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
url = 'https://finance.yahoo.com/quote/%5ENSEI/components?p=%5ENSEI'
r = requests.get(url,headers=headers).text
soup = BeautifulSoup(r,'html.parser')

symbols = []

#Grab Symbol and append top 30 of the nifty 50 symbols to a list 
for stock in soup.find_all('tr',{'class':'BdT Bdc($seperatorColor) Ta(end) Fz(s)'}):
    stock.find("a",{'class':'C($linkColor) Cur(p) Td(n) Fw(500)'})
    Symbol = stock.td.a.text
    symbols.append(Symbol)
#On futher inspection of websites of all the companies ,Mahindra and Mahindra does not have requied information on yahoo Finance 
# hence drop it from the symbols list 
symbols.remove('MM.NS') 

# '://finance.yahoo.com/quote/NTPC.NS?p=NTPC.NS' is the url with information on eaach of 50 stocks. Here we see that stock symbols after "?p="
#can be replaced with the stock symbol that we are analyzing. Create a dict with stock name and their url of the information page
urls = {}
for symbol in symbols:
    urls[str(symbol)]= 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'.format(symbol,symbol)

#Open a csv file writer all the headers and close the file 
finance_file = open('Stock_analysis.csv','w')
csv_writer = csv.writer(finance_file)
column_names = ['Symbol','Company_name','Stock_price','Market_cap','Trailing_PE','Forward_PE','Price_sales_ratio','Price_book_ratio','BVPS','Profits',
                'Quarterly_Earnings_Growth','D_E_ratio','outstanding_shares']
csv_writer.writerow(column_names)
finance_file.close()

#Visit Financial Statistics of each page and grab the required stat of each company 
company_name =[]
stock_price = []
market_cap = []
Trailing_PE = []
Forward_PE = []
price_sales_ratio =[]
price_book_ratio = []
bvps = []
profits = []
Quarterly_Earnings_Growth = []
D_E_ratio = []
outstanding_shares = []
index= [i for i in range(len(symbols))]

i = 0
for url in urls:
    headers = {"User-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    r = requests.get(url=urls[url],headers=headers).text
    soup = BeautifulSoup(r,'html.parser')
    #Company name list 
    company_name.append(soup.title.text.split("(")[0])
    #Stock Price list 
    stock_price.append(soup.find('fin-streamer',{'class':'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text)

    market_cap.append(soup.find("td",{'class':'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text)

    Trailing_PE.append(soup.find_all('td',{'class':'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})[2].text)

    Forward_PE.append(soup.find_all('td',{'class':'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})[3].text)

    price_sales_ratio.append(soup.find_all('td',{'class':'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})[5].text)

    price_book_ratio.append(soup.find_all('td',{'class':'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})[6].text)

    profit_table = soup.select('tbody')[5]
    profits.append(profit_table.find('td',{'class':'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text)
    
    Growth = soup.select('tbody')[7]
    Quarterly_Earnings_Growth.append((Growth.find_all('td',{'class':'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})[7].text))

    Balance_sheet = soup.select('tbody')[8]
    D_E_ratio.append(Balance_sheet.find_all('td',{'class':'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})[3].text)
    bvps.append(Balance_sheet.find_all('td',{'class':'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})[5].text)

    share_stats = soup.select('tbody')[2] 
    outstanding_shares.append(share_stats.find_all('td',{'class':'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})[2].text)
    print(url)
    print(i)
    i += 1
    print(' ')

#Import the empty dataframe and add all the scrapped values 
df = pd.read_csv('Stock_analysis.csv')
df['Symbol'] = symbols
df['Company_name'] = company_name
df['Stock_price'] = stock_price
df['Market_cap'] = market_cap
df['Trailing_PE'] = Trailing_PE
df['Forward_PE'] = Forward_PE
df['Price_sales_ratio'] = price_sales_ratio
df['Price_book_ratio'] = price_book_ratio
df['BVPS'] = bvps
df['Profits'] = profits
df['Quarterly_Earnings_Growth'] = Quarterly_Earnings_Growth
df['D_E_ratio'] = D_E_ratio
df['outstanding_shares'] = outstanding_shares

df.to_csv('Stock_analysis_df.csv')
    
   





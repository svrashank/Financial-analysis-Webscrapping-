# Stocks Analysis : Project Overview 
* A Webscraping Project for obtaining essential financial ratios of a company from Yahoo Finance's Stats section 
* This is followed by Analysis of the top 30 companies listed on the NIFTY 50 index of India. 
* The aim of the project was to see what the effect of change in major financial ratios (according to investopedia article) have on stock price 
* Mutual Information was the metric used to determine the relationship between the features and the target 
* Random Forest Regressor was the model used to capture variations within our data 

### Code and Resources 
* Python Version : 3.10 
* Packages: BeautifulSoup, Pandas ,Numpy , Sklearn, Seaborn ,Mathplotlib 
* Dataset : Webscraping Yahoo Fianance
* Webscraper : BeautifulSoup ,self-written 
* Article :Investopedia article on "must have metrics value investors"
* https://www.investopedia.com/articles/fundamental-analysis/09/five-must-have-metrics-value-investors.asp
  
### Webscraping 
* Yahoo finance have critical financial information on most of the stocks of major indexes 
* The statistics section of the Yahoo Finance website was the main focus of this project 
* URL for the statistics page contained the symbol ,hence ,I was able to format it and loop over it to and store the urls of top 30 companies of nifty 50 
* Futhermore, another loop was used to visit each URL and scrap necessary variables 

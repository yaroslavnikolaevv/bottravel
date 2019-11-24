class Search_capital:
	def __init__(self,search):
        	self.search=search.lower()
	def poisk(self):	
		a=self.search
		file=open('base_date_city.txt','r',encoding='UTF-8')
		for line in file:
			if a in line:
			    capital=line[:line.index(':')]
			    return(capital)

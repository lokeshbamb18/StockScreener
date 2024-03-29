import pandas as pd
import matplotlib.pyplot as plt
import os, shutil

folder = '/home/lokesh/ML/Android/sparklines'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

screener = pd.read_csv('/home/lokesh/ML/output.csv',delimiter=' ')
output = pd.DataFrame()
bors = list(screener['Date'])
sym = list(screener['Price'])
company = []
bs =[]
close = []
isin_data = pd.read_csv('/home/lokesh/ML/ind_nifty200list.csv')
script = list(isin_data['Symbol'])
isin = list(isin_data['ISIN Code'])
ISIN = []
imagepath = []
date = []

for i in range(0, len(bors), 1):
    if(bors[i] == 'Buy' or bors[i] == 'Sell'):
       #print(bors[i], sym[i])
       company.append(sym[i]+"-EQ")
       bs.append(bors[i])
       comp = pd.read_csv('/home/lokesh/ML/NIFTY-200/' + sym[i] + '.csv')
       close.append((list(comp['CLOSE']))[0])
       date.append((list(comp['DATE']))[0])
       n = script.index(sym[i])
       ISIN.append(isin[n])
       imagepath.append('https://github.com/lokeshbamb18/StockScreener/raw/main/sparklines/'+sym[i]+'.png')
       cp = list(comp['CLOSE'][:60])
       cp.reverse()
       plt.plot(cp, linewidth = 7.0)
       plt.axis('off')
       plt.savefig('/home/lokesh/ML/Android/sparklines/' + sym[i])
       plt.clf()
              
print(cp)
output['Signal'] = bs
output['Script'] = company
output['Previous Close'] = close
output['ISIN Code'] = ISIN
output['Date'] = date
output['Image'] = imagepath
output.index += 1
output = output.sort_values(by = 'Signal')
print(output)
output.to_excel('data.xls', index = False)

screener = screener.fillna(0)
first = list(screener['Date'])
second = list(screener['Price'])
third = list(screener['Signal'])
holdings = []
for i in range(0, len(third), 1):
	if(third[i] == 0 and third[i-1] == 'buy'):
		if(first[i] == 'Sell'):
			holdings.append(second[i])
		else:
			holdings.append(first[i])
sector = list(isin_data['Industry'])
piedata = dict.fromkeys(sector, 0)
for i in holdings:
	n = script.index(i)
	piedata[sector[n]] += 1
#print(piedata)
out = pd.DataFrame(list(piedata.items()), columns=['Sector', 'Quantity'])
color=['#928b92','#0ca404','#ea7406','#06ea87','#067cea','#5dea06','#1c4602','#c05c26','#e6c700','#000000','#000dc7','#7a3701','#6a7a01','#8e011b','#f0f901','#fe01a5','#ffffff','#f90101']
out['Colour'] = color
out.to_excel('sectorial.xls', index = False)

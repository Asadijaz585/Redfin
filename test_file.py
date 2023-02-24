import requests, re, csv
from bs4 import BeautifulSoup
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
}
urls = []
for i in range(1,10):
    res = requests.get('https://www.redfin.com/city/11203/CA/Los-Angeles/apartments-for-rent/page-{}'.format(i), headers=header)
    soup_data = BeautifulSoup(res.content, 'html.parser')
    for tag in soup_data.find_all('div', {'class': 'scrollable'}):
        url = 'https://www.redfin.com'+tag.find('a').get('href')
        urls.append(url)

HEADERS = ['price', 'beds', 'baths', 'URL', 'Sqft', 'Adress', 'In_unit_Amenities', 'Community_Amenities']
with open('redfin.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(HEADERS)

    for u in urls:
        res_url = requests.get(u, headers=header)
        soup_data_url = BeautifulSoup(res_url.content, 'html.parser')
        overview = soup_data_url.find_all('div', {'class': 'statsValue'})
        #overview
        price = overview[0].text
        beds = overview[1].text
        baths = overview[2].text
        # import pdb;pdb.set_trace()
        URL = url
        # Sqft
        overvieW = soup_data_url.find_all('div', {'class': 'stat-block sqft-section'})
        Sqft = overvieW[0].text
        adress = soup_data_url.find_all('div', {'class': 'homeAddress'})
        Adress = adress[0].text
        # Amenities
        In_unit_Amenities = []
        Community_Amenities = []
        amenities = soup_data_url.find_all('div', {'class': 'sectionContent'})
        try:
            in_Unit_ameni = amenities[4].find('ul').find_all('li')
            for i in range(len(in_Unit_ameni)):
                In_unit_Amenities.append(re.sub(r"[\([{})\]]", "",in_Unit_ameni[i].text))  
        except:
            In_unit_Amenities.append(re.sub(r"[\([{})\]]", "",'-'))
        try:
            Comu_ameni = amenities[5].find('ul').find_all('li')
            for m in range(len(Comu_ameni)):
                Community_Amenities.append(re.sub(r"[\([{})\]]", "",Comu_ameni[m].text))
        except:
            Community_Amenities.append(re.sub(r"[\([{})\]]", "",'-'))
        data = [price, beds, baths, URL, Sqft, Adress, In_unit_Amenities, Community_Amenities]
        writer.writerow(data)

print('ok')
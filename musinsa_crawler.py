import requests
import pandas as pd
from bs4 import BeautifulSoup


min_rev = 10

front_url = 'https://store.musinsa.com/app/items/lists/002020/?category=&d_cat_cd=002020&u_cat_cd=&brand=&sort=emt_high&sub_sort=&display_cnt=90&page='
end_url = '&page_kind=category&list_kind=small&free_dlv=&ex_soldout=&sale_goods=&exclusive_yn=&price=&color=&a_cat_cd=&size=&tag=&popup=&brand_favorite_yn=&goods_favorite_yn=&blf_yn=&campaign_yn=&bwith_yn=&price1=&price2='
page = 1
cloth_code = []
loop = True

while loop:
    URL = front_url + str(page) + end_url
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    cloth_section = soup.body.find_all('div', {"class", 'article_info'})
    for cloth in cloth_section:
        if int(cloth.find('span', {'class', 'count'}).get_text().replace(',', '')) < min_rev:
            loop = False
            break
        cloth_code.append(cloth.find('p', {'class', 'list_info'}).find('a')[
                          'href'].split('/')[-2])
    page += 1
# print(cloth_code)

print(len(cloth_code))

f = open('total_cloth.csv', 'w')
f.write('코드,이름,가격,평점,크기감,밝기,색감,두께감,촉감\n')
count = 1
for code in cloth_code:
    if count % 10 == 0:
        print(count)
    url = 'https://store.musinsa.com/app/product/detail/' + code + '/0'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cloth_cod = code
    cloth_nam = soup.find(
        'span', {'class', 'product_title'}).get_text().strip().replace('\n', ' ')
    cloth_prc = soup.find(
        'span', {'class', 'product_article_price'}).get_text().strip().replace(',', '')
    cloth_eval = soup.find('div', {"class", 'estimate-avg'})
    cloth_grd = float(cloth_eval.find(
        'span', {'class', 'rate'}).get_text().split('%')[0])
    eval_list = []
    evals = cloth_eval.find_all('div', {'class', 'per'})
    for eval_ in evals:
        eval_list.append(int(eval_.get_text().split('%')[0]))
    cloth_siz = 1 * eval_list[0] + 0.5 * eval_list[1] + 0 * eval_list[2]
    cloth_bri = 1 * eval_list[3] + 0.5 * eval_list[4] + 0 * eval_list[5]
    cloth_col = 1 * eval_list[6] + 0.5 * eval_list[7] + 0 * eval_list[8]
    cloth_thk = 1 * eval_list[9] + 0.5 * eval_list[10] + 0 * eval_list[11]
    cloth_tch = 1 * eval_list[12] + 0.5 * eval_list[13] + 0 * eval_list[14]
    f.write(cloth_cod+','+cloth_nam+','+cloth_prc+','+str(cloth_grd)+','+str(cloth_siz) +
            ','+str(cloth_bri)+','+str(cloth_col)+','+str(cloth_thk)+','+str(cloth_tch)+'\n')
    count += 1
f.close()

# df_ori = pd.read_csv('total_cloth.csv',encoding='euc-kr')
# df_ori

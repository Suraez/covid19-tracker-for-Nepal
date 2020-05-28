import requests
import bs4
import pandas as pd
# from prettytable import PrettyTable
from flask import Flask, render_template

app = Flask(__name__)
url = "https://kathmandupost.com/covid19"

html_content = requests.get(url).text
# all the html data
soup = bs4.BeautifulSoup(html_content, "html.parser")

# remember u need to work with tag not Resultset, check type(table_data)
table_data = soup.find_all("table", class_="district-wrapper")[0]

table_headings = []
for th in table_data.find_all("th"):
    table_headings.append(th.text)

extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
stats = []
# print(table_headings)
for row in table_data.tbody.find_all("tr"):
    stat = extract_contents(row.find_all("td"))
    stats.append(stat)



district_data = pd.DataFrame(data = stats, columns = table_headings)
# district_data.head()

district_data['Confirmed'] = district_data['Confirmed'].map(int)
district_data['Deaths'] = district_data['Deaths'].map(int)
district_data['Recovered'] = district_data['Recovered'].map(int)
district_data['Readmitted'] = district_data['Readmitted'].map(int)
# # print(type(district_data['Confirmed']))
total = ['Total',sum(district_data['Confirmed']),sum(district_data['Deaths']),sum(district_data['Recovered']),sum(district_data['Readmitted'])]
# table = PrettyTable()
# table.field_names = (table_headings)

# for i in stats:
#     table.add_row(i)

# table.add_row(['Total',sum(district_data['Confirmed']),sum(district_data['Deaths']),sum(district_data['Recovered']),sum(district_data['Readmitted'])])
# print(table)

@app.route('/')
def index():
    return render_template('index.html',districts=stats, total = total)

if __name__ == "__main__":
    app.run(debug=True)
# This file will download, import and digest the data
# into the database.
import pandas as pd
from datetime import datetime
from data_storage import connection
from receiving_sec_data import SEC
from tqdm import tqdm

# the following line of code, receivces all data from the SEC file server
SEC = SEC(connection, "BERKSHIRE HATHAWAY INC", "13F-HR")
# SEC.get_index(1993)
# SEC.save_to_database()

urls = pd.read_sql("SELECT TextUrl, DateOfIssue FROM SEC_filing_index",
                   connection, parse_dates=['DateOfIssue']).query('DateOfIssue <= "2012-03-01"')
until_2012 = SEC.extract_info_13F_until2012(urls["TextUrl"])

# urls = pd.read_sql("SELECT TextUrl, DateOfIssue FROM SEC_filing_index",
#                    connection, parse_dates=['DateOfIssue']).query('DateOfIssue >= "2013-08-01"')
# df = pd.DataFrame()
# standard_url = "https://www.sec.gov/Archives/"
# for url in tqdm(urls["TextUrl"]):
#     from_2014 = df.append(SEC.extract_info_13F_from2014(
#         standard_url + url, CIK="0000950123"))

until_2012.to_sql("Quarterly_investments_until2012",
                  connection, if_exists="replace")
# from_2014.to_sql("Quarterly_investments_from2014",
#                  connection, if_exists="replace")


# parse(standard_url + addon, "0000950123")
# urls = pd.read_sql("SELECT TextUrl, DateOfIssue FROM SEC_filing_index",
#                    connection, parse_dates=['DateOfIssue']).query('DateOfIssue <= "2012-01-01"')

# req = get(standard_url + "edgar/data/1067983/0000950129-04-003325.txt")
# html_soup = BeautifulSoup(req.text, 'html.parser')
# df = pd.DataFrame(columns=["Voting Authority", "Other Managers", "Investment Discretion",
#                            "Shares", "Market Value", "CUSIP", "Class", "NameOfCompany", "date", "url"])
# date_list, url_list = [], []
# for url in tqdm(urls["TextUrl"]):
#     #print(standard_url + url)
#     req = get(standard_url + url)
#     html_soup = BeautifulSoup(req.text, 'html.parser')
#     date = datetime.strptime(re.search(
#         r"[A-Za-z]*\s[0-3][0-9],\s[0-2][0-9][0-9][0-9]", html_soup.find_all("page")[-1].getText()).group(), "%B %d, %Y")
#     # print(date)
#     for tables in range(0, len(html_soup.find_all("table"))):
#         if "Shares" in html_soup.find_all("table")[tables].getText():
#             #print(f"Table: {tables}")
#             tm = html_soup.find_all("table")[tables].find(["c", "C"]).getText()[11:re.search("                         ------", html_soup.find_all(
#                 "table")[tables].find(["c", "C"]).getText()).start()]
#             tmp0 = re.sub(r"(?<=[\n])\s+", " ", tm)
#             tmp1 = re.sub(r"(?<=[a-z&.,])\n", "", tmp0)
#             tmp2 = re.sub(r"  (?=[a-z])", " ", tmp1)
#             tmp3 = re.sub(r"([a-z])([A-Z])", r"\1 \2", tmp2)
#             tmp4 = re.sub(r"-\n\s+", r"", tmp3)
#             tmp5 = re.sub(r"([.])([Com])", r"\1     \2",
#                           tmp4).replace("-\n", "")
#             tmp6 = re.sub(
#                 r"([ComBADRCVA])\s*([A-Z0-9][0-9][0-9][0-9][0-9][0-9A-Za-z][0-9][0-9][0-9A-Z])", r"\1       \2", tmp5)  # This should divide the Com from the CUISP
#             tmp7 = re.sub(
#                 r"(Com)\s([A-Z0-9][0-9][0-9][0-9][0-9][0-9A-Za-z][0-9][0-9][0-9A-Z])", r"\1       \2", tmp6)
#             tmp8 = re.sub(r"(Ins.)\s+\b([A-Z])", r"\1 \2", tmp7)
#             tmp9 = re.sub(r"\b([A-Za-z.])\s+(ComClADRCLA)", r"\1    \2", tmp8)
#             tmp10 = re.sub(r"(Co.)\s+(Del)", r"\1 \2", tmp9)
#             tmp11 = re.sub(r"([a-z\.])\s+(Corp\.)", r"\1 \2", tmp10)
#             tmp12 = re.sub(r"(PFD)\s+(CVA)", r"\1   \2", tmp11)
#             tmp13 = re.sub(r"(V)\s+(1)", r"\1\2", tmp12)
#             tmp14 = re.sub(
#                 r"([A-Z0-9][0-9][0-9][0-9][0-9][0-9A-Z])\s*([0-9][0-9])\s*([0-9A-Z])", r"\1\2\3", tmp13)
#             tmp15 = re.sub(r"([0-9][0-9][0-9])\s([0-9])", r"\1   \2", tmp14)
#             tmp16 = re.sub(r"(Block)\s*(H & R)", r"\1 \2", tmp15)
#             tmp17 = re.sub(r"(Standard)\s*(5, 10, 11, 13, 16,)", "", tmp16)
#             tmp18 = re.sub(r"(Data)\s*(5, 10, 11, 13, 16,)", r"", tmp17)
#             tmp19 = re.sub(r"(Inc.|Corp.|Corp)\s(Com)", r"\1     \2", tmp18)
#             tmp20 = re.sub(r"(LTD.)\s(CLA)", r"\1     \2", tmp19)
#             tmp21 = re.sub(r"(Com|B)\s([0-9])", r"\1      \2", tmp20)
#             tmp22 = re.sub(r"(,\s[0-9][0-9])\s([0-9])", r"\1       \2", tmp21)
#             tmp23 = re.sub(r"(Corporation)\s*(PFD)", r"\1 \2", tmp22)
#             for line in tmp23.replace("-\n", "").split("\n"):
#                 # print(line)
#                 # url_list.append(standard_url + url)
#                 tmp = pd.DataFrame([x for x in line.split("  ") if x][::-1]).T
#                 # This does not work. This puts the some lines into the wrong columns
#                 if len([x for x in line.split("  ") if x][::-1]) >= 5:
#                     tmp.columns = ["Voting Authority", "Other Managers", "Investment Discretion",
#                                    "Shares", "Market Value", "CUSIP", "Class", "NameOfCompany"][:tmp.shape[1]]
#                 else:
#                     tmp.columns = ["Investment Discretion",
#                                    "Shares", "Market Value", "CUSIP", "Class", "NameOfCompany"][:tmp.shape[1]]
#                # print(df.append(tmp, ignore_index=True))
#                 df = df.append(tmp, ignore_index=True)
#                 [date_list.append(date) for y in range(0, len(tmp))]
#                 [url_list.append(standard_url + url)
#                  for z in range(0, len(tmp))]
#         else:
#             continue

# df["date"] = date_list
# df["url"] = url_list

#df.to_sql("test", connection, if_exists="replace")

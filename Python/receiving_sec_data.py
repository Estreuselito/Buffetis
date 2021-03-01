import pandas as pd
import os
from tqdm import tqdm
import edgar
from bs4 import BeautifulSoup
from requests import get
from datetime import datetime
import re
from data_storage import connection


class SEC():
    """This class retrives SEC data, saves it and parses it"""

    def __init__(self, connection, company_name, filing, path="./data/SEC/"):
        """This function initilizes the SEC() class and creates a connection object

        Parameters
        ----------
        connection : cursor
            This cursor is the connection object to the database
        path : str
            The path where the data should be saved, by default "./data/SEC/"
        """
        self.connection = connection
        self.path = path
        self.company_name = company_name
        self.filing = filing

    def get_index(self, since_year):
        """This function retrieves the complete index with all filing from the EDGAR SEC archives

        Parameters
        ----------
        since_year : int
            The year as int, since when the filings should be loaded (lowest is 1993)
        path : str, optional
            The path where the data should be saved, by default "./data/SEC/"
        """
        edgar.download_index(self.path, since_year,
                             skip_all_present_except_last=False)

    def save_to_database(self):
        """Reads the data from the path and saves it to the database"""
        cols = ["CIK", "CompanyName", "Filing",
                "DateOfIssue", "TextUrl", "IndexHTML"]
        df = pd.DataFrame(columns=cols)
        list(map(lambda x: (pd.read_csv(self.path + x, sep="|", names=cols)
                            .query(f'CompanyName == "{self.company_name}" and Filing == "{self.filing}"')
                            .to_sql("SEC_filing_index",
                                    con=self.connection,
                                    if_exists="append")), tqdm(os.listdir(self.path))))

    def extract_info_13F_from2014(self, url, CIK):
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'lxml')
        try:
            date = datetime.strptime(html_soup.find(
                'signaturedate').contents[0], '%m-%d-%Y')
            name = html_soup.find('name').contents[0]
        except:
            return
        cols = ['nameOfIssuer', 'CUSIP', 'Market Value',
                'sshPrnamt', 'sshPrnamtType']
        data = []
        # print("Processing " + name + " (" + CIK + ") for date " + str(date))
        for infotable in html_soup.find_all(['ns1:infotable', 'infotable']):
            row = []
            for col in cols:
                data2 = infotable.find([col.lower(), 'ns1:' + col.lower()])
                if data2 is not None:
                    row.append(data2.getText())
            row.append(date)
            row.append(CIK)
            row.append(name)
            data.append(row)
        df = pd.DataFrame(data)
        cols.append('date')
        # cols.append('fund_cik')
        cols.append('fund')
        try:
            df.columns = cols
            return df
        except:
            return

    def extract_info_13F_until2012(self, urls):
        df = pd.DataFrame(columns=["Voting Authority", "Other Managers", "Investment Discretion",
                                   "Shares", "Market Value", "CUSIP", "Class", "NameOfCompany", "date", "url"])
        date_list, url_list = [], []
        standard_url = "https://www.sec.gov/Archives/"
        for url in tqdm(urls):
            #print(standard_url + url)
            req = get(standard_url + url)
            html_soup = BeautifulSoup(req.text, 'html.parser')
            date = datetime.strptime(re.search(
                r"[A-Za-z]*\s[0-3][0-9],\s[0-2][0-9][0-9][0-9]", html_soup.find_all("page")[-1].getText()).group(), "%B %d, %Y")
            # print(date)
            for tables in range(0, len(html_soup.find_all("table"))):
                if "Shares" in html_soup.find_all("table")[tables].getText():
                    #print(f"Table: {tables}")
                    tm = html_soup.find_all("table")[tables].find(["c", "C"]).getText()[11:re.search("                         ------", html_soup.find_all(
                        "table")[tables].find(["c", "C"]).getText()).start()]
                    tmp0 = re.sub(r"(?<=[\n])\s+", " ", tm)
                    tmp1 = re.sub(r"(?<=[a-z&.,])\n", "", tmp0)
                    tmp2 = re.sub(r"  (?=[a-z])", " ", tmp1)
                    tmp3 = re.sub(r"([a-z])([A-Z])", r"\1 \2", tmp2)
                    tmp4 = re.sub(r"-\n\s+", r"", tmp3)
                    tmp5 = re.sub(r"([.])([Com])", r"\1     \2",
                                  tmp4).replace("-\n", "")
                    tmp6 = re.sub(
                        r"([ComBADRCVASPL])\s*([A-Z0-9][0-9][0-9][0-9][0-9][0-9A-Za-z][0-9][0-9][0-9A-Z])", r"\1       \2", tmp5)  # This should divide the Com from the CUISP
                    tmp7 = re.sub(
                        r"(Com)\s([A-Z0-9][0-9][0-9][0-9][0-9][0-9A-Za-z][0-9][0-9][0-9A-Z])", r"\1       \2", tmp6)
                    tmp8 = re.sub(r"(Ins.)\s+\b([A-Z])", r"\1 \2", tmp7)
                    tmp9 = re.sub(
                        r"\b([A-Za-z.])\s+(ComClADRCLA)", r"\1    \2", tmp8)
                    tmp10 = re.sub(r"(Co.)\s+(Del)", r"\1 \2", tmp9)
                    tmp11 = re.sub(r"([a-z\.])\s+(Corp\.)", r"\1 \2", tmp10)
                    tmp12 = re.sub(r"(PFD)\s+(CVA)", r"\1   \2", tmp11)
                    tmp13 = re.sub(r"(V)\s+(1)", r"\1\2", tmp12)
                    tmp14 = re.sub(
                        r"([A-Z0-9][0-9][0-9][0-9][0-9][0-9A-Z])\s*([0-9][0-9])\s*([0-9A-Z])", r"\1\2\3", tmp13)
                    tmp15 = re.sub(
                        r"([0-9][0-9][0-9])\s([0-9])", r"\1   \2", tmp14)
                    tmp16 = re.sub(r"(Block)\s*(H & R)", r"\1 \2", tmp15)
                    tmp17 = re.sub(
                        r"(Standard)\s*(5, 10, 11, 13, 16,)", "", tmp16)
                    tmp18 = re.sub(
                        r"(Data)\s*(5, 10, 11, 13, 16,)", r"", tmp17)
                    tmp19 = re.sub(r"(Inc.|Corp.|Corp)\s(Com)",
                                   r"\1     \2", tmp18)
                    tmp20 = re.sub(r"(LTD.)\s(CLA)", r"\1     \2", tmp19)
                    tmp21 = re.sub(r"(Com|B)\s([0-9])", r"\1      \2", tmp20)
                    tmp22 = re.sub(
                        r"(,\s[0-9][0-9])\s([0-9])", r"\1       \2", tmp21)
                    tmp23 = re.sub(r"(Corporation)\s*(PFD)", r"\1 \2", tmp22)
                    for line in tmp23.replace("-\n", "").split("\n"):
                        # print(line)
                        # url_list.append(standard_url + url)
                        tmp = pd.DataFrame(
                            [x for x in line.split("  ") if x][::-1]).T
                        # This does not work. This puts the some lines into the wrong columns
                        if len([x for x in line.split("  ") if x][::-1]) >= 5:
                            tmp.columns = ["Voting Authority", "Other Managers", "Investment Discretion",
                                           "Shares", "Market Value", "CUSIP", "Class", "NameOfCompany"][:tmp.shape[1]]
                        else:
                            tmp.columns = ["Investment Discretion",
                                           "Shares", "Market Value", "CUSIP", "Class", "NameOfCompany"][:tmp.shape[1]]
                    # print(df.append(tmp, ignore_index=True))
                        df = df.append(tmp, ignore_index=True)
                        [date_list.append(date) for y in range(0, len(tmp))]
                        [url_list.append(standard_url + url)
                         for z in range(0, len(tmp))]
                else:
                    continue

        df["date"] = date_list
        df["url"] = url_list

        return df


# standard_url = "https://www.sec.gov/Archives/"
# addon = "edgar/data/1067983/0000950123-20-012127.txt"

# parse(standard_url + addon, "0000950123")

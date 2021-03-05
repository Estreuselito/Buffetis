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
                                    if_exists="append")), tqdm(os.listdir(self.path), desc="saving to database!")))

    def extract_info_13F_from2014(self, urls):
        """This function returns the infos from the 13F SEC filings from 2014 onwards

        Parameters
        ----------
        urls : list of str
            This is the list of the respective website endings to the edgar archive

        Returns
        -------
        pd.DataFrame
            Returns a Pandas Dataframe, where the SEC filings are stored
        """
        columns = ["SharesHeld", "MarketValue",
                   "CUSIP", "Class", "NameOfCompany", "date", "url"]
        df = pd.DataFrame(columns=columns)
        standard_url = "https://www.sec.gov/Archives/"
        for url in tqdm(urls, desc="getting data from 2014 onwards..."):
            response = get(standard_url + url)
            html_soup = BeautifulSoup(response.text, 'lxml')
            date = datetime.strptime(html_soup.find(
                'signaturedate').contents[0], '%m-%d-%Y')
            name = html_soup.find('name').contents[0]
            cols = ['sshPrnamt', 'value', 'cusip',
                    "titleOfClass", 'nameOfIssuer']
            data = []
            for infotable in html_soup.find_all(['ns1:infotable', 'infotable']):
                row = []
                for col in cols:
                    data2 = infotable.find([col.lower(), 'ns1:' + col.lower()])
                    if data2 is not None:
                        row.append(data2.getText())
                row.append(date)
                row.append(standard_url + url)
                data.append(row)
            tmp = pd.DataFrame(data)
            cols.append('date')
            tmp.columns = columns
            df = df.append(tmp)
        return df

    def extract_info_13F_until2012(self, urls):
        """This function extracts the SEC filing data \
            from the 13F filings until 2012. This function \
            is used for Berkshire Hathaway specificly \
            but could be transformed to work for any other \
            stock.

        Parameters
        ----------
        urls : pd.Series
            Contains the last part of the URLs for the edgar archive files

        Returns
        -------
        pd.DataFrame
            The extracted information from the SEC filings
        """
        df = pd.DataFrame(columns=["Voting Authority", "Other Managers", "Investment Discretion",
                                   "SharesHeld", "MarketValue", "CUSIP", "Class", "NameOfCompany", "date", "url"])
        date_list, url_list = [], []
        standard_url = "https://www.sec.gov/Archives/"
        for url in tqdm(urls, desc="getting data until 2012..."):
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
                    tmp = re.sub(r"(CLA SPL)\s(20030N200)",
                                 r"\1     \2", tmp0)
                    tmp = re.sub(r"(CLA SP L)\s(20030N200)",
                                 r"\1     \2", tmp)
                    tmp1 = re.sub(r"(?<=[a-z&.,])\n", "", tmp)
                    tmp2 = re.sub(r"  (?=[a-z])", " ", tmp1)
                    tmp3 = re.sub(r"([a-z])([A-Z])", r"\1 \2", tmp2)
                    tmp4 = re.sub(r"-\n\s+", r"", tmp3)
                    tmp5 = re.sub(r"([.])([Com])", r"\1     \2",
                                  tmp4).replace("-\n", "")
                    tmp6 = re.sub(
                        r"([ComBADRCVASPL])\s*([A-Z0-9][0-9][0-9][0-9][0-9][0-9A-Za-z][0-9][0-9][0-9A-Z])", r"\1       \2", tmp5)  # This should divide the Com from the CUISP
                    tmp7 = re.sub(
                        r"(ComSPL)\s([A-Z0-9][0-9][0-9][0-9][0-9][0-9A-Za-z][0-9][0-9][0-9A-Z])", r"\1       \2", tmp6)
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
                    tmp24 = re.sub(r"(Comcast)\s*(5, 10, 11, 13, 16,)(Corp)",
                                   r"\1 \3", tmp23)
                    tmp25 = re.sub(r"(?<=SPL)\s(20030N200)",
                                   r"        \1     ", tmp24)
                    tmp26 = re.sub(r"(?<=SP L)\s(20030N200)",
                                   r"        \1     ", tmp25)
                    tmp27 = re.sub(r"(Com A)\s(530322106)",
                                   r"\1     \2", tmp26)
                    tmp28 = re.sub(r"(CVA)\s*(81211K209)",
                                   r"\1      \2", tmp27)
                    tmp29 = re.sub(
                        r"(Liberty Media)\s*(Lib Cap Corp........)", r"\1 \2", tmp28)
                    tmp30 = re.sub(r"(82028k)\s(20)\s(0)", r"82028K200", tmp29)
                    for line in tmp30.replace("-\n", "").split("\n"):
                        data = [x.lstrip()  # added the lstrip here
                                for x in line.split("  ") if x][::-1]
                        if not data:
                            continue
                        tmp = pd.DataFrame(data).T
                        if len([x for x in line.split("  ") if x][::-1]) > 6:
                            tmp.columns = ["Voting Authority", "Other Managers", "Investment Discretion",
                                           "SharesHeld", "MarketValue", "CUSIP", "Class", "NameOfCompany"][:tmp.shape[1]]
                        elif len(data) == 6:
                            tmp.columns = ["Investment Discretion",
                                           "SharesHeld", "MarketValue", "CUSIP", "Class", "NameOfCompany"][:tmp.shape[1]]
                        elif len(data) == 5:
                            tmp.columns = ["Voting Authority", "Other Managers", "Investment Discretion",
                                           "SharesHeld", "MarketValue"][:tmp.shape[1]]
                        else:
                            tmp.columns = ["Investment Discretion",
                                           "SharesHeld", "MarketValue", "CUSIP", "Class", "NameOfCompany"][:tmp.shape[1]]
                        df = df.append(tmp, ignore_index=True)
                        [date_list.append(date) for y in range(0, len(tmp))]
                        [url_list.append(standard_url + url)
                         for z in range(0, len(tmp))]
                else:
                    continue

        # added this line here
        df = df[df["SharesHeld"].notna()]
        df = df[~df["SharesHeld"].isin(
            ["Companies", 'Chemical Corp.', 'house Inc.', 'Corp.', 'Mellon Corp.', 'Co.', 'X', 'cations Inc.', 'Co. 1887'])]
        df["SharesHeld"] = df["SharesHeld"].str.replace(
            ",", "", regex=True).astype(int)
        df["date"] = date_list[:len(df)]
        df["url"] = url_list[:len(df)]

        return df

    def clean_SEC_filings(self):
        """This function cleans the dataframe which was earlier saved in \
           in the database
        """
        (pd.read_sql("""SELECT CAST(CUSIP AS varchar) AS CUSIP,
                           CAST(MarketValue AS int) AS MarketValue,
                           CAST(SharesHeld as int) AS SharesHeld,
                           CAST(date AS varchar) AS date
                    FROM Quarterly_investments""",
                     connection)
         .ffill()
            .groupby(by=["CUSIP", "date"])
            .sum()
            .reset_index()
            .to_sql("Clean_SEC_filings", connection, if_exists="replace", index=False))

        return True

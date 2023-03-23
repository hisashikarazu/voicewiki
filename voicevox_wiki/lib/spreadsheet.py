import gspread
from oauth2client.service_account import ServiceAccountCredentials


class spread_sheet:

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
            'lib/client_secret_ws.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("wikitoss").sheet1

    def __init__(self, from_wiki):
        self.wday=from_wiki[0]
        self.url=from_wiki[1]

    def write_ss(self):
        self.sheet.clear()

        wday0 = [self.wday[0][:6], self.wday[0][7:]]
        i=1
        for s in self.wday:
            if i==1:
                self.sheet.insert_row(wday0, i)
            else:
                self.sheet.update_cell(i, 1, s)
            i=i+1
        wday_url = ['from:', self.url]
        self.sheet.insert_row(wday_url, i+2)
import pygsheets

def init_sheet(service_file, sheet_key):
    gc = pygsheets.authorize(service_file=service_file)
    return gc.open_by_key(sheet_key)

def log_trade(sheet, date, signal, price, pnl):
    ws = sheet.worksheet_by_title('trade_log')
    ws.append_table([[date, signal, price, pnl]])

from ingestion import fetch_data
from strategy import generate_signals
from ml_model import train_predictive_model
from sheets_logger import init_sheet, log_trade

def main():
    tickers = ["RELIANCE.NS","TCS.NS","INFY.NS"]
    df = fetch_data(tickers, "2025-01-01", "2025-06-20")
    signals = generate_signals(df)
    
    sheet = init_sheet('service_account.json', 'YOUR_SHEET_ID')
    
    for idx, row in signals.iterrows():
        if row['signal']:
            price = row['Close']
            log_trade(sheet, str(idx), int(row.signal), price, pnl=0)
    
    model, acc = train_predictive_model(df)
    print(f"ML Model Accuracy: {acc:.2%}")

if __name__ == "__main__":
    main()

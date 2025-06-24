# ml_model.py
import pandas as pd
import pandas_ta as ta
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix

def prepare_features(df):
    df = df.copy()
    df['RSI'] = ta.rsi(df['Close'], length=14)
    macd = ta.macd(df['Close'])
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_Signal'] = macd['MACDs_12_26_9']
    df['SMA20'] = df['Close'].rolling(20).mean()
    df['SMA50'] = df['Close'].rolling(50).mean()
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    return df.dropna()

def train_decision_tree(df):
    data = prepare_features(df)
    features = ['RSI', 'MACD', 'MACD_Signal', 'SMA20', 'SMA50', 'Volume']
    X = data[features]
    y = data['Target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    print("💡 Decision Tree accuracy:", acc)
    print("📊 Confusion Matrix:\n", cm)
    
    # Feature importance
    fi = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
    print("🔧 Feature Importance:\n", fi)
    
    # Optional: plot tree
    # import matplotlib.pyplot as plt
    # plt.figure(figsize=(12,8))
    # plot_tree(model, feature_names=features, class_names=['Down','Up'], filled=True)
    # plt.show()
    
    return model

if __name__ == "__main__":
    from ingestion import fetch_data
    df = fetch_data("RELIANCE.NS", "2020-01-01", "2025-06-20")
    train_decision_tree(df)

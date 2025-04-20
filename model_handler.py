from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 逻辑回归
    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)
    y_pred_logreg = logreg.predict(X_test)
    logreg_report = classification_report(y_test, y_pred_logreg)

    # 随机森林
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    rf_report = classification_report(y_test, y_pred_rf)

    return logreg, rf, logreg_report, rf_report
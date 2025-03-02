from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import logging

# Set up logging
logging.basicConfig(filename='model_logs.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
def data_splitt(df):
    # Feature extraction
    X = df.drop(columns=['Time', 'State'])  # Drop non-feature columns
    y = df['State']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(df,X_train=0,X_test=0):

    if X_train==0:
        X_train, X_test, y_train, y_test=data_splitt(df)
    # Train a Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = clf.predict(X_test)

    # Log classification report
    classification_rep = classification_report(y_test, y_pred)
    logging.info("Classification Report:\n" + classification_rep)

    # Log accuracy
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Model Accuracy: {accuracy * 100:.2f}%")
    return clf
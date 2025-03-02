import numpy as np
from truck_model.model import train_model
from sklearn.ensemble import RandomForestClassifier

def test_train_model():
    X_train = np.random.rand(100, 3)
    y_train = np.random.choice(["ACTIVE", "IDLE", "OFF"], 100)
    model = train_model(X_train, y_train)
    assert isinstance(model, RandomForestClassifier)
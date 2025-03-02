from truck_model.data_generation import simulate_data
from truck_model.model import train_model
from truck_model.visualization import plot_data

df, t, rms_vibration, speed, voltage, labels = simulate_data()
model = train_model(df)


df, t, rms_vibration, speed, voltage, labels = simulate_data()
plot_for_generated_data = plot_data(t, rms_vibration, speed, voltage, labels)

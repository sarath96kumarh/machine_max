import numpy as np
import pandas as pd
import logging

# Set up logging
logging.basicConfig(filename='model_logs.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Parameters
sampling_rate = 1  # Samples per second
duration = 24 * 3600  # 24 hours in seconds
t = np.arange(0, duration, 1)  # Time array

# Function to generate proportional noise
def generate_noise(signal, noise_level):
    return np.random.normal(0, noise_level * np.abs(signal))  # Noise proportional to signal

# Realistic value ranges for a tipper truck with added noise
def generate_data(t, state):
    if state == 'ACTIVE':
        rms_vibration = np.clip(1250 + np.random.uniform(-750, 750, len(t)) + generate_noise(1250, 0.25), 1000, 2000)  # 25% noise
        speed = np.clip(20 + np.random.uniform(-20, 20, len(t)) + generate_noise(20, 0.25), 10, 40)  # 25% noise
        voltage = np.clip(12500 + np.random.uniform(-1500, 1500, len(t)) + generate_noise(12500, 0.25), 13000, 14000)  # 25% noise
    elif state == 'IDLE':
        rms_vibration = np.clip(1250 + np.random.uniform(-750, 750, len(t)) + generate_noise(1250, 0.25), 900, 1100)  # 25% noise
        speed = np.clip(10 + np.random.uniform(-10, 10, len(t)) + generate_noise(10, 0.25), 0, 5)  # 25% noise
        voltage = np.clip(12500 + np.random.uniform(-1500, 1500, len(t)) + generate_noise(12500, 0.25), 12000, 13000)  # 25% noise
    elif state == 'OFF':
        rms_vibration = np.clip(1250 + np.random.uniform(-750, 750, len(t)) + generate_noise(1250, 0.25), 0, 100)  # 25% noise
        speed = np.zeros(len(t))  # Zero speed
        voltage = np.clip(12500 + np.random.uniform(-1500, 1500, len(t)) + generate_noise(12500, 0.25), 11000, 12000)  # 25% noise
    else:
        raise ValueError("Unknown state")
    
    return rms_vibration, speed, voltage

# Function to smooth transitions between states with random fluctuations
def smooth_transition(data, transition_start, transition_end, start_value, end_value):
    transition_duration = transition_end - transition_start
    for i in range(transition_start, transition_end):
        # Linear interpolation with random fluctuations
        t_frac = (i - transition_start) / transition_duration
        fluctuation = np.random.uniform(-0.1, 0.1) * (end_value - start_value)  # Random fluctuation
        data[i] = start_value + (end_value - start_value) * t_frac + fluctuation
    return data

def simulate_data():
    # Simulate a day's worth of data
    np.random.seed(42)
    rms_vibration = np.zeros_like(t, dtype=float)
    speed = np.zeros_like(t, dtype=float)
    voltage = np.zeros_like(t, dtype=float)
    labels = np.zeros_like(t, dtype=object)

    # Define proportions
    active_proportion = 0.5  # 50% of the day
    idle_proportion = 0.3  # 30% of the day
    off_proportion = 0.2  # 20% of the day

    # Define state sequence
    states = ['ACTIVE', 'IDLE', 'OFF']
    state_proportions = [active_proportion, idle_proportion, off_proportion]

    # Generate random durations and sequences
    current_time = 0
    transition_duration = 60  # 1 minute transition duration
    while current_time < duration:
        # Randomly select a state based on proportions
        state = np.random.choice(states, p=state_proportions)
        
        # Generate a random duration for the state
        if state == 'ACTIVE':
            state_duration = np.random.randint(10 * 60, 60 * 60)  # 10 minutes to 1 hour
        elif state == 'IDLE':
            state_duration = np.random.randint(5 * 60, 20 * 60)  # 5 minutes to 20 minutes
        elif state == 'OFF':
            state_duration = np.random.randint(5 * 60, 30 * 60)  # 5 minutes to 30 minutes
        
        # Ensure the duration does not exceed the remaining time
        state_duration = min(state_duration, duration - current_time)
        
        # Generate data for the current state
        idx = (t >= current_time) & (t < current_time + state_duration)
        rms_vibration[idx], speed[idx], voltage[idx] = generate_data(t[idx], state)
        labels[idx] = state
        
        # Smooth transition to the next state
        if current_time + state_duration < duration:
            transition_start = current_time + state_duration - transition_duration
            transition_end = current_time + state_duration
            next_state = np.random.choice(states, p=state_proportions)
            
            # Smooth RMS Vibration
            rms_vibration = smooth_transition(rms_vibration, transition_start, transition_end,
                                            rms_vibration[transition_start], np.random.uniform(500 if next_state == 'ACTIVE' else 500 if next_state == 'IDLE' else 500))
            
            # Smooth Speed
            speed = smooth_transition(speed, transition_start, transition_end,
                                    speed[transition_start], np.random.uniform(20 if next_state == 'ACTIVE' else 10 if next_state == 'IDLE' else 0))
            
            # Smooth Voltage
            voltage = smooth_transition(voltage, transition_start, transition_end,
                                    voltage[transition_start], np.random.uniform(12500 if next_state == 'ACTIVE' else 12500 if next_state == 'IDLE' else 12500))
        
        # Update current time
        current_time += state_duration

    # Create a DataFrame
    df = pd.DataFrame({
        'Time': t,
        'RMS_Vibration': rms_vibration,
        'Speed': speed,
        'Voltage': voltage,
        'State': labels
    })

    # Add feature-engineered columns
    def add_feature_engineered_columns(df, window_size=60):
        # Energy Consumption
        df['Energy_Consumption'] = df['RMS_Vibration'] * df['Voltage']

        # State Duration
        df['State_Duration'] = df.groupby((df['State'] != df['State'].shift()).cumsum()).cumcount()

        # Rolling Statistics for Speed
        df['Speed_Rolling_Mean'] = df['Speed'].rolling(window=window_size, min_periods=1).mean()
        df['Speed_Rolling_Std'] = df['Speed'].rolling(window=window_size, min_periods=1).std()

        return df

    df = add_feature_engineered_columns(df)

    # Log data description
    logging.info("Data Description:\n" + str(df.describe()))
    return df,t, rms_vibration, speed, voltage, labels

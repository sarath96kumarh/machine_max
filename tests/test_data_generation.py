import numpy as np

from truck_model.data_generation import generate_data, generate_noise


def test_generate_noise():
    signal = np.array([1, 2, 3])
    noise_level = 0.1
    noise = generate_noise(signal, noise_level)
    assert noise.shape == signal.shape


def test_generate_data():
    t = np.arange(0, 100, 1)
    state = "ACTIVE"
    rms_vibration, speed, voltage = generate_data(t, state)
    assert len(rms_vibration) == len(t)
    assert len(speed) == len(t)
    assert len(voltage) == len(t)

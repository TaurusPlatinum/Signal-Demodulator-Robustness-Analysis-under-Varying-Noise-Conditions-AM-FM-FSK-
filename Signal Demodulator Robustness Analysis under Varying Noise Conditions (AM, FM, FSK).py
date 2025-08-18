import numpy as np
import matplotlib.pyplot as plt

fs = 1000           
t = np.arange(0, 1, 1/fs)  
f_c = 100           
snr_range = np.arange(0, 15, 1)  
data = np.random.randint(0, 2, len(t))

def generate_am_signal(data, f_c, t):
    return (1 + data) * np.cos(2 * np.pi * f_c * t)

def generate_fm_signal(data, f_c, t):
    return np.cos(2 * np.pi * f_c * t + np.pi * data)

def generate_fsk_signal(data, f_c, t):
    f_shift = 10
    return np.where(data == 1, 
                    np.cos(2 * np.pi * (f_c + f_shift) * t), 
                    np.cos(2 * np.pi * (f_c - f_shift) * t))

def add_noise(signal, SNR_dB):
    SNR_linear = 10 ** (SNR_dB / 10)
    power_signal = np.mean(signal ** 2)
    power_noise = power_signal / SNR_linear
    noise = np.sqrt(power_noise) * np.random.randn(len(signal))
    return signal + noise

def demodulate_am(signal, t):
    envelope = np.abs(signal)
    return envelope > np.mean(envelope)

def demodulate_fm(signal, t, f_c):
    phase = np.unwrap(np.angle(signal))
    frequency_deviation = np.diff(phase) / (2.0 * np.pi * np.diff(t))
    return frequency_deviation > np.mean(frequency_deviation)

def demodulate_fsk(signal, t, f_c):
    analytic_signal = np.exp(1j * 2 * np.pi * f_c * t)
    product = signal * analytic_signal
    return np.real(product) > np.mean(np.real(product))

def calculate_error_rate(demodulated, data):
    errors = np.sum(demodulated != data[:len(demodulated)])
    return errors / len(demodulated)

error_rates_am = []
error_rates_fm = []
error_rates_fsk = []

for snr in snr_range:
    am_signal = generate_am_signal(data, f_c, t)
    fm_signal = generate_fm_signal(data, f_c, t)
    fsk_signal = generate_fsk_signal(data, f_c, t)

    noisy_am_signal = add_noise(am_signal, snr)
    noisy_fm_signal = add_noise(fm_signal, snr)
    noisy_fsk_signal = add_noise(fsk_signal, snr)

    demodulated_am = demodulate_am(noisy_am_signal, t)
    demodulated_fm = demodulate_fm(noisy_fm_signal, t, f_c)
    demodulated_fsk = demodulate_fsk(noisy_fsk_signal, t, f_c)

    error_rates_am.append(calculate_error_rate(demodulated_am, data))
    error_rates_fm.append(calculate_error_rate(demodulated_fm, data[:-1]))  
    error_rates_fsk.append(calculate_error_rate(demodulated_fsk, data))

plt.figure(figsize=(10, 6))
plt.plot(snr_range, error_rates_am, label="АМ", marker='o')
plt.plot(snr_range, error_rates_fm, label="ФМ", marker='x')
plt.plot(snr_range, error_rates_fsk, label="ЧМ", marker='s')
plt.xlabel("SNR (дБ)")
plt.ylabel("Ймовірність помилки (P_e)")
plt.yscale('log')
plt.title("Завадостійкість демодуляторів з АМ, ФМ і ЧМ")
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()

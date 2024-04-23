import numpy as np

with open('rec_1.dat', 'rb') as file:
    # Read binary data
    binary_data = file.read()
    
    # Convert binary data to a 1D array of integers
    values2= np.frombuffer(binary_data, dtype=np.int32)
    data1=values2.copy()
    values=data1[:9000]
    
    #fs is already known in medical signals
    fs = 500.0  # Sample rate in Hz
    
    # Calculate time values
    time_values = np.arange(0, len(values) / fs, 1 / fs)


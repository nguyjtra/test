import random

def generate_secret_message(m):
    message = []
    for _ in range(m):
        bit = random.randint(0, 1) 
        message.append(bit)
    return message

# Hàm tạo thời gian gói tin đến từ Source
def generate_arrival_times(m, distribution):
    times = [0]  
    for _ in range(m - 1): 
        if distribution == "uniform":
            delay = random.uniform(0, 1) 
        elif distribution == "exponential":
            delay = random.expovariate(1)  
            if delay > 5:
                delay = 5  
        times.append(times[-1] + delay) 
    return times

def generate_transmission_delays(secret_msg, distribution):
    delays = []
    if distribution == "uniform":
        for bit in secret_msg:
            if bit == 0:
                delay = random.uniform(0, 0.5)  
            else:
                delay = random.uniform(0.5, 1) 
            delays.append(delay)
    elif distribution == "exponential":
        median = 0.693147 
        max_delay = 5
        for bit in secret_msg:
            if bit == 0:
                delay = random.uniform(0, median)  
            else:
                delay = random.uniform(median, max_delay)  
            delays.append(delay)
    return delays

def simulate_experiment(m, B, i, distribution):
    arrival_times = generate_arrival_times(1000, distribution)
    t_start = arrival_times[i - 1] 
    
    secret_msg = generate_secret_message(m)
    delays = generate_transmission_delays(secret_msg, distribution)
    
    transmission_times = [t_start]
    current_time = t_start
    for delay in delays:
        current_time += delay
        transmission_times.append(current_time)
    
    tm = transmission_times[-1]
    
    events = []
    for t in arrival_times:
        if t <= tm:
            events.append((t, "arrival"))
    for t in transmission_times:
        events.append((t, "transmission"))
    events.sort()  # Put events in time order
    
    buffer_size = 0
    overflow = False
    underflow = False
    for time, event_type in events:
        if event_type == "arrival":
            buffer_size += 1  
            if buffer_size > B:
                overflow = True  
                break
        elif event_type == "transmission":
            if buffer_size == 0:
                underflow = True  
                break
            buffer_size -= 1  
    return overflow, underflow

# Hàm chạy nhiều lần để tính xác suất
def run_experiments(m, B, i, distribution, num_experiments=500):
    overflows = 0
    underflows = 0
    for _ in range(num_experiments):
        overflow, underflow = simulate_experiment(m, B, i, distribution)
        if overflow:
            overflows += 1
        if underflow:
            underflows += 1
    success = 1 - (overflows + underflows) / num_experiments
    return overflows / num_experiments, underflows / num_experiments, success

distribution = input(" (exponential/uniform): ")
m = int(input(" (16 or 32): "))
i = int(input(" i = 2, 6, 10, 14, 18: pick one "))

B = 20
overflow_prob, underflow_prob, success_prob = run_experiments(m, B, i, distribution)
print(f"Probability  Underflow: {underflow_prob:.3f}")
print(f"Probability Overflow: {overflow_prob:.3f}")
print(f"Probability success: {success_prob:.3f}")
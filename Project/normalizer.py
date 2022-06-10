def normalizeC1_C5(value):
    if value == "yes":
        return 1
    elif value == "no":
        return 0.01
    else:
        return None

def normalizeC2(value):
    if 0 <= value < 9.5:
        return 0.01
    elif 9.5 <= value < 12.5:
        return 0.25
    elif 12.5 <= value < 15:
        return 0.5
    elif 15 <= value < 17.5:
        return 0.75
    elif 17.5 <= value <= 20:
        return 1

def normalizeC3(value):
    if 0 <= value <= 10000:
        return 1
    elif 10000 < value <= 40245:
        return 0.66
    elif 40245 < value <= 100000:
        return 0.33
    elif value > 100000:
        return 0.01

def normalizeC4(value):
    if 0 <= value <= 5000:
        return 1
    elif 5000 < value <= 12500:
        return 0.75
    elif 12500 < value <= 25000:
        return 0.5
    elif 25000 < value <= 50000:
        return 0.25
    elif value > 50000:
        return 0.01
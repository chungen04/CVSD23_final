def s316_to_dec(str):
    hex_value = int(str, 16)

    # Check if the value is negative (i.e., the first bit is 1)
    if hex_value & 0x80000:
        # Convert to negative value in 2's complement
        hex_value -= 0x100000
    hex_value = hex_value / (2**16)
    return hex_value
    
def bin2_to_int(str):
    if(str[0] == '0'):
        if(str[1] == '0'):
            return 0
        else:
            return 1
    else:
        if(str[1] == '0'):
            return 2
        else:
            return 3

def read_in_r(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line.strip())
    lines = [[ line[i*5:(i+1)*5] for i in range(16)] for line in lines]
    lines = [[s316_to_dec(line[i]) for i in range(16)] for line in lines]
    lines = [[complex(line[0], 0), complex(line[2], line[1]), complex(line[4], line[3]), complex(line[6], line[5]), complex(line[7], 0), complex(line[9], line[8]), complex(line[11], line[10]), complex(line[12], 0), complex(line[14], line[13]), complex(line[15], 0)] for line in lines]
    # print(lines[0])
    return lines

def read_in_y_hat(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line.strip())
    lines = [[ line[i*5:(i+1)*5] for i in range(8)] for line in lines]
    lines = [[s316_to_dec(line[i]) for i in range(8)] for line in lines]
    lines = [[complex(line[7], line[6]), complex(line[5], line[4]), complex(line[3], line[2]), complex(line[1], line[0])] for line in lines]
    # print(lines[0])
    return lines

def reshape_to_2d(input_list, col):
    num_rows = len(input_list) // col
    output_list = [[] for _ in range(num_rows)]
    for i in range(len(input_list)):
        row = i // col
        output_list[row].append(input_list[i])
    return output_list

def read_in_hb(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line.strip())
    lines = reshape_to_2d(lines, 2)
    lines = ["".join(e) for e in lines]
    lines = reshape_to_2d(lines, 4)
    return lines

branches = [3, 2, 1, 1]

r = read_in_r("PATTERN/packet1/SNR10dB_pat_r.dat")
y_hat = read_in_y_hat("PATTERN/packet1/SNR10dB_pat_y_hat.dat")
golden = read_in_hb("PATTERN/packet1/SNR10dB_hb.dat")

# for i in y_hat:
#     print(i[3])
# exit()

a = 1/(2**0.5)
s_candidates = [complex(a, a), complex(a, -a), complex(-a, a), complex(-a, -a)]

result = []
acc = 0
for i in range(len(r)): # 1000
    result.append([])
    # print(y_hat[i][3])
    for s in s_candidates:
        result[i].append(abs(y_hat[i][3] - r[i][0]*s))
    result[i] = result[i].index(min(result[i]))
    if(result[i]!=bin2_to_int(golden[i][3])):
        print("Testcase", i, "Error,", y_hat[i][3] ,"expect", bin2_to_int(golden[i][3]), "but find", result[i])
    else:
        acc += 1
print("acc:", acc/10, "%")
# acc = 1000
# for i in range(len(r)): # 1000
#     if(result[i] == bin2_to_int(golden[i][3])):
#         acc -= 1
# acc = acc / 10
# print(acc)
def shutter1_protocol(helper):
    pulses_to_binary_mapping = {
        '32': '',
        '01': '0',
        '10': '1',
        '14': ''
    }
    binary_to_pulse = {
        '0': '01',
        '1': '10'
    }
    protocol_info = {
        'name': 'shutter1',
        'type': 'command',
        'commands': ["up", "down", "stop"],
        'values': {
            'id': {'type': "number"},
            'command': {'type': "string"}
        },
        'brands': ["Nobily"],
        'pulseLengths': [280, 736, 1532, 4752, 7796],
        'pulseCount': 164,
        'decodePulses': lambda pulses: decode_pulses(pulses, helper, pulses_to_binary_mapping),
        'encodeMessage': lambda message: encode_message(message, helper, binary_to_pulse)
    }
    return protocol_info

def decode_pulses(pulses, helper, pulses_to_binary_mapping):
    binary = "".join(pulses_to_binary_mapping.get(pulse, '') for pulse in pulses)
    commandcode = binary[31:35]
    if commandcode == '1000':
        command = 'up'
    elif commandcode == '1001':
        command = 'down'
    elif commandcode == '1010':
        command = 'stop'
    else:
        command = None
    result = {
        'id': helper.binary_to_number(binary, 0, 30),
        'command': command
    }
    return result

def encode_message(message, helper, binary_to_pulse):
    id_binary = helper.number_to_binary(message['id'], 31)
    id_pulses = "".join(binary_to_pulse[bit] for bit in id_binary)
    if message['command'] == 'up':
        commandcode = '1000'
    elif message['command'] == 'down':
        commandcode = '1001'
    elif message['command'] == 'stop':
        commandcode = '1010'
    else:
        commandcode = None
    command_pulses = "".join(binary_to_pulse[bit] for bit in commandcode)
    return "32" + id_pulses + command_pulses + command_pulses + "1032" + id_pulses + command_pulses + command_pulses + "14"

class Helper:
    def binary_to_number(self, binary_string, start, end):
        return int(binary_string[start:end+1], 2)

    def number_to_binary(self, number, length):
        return bin(number)[2:].zfill(length)

# Test the Python code
helper = Helper()
protocol = shutter1_protocol(helper)

# Test decodePulses
pulses_test = ['32'] + ['01']*10 + ['10']*21 + ['10','01','01','01'] + ['10','01','10','10']
decoded_result = protocol['decodePulses'](pulses_test)
print("Decoded Result:", decoded_result)

# Test encodeMessage
message_test = {'id': 1234567, 'command': 'up'}
encoded_result = protocol['encodeMessage'](message_test)
print("Encoded Result:", encoded_result)

message_test_down = {'id': 1234567, 'command': 'down'}
encoded_result_down = protocol['encodeMessage'](message_test_down)
print("Encoded Result Down:", encoded_result_down)

message_test_stop = {'id': 1234567, 'command': 'stop'}
encoded_result_stop = protocol['encodeMessage'](message_test_stop)
print("Encoded Result Stop:", encoded_result_stop)

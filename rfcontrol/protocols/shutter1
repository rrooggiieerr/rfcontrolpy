# This Python code was automatically converted from the rfcontroljs repo, in particular from the shutter1.coffee protocol file using codeconvert.ai 
# It was done because this protocol implementation was still missing in the rfcontrolpy repo.

def protocol_info(helper):
    pulses_to_binary_mapping = {
        '32': '',  # header
        '01': '0',  # binary 0
        '10': '1',  # binary 1
        '14': ''  # footer
    }
    binary_to_pulse = {
        '0': '01',
        '1': '10'
    }
    
    def decode_pulses(pulses):
        # pulses for up, down and stop are something like:
        # 32
        # 01011001010101100101010101010110011010100101101010010110010101
        # 10010101
        # 10010101
        # 10
        # 32
        # 01011001010101100101010101010110011010100101101010010110010101
        # 10010101
        # 10010101
        # 14

        # we first map the sequences to binary
        binary = helper.map(pulses, pulses_to_binary_mapping)
        # binary is now something like: '001000010000000101110011100100010011001'
        # now we extract the data from that string
        # | 0010000100000001011100111001000 | 1000     | 1000     |
        # | ID                              | command  | command  |
        #
        # | 1     |
        # | fixed |
        #
        # | 0010000100000001011100111001000 | 1000     | 1000     |
        # | ID                              | command  | command  |

        commandcode = binary[31:35]
        if commandcode == '1000':
            command = 'up'
        elif commandcode == '1001':
            command = 'down'
        elif commandcode == '1010':
            command = 'stop'
        
        return {
            'id': helper.binary_to_number(binary, 0, 30),
            'command': command
        }

    def encode_message(message):
        id = helper.map(helper.number_to_binary(message['id'], 31), binary_to_pulse)
        if message['command'] == 'up':
            commandcode = '1000'
        elif message['command'] == 'down':
            commandcode = '1001'
        elif message['command'] == 'stop':
            commandcode = '1010'
        
        commandcode = helper.map(commandcode, binary_to_pulse)

        return f"32{id}{commandcode}{commandcode}1032{id}{commandcode}{commandcode}14"

    return {
        'name': 'shutter1',
        'type': 'command',
        'commands': ["up", "down", "stop"],
        'values': {
            'id': {
                'type': "number"
            },
            'command': {
                'type': "string"
            }
        },
        'brands': ["Nobily"],
        'pulseLengths': [280, 736, 1532, 4752, 7796],
        'pulseCount': 164,
        'decodePulses': decode_pulses,
        'encodeMessage': encode_message
    }


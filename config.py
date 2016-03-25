import ConfigParser

class Settings(object):
    """docstring for ClassName"""
    def __init__(self):
        super(Settings, self).__init__()

def get_config_from_user():
    #CSV Section
    print("Enter the filepath of the CSV file to Read")
    csv_filepath = raw_input("FILEPATH = ")
    print("Enter the IP Address from which to serve the Modbus TCP Server")
    print("For Self-Hosting Server Enter localhost")
    ip_addr = raw_input("IP Address = ")
    ip_port = int(raw_input("Port = "))
    print("Define how frequently program will update Server context (in seconds)")
    update_frequency = int(raw_input("Update Frequency = "))
    config_data = [csv_filepath, ip_addr, ip_port, update_frequency]
    return config_data


def write_to_config_file(config_data):
    config = ConfigParser.RawConfigParser()
    config.add_section('CSV')
    config.add_section('TCP Server')
    config.set('CSV', 'Filepath', config_data[0])
    config.set('TCP Server', 'IP Address', config_data[1])
    config.set('TCP Server', 'Port', config_data[2])
    config.set('TCP Server', 'Update Frequency', config_data[3])

    with open('settings.ini', 'wb') as configfile:
        config.write(configfile)

def read_from_config_file():
    config = ConfigParser.RawConfigParser()
    config.read('settings.ini')
    settings = Settings()
    settings.CSV_FILEPATH = config.get('CSV', 'Filepath')
    settings.IP_ADDRESS = config.get('TCP Server', 'IP Address')
    settings.IP_PORT = config.getint('TCP Server', 'Port')
    settings.UPDATE_FREQ = config.getfloat('TCP Server', 'Update Frequency')
    return settings


'''
csv2modbus_singlefile is a utility script that reads a CSV file in
a particular format and outputs its values on a MODBUS TCP Server
as F-32 registers.

If the file is empty the script retains old data that continues to be passed
to the Modbus Server

CSV Format -
datetime, value1, value2, value3, value4 .... upto value 120

-- The file should be single row with values as columns
-- The max number of values is 125

ModbusServer -
Created using the pymodbus library.
Outputs the columns of the CSV file as consecutive registers
'''

#---------------------------------------------------------------------------#
# Imports
#---------------------------------------------------------------------------#

# Import Pymodbus libraries
import multiprocessing
# Explicit import of _cffi_backend required for Pyinstaller packaging
import _cffi_backend
from pymodbus.server.async import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
import config
# Import Twisted
from twisted.internet.task import LoopingCall

# Import CSV Reading libraries
import csv

#---------------------------------------------------------------------------#
# Constants
#---------------------------------------------------------------------------#
identity = ModbusDeviceIdentification()
identity.VendorName  = 'ForbesMarshall'
identity.ProductCode = 'FMPL'
identity.VendorUrl   = 'http://www.forbesmarshall.com'
identity.ProductName = 'FM Modbus Server'
identity.ModelName   = 'FM Modbus Server'
identity.MajorMinorRevision = '1.0'
STORED_DATA = []

#---------------------------------------------------------------------------#
# Function Definitions
#---------------------------------------------------------------------------#

def get_config_file():
    while True:
        try:
            settings = config.read_from_config_file()
            print settings
            return settings
        except Exception as e:
            print str(e)
            print "Oops! Can't Read Configuration Data"
            print "Please reenter the Configuration"
            config_data = config.get_config_from_user()
            try:
                config.write_to_config_file(config_data)
                print "OK! Now Let's loop back"
            except Exception as e:
                print "Wow! Something is really whacky here. Can't even create a config file"
                continue
        break

def read_data_file(filepath):
    """
        Reads a csv file on the given file path, outputs the first row to a array.
        If file is not present creates a empty file
    """

    try:
        with open(filepath, 'rb') as csvfile:
            file = csv.reader(csvfile, delimiter=',')
            first_row = next(file)
            data = first_row[0:40]
            print data
            data = [float(i) for i in data]
            if not data:
                raise EmptyFileError(filepath)
            return data
    except StopIteration as e:
        print str(e)
        pass
    except EmptyFileError as empty:
        print "Oops! The file at %s is empty!" % (empty.filepath)
        print "Please configure it correctly..."
        pass

class EmptyFileError(Exception):
    """
        Exception raised when the read file is empty.
        Attributes:
            - filename
            - msg
    """

    def __init__(self, filepath):
        self.filepath = filepath

def initialize_datastore():
    block = ModbusSequentialDataBlock.create()
    store = ModbusSlaveContext(di = block, co = block, hr = block, ir = block)
    context = ModbusServerContext(slaves=store, single=True)
    return context

def update_datastore(a):
    print 'Running Update'
    context = a[0]
    settings = a[1]
    global STORED_DATA
    function = 3
    slave_id = 0x00
    start_address  = 0x00
    data = read_data_file(settings.CSV_FILEPATH)
    print data
    if not data:
        data = STORED_DATA
        print "File Empty so taking STORED DATA"
        print STORED_DATA
    else:
        STORED_DATA = data
        print "New Stored Data is"
        print STORED_DATA
    if len(data) <= 60:
        builder = BinaryPayloadBuilder(endian=Endian.Big)
        for value in data:
            builder.add_32bit_float(value)
        payload = builder.to_registers()
        context[slave_id].setValues(function, start_address, payload)
    else:
        builder = BinaryPayloadBuilder(endian=Endian.Big)
        for value in data[:60]:
            builder.add_32bit_float(value)
        builder.add_32bit_float(0.00)
        for value in data[60:]:
            builder.add_32bit_float(value)
        payload = builder.to_registers()
        context[slave_id].setValues(function, start_address, payload)
    pass

#---------------------------------------------------------------------------#
# Function Calls
#---------------------------------------------------------------------------#
if __name__ == '__main__':
    # Multiprocessing module fix for Pyinstaller packaging
    multiprocessing.freeze_support()
    settings = get_config_file()
    context = initialize_datastore()
    loop = LoopingCall(f=update_datastore, a=(context, settings))
    loop.start(settings.UPDATE_FREQ, now=True)
    StartTcpServer(context, identity=identity, address=(settings.IP_ADDRESS, settings.IP_PORT), console=True)

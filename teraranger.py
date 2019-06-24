###### TeraRanger Evo Implementation by EmergenTek #######
#                                                        #
#        Originally by Terabee France (c) 2018           #
#                                                        #
############ www.terabee.com #############################

# Original Code at https://github.com/Terabee/sample_codes/tree/master/Python/Evo60m-3m-600Hz_display_range.py
# ./RANGE/teraranger.py

import serial
import serial.tools.list_ports
import crcmod.predefined  # To install: pip install crcmod

class Evo:
    def __init__(self):
        # Get the port the evo has been connected to
        self.port = self.findEvo()

        if self.port == None:
            raise serial.serialutil.SerialException("\nCould not find the Evo. \nMake sure it is plugged in correctly.")
            
        else:
            self.evo = self.openEvo()

    def __del__(self):
        print("Closing EVO")
        self.evo.close()
        
	# START: Original Code by Terabee
    def findEvo(self):
        '''Find the serial port on which the Evo is connected.'''
        # Find Live Ports, return port name if found, NULL if not
        print('Scanning all USB ports for Range Finder.')
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            # print(p) # This causes each port's information to be printed out.
            if "5740" in p[2]:
                print('Evo found on port ', p[0])
                return p[0]
        return None
    
    def openEvo(self):
        '''Open Evo on specified port name.'''
        
        # Open the Evo and catch any exceptions thrown by the OS
        portname=self.port
        print('Attempting to open port {}'.format(portname))
        evo = serial.Serial(portname, baudrate=115200, timeout=2)
        # Send the command "Binary mode"
        set_bin = (0x00, 0x11, 0x02, 0x4C)
        # rset in the buffer
        evo.reset_input_buffer()
        # Write the binary command to the Evo
        evo.write(set_bin)
        # reset out the buffer
        evo.reset_output_buffer()
        print('Serial port opened')
        return evo
	# END

	# START: Modified Code by Terabee (Original code marked by ### )
    def get_evo_range(self):
        """Return the Teraranger Evo range in meters"""		###
        crc8_fn = crcmod.predefined.mkPredefinedCrcFun('crc-8')		###
        
        #TODO: Test Connection	
        
        #Reset Buffer	
        self.evo.reset_input_buffer()	
        # Read one byte
        data=None
        while not data == b'T':
            try:
                data = self.evo.read(1)		###
            except serial.serialutil.SerialException:
                print("Device disconnected (or multiple access on port)")
                return None
            #print(data)    #debugLC
            if data == b'T':
                # After T read 3 bytes		###
                frame = data + self.evo.read(3)		###
                #print(frame)   #debugLC
                if frame[3] == crc8_fn(frame[0:3]):		###
                    # Convert binary frame to decimal in shifting by 8 the frame
                    rng = frame[1] << 8
                    rng = rng | (frame[2] & 0xFF)
                else:		###
                    raise Exception("CRC mismatch. Check connection to Range Finder or make sure only one progam access the sensor port.")
            # Check special cases (limit values)
            else:		###
                # raise Exception("Wating for frame header")
                # print("Wating for frame header")		###
                pass
			
		### <original code>
        # Checking error codes
        if rng == 65535: # Sensor measuring above its maximum limit
            dec_out = float('inf')
        elif rng == 1: # Sensor not able to measure
            dec_out = float('nan')
        elif rng == 0: # Sensor detecting object below minimum range
            dec_out = -float('inf')
        else:
            # Convert frame in meters
            dec_out = rng / 1000.0
        return dec_out
		### </original code>

import serial
import re


class Error:
    """Class for errors of the photometer"""

    def __init__(self, line):
        """Create instance of the class from response line"""
        mo = re.match("(\d+)\s(.+?)\((\d+)\)", line)
        if not mo:
            raise ValueError(
                "Error string " + line + " does not match expected format."
            )
        self.code = int(mo[1])
        self.text = mo[2]
        self.run = int(mo[3])

    def __str__(self):
        return f"{self.code} {self.text} ({self.run})"


class Spectramax:
    """Class for the communication with Molecular Devices Spectramax well plate reader"""

    def clear_state(self):
        """Clears state of the instrument in the class at the beginning or on reset"""
        self.door_open = None
        self._status = None

    def __init__(self, tty, baudrate=9600, timeout=1):
        self.port = None
        self.port = serial.Serial(tty, baudrate=baudrate, timeout=timeout)
        self.clear_state()

    def __del__(self):
        if self.port and self.port.isOpen():
            self.port.close()

    def cmd(self, command, decode=True):
        """Executes command given as string, and return result as non-decoded bytes/ascii"""
        self.port.write((command + "\n").encode("ascii"))
        r = b""
        while line := self.port.readline():
            r += line
            if line == b">":
                break
        if decode:
            try:
                return r.decode("ascii")
            except Exception:
                return ""
        else:
            return r

    def execute(self, command):
        """Execute command and check it returned OK"""
        r = self.cmd(command, True)
        if r[0:2] == "OK":
            return True
        return False

    def open(self):
        """Open door to insert well plate"""
        if self.execute("!OPEN"):
            self.door_open = True

    def close(self):
        """Close door for well plates"""
        if self.execute("!CLOSE"):
            self.door_open = False

    def clear(self):
        """Clear errors"""
        r = self.cmd("!CLEAR")

    def errors(self):
        """Read errors"""
        r = self.cmd("!ERROR", True)
        lines = r.split("\r\n")
        errors = []
        for l in lines:
            if not re.match("^\d", l):
                continue
            err = Error(l)
            errors.append(err)
        return errors

    def nvram(self):
        """Read parameters from NVRAM"""
        r = self.cmd("!NVRAM")
        print(r)

    def status(self):
        """Read and update status of the instrument: is door open or not, and if it is idle or measuring"""
        r = self.cmd("!STATUS", True)
        """
        # The command returns somthing like that. Assuming line numbers are conserved between instrument models.
        OK
        >
        OPEN
        IDLE
        
        >
        """
        l = r.split("\r\n")
        if l[2].strip() == "OPEN":
            self.door_open = True
        elif l[2].strip() == "CLOSED":
            self.door_open = False
        # this is usually IDLE. But can be MEASURING or AIR CAL206 for instance on power on
        self._status = l[3].strip()
        return {"door_open": self.door_open, "status": self._status}

    def read(self):
        self.cmd("!CLEAR DATA")

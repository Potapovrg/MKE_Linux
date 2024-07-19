from smbus import SMBus
import sys
import time

bus = SMBus(0)
addr = 0x28

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

regs = {
    'ALERT_STATUS' : 0x0B,
    'ALERT_STATUS_MASK_CTRL' : 0x0C,
    'CC_CONNECTION_STATUS_TRANS' : 0x0D,
    'CC_CONNECTION_STATUS' : 0x0E,
    'MONITORING_STATUS_TRANS' : 0x0F,
    'MONITORING_STATUS' : 0x10,
    'CC_OPERATION_STATUS' : 0x11,
    'HW_FAULT_STATUS_TRANS' : 0x12,
    'HW_FAULT_STATUS' : 0x13,
    'CC_CAPABILITY_CTRL' : 0x18,
    'CC_VCONN_SWITCH_CTRL' : 0x1E,
    'VCONN_MONITORING_CTRL' : 0x20,
    'VBUS_MONITORING_RANGE_CTRL' : 0x22,
    'RESET_CTRL' : 0x23,
    'VBUS_DISCHARGE_TIME_CTRL' : 0x25,
    'VBUS_DISCHARGE_STATUS' : 0x26,
    'VBUS_ENABLE_STATUS' : 0x27,
    'CC_POWER_MODE_CTRL' : 0x28,
    'VBUS_MONITORING_CTRL' : 0x2E
} 

source_cfg = [{ #source
    0x18 : 0x61,
    0x1E : 0x00,
    0x20 : 0xA0,
    0x22 : 0x55,
    0x25 : 0x60,
    0x28 : 0x00,
    0x2E : 0x01
}, { #think
    0x18 : 0x61,
    0x1E : 0x00,
    0x20 : 0xA0,
    0x22 : 0x5F,
    0x25 : 0x60,
    0x28 : 0x01,
    0x2E : 0x01
}, { #dual role source
    0x18 : 0x61,
    0x1E : 0x00,
    0x20 : 0xA0,
    0x22 : 0x5F,
    0x25 : 0x60,
    0x28 : 0x04,
    0x2E : 0x01
}, { #dual role think
    0x18 : 0x61,
    0x1E : 0x00,
    0x20 : 0xA0,
    0x22 : 0x5F,
    0x25 : 0x60,
    0x28 : 0x05,
    0x2E : 0x01
} ]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        config = int(sys.argv[1])
        print(f"Reset {config}")
        bus.write_byte_data(addr, 0x23, 1)
        time.sleep(0.05)
        bus.write_byte_data(addr, 0x23, 0)
        time.sleep(0.05)
        print(f"{bcolors.WARNING}Write config {config}{bcolors.ENDC}")
        for reg, val in source_cfg[config].items():
            bus.write_byte_data(addr, reg, val)            

    for name, reg in regs.items():
        v = bus.read_byte_data(addr, reg)
        print(f"{bcolors.HEADER}{name:30} {bcolors.OKGREEN}(0x{reg:2X}) : 0x{v:2X}{bcolors.ENDC}")
    status = bus.read_byte_data(addr, 0x0E)
    cc_attach_mode = ["No dev", "Sink attached", "Source attached",
                      "Debug attached", "Audio attached", "Not used",
                      "Not used", "Not used"]
    print(f"{bcolors.HEADER}CC_ATTACHED_MODE    {bcolors.OKGREEN}{cc_attach_mode[status>>5]}{bcolors.ENDC}")
    print(f"{bcolors.HEADER}DEVICE_POWER_MODE   {bcolors.OKGREEN}{'Stanby' if status & 0x10 else 'Normal'}{bcolors.ENDC}")
    print(f"{bcolors.HEADER}CC_POWER_ROLE       {bcolors.OKGREEN}{'Source' if status & 0x08 else 'Sink'}{bcolors.ENDC}")
    print(f"{bcolors.HEADER}CC_VCONN_SUPPLY     {bcolors.OKGREEN}{'Vcon on CC' if status & 0x02 else 'No'}{bcolors.ENDC}")
    print(f"{bcolors.HEADER}CC_ATTACH           {bcolors.OKGREEN}{'true' if status & 0x02 else 'false'}{bcolors.ENDC}")

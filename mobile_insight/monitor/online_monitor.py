#!/usr/bin/python
# Filename: online_monitor.py
"""
A universal, cross-platform MobileInsight online monitor.

It abstracts the low-level complexity of platform-dependent monitors.
It wraps monitors for mobile version (currently Android only) and desktop version.

Author: Yuanjie Li
"""

__all__ = ["OnlineMonitor"]



# Test the OS version
is_android = False

try:
    from jnius import autoclass  # For Android
    is_android = True


    import subprocess
    ANDROID_SHELL = "/system/bin/sh"
    class ChipsetType:
        """
        Cellular modem type
        """
        QUALCOMM = 0
        MTK = 1

    def run_shell_cmd(cmd, wait=False):
        p = subprocess.Popen(
            "su",
            executable=ANDROID_SHELL,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        res, err = p.communicate(cmd + '\n')

        if wait:
            p.wait()
            return res
        else:
            return res

    def get_chipset_type():
        """
        Determine the type of the chipset

        :returns: an enum of ChipsetType
        """


        """
        MediaTek: [ro.board.platform]: [mt6735m]
        Qualcomm: [ro.board.platform]: [msm8084]
        """
        cmd = "getprop ro.board.platform;"
        res = run_shell_cmd(cmd)
        if res.startswith("mt"):
            return ChipsetType.MTK
        elif res.startswith("msm") or res.startswith("mdm"):
            return ChipsetType.QUALCOMM
        else:
            return None

    
    chipset_type = get_chipset_type()
    print "chipset_type",chipset_type

    if chipset_type == ChipsetType.QUALCOMM:
        from android_dev_diag_monitor import AndroidDevDiagMonitor
        class OnlineMonitor(AndroidDevDiagMonitor):
            def __init__(self):
                AndroidDevDiagMonitor.__init__(self)
        
            def set_serial_port(self, phy_ser_name):
                """
                NOT USED: Compatability with DMCollector

                :param phy_ser_name: the serial port name (path)
                :type phy_ser_name: string
                """
                print "WARNING: Android version does not need to configure serial port"

            def set_baudrate(self, rate):
                """
                NOT USED: Compatability with DMCollector

                :param rate: the baudrate of the port
                :type rate: int
                """
                print "WARNING: Android version does not need to configure baudrate"
    elif chipset_type == ChipsetType.MTK:
        from android_muxraw_monitor import AndroidMuxrawMonitor
        class OnlineMonitor(AndroidMuxrawMonitor):
            def __init__(self):
                AndroidMuxrawMonitor.__init__(self)
        
            def set_serial_port(self, phy_ser_name):
                """
                NOT USED: Compatability with DMCollector

                :param phy_ser_name: the serial port name (path)
                :type phy_ser_name: string
                """
                print "WARNING: Android version does not need to configure serial port"

            def set_baudrate(self, rate):
                """
                NOT USED: Compatability with DMCollector

                :param rate: the baudrate of the port
                :type rate: int
                """
                print "WARNING: Android version does not need to configure baudrate"
    

except Exception as e:
    # import traceback
    # traceback.print_exc()

    # not used, but bugs may exist on laptop
    from dm_collector.dm_collector import DMCollector
    is_android = False

    class OnlineMonitor(DMCollector):
        def __init__(self):
            DMCollector.__init__(self)

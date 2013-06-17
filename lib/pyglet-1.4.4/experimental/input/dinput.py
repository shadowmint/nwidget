#!/usr/bin/python
# $Id:$

import ctypes

import pyglet
from pyglet import com
from pyglet.window.win32 import _kernel32

lib = ctypes.oledll.dinput8

LPVOID = ctypes.c_void_p
WORD = ctypes.c_uint16
DWORD = ctypes.c_uint32
LPDWORD = ctypes.POINTER(DWORD)
BOOL = ctypes.c_int
WCHAR = ctypes.c_wchar
UINT = ctypes.c_uint
HWND = ctypes.c_uint32
MAX_PATH = 260

DIENUM_STOP = 0
DIENUM_CONTINUE = 1

DIEDFL_ALLDEVICES = 0x00000000
DIEDFL_ATTACHEDONLY = 0x00000001
DIEDFL_FORCEFEEDBACK = 0x00000100
DIEDFL_INCLUDEALIASES = 0x00010000
DIEDFL_INCLUDEPHANTOMS = 0x00020000
DIEDFL_INCLUDEHIDDEN = 0x00040000

DI8DEVCLASS_ALL = 0
DI8DEVCLASS_DEVICE = 1
DI8DEVCLASS_POINTER = 2
DI8DEVCLASS_KEYBOARD = 3
DI8DEVCLASS_GAMECTRL = 4

DI8DEVTYPE_DEVICE = 0x11
DI8DEVTYPE_MOUSE = 0x12
DI8DEVTYPE_KEYBOARD = 0x13
DI8DEVTYPE_JOYSTICK = 0x14
DI8DEVTYPE_GAMEPAD = 0x15
DI8DEVTYPE_DRIVING = 0x16
DI8DEVTYPE_FLIGHT = 0x17
DI8DEVTYPE_1STPERSON = 0x18
DI8DEVTYPE_DEVICECTRL = 0x19
DI8DEVTYPE_SCREENPOINTER = 0x1A
DI8DEVTYPE_REMOTE = 0x1B
DI8DEVTYPE_SUPPLEMENTAL = 0x1C
DI8DEVTYPEMOUSE_UNKNOWN = 1
DI8DEVTYPEMOUSE_TRADITIONAL = 2
DI8DEVTYPEMOUSE_FINGERSTICK = 3
DI8DEVTYPEMOUSE_TOUCHPAD = 4
DI8DEVTYPEMOUSE_TRACKBALL = 5
DI8DEVTYPEMOUSE_ABSOLUTE = 6

DI8DEVTYPEKEYBOARD_UNKNOWN = 0
DI8DEVTYPEKEYBOARD_PCXT = 1
DI8DEVTYPEKEYBOARD_OLIVETTI = 2
DI8DEVTYPEKEYBOARD_PCAT = 3
DI8DEVTYPEKEYBOARD_PCENH = 4
DI8DEVTYPEKEYBOARD_NOKIA1050 = 5
DI8DEVTYPEKEYBOARD_NOKIA9140 = 6
DI8DEVTYPEKEYBOARD_NEC98 = 7
DI8DEVTYPEKEYBOARD_NEC98LAPTOP = 8
DI8DEVTYPEKEYBOARD_NEC98106 = 9
DI8DEVTYPEKEYBOARD_JAPAN106 = 10
DI8DEVTYPEKEYBOARD_JAPANAX = 11
DI8DEVTYPEKEYBOARD_J3100 = 12

DI8DEVTYPE_LIMITEDGAMESUBTYPE = 1

DI8DEVTYPEJOYSTICK_LIMITED = DI8DEVTYPE_LIMITEDGAMESUBTYPE
DI8DEVTYPEJOYSTICK_STANDARD = 2

DI8DEVTYPEGAMEPAD_LIMITED = DI8DEVTYPE_LIMITEDGAMESUBTYPE
DI8DEVTYPEGAMEPAD_STANDARD = 2
DI8DEVTYPEGAMEPAD_TILT = 3

DI8DEVTYPEDRIVING_LIMITED = DI8DEVTYPE_LIMITEDGAMESUBTYPE
DI8DEVTYPEDRIVING_COMBINEDPEDALS = 2
DI8DEVTYPEDRIVING_DUALPEDALS = 3
DI8DEVTYPEDRIVING_THREEPEDALS = 4
DI8DEVTYPEDRIVING_HANDHELD = 5

DI8DEVTYPEFLIGHT_LIMITED = DI8DEVTYPE_LIMITEDGAMESUBTYPE
DI8DEVTYPEFLIGHT_STICK = 2
DI8DEVTYPEFLIGHT_YOKE = 3
DI8DEVTYPEFLIGHT_RC = 4

DI8DEVTYPE1STPERSON_LIMITED = DI8DEVTYPE_LIMITEDGAMESUBTYPE
DI8DEVTYPE1STPERSON_UNKNOWN = 2
DI8DEVTYPE1STPERSON_SIXDOF = 3
DI8DEVTYPE1STPERSON_SHOOTER = 4

DI8DEVTYPESCREENPTR_UNKNOWN = 2
DI8DEVTYPESCREENPTR_LIGHTGUN = 3
DI8DEVTYPESCREENPTR_LIGHTPEN = 4
DI8DEVTYPESCREENPTR_TOUCH = 5

DI8DEVTYPEREMOTE_UNKNOWN = 2

DI8DEVTYPEDEVICECTRL_UNKNOWN = 2
DI8DEVTYPEDEVICECTRL_COMMSSELECTION = 3
DI8DEVTYPEDEVICECTRL_COMMSSELECTION_HARDWIRED = 4

DI8DEVTYPESUPPLEMENTAL_UNKNOWN = 2
DI8DEVTYPESUPPLEMENTAL_2NDHANDCONTROLLER = 3
DI8DEVTYPESUPPLEMENTAL_HEADTRACKER = 4
DI8DEVTYPESUPPLEMENTAL_HANDTRACKER = 5
DI8DEVTYPESUPPLEMENTAL_SHIFTSTICKGATE = 6
DI8DEVTYPESUPPLEMENTAL_SHIFTER = 7
DI8DEVTYPESUPPLEMENTAL_THROTTLE = 8
DI8DEVTYPESUPPLEMENTAL_SPLITTHROTTLE = 9
DI8DEVTYPESUPPLEMENTAL_COMBINEDPEDALS = 10
DI8DEVTYPESUPPLEMENTAL_DUALPEDALS = 11
DI8DEVTYPESUPPLEMENTAL_THREEPEDALS = 12
DI8DEVTYPESUPPLEMENTAL_RUDDERPEDALS = 13
DIDC_ATTACHED = 0x00000001
DIDC_POLLEDDEVICE = 0x00000002
DIDC_EMULATED = 0x00000004
DIDC_POLLEDDATAFORMAT = 0x00000008
DIDC_FORCEFEEDBACK = 0x00000100
DIDC_FFATTACK = 0x00000200
DIDC_FFFADE = 0x00000400
DIDC_SATURATION = 0x00000800
DIDC_POSNEGCOEFFICIENTS = 0x00001000
DIDC_POSNEGSATURATION = 0x00002000
DIDC_DEADBAND = 0x00004000
DIDC_STARTDELAY = 0x00008000
DIDC_ALIAS = 0x00010000
DIDC_PHANTOM = 0x00020000
DIDC_HIDDEN = 0x00040000

DIDFT_ALL = 0x00000000

DIDFT_RELAXIS = 0x00000001
DIDFT_ABSAXIS = 0x00000002
DIDFT_AXIS = 0x00000003

DIDFT_PSHBUTTON = 0x00000004
DIDFT_TGLBUTTON = 0x00000008
DIDFT_BUTTON = 0x0000000C

DIDFT_POV = 0x00000010
DIDFT_COLLECTION = 0x00000040
DIDFT_NODATA = 0x00000080

DIDFT_ANYINSTANCE = 0x00FFFF00
DIDFT_INSTANCEMASK = DIDFT_ANYINSTANCE
DIDFT_FFACTUATOR = 0x01000000
DIDFT_FFEFFECTTRIGGER = 0x02000000
DIDFT_OUTPUT = 0x10000000
DIDFT_VENDORDEFINED = 0x04000000
DIDFT_ALIAS = 0x08000000
DIDFT_OPTIONAL = 0x80000000

DIDFT_NOCOLLECTION = 0x00FFFF00

DIA_FORCEFEEDBACK = 0x00000001
DIA_APPMAPPED = 0x00000002
DIA_APPNOMAP = 0x00000004
DIA_NORANGE = 0x00000008
DIA_APPFIXED = 0x00000010

DIAH_UNMAPPED = 0x00000000
DIAH_USERCONFIG = 0x00000001
DIAH_APPREQUESTED = 0x00000002
DIAH_HWAPP = 0x00000004
DIAH_HWDEFAULT = 0x00000008
DIAH_DEFAULT = 0x00000020
DIAH_ERROR = 0x80000000
DIAFTS_NEWDEVICELOW = 0xFFFFFFFF
DIAFTS_NEWDEVICEHIGH = 0xFFFFFFFF
DIAFTS_UNUSEDDEVICELOW = 0x00000000
DIAFTS_UNUSEDDEVICEHIGH = 0x00000000

DIDBAM_DEFAULT = 0x00000000
DIDBAM_PRESERVE = 0x00000001
DIDBAM_INITIALIZE = 0x00000002
DIDBAM_HWDEFAULTS = 0x00000004

DIDSAM_DEFAULT = 0x00000000
DIDSAM_NOUSER = 0x00000001
DIDSAM_FORCESAVE = 0x00000002

DICD_DEFAULT = 0x00000000
DICD_EDIT = 0x00000001

DIDOI_FFACTUATOR = 0x00000001
DIDOI_FFEFFECTTRIGGER = 0x00000002
DIDOI_POLLED = 0x00008000
DIDOI_ASPECTPOSITION = 0x00000100
DIDOI_ASPECTVELOCITY = 0x00000200
DIDOI_ASPECTACCEL = 0x00000300
DIDOI_ASPECTFORCE = 0x00000400
DIDOI_ASPECTMASK = 0x00000F00
DIDOI_GUIDISUSAGE = 0x00010000

DIPH_DEVICE = 0
DIPH_BYOFFSET = 1
DIPH_BYID = 2
DIPH_BYUSAGE = 3

DISCL_EXCLUSIVE = 0x00000001
DISCL_NONEXCLUSIVE = 0x00000002
DISCL_FOREGROUND = 0x00000004
DISCL_BACKGROUND = 0x00000008
DISCL_NOWINKEY = 0x00000010

DIPROP_BUFFERSIZE = 1

class DIDEVICEINSTANCE(ctypes.Structure):
    _fields_ = (
        ('dwSize', DWORD),
        ('guidInstance', com.GUID),
        ('guidProduct', com.GUID),
        ('dwDevType', DWORD),
        ('tszInstanceName', WCHAR * MAX_PATH),
        ('tszProductName', WCHAR * MAX_PATH),
        ('guidFFDriver', com.GUID),
        ('wUsagePage', WORD),
        ('wUsage', WORD)
    )
LPDIDEVICEINSTANCE = ctypes.POINTER(DIDEVICEINSTANCE)
LPDIENUMDEVICESCALLBACK = ctypes.WINFUNCTYPE(BOOL, LPDIDEVICEINSTANCE, LPVOID)

class DIDEVICEOBJECTINSTANCE(ctypes.Structure):
    _fields_ = (    
        ('dwSize', DWORD),
        ('guidType', com.GUID),
        ('dwOfs', DWORD),
        ('dwType', DWORD),
        ('dwFlags', DWORD),
        ('tszName', WCHAR * MAX_PATH),
        ('dwFFMaxForce', DWORD),
        ('dwFFForceResolution', DWORD),
        ('wCollectionNumber', WORD),
        ('wDesignatorIndex', WORD),
        ('wUsagePage', WORD),
        ('wUsage', WORD),
        ('dwDimension', DWORD),
        ('wExponent', WORD),
        ('wReportId', WORD)
    )
LPDIDEVICEOBJECTINSTANCE = ctypes.POINTER(DIDEVICEOBJECTINSTANCE)
LPDIENUMDEVICEOBJECTSCALLBACK = \
    ctypes.WINFUNCTYPE( BOOL, LPDIDEVICEOBJECTINSTANCE, LPVOID)

class DIOBJECTDATAFORMAT(ctypes.Structure):
    _fields_ = (
        ('pguid', ctypes.POINTER(com.GUID)),
        ('dwOfs', DWORD),
        ('dwType', DWORD),
        ('dwFlags', DWORD)
    )
    __slots__ = [n for n, t in _fields_]
LPDIOBJECTDATAFORMAT = ctypes.POINTER(DIOBJECTDATAFORMAT)

class DIDATAFORMAT(ctypes.Structure):
    _fields_ = (
        ('dwSize', DWORD),
        ('dwObjSize', DWORD),
        ('dwFlags', DWORD),
        ('dwDataSize', DWORD),
        ('dwNumObjs', DWORD),
        ('rgodf', LPDIOBJECTDATAFORMAT)
    )
    __slots__ = [n for n, t in _fields_]
LPDIDATAFORMAT = ctypes.POINTER(DIDATAFORMAT)

class DIDEVICEOBJECTDATA(ctypes.Structure):
    _fields_ = (
        ('dwOfs', DWORD),
        ('dwData', DWORD),
        ('dwTimeStamp', DWORD),
        ('dwSequence', DWORD),
        ('uAppData', ctypes.POINTER(UINT))
    )
LPDIDEVICEOBJECTDATA = ctypes.POINTER(DIDEVICEOBJECTDATA)

class DIPROPHEADER(ctypes.Structure):
    _fields_ = (
        ('dwSize', DWORD),
        ('dwHeaderSize', DWORD),
        ('dwObj', DWORD),
        ('dwHow', DWORD)
    )
LPDIPROPHEADER = ctypes.POINTER(DIPROPHEADER)

class DIPROPDWORD(ctypes.Structure):
    _fields_ = (
        ('diph', DIPROPHEADER),
        ('dwData', DWORD)
    )

# All method names in the interfaces are filled in, but unused (so far)
# methods have no parameters.. they'll crash when we try and use them, at
# which point we can go in and fill them in.

# IDirect* interfaces are all Unicode (e.g. IDirectInputDevice8W).

class IDirectInputDevice8(com.IUnknown):
    _methods_ = [
        ('GetCapabilities',
         com.STDMETHOD()),
        ('EnumObjects',
         com.STDMETHOD(LPDIENUMDEVICEOBJECTSCALLBACK, LPVOID, DWORD)),
        ('GetProperty',
         com.STDMETHOD()),
        ('SetProperty',
         com.STDMETHOD(LPVOID, LPDIPROPHEADER)),
        ('Acquire',
         com.STDMETHOD()),
        ('Unacquire',
         com.STDMETHOD()),
        ('GetDeviceState',
         com.STDMETHOD()),
        ('GetDeviceData',
         com.STDMETHOD(DWORD, LPDIDEVICEOBJECTDATA, LPDWORD, DWORD)),
        ('SetDataFormat',
         com.STDMETHOD(LPDIDATAFORMAT)),
        ('SetEventNotification',
         com.STDMETHOD()),
        ('SetCooperativeLevel',
         com.STDMETHOD(HWND, DWORD)),
        ('GetObjectInfo',
         com.STDMETHOD()),
        ('GetDeviceInfo',
         com.STDMETHOD()),
        ('RunControlPanel',
         com.STDMETHOD()),
        ('Initialize',
         com.STDMETHOD()),
        ('CreateEffect',
         com.STDMETHOD()),
        ('EnumEffects',
         com.STDMETHOD()),
        ('GetEffectInfo',
         com.STDMETHOD()),
        ('GetForceFeedbackState',
         com.STDMETHOD()),
        ('SendForceFeedbackCommand',
         com.STDMETHOD()),
        ('EnumCreatedEffectObjects',
         com.STDMETHOD()),
        ('Escape',
         com.STDMETHOD()),
        ('Poll',
         com.STDMETHOD()),
        ('SendDeviceData',
         com.STDMETHOD()),
        ('EnumEffectsInFile',
         com.STDMETHOD()),
        ('WriteEffectToFile',
         com.STDMETHOD()),
        ('BuildActionMap',
         com.STDMETHOD()),
        ('SetActionMap',
         com.STDMETHOD()),
        ('GetImageInfo',
         com.STDMETHOD()),
     ]

class IDirectInput8(com.IUnknown):
    _methods_ = [
        ('CreateDevice',
         com.STDMETHOD(ctypes.POINTER(com.GUID), 
                       ctypes.POINTER(IDirectInputDevice8),
                       ctypes.c_void_p)),
        ('EnumDevices',
         com.STDMETHOD(DWORD, LPDIENUMDEVICESCALLBACK, LPVOID, DWORD)),
        ('GetDeviceStatus',
         com.STDMETHOD()),
        ('RunControlPanel',
         com.STDMETHOD()),
        ('Initialize',
         com.STDMETHOD()),
        ('FindDevice',
         com.STDMETHOD()),
        ('EnumDevicesBySemantics',
         com.STDMETHOD()),
        ('ConfigureDevices',
         com.STDMETHOD()),
    ]

IID_IDirectInput8W = \
    com.GUID(0xBF798031,0x483A,0x4DA2,0xAA,0x99,0x5D,0x64,0xED,0x36,0x97,0x00)

lib.DirectInput8Create.argtypes = \
    (ctypes.c_void_p, DWORD, com.LPGUID, ctypes.c_void_p, ctypes.c_void_p)

class Element(object):
    value = None
    def __init__(self, object_instance):
        self.name = object_instance.tszName
        self._flags = object_instance.dwFlags
        self._guid = object_instance.guidType
        self._type = object_instance.dwType

    def get_value(self):
        return self.value
        
class Device(object):
    def __init__(self, device, device_instance):
        self.name = device_instance.tszInstanceName
        #print self.name, hex(device_instance.dwDevType & 0xff), \
        #                hex(device_instance.dwDevType & 0xff00)
        #print hex(device_instance.wUsagePage), hex(device_instance.wUsage)

        self._device = device
        self._init_elements()
        self._set_format()

    def _init_elements(self):
        self.elements = []
        self._device.EnumObjects(
            LPDIENUMDEVICEOBJECTSCALLBACK(self._object_enum), None, DIDFT_ALL)

    def _object_enum(self, object_instance, arg):
        type = object_instance.contents.dwType
        flags = object_instance.contents.dwFlags
        if type & DIDFT_NODATA:
            return DIENUM_CONTINUE

        element = Element(object_instance.contents)
        self.elements.append(element)        
        return DIENUM_CONTINUE

    def _set_format(self):
        if not self.elements:
            return

        object_formats = (DIOBJECTDATAFORMAT * len(self.elements))()
        offset = 0
        for object_format, element in zip(object_formats, self.elements):
            object_format.dwOfs = offset
            object_format.dwType = element._type
            offset += 4
             
        format = DIDATAFORMAT()
        format.dwSize = ctypes.sizeof(format)
        format.dwObjSize = ctypes.sizeof(DIOBJECTDATAFORMAT)
        format.dwFlags = 0
        format.dwDataSize = offset
        format.dwNumObjs = len(object_formats)
        format.rgodf = ctypes.cast(ctypes.pointer(object_formats),
                                   LPDIOBJECTDATAFORMAT)
        self._device.SetDataFormat(format)

        prop = DIPROPDWORD()
        prop.diph.dwSize = ctypes.sizeof(prop)
        prop.diph.dwHeaderSize = ctypes.sizeof(prop.diph)
        prop.diph.dwObj = 0
        prop.diph.dwHow = DIPH_DEVICE
        prop.dwData = 64 * ctypes.sizeof(DIDATAFORMAT)
        self._device.SetProperty(DIPROP_BUFFERSIZE, ctypes.byref(prop.diph))

    def open(self, window=None):
        if not self.elements:
            return

        if window is None:
            # Pick any open window, or the shadow window if no windows
            # have been created yet.
            window = pyglet.gl._shadow_window
            for window in pyglet.app.windows:
                break

        self._device.SetCooperativeLevel(window._hwnd, 
            DISCL_BACKGROUND | DISCL_NONEXCLUSIVE)
        self._device.Acquire()
        
        # XXX HACK
        pyglet.clock.schedule(self.dispatch_events)

    def close(self):
        if not self.elements:
            return

        self._device.Unacquire()

    # XXX HACK?
    def dispatch_events(self, dt): # dt HACK
        if not self.elements:
            return
        
        events = (DIDEVICEOBJECTDATA * 64)()
        n_events = DWORD(len(events))
        self._device.GetDeviceData(ctypes.sizeof(DIDEVICEOBJECTDATA),
                                   ctypes.cast(ctypes.pointer(events), 
                                               LPDIDEVICEOBJECTDATA),
                                   ctypes.byref(n_events),
                                   0)
        for event in events[:n_events.value]:
            index = event.dwOfs // 4
            self.elements[index].value = event.dwData

def _device_enum(device_instance, arg):
    device = IDirectInputDevice8()
    dinput.CreateDevice(device_instance.contents.guidInstance,
                        ctypes.byref(device),
                        None)
    _devices.append(Device(device, device_instance.contents))
    
    return DIENUM_CONTINUE

def get_devices():
    global _devices
    _devices = []
    dinput.EnumDevices(DI8DEVCLASS_ALL, LPDIENUMDEVICESCALLBACK(_device_enum), 
                       None, DIEDFL_ATTACHEDONLY)
    return _devices

def _init_directinput():
    global dinput
    dinput = IDirectInput8()
    module = _kernel32.GetModuleHandleW(None)
    DIRECTINPUT_VERSION = 0x0800
    lib.DirectInput8Create(module, DIRECTINPUT_VERSION,
                           IID_IDirectInput8W, ctypes.byref(dinput), None)

_init_directinput()
'''
#for device in get_devices():
device = get_devices()[0]
device.open(w)
print device.name

pyglet.app.run()
'''

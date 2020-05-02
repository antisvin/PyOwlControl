from enum import IntEnum, auto


class Midi(object):
    class Sysex(object):
        Start        = 0xf0
        Manufacturer = 0x7d
        Device       = 0x52
        OwlDevice    = 0x20
        Version      = 0x03
        End          = 0xf7

        @classmethod
        def getHeader(cls):
            return [cls.Start, cls.Manufacturer, cls.Device]


class PatchParameterId(IntEnum):
    PARAMETER_A = 0
    PARAMETER_B = auto()
    PARAMETER_C = auto()
    PARAMETER_D = auto()
    PARAMETER_E = auto()
    PARAMETER_F = auto()
    PARAMETER_G = auto()
    PARAMETER_H = auto()
    PARAMETER_AA = auto()
    PARAMETER_AB = auto()
    PARAMETER_AC = auto()
    PARAMETER_AD = auto()
    PARAMETER_AE = auto()
    PARAMETER_AF = auto()
    PARAMETER_AG = auto()
    PARAMETER_AH = auto()
    PARAMETER_BA = auto()
    PARAMETER_BB = auto()
    PARAMETER_BC = auto()
    PARAMETER_BD = auto()
    PARAMETER_BE = auto()
    PARAMETER_BF = auto()
    PARAMETER_BG = auto()
    PARAMETER_BH = auto()
    PARAMETER_CA = auto()
    PARAMETER_CB = auto()
    PARAMETER_CC = auto()
    PARAMETER_CD = auto()
    PARAMETER_CE = auto()
    PARAMETER_CF = auto()
    PARAMETER_CG = auto()
    PARAMETER_CH = auto()
    PARAMETER_DA = auto()
    PARAMETER_DB = auto()
    PARAMETER_DC = auto()
    PARAMETER_DD = auto()
    PARAMETER_DE = auto()
    PARAMETER_DF = auto()
    PARAMETER_DG = auto()
    PARAMETER_DH = auto()


class PatchButtonId(IntEnum):
    BYPASS_BUTTON = 0
    PUSHBUTTON = auto()
    GREEN_BUTTON = auto()
    RED_BUTTON = auto()
    BUTTON_A = auto()
    BUTTON_B = auto()
    BUTTON_C = auto()
    BUTTON_D = auto()
    BUTTON_E = auto()
    BUTTON_F = auto()
    BUTTON_G = auto()
    BUTTON_H = auto()
    GATE_BUTTON = 0x7f
    MIDI_NOTE_BUTTON = 0x80


class Sysex(object):
    class Confinguration(object):
        AudioRate         = "FS"
        Bitdepth          = "BD"
        Dataformat        = "DF"
        Blocksize         = "BS"
        Swap              = "SW"
        Bypass            = "BY"
        InputGain         = "IG"
        OutputGain        = "OG"
        PcButton          = "PC"
        InputOffset       = "IO"
        InputScalar       = "IS"
        OutputOffset      = "OO"
        OutputScalar      = "OS"
        MidiInputChannel  = "MI"
        MidiOutputChannel = "MO"
        BusEnable         = "BE"
        BusForwardMidi    = "BM"


class OpenWareMidiSysexCommand(IntEnum):
    SYSEX_PRESET_NAME_COMMAND       = 0x01
    SYSEX_PARAMETER_NAME_COMMAND    = 0x02
    SYSEX_CONFIGURATION_COMMAND     = 0x03
    SYSEX_DEVICE_RESET_COMMAND      = 0x7d
    SYSEX_BOOTLOADER_COMMAND        = 0x7e
    SYSEX_FIRMWARE_UPLOAD           = 0x10
    SYSEX_FIRMWARE_STORE            = 0x11
    SYSEX_FIRMWARE_RUN              = 0x12
    SYSEX_FIRMWARE_FLASH            = 0x13
    SYSEX_FLASH_ERASE               = 0x14
    SYSEX_SETTINGS_RESET            = 0x15
    SYSEX_SETTINGS_STORE            = 0x16
    SYSEX_FIRMWARE_VERSION          = 0x20
    SYSEX_DEVICE_ID                 = 0x21
    SYSEX_PROGRAM_MESSAGE           = 0x22
    SYSEX_DEVICE_STATS              = 0x23
    SYSEX_PROGRAM_STATS             = 0x24
    SYSEX_PROGRAM_ERROR             = 0x30


class OpenWareMidiControl(IntEnum):
    PATCH_PARAMETER_A      = 20 # Parameter A
    PATCH_PARAMETER_B      = 21 # Parameter B
    PATCH_PARAMETER_C      = 22 # Parameter C
    PATCH_PARAMETER_D      = 23 # Parameter D
    PATCH_PARAMETER_E      = 24 # Expression pedal / input
    PATCH_PARAMETER_F      = 1  # Extended parameter Modulation
    PATCH_PARAMETER_G      = 12 # Extended parameter Effect Ctrl 1
    PATCH_PARAMETER_H      = 13 # Extended parameter Effect Ctrl 2

    PATCH_BUTTON           = 25 # LED Pushbutton: 0=not pressed, 127=pressed
    PATCH_CONTROL          = 26 # Remote control: 0=local, 127=MIDI
    LED                    = 30 # set/get LED value:
                                #  * 0-41 = off
                                #  * 42-83 = green
                                #  * 84-127 = red

    LEFT_INPUT_GAIN        = 32 # left channel input gain, -34.5dB to +12dB (92 = 0dB)
    RIGHT_INPUT_GAIN       = 33
    LEFT_OUTPUT_GAIN       = 34 # left channel output gain, -73dB to +6dB (121 = 0dB)
    RIGHT_OUTPUT_GAIN      = 35
    LEFT_INPUT_MUTE        = 36 # mute left input (127=muted)
    RIGHT_INPUT_MUTE       = 37
    LEFT_OUTPUT_MUTE       = 38 # mute left output (127=muted)
    RIGHT_OUTPUT_MUTE      = 39
    BYPASS                 = 40 # codec bypass mode (127=bypass)
    REQUEST_SETTINGS       = 67 # load settings from device (127=all settings) (30 for LED) (more to come)
    SAVE_SETTINGS          = 68 # save settings to device
    FACTORY_RESET          = 70 # reset all settings
    DEVICE_STATUS          = 71

    PATCH_PARAMETER_AA     = 75
    PATCH_PARAMETER_AB     = 76
    PATCH_PARAMETER_AC     = 77
    PATCH_PARAMETER_AD     = 78
    PATCH_PARAMETER_AE     = 79
    PATCH_PARAMETER_AF     = 80
    PATCH_PARAMETER_AG     = 81
    PATCH_PARAMETER_AH     = 82
    PATCH_PARAMETER_BA     = 83
    PATCH_PARAMETER_BB     = 84
    PATCH_PARAMETER_BC     = 85
    PATCH_PARAMETER_BD     = 86
    PATCH_PARAMETER_BE     = 87
    PATCH_PARAMETER_BF     = 88
    PATCH_PARAMETER_BG     = 89
    PATCH_PARAMETER_BH     = 90
    PATCH_PARAMETER_CA     = 91
    PATCH_PARAMETER_CB     = 92
    PATCH_PARAMETER_CC     = 93
    PATCH_PARAMETER_CD     = 94
    PATCH_PARAMETER_CE     = 95
    PATCH_PARAMETER_CF     = 96
    PATCH_PARAMETER_CG     = 97
    PATCH_PARAMETER_CH     = 98
    PATCH_PARAMETER_DA     = 99
    PATCH_PARAMETER_DB     = 100
    PATCH_PARAMETER_DC     = 101
    PATCH_PARAMETER_DD     = 102
    PATCH_PARAMETER_DE     = 103
    PATCH_PARAMETER_DF     = 104
    PATCH_PARAMETER_DG     = 105
    PATCH_PARAMETER_DH     = 106

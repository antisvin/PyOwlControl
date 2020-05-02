import array
import sys
import pygame.midi
import open_ware_midi_control as owmc
from typing import List, Tuple, Union


class MidiDevice(object):
    def __init__(
            self, id: int, interf: bytes, name: bytes, input: int, output: int, opened: int):
        self.id = id
        enc = sys.getdefaultencoding()
        self.interf = interf.decode(encoding=enc)
        self.name = name.decode(encoding=enc)
        self.input = bool(input)
        self.output = bool(output)
        self.opened = bool(opened)
        if self.input:
            self.device = pygame.midi.Input(self.id)
        else:
            self.device = pygame.midi.Output(self.id)

    def isOwlDevice(self) -> bool:
        return 'OWL-MIDI' in self.name

    def sendCommand(self, command, *args):
        sysex = owmc.Midi.Sysex.getHeader()
        #f0 7d 52 7e f7
        arg = int(command)
        sysex.append(arg & 0xff)
        if args:
            sysex.append(len(args))
            for arg in args:
                if isinstance(arg, str):
                    sysex.extend(ord(c) for c in str)
                elif isintace(arg, int):
                    sysex.append(arg & 0xff)
        sysex.append(owmc.Midi.Sysex.End)
        print(sysex)
        self.device.write_sys_ex(0, sysex)

    def sendMidiCc(
            self, cc: owmc.OpenWareMidiControl,
            value: Union[int, owmc.OpenWareMidiControl]):
        self.device.write_short(0xb0, cc, value)
        print(f'Send {cc} = {value}')

    def receiveResponse(self):
        if self.device.poll():
            return self.device.read(1)


class MidiParser(object):
    """
    This class is based on generators that exhaust input data stream
    """
    def parse_midi(self, data: List[int]):
        """
        Process MIDI - main entrance point

        We only handle Sysex for now
        """
        while data:
            first = data.pop(0)
            if first == owmc.Midi.Sysex.Start:
                yield from self.parse_sysex(data)

    def parse_sysex(self, data: List[int]):
        """
        Process Sysex data
        """
        manufacturer = data.pop(0)
        if manufacturer != owmc.Midi.Sysex.Manufacturer:
            return

        owl_device = data.pop(0)
        if owl_device != owmc.Midi.Sysex.OwlDevice:
            return

        cmd = data.pop(0)
        if cmd == owmc.OpenWareMidiSysexCommand.SYSEX_DEVICE_ID:
            yield from self.parse_sysex_device_id(data)

    def parse_sysex_device_id(self, data: List[int]) -> str:
        """
        Parse device ID command response
        """
        arr = array.array('B')
        arr.fromlist([data.pop(0) for i in range(26)])
        id = arr.tobytes().decode()
        if data.pop(0) == owmc.Midi.Sysex.End and data.pop(0) == 0:
            yield id


class MidiController(object):
    def __init__(self):
        self.input_device = None
        self.output_device = None

    def reset(self):
        if self.input_device:
            self.input_device.device.close()
            self.input_device = None
        if self.output_device:
            self.output_device.device.close()
            self.output_device = None

    def searchForDevices(self) -> Tuple[List[MidiDevice], List[MidiDevice]]:
        pygame.midi.quit()
        pygame.midi.init()

        input_devices = []
        output_devices = []
        for i in range(pygame.midi.get_count()):
            device = MidiDevice(i, *pygame.midi.get_device_info(i))
            if device.isOwlDevice():
                if device.input:
                    input_devices.append(device)
                if device.output:
                    output_devices.append(device)
        return input_devices, output_devices

    def setInput(self, device: MidiDevice):
        self.input_device = device

    def setOutput(self, device: MidiDevice):
        self.output_device = device

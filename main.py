# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget, QListWidgetItem
from PySide2.QtCore import QFile, Qt, QTimer
from PySide2.QtUiTools import QUiLoader

import midi
import open_ware_midi_control as owmc



class PyOwlControl(QWidget):
    def __init__(self, midi_controller: midi.MidiController):
        super(PyOwlControl, self).__init__()
        self.ui = None
        self.midi_in_selected = False
        self.midi_out_selected = False
        self.loadUi()
        self.midi_controller = midi_controller
        self.midi_inputs = []
        self.midi_outputs = []
        self.midi_parser = midi.MidiParser()
        self.searchMidi()

        self.timer = QTimer()
        self.timer.timeout.connect(self.pollMidi)
        self.timer.start(1000)

        self.ui.cmdBootloader.clicked.connect(self.sendCmdBootloader)
        self.ui.cmdDeviceId.clicked.connect(self.sendCmdDeviceId)

    def loadUi(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.ui.searchButton.clicked.connect(self.searchMidi)
        self.ui.inputDevicesList.itemSelectionChanged.connect(
            self.selectMidiInput)
        self.ui.outputDevicesList.itemSelectionChanged.connect(
            self.selectMidiOutput)

    def pollMidi(self):
        if self.midi_controller.input_device:
            buf = []
            while True:
                response = self.midi_controller.input_device.receiveResponse()
                if response:
                    buf.extend(response[0][0])
                else:
                    break
            # Parse response
            if buf:
                results = [result for result in self.midi_parser.parse_midi(buf)]
                self.addLog(f'Received MIDI result: {results}')
            else:
                self.addLog('No response')
        else:
            self.addLog('No device')

    def sendCmdDeviceId(self):
        if self.midi_controller.output_device:
            self.midi_controller.output_device.sendMidiCc(
                owmc.OpenWareMidiControl.REQUEST_SETTINGS,
                owmc.OpenWareMidiSysexCommand.SYSEX_DEVICE_ID)

    def sendCmdBootloader(self):
        if self.midi_controller.output_device:
            self.midi_controller.output_device.sendCommand(
                owmc.OpenWareMidiSysexCommand.SYSEX_BOOTLOADER_COMMAND)

    def searchMidi(self):
        self.addLog('Searching for OWL MIDI devices...')
        self.ui.inputDevicesList.clear()
        self.ui.outputDevicesList.clear()
        self.midi_controller.reset()
        self.midi_inputs, self.midi_outputs = \
            midi_controller.searchForDevices()

        # List MIDI inputs
        if self.midi_inputs:
            for i, input_device in enumerate(self.midi_inputs):
                self.addLog(f'Found input device: {input_device.name}')
                item = QListWidgetItem(input_device.name)
                item.setData(Qt.UserRole, input_device)
                self.ui.inputDevicesList.addItem(item)
                if not self.midi_in_selected and i == 0:
                    self.midi_in_selected = True
                    self.ui.inputDevicesList.item(0).setSelected(True)

        else:
            self.addLog('No input devices found')
            self.ui.inputDevicesList.addItem('-- no devices found --')
            item = self.ui.inputDevicesList.item(0)
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)

        # List MIDI outputs
        if self.midi_outputs:
            for output_device in self.midi_outputs:
                self.addLog(f'Found output device: {output_device.name}')
                item = QListWidgetItem(output_device.name)
                item.setData(Qt.UserRole, output_device)
                self.ui.outputDevicesList.addItem(item)
                if not self.midi_out_selected and i == 0:
                    self.midi_out_selected = True
                    self.ui.outputDevicesList.item(0).setSelected(True)
        else:
            self.addLog('No output devices found')
            self.ui.outputDevicesList.addItem('-- no devices found --')
            item = self.ui.outputDevicesList.item(0)
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)

    def selectMidiInput(self):
        item = self.ui.inputDevicesList.selectedItems()[0].data(Qt.UserRole)
        self.midi_controller.setInput(item)
        self.addLog(f'MIDI input #{item.id} selected')

    def selectMidiOutput(self):
        item = self.ui.outputDevicesList.selectedItems()[0].data(Qt.UserRole)
        self.midi_controller.setOutput(item)
        self.addLog(f'MIDI output #{item.id} selected')

    def addLog(self, message):
        self.ui.logText.append(message)


if __name__ == "__main__":
    midi_controller = midi.MidiController()
    app = QApplication([])
    widget = PyOwlControl(midi_controller)
    widget.show()
    sys.exit(app.exec_())

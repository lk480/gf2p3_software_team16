"""Implement the graphical user interface for the Logic Simulator.

Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.

Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
Gui - configures the main window and all the widgets.
"""
import wx
import wx.glcanvas as wxcanvas
from OpenGL import GL, GLUT

"""
from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser
"""


class MyGLCanvas(wxcanvas.GLCanvas):
    """Handle all drawing operations.

    This class contains functions for drawing onto the canvas. It
    also contains handlers for events relating to the canvas.

    Parameters
    ----------
    parent: parent window.
    devices: instance of the devices.Devices() class.
    monitors: instance of the monitors.Monitors() class.

    Public methods
    --------------
    init_gl(self): Configures the OpenGL context.

    render(self, text): Handles all drawing operations.

    on_paint(self, event): Handles the paint event.

    on_size(self, event): Handles the canvas resize event.

    on_mouse(self, event): Handles mouse events.

    render_text(self, text, x_pos, y_pos): Handles text drawing
                                           operations.
    """

    def __init__(self, parent, devices, monitors):
        """Initialise canvas properties and useful variables."""
        super().__init__(
            parent,
            -1,
            attribList=[
                wxcanvas.WX_GL_RGBA,
                wxcanvas.WX_GL_DOUBLEBUFFER,
                wxcanvas.WX_GL_DEPTH_SIZE,
                16,
                0,
            ],
        )
        GLUT.glutInit()
        self.init = False
        self.context = wxcanvas.GLContext(self)

        # Initialise variables for panning
        self.pan_x = 0
        self.pan_y = 0
        self.last_mouse_x = 0  # previous mouse x position
        self.last_mouse_y = 0  # previous mouse y position

        # Initialise variables for zooming
        self.zoom = 1

        # Bind events to the canvas
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)

        # Colours
        self.BLACK = (0.0, 0.0, 0.0)
        self.WHITE = (1.0, 1.0, 1.0)
        self.RED = (1.0, 0.0, 0.0)
        self.GREEN = (0.0, 1.0, 0.0)
        self.BLUE = (0.0, 0.0, 1.0)
        self.colours = [self.WHITE, self.RED, self.GREEN, self.BLUE]
        self.signals_list = []

        self.BG_WHITE = (1.0, 1.0, 1.0)
        self.BG_BLACK = (0.20, 0.20, 0.20)
        self.BG_COLOUR = self.BG_BLACK

    def init_gl(self):
        """Configure and initialise the OpenGL context."""

        size = self.GetClientSize()
        self.SetCurrent(self.context)
        GL.glDrawBuffer(GL.GL_BACK)
        GL.glClearColor(self.BG_COLOUR[0], self.BG_COLOUR[1], self.BG_COLOUR[2], 1.0)
        GL.glViewport(0, 0, size.width, size.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, size.width, 0, size.height, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslated(self.pan_x, self.pan_y, 0.0)
        GL.glScaled(self.zoom, self.zoom, self.zoom)

    def set_dark_mode(self):
        GL.glClearColor(self.BG_BLACK[0], self.BG_BLACK[1], self.BG_BLACK[2], 1.0)
        self.colours[0] = self.WHITE

    def set_light_mode(self):
        GL.glClearColor(self.BG_WHITE[0], self.BG_WHITE[1], self.BG_WHITE[2], 1.0)
        self.colours[0] = self.BLACK

    def draw_trace(self, signal, colour, position):
        """Draw a trace for a given signal."""
        GL.glColor3f(colour[0], colour[1], colour[2])
        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range(len(signal)):
            x = (i * 50) + 30
            x_next = (i * 50) + 80
            y = 450 + 50 * int(signal[i]) - 90 * position
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next, y)
        GL.glEnd()
        self.draw_markers(signal, position)

    def draw_markers(self, signal, position):
        GL.glColor3f(0.5, 0.5, 0.5)

        for i in range(len(signal) + 1):
            GL.glBegin(GL.GL_LINE_STRIP)
            x = (i * 50) + 30
            y = 450 - 5 - 90 * position
            y_next = 450 - 15 - 90 * position
            GL.glVertex2f(x, y)
            GL.glVertex2f(x, y_next)
            GL.glEnd()

    def render_signals(self):
        """Render all the signals and labels."""
        for i in range(len(self.signals_list)):
            self.draw_trace(self.signals_list[i][1], self.colours[i % 4], i)
            self.render_text(self.signals_list[i][0], 10, 470 - 90 * i)

    def render(self, signals_list):
        """Handle all drawing operations."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # Draw specified text at position (10, 10)

        # Draw a sample signal trace

        if signals_list is not None:
            self.signals_list = signals_list
        self.render_signals()

        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def on_paint(self, event):
        """Handle the paint event."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        self.render(self.signals_list)

    def on_size(self, event):
        """Handle the canvas resize event."""
        # Forces reconfiguration of the viewport, modelview and projection
        # matrices on the next paint event
        self.init = False

    def on_mouse(self, event):
        """Handle mouse events."""

        # Calculate object coordinates of the mouse position
        size = self.GetClientSize()
        ox = (event.GetX() - self.pan_x) / self.zoom
        oy = (size.height - event.GetY() - self.pan_y) / self.zoom
        old_zoom = self.zoom
        if event.ButtonDown():
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
        if event.Dragging():
            self.pan_x += event.GetX() - self.last_mouse_x
            self.pan_y -= event.GetY() - self.last_mouse_y
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False
        if event.GetWheelRotation() < 0:
            self.zoom *= 1.0 + (event.GetWheelRotation() / (10 * event.GetWheelDelta()))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
        if event.GetWheelRotation() > 0:
            self.zoom /= 1.0 - (event.GetWheelRotation() / (10 * event.GetWheelDelta()))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
        self.render(self.signals_list)
        self.Refresh()  # triggers the paint event

    def render_text(self, text, x_pos, y_pos):
        """Handle text drawing operations."""
        GL.glColor3f(0.0, 0.0, 0.0)  # text is black
        GL.glRasterPos2f(x_pos, y_pos)
        font = GLUT.GLUT_BITMAP_HELVETICA_12

        for character in text:
            if character == "\n":
                y_pos = y_pos - 20
                GL.glRasterPos2f(x_pos, y_pos)
            else:
                GLUT.glutBitmapCharacter(font, ord(character))


class Gui(wx.Frame):
    """Configure the main window and all the widgets.

    This class provides a graphical user interface for the Logic Simulator and
    enables the user to change the circuit properties and run simulations.

    Parameters
    ----------
    title: title of the window.

    Public methods
    --------------
    on_menu(self, event): Event handler for the file menu.

    on_spin(self, event): Event handler for when the user changes the spin
                           control value.

    on_run_button(self, event): Event handler for when the user clicks the run
                                button.

    on_text_box(self, event): Event handler for when the user enters text.
    """

    def __init__(self, title, path, names, devices, network, monitors):
        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(800, 600))

        self.names = names
        self.devices = devices
        self.monitors = monitors
        self.network = network

        self.cycle_count = 16

        self.devices_list = self.set_up_devices(devices, names)

        self.signals_list = self.gather_signal_data(devices, names, self.cycle_count)

        # Configure the file menu
        # Initialise menus and bar
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()

        # Add items to the file and help menus
        fileMenu.Append(wx.ID_ABOUT, "&About")
        fileMenu.Append(wx.ID_FILE1, "&Import")
        fileMenu.Append(wx.ID_FILE2, "&Export")
        helpMenu.Append(wx.ID_HELP, "&Tutorial")
        fileMenu.Append(wx.ID_EXIT, "&Exit")

        self.dark_mode_flag = True

        # Add the file and help menus to the menu bar and set bar
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)

        self.current_device = len(self.devices_list) + 2

        # Canvas for drawing signals
        self.canvas = MyGLCanvas(self, devices, monitors)

        # Set up help menu text
        self.HELP_TEXT = "HELP ME"

        # Configure the widgets
        self.cycles_text = wx.StaticText(self, wx.ID_ANY, "Cycles")
        self.cycles_spin = wx.SpinCtrl(
            self, wx.ID_ANY, "16", style=wx.ALIGN_CENTER_HORIZONTAL | wx.TE_CENTER
        )
        self.run_button = wx.Button(self, wx.ID_ANY, "Run")
        self.stop_button = wx.Button(self, wx.ID_ANY, "Stop")
        self.devices_text = wx.StaticText(self, wx.ID_ANY, "No device selected \n \n")
        font = wx.Font(
            18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )
        self.devices_text.SetFont(font)
        self.devices_spin_button = wx.SpinButton(
            self, wx.ID_ANY, style=wx.SP_HORIZONTAL, name="Current device"
        )
        self.dark_mode_button = wx.Button(self, wx.ID_ANY, "Light mode")
        self.device_scroll = wx.ScrolledWindow(self, wx.ID_ANY, style=wx.VSCROLL)

        # Create a sizer for the device scroll panel
        device_sizer = wx.BoxSizer(wx.VERTICAL)

        # Add devices to the sizer
        for device in self.devices_list:
            device_text = wx.StaticText(self.device_scroll, label=device[0])
            device_sizer.Add(device_text, 0, wx.ALL, 5)

        # Set the sizer for the device scroll panel
        self.device_scroll.SetSizer(device_sizer)
        self.device_scroll.Layout()
        self.device_scroll.SetScrollRate(0, 20)

        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.cycles_spin.Bind(wx.EVT_SPINCTRL, self.on_spin_cycles)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop_button)
        self.devices_spin_button.Bind(wx.EVT_SPIN, self.on_spin_devices)
        self.dark_mode_button.Bind(wx.EVT_BUTTON, self.on_toggle_dark_mode)

        # Set spin range and initialise flag for first run
        self.devices_spin_button.SetRange(-1, len(self.devices_list))
        self.no_devices = True

        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer = wx.BoxSizer(wx.VERTICAL)

        # Add widgets to sizers
        main_sizer.Add(self.canvas, 50, wx.EXPAND | wx.ALL, 5)

        side_sizer.Add(self.cycles_text, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)
        side_sizer.Add(self.cycles_spin, 1, wx.ALL | wx.EXPAND, 5)
        side_sizer.Add(self.run_button, 3, wx.ALL | wx.EXPAND, 5)
        side_sizer.Add(self.stop_button, 3, wx.ALL | wx.EXPAND, 5)
        side_sizer.Add(self.devices_spin_button, 10, wx.ALL | wx.EXPAND, 5)
        side_sizer.Add(self.devices_text, 3, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        side_sizer.Add(self.device_scroll, 10, wx.ALL | wx.EXPAND, 5)

        # Add side_sizer to main_sizer as the last item
        main_sizer.Add(side_sizer, 10, wx.ALL | wx.EXPAND, 5)
        side_sizer.Add(self.dark_mode_button, 1, wx.BOTTOM | wx.EXPAND, 5)

        # Set the sizer and configure the window
        # self.SetSizeHints(600, 600)
        self.Maximize(True)
        self.SetSizer(main_sizer)

    def set_up_devices(self, devices, names):
        devices_list = []
        for device in devices.devices_list:
            single_device_list = []
            id = device.device_id
            single_device_list.append(names.get_name_string(id))
            single_device_list.append(self.device_number_to_string(device.device_kind))
            single_device_list.append(devices.return_property(id))

            devices_list.append(single_device_list)

        return devices_list

    def gather_signal_data(self, devices, names, cycle_count):
        signals_list = []
        self.run(cycle_count)
        for item in self.monitors.monitors_dictionary.items():
            single_signal = []
            single_signal.append(names.get_name_string(item[0][0]))
            single_signal.append(item[1])
            signals_list.append(single_signal)

        return signals_list

    def run(self, cycles):
        self.monitors.reset_monitors()
        self.devices.cold_startup()
        for _ in range(cycles):
            if self.network.execute_network():
                self.monitors.record_signals()

    def device_number_to_string(self, device_number):
        if device_number == 2:
            return "NAND"
        elif device_number == 5:
            return "CLOCK"
        elif device_number == 6:
            return "SWITCH"
        elif device_number == 7:
            return "DTYPE"
        else:
            return str(device_number)

    # Event handlers
    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)
        if Id == wx.ID_ABOUT:
            wx.MessageBox(
                "Logic Simulator\nCreated by Mojisola Agboola\n2017",
                "About Logsim",
                wx.ICON_INFORMATION | wx.OK,
            )
        if Id == wx.ID_HELP:
            wx.MessageBox(
                self.HELP_TEXT,
                "HELP BOX",
                wx.ICON_INFORMATION | wx.OK,
            )

        # Import and export files
        if Id == wx.ID_FILE1:
            dialog = wx.TextEntryDialog(self, "Enter file name", "Import", "")
            if dialog.ShowModal() == wx.ID_OK:
                file_name = dialog.GetValue()
                print("File name:", file_name)
        if Id == wx.ID_FILE2:
            dialog = wx.TextEntryDialog(self, "Enter file name", "Export", "")
            if dialog.ShowModal() == wx.ID_OK:
                file_name = dialog.GetValue()
                print("File name:", file_name)

    def on_spin_cycles(self, event):
        """Handle the event when the user changes the spin control value."""
        self.cycle_count = self.cycles_spin.GetValue()
        self.canvas.render(self.signals_list)

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""
        self.signals_list = self.gather_signal_data(
            self.devices, self.names, self.cycle_count
        )
        self.canvas.render(self.signals_list)

    def on_stop_button(self, event):
        """Handle the event when the user clicks the run button."""
        self.canvas.render(self.signals_list)
        print(self.devices_list)

    def on_spin_devices(self, event):
        """Handle the event when the user selects a new device"""

        if self.no_devices:
            self.no_devices = False
            self.devices_spin_button.SetValue(0)
            self.update_current_device(self.devices_list[0])
            return

        spin_value = self.devices_spin_button.GetValue()
        if spin_value <= -1:
            self.devices_spin_button.SetValue(len(self.devices_list) - 1)
            spin_value = len(self.devices_list) - 1
        elif spin_value >= len(self.devices_list):
            self.devices_spin_button.SetValue(0)
            spin_value = 0

        self.current_device = spin_value
        self.update_current_device(self.devices_list[spin_value])

    def on_toggle_dark_mode(self, event):
        if self.dark_mode_flag:
            self.dark_mode_flag = False
            self.canvas.set_light_mode()
            self.canvas.BG_COLOUR = self.canvas.BG_WHITE
            self.dark_mode_button.SetLabel("Dark Mode")

        else:
            self.dark_mode_flag = True
            self.canvas.set_dark_mode()
            self.canvas.BG_COLOUR = self.canvas.BG_BLACK
            self.dark_mode_button.SetLabel("Light Mode")

        self.canvas.render(None)

    # Helper functions
    def update_current_device(self, devices):
        """Update the current device text label"""
        property = None
        if devices[1] == "SWITCH":
            property = "STATE"
        elif devices[1] == "CLOCK":
            property = "PERIOD"
        elif devices[1] == "DTYPE":
            property = "MEMORY"
        else:
            self.devices_text.SetLabel(f" Device: {devices[0]} \n Type: {devices[1]}")
            return
        self.devices_text.SetLabel(
            f" Device: {devices[0]} \n Type: {devices[1]} \n {property}: {devices[2]}"
        )

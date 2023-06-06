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

        # Colours for signals
        self.BLACK = (0.0, 0.0, 0.0)
        self.WHITE = (1.0, 1.0, 1.0)
        self.RED = (1.0, 0.0, 0.0)
        self.GREEN = (0.0, 1.0, 0.0)
        self.BLUE = (0.0, 0.0, 1.0)
        self.colours = [self.WHITE, self.RED, self.GREEN, self.BLUE]
        self.signals_list = []

        # Background colours
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
        """Set the background colour to black and first signal colour to white."""

        GL.glClearColor(self.BG_BLACK[0], self.BG_BLACK[1], self.BG_BLACK[2], 1.0)
        self.colours[0] = self.WHITE

    def set_light_mode(self):
        """Set the background colour to white and first signal colour to black."""

        GL.glClearColor(self.BG_WHITE[0], self.BG_WHITE[1], self.BG_WHITE[2], 1.0)
        self.colours[0] = self.BLACK

    def draw_trace(self, signal, colour, position):
        """Draw a trace for a given signal."""

        GL.glColor3f(colour[0], colour[1], colour[2])
        GL.glBegin(GL.GL_LINE_STRIP)

        for i in range(len(signal)):
            x = (i * 50) + 30
            x_next = (i * 50) + 80
            y = 930 + 50 * int(signal[i]) - 90 * position
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next, y)
        GL.glEnd()
        self.draw_markers(signal, position)

    def draw_markers(self, signal, position):
        """Draw markers for a given signal."""

        GL.glColor3f(0.5, 0.5, 0.5)

        for i in range(len(signal) + 1):
            GL.glBegin(GL.GL_LINE_STRIP)
            x = (i * 50) + 30
            y = 930 - 5 - 90 * position
            y_next = 930 - 15 - 90 * position
            GL.glVertex2f(x, y)
            GL.glVertex2f(x, y_next)
            GL.glEnd()

    def render_signals(self):
        """Render all the signals and labels."""

        for i in range(len(self.signals_list)):
            self.draw_trace(self.signals_list[i][1], self.colours[i % 4], i)
            self.render_text(self.signals_list[i][0], 10, 950 - 90 * i)

    def render(self, signals_list):
        """Handle all drawing operations."""

        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # Update signal list and draw signals
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

        # TODO CHANGE COLOUR READABILITY
        GL.glColor3f(0.0, 0.0, 0.0)
        GL.glRasterPos2f(x_pos, y_pos)

        # Choose a font and size
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
        """Initialise widgets, layout and variables."""

        super().__init__(parent=None, title=title, size=(800, 600))

        # Assign variable to the other modules
        self.names = names
        self.devices = devices
        self.monitors = monitors
        self.network = network

        # Initialise dictionaries and lists for the checks for switches and monitoring
        self.on_checks = {}
        self.monitor_checks = {}
        self.monitored_list = self.generate_monitored_list(devices, names)

        # Used to use the continue button to run on first click
        self.running = False

        # Default number of cycles
        self.cycle_count = 16

        # Set up list of devices and signals
        self.devices_list = self.set_up_devices(devices, names)
        self.signals_list = self.gather_signal_data(names, self.cycle_count)

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

        # Default to dark mode
        self.dark_mode_flag = True

        """Add the file and help menus to the menu bar and set bar"""
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)

        # Canvas for drawing signals
        self.canvas = MyGLCanvas(self, devices, monitors)

        # TODO Set up help menu text
        self.HELP_TEXT = """Select the number of Cycles at the top of the control panel on the right,
         and click the button labelled "Run" to simulate the circuit. You can use the button labelled
         "Continue" to continue simulating the circuit for another N cycles (N is the number in the Cycles box).\n \n """

        # Configure the widgets
        self.set_up_widgets()

        # Choose and set font for buttons
        button_font = wx.Font(
            16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )
        self.run_button.SetFont(button_font)
        self.continue_button.SetFont(button_font)

        # Create a sizer for the device info scroll panel
        device_sizer = wx.BoxSizer(wx.VERTICAL)

        # Add devices to the sizer
        for device in self.devices_list:
            self.add_scroll_widgets(device_sizer, device)

        # Set the sizer for the device list scroll panel
        self.device_scroll.SetSizer(device_sizer)
        self.device_scroll.Layout()
        self.device_scroll.SetScrollRate(0, 20)

        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.cycles_spin.Bind(wx.EVT_SPINCTRL, self.on_spin_cycles)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.continue_button.Bind(wx.EVT_BUTTON, self.on_continue_button)
        self.dark_mode_button.Bind(wx.EVT_BUTTON, self.on_toggle_dark_mode)

        # Configure main and side sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer = wx.BoxSizer(wx.VERTICAL)

        # Add widgets to sizers
        main_sizer.Add(self.canvas, 50, wx.EXPAND | wx.ALL, 5)
        side_sizer.Add(self.cycles_text, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)
        side_sizer.Add(self.cycles_spin, 1, wx.ALL | wx.EXPAND, 5)
        side_sizer.Add(self.run_button, 3, wx.ALL | wx.EXPAND, 5)
        side_sizer.Add(self.continue_button, 3, wx.ALL | wx.EXPAND, 5)
        side_sizer.Add(self.device_scroll, 10, wx.ALL | wx.EXPAND, 5)

        # Add side_sizer to main_sizer as the last item
        main_sizer.Add(side_sizer, 10, wx.ALL | wx.EXPAND, 5)
        side_sizer.Add(self.dark_mode_button, 1, wx.BOTTOM | wx.EXPAND, 5)

        # Set the sizer and configure the window
        # TODO cut this for final version: self.SetSizeHints(600, 600)
        self.Maximize(True)
        self.SetSizer(main_sizer)

        # TODO test and potentially cut this warning from final vers
        # WARNING THESE MIGHT BREAK LINUX
        # Render canvas and set running flag to true
        self.canvas.render(self.signals_list)
        self.running = True

    def set_up_widgets(self):
        """Sets up the widgets for the GUI."""

        self.cycles_text = wx.StaticText(self, wx.ID_ANY, "Cycles")
        self.cycles_spin = wx.SpinCtrl(
            self, wx.ID_ANY, "18", style=wx.ALIGN_CENTER_HORIZONTAL | wx.TE_CENTER
        )
        self.run_button = wx.Button(self, wx.ID_ANY, "Run")
        self.continue_button = wx.Button(self, wx.ID_ANY, "Continue")
        self.dark_mode_button = wx.Button(self, wx.ID_ANY, "Light mode")
        self.device_scroll = wx.ScrolledWindow(self, wx.ID_ANY, style=wx.VSCROLL)

    def set_up_devices(self, devices, names):
        """NOT SURE WHAT THIS DOES TODO."""

        devices_list = []
        for device in devices.devices_list:
            single_device_list = []
            id = device.device_id
            single_device_list.append(names.get_name_string(id))
            single_device_list.append(self.device_number_to_string(device.device_kind))
            single_device_list.append(devices.return_property(id))

            devices_list.append(single_device_list)

        return devices_list

    def add_scroll_widgets(self, device_sizer, device):
        """Adds widgets for every device to the device scroll panel."""

        # Create a sizer for the device entry
        device_entry = wx.BoxSizer(wx.HORIZONTAL)

        # Add name label
        device_text = wx.StaticText(self.device_scroll, label=device[0])
        device_entry.Add(device_text, 1, wx.ALL, 5)

        # Based on device type, add the appropriate widgets
        if device[1] == "SWITCH":
            self.add_switch_scroll_widget(device_entry, device)

        elif device[1] == "CLOCK":
            self.add_clock_scroll_widget(device_entry, device)

        else:
            self.add_other_scroll_widget(device_entry, device)

        # Add to device sizer
        device_sizer.Add(device_entry, 0, wx.EXPAND)

    def add_switch_scroll_widget(self, device_entry, device):
        """Adds a monitor and on/off checkbox for a switch device to the device scroll panel."""

        # Add monitor checkbox
        device_checkbox = wx.CheckBox(self.device_scroll, label="Monitor")

        # If monitored in file, initialise as on
        if device[0] in self.monitored_list:
            device_checkbox.SetValue(True)

        # Add to dictionary of checks and add to device entry row
        self.monitor_checks[device_checkbox] = device[0]
        device_entry.Add(device_checkbox, 1, wx.ALL, 5)

        # Bind an event handler to the checkbox
        device_checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_changed)

        # Add on/off checkbox
        device_checkbox = wx.CheckBox(self.device_scroll, label="On")

        # If on in file, initialise as on
        if device[2] == 1:
            device_checkbox.SetValue(True)

        # Add to dictionary of checks and add to device entry row
        self.on_checks[device_checkbox] = device[0]
        device_entry.Add(device_checkbox, 1, wx.ALL, 5)

        # Bind an event handler to the checkbox
        device_checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_changed)

    def add_clock_scroll_widget(self, device_entry, device):
        """Adds a monitor and spin box for a clock device to the device scroll panel."""

        # Add monitor checkbox
        device_checkbox = wx.CheckBox(self.device_scroll, label="Monitor")

        # If monitored in file, initialise as on
        if device[0] in self.monitored_list:
            device_checkbox.SetValue(True)

        # Add to dictionary of checks and add to device entry row
        self.monitor_checks[device_checkbox] = device[0]
        device_entry.Add(device_checkbox, 1, wx.ALL, 5)

        # Bind an event handler to the checkbox
        device_checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_changed)

        # Add spin box with initial value as set in file
        device_spin = wx.SpinCtrl(self.device_scroll, wx.ID_ANY, str(device[2]))
        device_entry.Add(device_spin, 1, wx.ALL, 5)

        # Bind an event handler to the checkbox TODO
        return

    def add_other_scroll_widget(self, device_entry, device):
        """Adds a monitor checkbox for a non-switch/clock device to the device scroll panel."""

        # Add monitor checkbox
        device_checkbox = wx.CheckBox(self.device_scroll, label="Monitor")

        # If monitored in file, initialise as on
        if device[0] in self.monitored_list:
            device_checkbox.SetValue(True)

        # Add to dictionary of checks and add to device entry row
        self.monitor_checks[device_checkbox] = device[0]
        device_entry.Add(device_checkbox, 2, wx.ALL, 5)

        # Bind an event handler to the checkbox
        device_checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_changed)

    def generate_monitored_list(self, devices, names):
        """Generates and returns a list of monitored devices."""

        monitored_list = []
        for item in self.monitors.monitors_dictionary.items():
            monitored_list.append(names.get_name_string(item[0][0]))
        return monitored_list

    def gather_signal_data(self, names, cycle_count):
        """Run the circuit, then record and return signals for monitored devices."""

        signals_list = []
        self.run(cycle_count)
        for item in self.monitors.monitors_dictionary.items():
            single_signal = []
            single_signal.append(names.get_name_string(item[0][0]))
            single_signal.append(item[1])
            signals_list.append(single_signal)

        return signals_list

    def run(self, cycles):
        """Runs the circuit for a given number of cycles."""

        for _ in range(cycles):
            if self.network.execute_network():
                self.monitors.record_signals()

    def device_number_to_string(self, device_number):
        """Returns a string containing the name of the device with the given number."""

        # TODO What the fuck is this used for
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
    def on_checkbox_changed(self, event):
        """Event handler for checkboxes."""

        # Get the checkbox that triggered the event and the state
        checkbox = event.GetEventObject()
        isChecked = checkbox.GetValue()

        if isChecked:
            # If it's switch on/off
            if checkbox in self.on_checks:
                name_id = self.names.query(self.on_checks[checkbox])
                self.devices.set_switch(name_id, 1)

            # If it's monitor
            if checkbox in self.monitor_checks:
                # BREAK FOR DTYPE TODO TODO
                name_id = self.names.query(self.monitor_checks[checkbox])
                self.monitors.make_monitor(name_id, None, self.cycle_count)

        else:
            # If it's switch on/off
            if checkbox in self.on_checks:
                name_id = self.names.query(self.on_checks[checkbox])
                self.devices.set_switch(name_id, 0)
            # If it's monitor
            if checkbox in self.monitor_checks:
                # BREAK FOR DTYPE TODO TODO
                name_id = self.names.query(self.monitor_checks[checkbox])
                self.monitors.remove_monitor(name_id, None)

        # Update the canvas if the circuit has been run
        if not self.running:
            return
        self.signals_list = self.on_run_button("")
        self.canvas.render(self.signals_list)

    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""

        Id = event.GetId()
        # Exit the program
        if Id == wx.ID_EXIT:
            self.Close(True)

        # About dialog
        if Id == wx.ID_ABOUT:
            wx.MessageBox(
                "Logic Simulator\nCreated by Lohith Konathala, Ognjen Stefanovic, Juan Pedro Montes Moreno\n2023\nBased on skeleton code by Mojisola Agboola 2017",
                "About Logsim",
                wx.ICON_INFORMATION | wx.OK,
            )

        # Help dialog
        if Id == wx.ID_HELP:
            wx.MessageBox(
                self.HELP_TEXT,
                "Additional information",
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
        """Handle the event when the user changes the number of cycles value."""

        self.cycle_count = self.cycles_spin.GetValue()
        self.canvas.render(self.signals_list)

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""

        # Reset monitors and cold start the devices
        self.monitors.reset_monitors()
        self.devices.cold_startup()

        # Run the circuit and record signals for monitored devices
        self.signals_list = self.gather_signal_data(self.names, self.cycle_count)

        # Render the canvas, set to running
        self.canvas.render(self.signals_list)
        self.running = True

    def on_continue_button(self, event):
        """Handle the event when the user clicks the run button."""
        if not self.running:
            self.on_run_button("")
            return
        self.signals_list = self.gather_signal_data(self.names, self.cycle_count)
        self.canvas.render(self.signals_list)

    def on_toggle_dark_mode(self, event):
        """Handle the event when the user clicks the dark mode button."""

        # Turn dark mode off
        if self.dark_mode_flag:
            self.dark_mode_flag = False
            self.canvas.set_light_mode()
            self.canvas.BG_COLOUR = self.canvas.BG_WHITE
            self.dark_mode_button.SetLabel("Dark Mode")

        # Turn dark mode on
        else:
            self.dark_mode_flag = True
            self.canvas.set_dark_mode()
            self.canvas.BG_COLOUR = self.canvas.BG_BLACK
            self.dark_mode_button.SetLabel("Light Mode")

        # Render the canvas
        self.canvas.render(None)

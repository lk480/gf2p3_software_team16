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
        self.RED = (1.0, 0.0, 0.0)
        self.GREEN = (0.0, 1.0, 0.0)
        self.BLUE = (0.0, 0.0, 1.0)
        self.COLOURS = [self.BLACK, self.RED, self.GREEN, self.BLUE]

        # TEMP STUFF
        self.signals = [
            [1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1],
            [0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0],
            [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0],
            [1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        ]
        self.names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

        self.BG_WHITE = (1.0, 1.0, 1.0)
        self.BG_BLACK = (0.0, 0.0, 0.0)

    def init_gl(self):
        """Configure and initialise the OpenGL context."""
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        GL.glDrawBuffer(GL.GL_BACK)
        GL.glClearColor(self.BG_WHITE[0], self.BG_WHITE[1], self.BG_WHITE[2], 1.0)
        GL.glViewport(0, 0, size.width, size.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, size.width, 0, size.height, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslated(self.pan_x, self.pan_y, 0.0)
        GL.glScaled(self.zoom, self.zoom, self.zoom)

    def draw_trace(self, signal, colour, position):
        """Draw a trace for a given signal."""
        GL.glColor3f(colour[0], colour[1], colour[2])
        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range(10):
            x = (i * 50) + 30
            x_next = (i * 50) + 80
            y = 450 + 50 * signal[i] - 90 * position
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next, y)
        GL.glEnd()

    def render_signals(self, signals, names):
        """Render all the signals and labels."""
        for i in range(len(self.signals)):
            self.draw_trace(self.signals[i], self.COLOURS[i % 4], i)
            self.render_text(self.names[i], 10, 470 - 90 * i)

    def render(self, text):
        """Handle all drawing operations."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # Draw specified text at position (10, 10)
        self.render_text(text, 10, 10)

        # Draw a sample signal trace
        self.render_signals("a", "b")

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

        size = self.GetClientSize()
        text = "".join(
            [
                "Canvas redrawn on paint event, size is ",
                str(size.width),
                ", ",
                str(size.height),
            ]
        )
        self.render(text)

    def on_size(self, event):
        """Handle the canvas resize event."""
        # Forces reconfiguration of the viewport, modelview and projection
        # matrices on the next paint event
        self.init = False

    def on_mouse(self, event):
        """Handle mouse events."""
        text = ""
        # Calculate object coordinates of the mouse position
        size = self.GetClientSize()
        ox = (event.GetX() - self.pan_x) / self.zoom
        oy = (size.height - event.GetY() - self.pan_y) / self.zoom
        old_zoom = self.zoom
        if event.ButtonDown():
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            text = "".join(
                [
                    "Mouse button pressed at: ",
                    str(event.GetX()),
                    ", ",
                    str(event.GetY()),
                ]
            )
        if event.ButtonUp():
            text = "".join(
                [
                    "Mouse button released at: ",
                    str(event.GetX()),
                    ", ",
                    str(event.GetY()),
                ]
            )
        if event.Leaving():
            text = "".join(
                ["Mouse left canvas at: ", str(event.GetX()), ", ", str(event.GetY())]
            )
        if event.Dragging():
            self.pan_x += event.GetX() - self.last_mouse_x
            self.pan_y -= event.GetY() - self.last_mouse_y
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False
            text = "".join(
                [
                    "Mouse dragged to: ",
                    str(event.GetX()),
                    ", ",
                    str(event.GetY()),
                    ". Pan is now: ",
                    str(self.pan_x),
                    ", ",
                    str(self.pan_y),
                ]
            )
        if event.GetWheelRotation() < 0:
            self.zoom *= 1.0 + (event.GetWheelRotation() / (10 * event.GetWheelDelta()))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(
                ["Negative mouse wheel rotation. Zoom is now: ", str(self.zoom)]
            )
        if event.GetWheelRotation() > 0:
            self.zoom /= 1.0 - (event.GetWheelRotation() / (10 * event.GetWheelDelta()))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(
                ["Positive mouse wheel rotation. Zoom is now: ", str(self.zoom)]
            )
        if text:
            self.render(text)
        else:
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

        # Add the file and help menus to the menu bar and set bar
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)

        # TEMP list of devices to test
        self.devices = [["G1", "0", "1"], ["G2", "1", "0"], ["G3", "2", "3"]]
        self.current_device = len(self.devices) + 2

        # Canvas for drawing signals
        self.canvas = MyGLCanvas(self, devices, monitors)

        # Set up help menu text
        self.HELP_TEXT = "HELP ME"

        # Configure the widgets
        self.cycles_text = wx.StaticText(self, wx.ID_ANY, "Cycles")
        self.cycles_spin = wx.SpinCtrl(self, wx.ID_ANY, "10")
        self.run_button = wx.Button(self, wx.ID_ANY, "Run")
        self.stop_button = wx.Button(self, wx.ID_ANY, "Stop")
        self.speed_text = wx.StaticText(self, wx.ID_ANY, "Cycles /s")
        self.speed_spin = wx.SpinCtrl(self, wx.ID_ANY, "1")
        self.text_box = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.devices_text = wx.StaticText(self, wx.ID_ANY, "No device selected")
        self.devices_spin_button = wx.SpinButton(
            self, wx.ID_ANY, style=wx.SP_HORIZONTAL, name="Current device"
        )

        # Bind events to widgets
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.cycles_spin.Bind(wx.EVT_SPINCTRL, self.on_spin_cycles)
        self.speed_spin.Bind(wx.EVT_SPINCTRL, self.on_spin_speed)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop_button)
        self.text_box.Bind(wx.EVT_TEXT_ENTER, self.on_text_box)
        self.devices_spin_button.Bind(wx.EVT_SPIN, self.on_spin_devices)

        # Set spin range and initialise flag for first run
        self.devices_spin_button.SetRange(0, len(self.devices))
        self.no_devices = True

        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        side_sizer = wx.BoxSizer(wx.VERTICAL)

        # Add widgets to sizers
        main_sizer.Add(self.canvas, 5, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(side_sizer, 1, wx.ALL, 5)
        side_sizer.Add(self.cycles_text, 1, wx.TOP, 10)
        side_sizer.Add(self.cycles_spin, 1, wx.ALL, 5)
        side_sizer.Add(self.run_button, 1, wx.ALL, 5)
        side_sizer.Add(self.stop_button, 1, wx.ALL, 5)
        side_sizer.Add(self.speed_text, 1, wx.ALL, 10)
        side_sizer.Add(self.speed_spin, 1, wx.ALL, 5)
        side_sizer.Add(self.text_box, 1, wx.ALL, 5)
        side_sizer.Add(self.devices_spin_button, 1, wx.ALL, 5)
        side_sizer.Add(self.devices_text, 1, wx.ALL, 5)

        # Set the sizer and configure the window
        self.SetSizeHints(600, 600)
        self.SetSizer(main_sizer)

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
        spin_value = self.cycles_spin.GetValue()
        text = "".join(["New cycles control value: ", str(spin_value)])
        self.canvas.render(text)

    def on_spin_speed(self, event):
        """Handle the event when the user changes the spin control value."""
        spin_value = self.speed_spin.GetValue()
        text = "".join(["New rate control value: ", str(spin_value)])
        self.canvas.render(text)

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""
        text = "Run button pressed."
        self.canvas.render(text)

    def on_stop_button(self, event):
        """Handle the event when the user clicks the run button."""
        text = "Stop button pressed."
        self.canvas.render(text)

    def on_text_box(self, event):
        """Handle the event when the user enters text."""
        text_box_value = self.text_box.GetValue()
        text = "".join(["New text box value: ", text_box_value])
        self.canvas.render(text)

    def on_spin_devices(self, event):
        """Handle the event when the user selects a new device"""

        if self.no_devices:
            self.no_devices = False
            self.devices_spin_button.SetValue(0)
            self.update_current_device(self.devices[0])
            return

        spin_value = self.devices_spin_button.GetValue()

        if spin_value <= -1:
            self.devices_spin_button.SetValue(len(self.devices) - 1)
            spin_value = len(self.devices) - 1
        elif spin_value >= len(self.devices):
            self.devices_spin_button.SetValue(0)
            spin_value = 0

        self.current_device = spin_value
        self.update_current_device(self.devices[spin_value])

    # Helper functions
    def update_current_device(self, devices):
        """Update the current device text label"""
        self.devices_text.SetLabel(
            f" Device: {devices[0]} \n ID: {devices[1]} \n Property: {devices[2]}"
        )

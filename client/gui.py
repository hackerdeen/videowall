from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line

import udpfpga
import socket

HOST = ("127.0.0.1", 2600)

# Basic code from kivy examples
# from examples/guide/firstwidget

#notes from someone in #kivy
#
#bionoid | [tj]: so there are many ways to approach this, but the simplest is
#        | probably to do parent = FloatLayout() instead of Widget(), since it
#        | respects the size_hint of children, it will stretch it to fill all 
#        | the available space
#bionoid | you'll have to set size_hint = (None, None) for the buttons though
#

class PaintWidget(Widget):
    def on_touch_down(self, touch):
        color = (random(), 1, 1)
        with self.canvas:
            Color(*color, mode='hsv')
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

class PaintApp(App):

    def build(self):
        parent = Widget()
        self.painter = PaintWidget()
        parent.add_widget(self.painter)
	self.painter.size = (800,600)

        clearbtn = Button(text='clear')
        clearbtn.bind(on_release=self.clear_canvas)
        clearbtn.size = (50,50)
        clearbtn.pos = (0,0)
        parent.add_widget(clearbtn)

        sendudpbtn = Button(text='send udp')
        sendudpbtn.bind(on_release=self.sendudp_canvas)
        sendudpbtn.size = (50,50)
        sendudpbtn.pos = (60,0)
        parent.add_widget(sendudpbtn)

        sendtcpbtn = Button(text='send tcp')
        sendtcpbtn.bind(on_release=self.sendtcp_canvas)
        sendtcpbtn.size = (50,50)
        sendtcpbtn.pos = (120,0)
        parent.add_widget(sendtcpbtn)

        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()

    def sendudp_canvas(self, obj):
	filename = "canvas.png"
	print "saving to", filename
        self.painter.export_to_png(filename)

	udpfpga.client(HOST[0],HOST[1], filename)

    def sendtcp_canvas(self, obj):
	filename = "canvas.png"
	print "saving to", filename
        self.painter.export_to_png(filename)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect(HOST)

	f = open(filename,'rb')
	l = f.read(1024)
	while (l):
	    s.send(l)
	    l = f.read(1024)
	f.close()
	s.close()


if __name__ == '__main__':
    PaintApp().run()

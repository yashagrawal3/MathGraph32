#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007-2008 One Laptop Per Child
# Copyright 2007 Gerard J. Cerchio <www.circlesoft.com>
# Copyright 2008 Andrés Ambrois <andresambrois@gmail.com>
# Copyright 2010 Marcos Orfila <www.marcosorfila.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import commands
import sys
import platform
import gi
gi.require_version('Pango', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Pango
from gi.repository import Gtk

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import StopButton

from gettext import gettext as _


class MathGraph32Start(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.ceibaljam_icon_path = os.getenv("SUGAR_BUNDLE_PATH") + "/images/ceibaljam.png"
        self.java_path = self.get_java_path()
        self.build_toolbar()
        self.build_canvas()
        self.show_all()

    def build_toolbar(self):

        self.max_participants = 1

        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

    def build_canvas(self):

        box_canvas = Gtk.VBox(False, 0)
        self.set_canvas(box_canvas)

        # Title
        box_title = Gtk.VBox(False, 0)
        label_title = Gtk.Label(_("MathGraph32"))
        label_title.set_justify(Gtk.Justification.CENTER)
        label_title.modify_font(Pango.FontDescription("Arial 22"))

        box_title.add(Gtk.Label("\n\n"))
        box_title.add(label_title)
        box_title.add(Gtk.Label("\n"))

        # Author
        box_author = Gtk.VBox(False, 0)
        box_author.add(Gtk.Label(_("Created by Yves Biton")))
        label_author_url = Gtk.Label('<b>http://www.mathgraph32.org</b>')
        label_author_url.set_use_markup(True)
        box_author.add(label_author_url)

        # Credits
        box_credits = Gtk.VBox(False, 0)
        box_credits.add(Gtk.Label(""))
        box_credits.add(Gtk.Label(_('Spanish translation and pedagogical evaluation by %(TEACHER)s') % { 'TEACHER': 'Luis Belcredi' }))
        label_teacher_email= Gtk.Label('<b>http://xsubcero.50webs.biz</b>')
        label_teacher_email.set_use_markup(True)
        box_credits.add(label_teacher_email)
        box_credits.add(Gtk.Label(""))
        box_credits.add(Gtk.Label(_('Sugarized by %(SUGARIZER)s') % { 'SUGARIZER': 'Marcos Orfila' }))
        label_sugarizer_website = Gtk.Label('<b>http://www.marcosorfila.com</b>')
        label_sugarizer_website.set_use_markup(True)
        box_credits.add(label_sugarizer_website)
        box_credits.add(Gtk.Label(""))

        # Footer box (Activities on CeibalJAM! website)
        box_footer = Gtk.VBox(False, 0)
        box_footer.add(Gtk.Label(""))
        box_footer.add(Gtk.Label(_('Find more activities on %(CEIBALJAM)s website:') % { 'CEIBALJAM': 'CeibalJAM!'}))
        label_ceibaljam_website = Gtk.Label('<b>http://activities.ceibaljam.org</b>')
        label_ceibaljam_website.set_use_markup(True)
        box_footer.add(label_ceibaljam_website)
        box_footer.add(Gtk.Label(""))

        # CeibalJAM! image
        box_ceibaljam_image = Gtk.VBox(False, 0)
        image_ceibaljam = Gtk.Image()
        image_ceibaljam.set_from_file(self.ceibaljam_icon_path)
        box_ceibaljam_image.pack_end(image_ceibaljam, False, False, 0)

        # Get all the boxes together
        box_canvas.pack_start(box_title, False, False, 0)
        box_canvas.pack_start(box_author, False, False, 0)
        box_canvas.pack_start(Gtk.Label("\n"), False, False, 0)
        if self.java_path == "":
           box_java_not_found = Gtk.VBox(False, 0)
           label_java_not_found = Gtk.Label('<span foreground="red"><b>' + _("Java was not found!") + '</b></span>')
           label_java_not_found.set_justify(Gtk.Justification.CENTER)
           label_java_not_found.set_use_markup(True)
           label_java_not_found.modify_font(Pango.FontDescription("Arial 20"))
           box_java_not_found.add(label_java_not_found)
           box_java_not_found.add(Gtk.Label(_('You can download the Java activity from %s website (see below)') % 'CeibalJAM!'))
           box_canvas.pack_start(box_java_not_found, False, False, 0)
           box_canvas.pack_start(Gtk.Label(""), False, False, 0)
        else:
           box_java_found = Gtk.VBox(False, 0)
           label_version_info_title = Gtk.Label('<b>' + _("Java version found:") + '</b>')
           label_version_info_title.set_use_markup(True)
           version_information = commands.getoutput(self.java_path + " -version")
           label_version_info = Gtk.Label(version_information)
           label_version_info.set_justify(Gtk.Justification.CENTER)
           box_java_found.add(label_version_info_title)
           box_java_found.add(label_version_info)
           box_canvas.pack_start(box_java_found, False, False, 0)
        box_canvas.pack_end(Gtk.Label("\n"), False, False, 0)
        self.add_buttons(box_canvas)
        box_canvas.pack_end(box_footer, False, False, 0)
        box_canvas.pack_end(box_ceibaljam_image, False, False, 0)
        box_canvas.pack_end(box_credits, False, False, 0)

        if self.java_path != '':
           self.button_play.grab_focus()
        else:
           self.button_exit.grab_focus()

    def create_script(self, script_path):
        """Create the script to run the program"""

        # In the future, some options to be included in the tuxmath script (like "--nosound")
        # could be selected by the user.
        script_text = self.java_path + " -jar $SUGAR_BUNDLE_PATH/MathGraph32/MathGraph32.jar"

        f = open(script_path, 'w')
        f.write(script_text)
        f.close()
        os.chmod(script_path, 0755)

    def add_buttons(self, box_canvas):
        """Add the buttons at the bottom of the page"""
        box_buttons = Gtk.HBox(False, 0)
        self.button_play = Gtk.Button(_("Start"))
        self.button_play.connect("clicked", self._button_play_clicked_cb)
        self.button_exit = Gtk.Button(_("Exit"))
        self.button_exit.connect("clicked", self._button_exit_clicked_cb)
        if self.java_path != '':
          box_buttons.add(Gtk.VBox())
          box_buttons.add(self.button_play)
          box_buttons.add(Gtk.VBox())
          box_buttons.add(self.button_exit)
          box_buttons.add(Gtk.VBox())
        else:
          box_buttons.add(Gtk.VBox())
          box_buttons.add(Gtk.VBox())
          box_buttons.add(self.button_exit)
          box_buttons.add(Gtk.VBox())
          box_buttons.add(Gtk.VBox())
        box_canvas.pack_end(box_buttons, False, False, 0)
 
    def _button_play_clicked_cb(self, widget):
        path = os.getenv("SUGAR_ACTIVITY_ROOT")+"/mathgraph32_script.sh"
        if os.path.exists(path):
            os.remove(path)
        self.create_script(path)
        os.system(path+" &")
        sys.exit(0)

    def _button_exit_clicked_cb(self, widget):
        sys.exit(0)

    def get_java_path(self):
        """
        Check whether java exists and return the path to the "java" command.
        Returns an empty string in case java is not found.
        """
        # If "jre_32" is not in Java.activity, it is not installed or it isn't the latest version
        if not os.path.exists(os.environ["SUGAR_BUNDLE_PATH"]+"/../Java.activity/jre_32"):
            return ''
        if platform.machine().startswith('arm'):
            return os.environ["SUGAR_BUNDLE_PATH"]+"/../Java.activity/jre_arm/bin/java"
        else:
            if platform.architecture()[0] == '64bit':
                return os.environ["SUGAR_BUNDLE_PATH"]+"/../Java.activity/jre_64/bin/java"
            else:
                return os.environ["SUGAR_BUNDLE_PATH"]+"/../Java.activity/jre_32/bin/java"

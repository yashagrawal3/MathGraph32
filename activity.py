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

import pango
import os
import commands
import sys
import gtk

from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import StopButton

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

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        separator = gtk.SeparatorToolItem()
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

        box_canvas = gtk.VBox(False, 0)
        self.set_canvas(box_canvas)

        # Title
        box_title = gtk.VBox(False, 0)
        label_title = gtk.Label(_("MathGraph32"))
        label_title.set_justify(gtk.JUSTIFY_CENTER)
        label_title.modify_font(pango.FontDescription("Arial 22"))

        box_title.add(gtk.Label("\n\n"))
        box_title.add(label_title)
        box_title.add(gtk.Label("\n"))

        # Author
        box_author = gtk.VBox(False, 0)
        box_author.add(gtk.Label(_("Created by Yves Biton")))
        label_author_url = gtk.Label('<b>http://www.mathgraph32.org</b>')
        label_author_url.set_use_markup(True)
        box_author.add(label_author_url)

        # Credits
        box_credits = gtk.VBox(False, 0)
        box_credits.add(gtk.Label(""))
        box_credits.add(gtk.Label(_('Spanish translation and pedagogical evaluation by %(TEACHER)s') % { 'TEACHER': 'Luis Belcredi' }))
        label_teacher_email= gtk.Label('<b>http://xsubcero.50webs.biz</b>')
        label_teacher_email.set_use_markup(True)
        box_credits.add(label_teacher_email)
        box_credits.add(gtk.Label(""))
        box_credits.add(gtk.Label(_('Sugarized by %(SUGARIZER)s') % { 'SUGARIZER': 'Marcos Orfila' }))
        label_sugarizer_website = gtk.Label('<b>http://www.marcosorfila.com</b>')
        label_sugarizer_website.set_use_markup(True)
        box_credits.add(label_sugarizer_website)
        box_credits.add(gtk.Label(""))

        # Footer box (Activities on CeibalJAM! website)
        box_footer = gtk.VBox(False, 0)
        box_footer.add(gtk.Label(""))
        box_footer.add(gtk.Label(_('Find more activities on %(CEIBALJAM)s website:') % { 'CEIBALJAM': 'CeibalJAM!'}))
        label_ceibaljam_website = gtk.Label('<b>http://activities.ceibaljam.org</b>')
        label_ceibaljam_website.set_use_markup(True)
        box_footer.add(label_ceibaljam_website)
        box_footer.add(gtk.Label(""))

        # CeibalJAM! image
        box_ceibaljam_image = gtk.VBox(False, 0)
        image_ceibaljam = gtk.Image()
        image_ceibaljam.set_from_file(self.ceibaljam_icon_path)
        box_ceibaljam_image.pack_end(image_ceibaljam, False, False, 0)

        # Get all the boxes together
        box_canvas.pack_start(box_title, False, False, 0)
        box_canvas.pack_start(box_author, False, False, 0)
        box_canvas.pack_start(gtk.Label("\n"), False, False, 0)
        if self.java_path == "":
           box_java_not_found = gtk.VBox(False, 0)
           label_java_not_found = gtk.Label('<span foreground="red"><b>' + _("Java was not found!") + '</b></span>')
           label_java_not_found.set_justify(gtk.JUSTIFY_CENTER)
           label_java_not_found.set_use_markup(True)
           label_java_not_found.modify_font(pango.FontDescription("Arial 20"))
           box_java_not_found.add(label_java_not_found)
           box_java_not_found.add(gtk.Label(_('You can download the Java activity from %s website (see below)') % 'CeibalJAM!'))
           box_canvas.pack_start(box_java_not_found, False, False, 0)
           box_canvas.pack_start(gtk.Label(""), False, False, 0)
        else:
           box_java_found = gtk.VBox(False, 0)
           label_version_info_title = gtk.Label('<b>' + _("Java version found:") + '</b>')
           label_version_info_title.set_use_markup(True)
           version_information = commands.getoutput(self.java_path + " -version")
           label_version_info = gtk.Label(version_information)
           label_version_info.set_justify(gtk.JUSTIFY_CENTER)
           box_java_found.add(label_version_info_title)
           box_java_found.add(label_version_info)
           box_canvas.pack_start(box_java_found, False, False, 0)
        box_canvas.pack_end(gtk.Label("\n"), False, False, 0)
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
        box_buttons = gtk.HBox(False, 0)
        self.button_play = gtk.Button(_("Start"))
        self.button_play.connect("clicked", self._button_play_clicked_cb)
        self.button_exit = gtk.Button(_("Exit"))
        self.button_exit.connect("clicked", self._button_exit_clicked_cb)
        if self.java_path != '':
          box_buttons.add(gtk.VBox())
          box_buttons.add(self.button_play)
          box_buttons.add(gtk.VBox())
          box_buttons.add(self.button_exit)
          box_buttons.add(gtk.VBox())
        else:
          box_buttons.add(gtk.VBox())
          box_buttons.add(gtk.VBox())
          box_buttons.add(self.button_exit)
          box_buttons.add(gtk.VBox())
          box_buttons.add(gtk.VBox())
        box_canvas.pack_end(box_buttons, False, False, 0)
 
    def _button_play_clicked_cb(self, widget):
        path = os.getenv("MATHGRAPH_SCRIPT")
        self.create_script(path)
        sys.exit(0)

    def _button_exit_clicked_cb(self, widget):
        sys.exit(0)

    def get_java_path(self):
        """
        Check whether java exists and return the path to the "java" command.
        Returns an empty string in case java is not found.
        """
        # If "java -version" command fails, then java is not in the PATH
        status, output = commands.getstatusoutput('java -version')
        if status == 0:
            # Java was found
            return commands.getoutput('which java')
        else:
            return ''


# -*- coding: utf-8 -*-
# PEP8:OK, LINT:OK, PY3:OK


#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################


# metadata
" Ninja open with "
__version__ = ' 0.1 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ''
__date__ = ' 15/12/2013 '
__prj__ = ' openwith '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = ''


# imports
from mimetypes import guess_type
from os import path
from platform import linux_distribution
from subprocess import PIPE, Popen

from PyQt4.QtGui import QAction, QIcon, QMenu

from ninja_ide.core import plugin


###############################################################################


def xdg_query(command, param):
    """ query xdg to get the default app """
    p = Popen(['xdg-mime', 'query', command, param], stdout=PIPE, stderr=PIPE)
    output, errors = p.communicate()
    if p.returncode or errors:
        print(('ERROR: {}: {}'.format(p.returncode, errors.strip())))
        return
    return output.strip()


class Main(plugin.Plugin):
    " Main Class "
    def initialize(self, *args, **kwargs):
        " Init Main Class "
        super(Main, self).initialize(*args, **kwargs)
        if linux_distribution():
            self.menu = QMenu('Open with')
            self.menu.aboutToShow.connect(self.build_submenu)
            self.ex_locator = self.locator.get_service('explorer')
            self.ex_locator.add_project_menu(self.menu, lang='all')

    def build_submenu(self):
        ''' build sub menu on the fly based on file path '''
        self.menu.clear()
        if self.ex_locator.get_current_project_item().isFolder is not True:
            filenam = self.ex_locator.get_current_project_item().get_full_path()
            entry = xdg_query('default', guess_type(filenam, strict=False)[0])
            if entry:
                app = entry.replace('.desktop', '')
                self.menu.addActions([
                    QAction(QIcon.fromTheme(app), app, self,
                            triggered=lambda: Popen([app, filenam])),
                    QAction(QIcon.fromTheme('folder-open'), 'File Manager',
                            self, triggered=lambda: Popen(['xdg-open',
                                                    path.dirname(filenam)]))])
                self.menu.show()


###############################################################################


if __name__ == "__main__":
    print(__doc__)

from PyQt4 import QtGui



class MenuBar(QtGui.QMenuBar):
    '''
    QMenuBar with easier insertMenu methods
    methods are used from:
    http://scribus.info/svn/Scribus/trunk/Scribus/scribus/plugins/scripter/python/scripter_hooks.py
    '''

    def __init__(self):
        super(MenuBar, self).__init__()


    def iter_menus(self):
        for action in self.actions():
            menu = action.menu()
            if menu:
                yield menu


    def iter_inner_menus(self, menu):
        for action in menu.actions():
            menu = action.menu()
            if menu:
                yield menu


    def findMenu(self, title):
        """
        find a menu with a given title

        @type  title: string
        @param title: English title of the menu
        @rtype:       QMenu
        @return:      None if no menu was found, else the menu with title
        """
        # See also http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/pyqt4ref.html#differences-between-pyqt-and-qt
        #title = QApplication.translate(mikro.classname(self.window), title) 
        for menu in self.iter_menus():
            if menu.title() == title:
                return menu
            for innerMenu in self.iter_inner_menus(menu):
                if innerMenu.title() == title:
                    return innerMenu


    def actionForMenu(self, menu):
        for action in self.actions():
            if action.menu() == menu:
                return action


    def insertMenuBefore(self, before_menu, new_menu):
        """
        Insert a menu after another menu in the menubar

        @type: before_menu QMenu instance or title string of menu
        @param before_menu: menu which should be after the newly inserted menu
        @rtype: QAction instance
        @return: action for inserted menu
        """
        if isinstance(before_menu, basestring):
            before_menu = self.findMenu(before_menu)
        before_action = self.actionForMenu(before_menu)
        # I have no clue why QMenuBar::insertMenu only allows
        # to insert before another menu and not after a menu...
        new_action = self.insertMenu(before_action, new_menu)
        return new_action
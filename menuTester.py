from pymenu import Menu

menu = Menu('Menu title')
menu.add_option("Option 1", lambda: print("Option 1"))
menu.add_option("Option 2", lambda: print("Option 2"))
menu.add_option("Option 3", lambda: print("Option 3"))

submenu = Menu('Submenu title')
submenu.add_option("Suboption 1", lambda: print("Suboption 1"))
submenu.add_option("Suboption 2", lambda: print("Suboption 2"))
submenu.add_option("Suboption 3", lambda: print("Suboption 3"))

menu.add_option("Submenu", submenu)
menu.show()
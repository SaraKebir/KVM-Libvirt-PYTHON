# -*- coding: utf-8 -*-
# Import the necessary packages
from libvirtFunctions import *
import sys
sys.path.append('./cursesmenu')
from cursesmenu import *
from cursesmenu.items import *

# Create the menu
menu = CursesMenu("Libvirt", "Choisissez une option")

# Create some items
functionItems = []
# MenuItem is the base class for all items, it doesn"t do anything when selected
menu_item = MenuItem("Menu Item")

# A FunctionItem runs a Python function when selected
functionItems.append(FunctionItem("Afficher des informations sur l'hote", function=hostInfo))
domainNames = domainList()

#Submenu with the list of VM
vmListInfo = CursesMenu("Liste des machines virtuelles", "Choisissez une machine pour afficher ses informations")
vmListStart = CursesMenu("Liste des machines virtuelles", "Choisissez la machine à démarrer ")
vmListStop = CursesMenu("Liste des machines virtuelles", "Choisissez la machine à stopper")
vmListIp = CursesMenu("Liste des machines virtuelles", "Choisissez une machine pour afficher son adresse IP")

for domain in domainNames :
    vmListInfo.append_item(FunctionItem(domain,vmInfo,args=[domain]))

for domain in domainNames :
    vmListStart.append_item(FunctionItem(domain,startDomain,args=[domain]))

for domain in domainNames :
    vmListStop.append_item(FunctionItem(domain,destroyDomain,args=[domain]))

for domain in domainNames :
    vmListIp.append_item(FunctionItem(domain,networkDomain,args=[domain]))

# A SelectionMenu constructs a menu from a list of strings
selection_menu = SelectionMenu(["item1", "item2", "item3"])

# A SubmenuItem lets you add a menu (the selection_menu above, for example)
# as a submenu of another menu
submenu_item1 = SubmenuItem("Afficher la liste des machines disponible", vmListInfo, menu)
submenu_item2 = SubmenuItem("Démarrer une machine", vmListStart, menu)
submenu_item3 = SubmenuItem("Stopper une machine", vmListStop, menu)
submenu_item4 = SubmenuItem("Adresse ip d'une machine", vmListIp, menu)

# Once we"re done creating them, we just add the items to the menu
menu.append_item(FunctionItem("Afficher des informations sur l'hôte", function=hostInfo))
menu.append_item(submenu_item1)
menu.append_item(submenu_item2)
menu.append_item(submenu_item3)
menu.append_item(submenu_item4)



# Finally, we call show to show the menu and allow the user to interact
menu.show()

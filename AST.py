def create_node(tag,attr={},child=[]):
    return {'tag':tag,'attr':attr.copy(),'child':child[:],'parent':0}


def open_tag(tag):
    global curr_element
    new_item = create_node(tag)
    new_item['parent']=curr_element
    curr_element['child'].append(new_item)
    curr_element = new_item
    return curr_element

def new_attr_tag(attr,val):
    global curr_element
    curr_element['attr'][attr]=val
    return curr_element

def move_up_to_close_tag(tag):
    global curr_element
    while curr_element['tag']!=tag:
        curr_element = curr_element['parent']
    curr_element = curr_element['parent']
    return curr_element


temp_style={'size':'normal','align':'left'}

AST_tree=create_node('DOM')

curr_element=AST_tree
new_attr_tag('windowtitle','test')




import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QMainWindow)
from __feature__ import snake_case, true_property


def analyze_tag(tag,widget):
    if tag['tag']=="text":
        label = QLabel(tag['attr']['innertext'])
        if 'align' in tag['attr'] and tag['attr']['align']=="center":
            label.alignment = Qt.AlignCenter
            
        if 'size' in tag['attr'] and tag['attr']['size']=="h1":
            label.set_style_sheet(''' font-size: 24px; ''')
            print("grubas")
        widget.layout.add_widget(label)
        
    if tag['tag']=="button":
        widget.layout.add_widget(QPushButton(tag['attr']['innertext']))

def recursive_analyze_AST_tree(widget,tag=AST_tree):
    analyze_tag(tag,widget)
    for i in tag['child']:
        recursive_analyze_AST_tree(widget,i)

def renderowanie():
    app = QApplication(sys.argv)

    widget = QWidget()
    
    widget.layout = QVBoxLayout(widget)
    recursive_analyze_AST_tree(widget)

    main_window = QMainWindow()
    main_window.set_central_widget(widget)
    main_window.set_window_title(AST_tree['attr']['windowtitle'])



    main_window.show()

    sys.exit(app.exec_())

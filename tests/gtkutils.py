import pygtk
pygtk.require('2.0')
import gtk

def dump_tree_store(store):
    sibling = store.get_iter_first()
    while sibling != None:
        dump_children(store, sibling)
        sibling = store.iter_next(sibling)

def dump_children(store, iter, level=0):
    item = store.get_value(iter, 1)
    print '    '*level, item.question

    child = store.iter_children(iter)
    while child != None:
        dump_children(store, child, level+1)
        child = store.iter_next(child)
        
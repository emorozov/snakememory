#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@+leo-ver=4-thin
#@+node:eugene.20041103145917:@thin snakememory.py
#@@first
#@@first
#@@language python

# Copyright (C) 2004 Eugene Morozov <jmv@emorozov.net>
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#@<<snakememory declarations>>
#@+node:eugene.20041103152728:<< snakememory declarations >>
import os
import sys
import time
import random
import datetime
import shutil
import socket
import binascii
import threading
import xml
from xml.sax import make_parser
from glob import glob

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import pango

from xmlwriter import XMLWriter

import locale
import gettext

#@-node:eugene.20041103152728:<< snakememory declarations >>
#@nl
#@<<localization>>
#@+node:eugene.20041114214930:<< localization >>
if sys.platform != 'win32':
    locale.setlocale(locale.LC_MESSAGES, '')
gtk.glade.bindtextdomain('snakememory')
gtk.glade.textdomain('snakememory')
cat = gettext.install('snakememory')
#@nonl
#@-node:eugene.20041114214930:<< localization >>
#@nl
#@+others
#@+node:eugene.20041110165904:debug
def debug(str):
    print str
#@nonl
#@-node:eugene.20041110165904:debug
#@+node:eugene.20041118234210:get_guid
# This function was borrowed from Pyro: http://pyro.sourceforge.net
_getGUID_counter = 0		# extra safeguard against double numbers
_getGUID_lock = threading.Lock()

def get_guid():
    # Generate readable GUID string.
    # The GUID is constructed as follows: hexlified string of
    # AAAAAAAA-AAAABBBB-BBBBBBBB-BBCCCCCC  (a 128-bit number in hex)
    # where A=network address, B=timestamp, C=random.
    # The 128 bit number is returned as a string of 16 8-bits characters.
    # For A: should use the machine's MAC ethernet address, but there is no
    # portable way to get it... use the IP address + 2 bytes process id.
    try:
        # Bad, because addresses can be from private ranges, but
        # there's no portable alternative
        ip = socket.gethostbyname(socket.gethostname())
        networkAddrStr = binascii.hexlify(socket.inet_aton(ip))+"%04x" % os.getpid()
    except socket.error:
        # can't get IP address... use another value, like our Python id() and PID
        ip = os.getpid()
        ip += id(get_guid)
        networkAddrStr = "%08lx%04x" % (ip, os.getpid())

    _getGUID_lock.acquire()  # cannot generate multiple GUIDs at once
    global _getGUID_counter
    t1 = time.time()*100 + _getGUID_counter
    _getGUID_counter += 1
    _getGUID_lock.release()
    t2 = int((t1*time.clock()) % sys.maxint) & 0xffffff
    t1 = int(t1 % sys.maxint)
    timestamp = (long(t1) << 24) | t2
    r2 = (random.randint(0, sys.maxint/2)>>4) & 0xffff
    r3 = (random.randint(0, sys.maxint/2)>>5) & 0xff
    return networkAddrStr+'%014x%06x' % (timestamp, (r2<<8)|r3)
#@nonl
#@-node:eugene.20041118234210:get_guid
#@+node:eugene.20041106214235:class SuperMemo
class SuperMemo(object):
    "Implementation of the SM-2 algorithm."
    #@    @+others
    #@+node:eugene.20041109165620:__init__
    def __init__(self):
        pass
    #@nonl
    #@-node:eugene.20041109165620:__init__
    #@+node:eugene.20041108171409:schedule_item
    def schedule_item(self, item):
        if len(item.efficiency) == 1:
            deltas = [1]
        elif len(item.efficiency) == 2:
            deltas = [1, 6]
        elif len(item.efficiency) > 2:
            deltas = [1, 6]
            for ef in item.efficiency[2:]:
                deltas.append(deltas[-1]*ef)
        delta = int(round(reduce(lambda x, y: x+y, deltas)))
        delta += len(deltas)
        scheduled_date = item.start_date + datetime.timedelta(days=delta)
        item.scheduled_date = scheduled_date
    
        if (datetime.date.today()-item.scheduled_date).days > 0:
            # some repetitions was skipped, I see no alternative
            # to starting from scratch
            debug("Warning, you've skipped item %s: %s, restarting repetition schedule" % (item.question, item.scheduled_date))
            item.start_date = datetime.date.today()
            item.efficiency = [2.5]
            self.schedule_item(item)
    #@-node:eugene.20041108171409:schedule_item
    #@+node:eugene.20041110153107:schedule_next_repetition
    def schedule_next_repetition(self, item, quality):
        if quality < 3:
            # start repeating from scratch
            debug('Bad quality, restarting %s' % item.question)
            del item.efficiency[:-1]
            item.start_date = datetime.date.today()
            self.schedule_item(item)
            return
        ef = item.efficiency[-1]
        debug('old ef: %f' % ef)
        ef = self.adjust_efficiency(ef, quality)
        if ef < 1.3:
            ef = 1.3
        if ef > 2.5:
            ef = 2.5
        debug('new ef: %f' % ef)
        item.efficiency.append(ef)
        self.schedule_item(item)
        debug('next repetition on %s' % item.scheduled_date)
    #@nonl
    #@-node:eugene.20041110153107:schedule_next_repetition
    #@+node:eugene.20041110155829:adjust_efficiency
    def adjust_efficiency(self, ef, q):
        return ef - 0.8 + 0.28*q - 0.02*q**2
    #@nonl
    #@-node:eugene.20041110155829:adjust_efficiency
    #@-others
#@nonl
#@-node:eugene.20041106214235:class SuperMemo
#@+node:eugene.20041103170106:class Item
class Item(object):
    __slots__ = ['question', 'answer', '__start_date',
                'scheduled_date', '__efficiency',
                '__repeat', '__creation_date',
                'store', 'guid']
    #@    @+others
    #@+node:eugene.20041103170106.1:__init__
    def __init__(self, store, question, answer, guid=None):
        self.store = store
        self.question = question
        self.answer = answer
        if not guid:
            self.guid = get_guid()
        else:
            self.guid = guid
    
        self.__creation_date = datetime.date.today()
        self.__start_date = datetime.date.today()
        self.__efficiency = [2.5]
    
        # Whether item scored less than four on last drill and
        # needs to be repeated again today
        self.__repeat = False
    #@nonl
    #@-node:eugene.20041103170106.1:__init__
    #@+node:eugene.20041124210449:Multimedia properties
    #@+node:eugene.20041120145350:set_question_audio
    def set_question_audio(self, filename):
        self.store.set_question_audio(self.guid, filename)
    #@nonl
    #@-node:eugene.20041120145350:set_question_audio
    #@+node:eugene.20041120233318:set_answer_audio
    def set_answer_audio(self, filename):
        self.store.set_answer_audio(self.guid, filename)
    #@nonl
    #@-node:eugene.20041120233318:set_answer_audio
    #@+node:eugene.20041122230750:set_question_video
    def set_question_video(self, filename):
        self.store.set_question_video(self.guid, filename)
    #@nonl
    #@-node:eugene.20041122230750:set_question_video
    #@+node:eugene.20041122230750.1:set_answer_video
    def set_answer_video(self, filename):
        self.store.set_answer_video(self.guid, filename)
    #@nonl
    #@-node:eugene.20041122230750.1:set_answer_video
    #@+node:eugene.20041121002154:get_question_audio
    def get_question_audio(self):
        return self.store.get_question_audio(self.guid)
    #@nonl
    #@-node:eugene.20041121002154:get_question_audio
    #@+node:eugene.20041121002154.1:get_answer_audio
    def get_answer_audio(self):
        return self.store.get_answer_audio(self.guid)
    #@nonl
    #@-node:eugene.20041121002154.1:get_answer_audio
    #@+node:eugene.20041122231056:get_question_video
    def get_question_video(self):
        return self.store.get_question_video(self.guid)
    #@nonl
    #@-node:eugene.20041122231056:get_question_video
    #@+node:eugene.20041122231056.1:get_answer_video
    def get_answer_video(self):
        return self.store.get_answer_video(self.guid)
    #@nonl
    #@-node:eugene.20041122231056.1:get_answer_video
    #@-node:eugene.20041124210449:Multimedia properties
    #@+node:eugene.20041108012917:set_start_date
    def set_start_date(self, date):
        if isinstance(date, (unicode, str)):
            year, month, day = [int(x) for x in date.split('-')]
            self.__start_date = datetime.date(year, month, day)
        elif isinstance(date, datetime.date):
            self.__start_date = date
        else:
            raise ValueError, _('Unsupported type for the start_date property')
    #@-node:eugene.20041108012917:set_start_date
    #@+node:eugene.20041108011929:get_start_date
    def get_start_date(self):
        return self.__start_date
    
    #@-node:eugene.20041108011929:get_start_date
    #@+node:eugene.20041116210147:set_creation_date
    def set_creation_date(self, date):
        if isinstance(date, (unicode, str)):
            year, month, day = [int(x) for x in date.split('-')]
            self.__creation_date = datetime.date(year, month, day)
        elif isinstance(date, datetime.date):
            self.__creation_date = date
        else:
            raise ValueError, _('Unsupported type for the creation_date property')
    #@-node:eugene.20041116210147:set_creation_date
    #@+node:eugene.20041116210215:get_creation_date
    def get_creation_date(self):
        return self.__creation_date
    
    #@-node:eugene.20041116210215:get_creation_date
    #@+node:eugene.20041108024929:set_efficiency
    def set_efficiency(self, history):
        if isinstance(history, (unicode, str)):
            history = history.strip()
            if len(history) > 0:
                self.__efficiency = [float(x) for x in history.split(',')]
            else:
                self.__efficiency = [2.5]
        elif isinstance(history, list):
            self.__efficiency = history
        else:
            raise ValueError, _('Unsupported type for the efficiency property')
    #@nonl
    #@-node:eugene.20041108024929:set_efficiency
    #@+node:eugene.20041108024929.1:get_efficiency
    def get_efficiency(self):
        return self.__efficiency
    #@nonl
    #@-node:eugene.20041108024929.1:get_efficiency
    #@+node:eugene.20041112124058:set_repeat_again
    def set_repeat(self, repeat):
        if isinstance(repeat, (unicode, str)):
            repeat = repeat.strip().lower()
            if repeat == 'true':
                self.__repeat = True
            elif repeat == 'false':
                self.__repeat = 'False'
            else:
                raise ValueError, _('Unsupported type for the repeat property')
        elif isinstance(repeat, bool):
            self.__repeat = repeat
        else:
            raise ValueError, _('Unsupported type for the repeat property')
    #@nonl
    #@-node:eugene.20041112124058:set_repeat_again
    #@+node:eugene.20041112124149:get_repeat_again
    def get_repeat(self):
        return self.__repeat
    #@nonl
    #@-node:eugene.20041112124149:get_repeat_again
    #@-others
    #@    << properties >>
    #@+node:eugene.20041108013056:<< properties >>
    start_date = property(get_start_date, set_start_date)
    creation_date = property(get_creation_date, set_creation_date)
    efficiency = property(get_efficiency, set_efficiency)
    repeat = property(get_repeat, set_repeat)
    #@-node:eugene.20041108013056:<< properties >>
    #@nl
#@nonl
#@-node:eugene.20041103170106:class Item
#@+node:eugene.20041103164710:class CardHandler
class CardHandler(xml.sax.handler.ContentHandler):
    #@    << states >>
    #@+node:eugene.20041103164710.1:<< states >>
    STATE_SNAKEMEMORY = 0
    STATE_PREFERENCES = 1
    STATE_ITEMS = 2
    STATE_ITEM = 3
    STATE_QUESTION = 4
    STATE_ANSWER = 5
    STATE_PROPERTY = 6
    
    transitions = {
        STATE_SNAKEMEMORY: (STATE_ITEMS, STATE_PREFERENCES),
        STATE_ITEMS: (STATE_ITEM,),
        STATE_ITEM: (STATE_QUESTION, STATE_ANSWER, STATE_PROPERTY, STATE_ITEM,),
        STATE_PREFERENCES: (STATE_PROPERTY,)
    }
    #@nonl
    #@-node:eugene.20041103164710.1:<< states >>
    #@nl
    #@    @+others
    #@+node:eugene.20041103164710.2:__init__
    def __init__(self, store):
        self.store = store
        self.items = store.get_items()
        self.preferences = store.preferences
    
        self.buffer = ''
        self.state_stack = []
        self.ref_stack = []
        self.current_property = None
    
    #@-node:eugene.20041103164710.2:__init__
    #@+node:eugene.20041103164710.3:startElement
    def startElement(self, name, attrs):
        if name != 'snakememory' and len(self.state_stack) < 1:
            raise SyntaxError, _('root tag must me <snakememory>')
        self.buffer = ''
    
        if name == 'snakememory':
            self.to_state(self.STATE_SNAKEMEMORY)
        elif name == 'preferences':
            self.to_state(self.STATE_PREFERENCES)
        elif name == 'items':
            self.to_state(self.STATE_ITEMS)
        elif name == 'item':
            self.to_state(self.STATE_ITEM)
            item = Item(self.store, '', '')
            if self.state_stack[-2] != self.STATE_ITEM:
                iter = self.items.append(None, (item, 'first level', 'answer'))
            else:
                iter = self.items.get_iter(self.ref_stack[-1].get_path())
                iter = self.items.append(iter, (item, 'next level', 'answer'))
            ref = gtk.TreeRowReference(self.items, self.items.get_path(iter))
            self.ref_stack.append(ref)
        elif name == 'question':
            self.to_state(self.STATE_QUESTION)
        elif name == 'answer':
            self.to_state(self.STATE_ANSWER)
        elif name == 'property':
            self.to_state(self.STATE_PROPERTY)
            self.current_property = attrs['name']
        else:
            raise SyntaxError, _('Unknown tag: %s') % name
    #@-node:eugene.20041103164710.3:startElement
    #@+node:eugene.20041103164710.4:to_state
    def to_state(self, state):
        """Verify that transition to given state is allowed in the
        current state and follow the transition. Raise ParseException
        otherwise."""
        if len(self.state_stack) > 0:
            allowed_transitions = self.transitions[self.state_stack[-1]]
        else:
            allowed_transitions = (self.STATE_SNAKEMEMORY,)
        if state not in allowed_transitions:
            raise SyntaxError, _('Invalid tag nesting order')
        self.state_stack.append(state)
    #@nonl
    #@-node:eugene.20041103164710.4:to_state
    #@+node:eugene.20041103164710.5:endElement
    def endElement(self, name):
        state = self.state_stack.pop()
        if state == self.STATE_ITEM:
            ref = self.ref_stack.pop()
            iter = self.items.get_iter(ref.get_path())
            item = self.items.get_value(iter, 0)
            self.items.set_value(iter, 1, item.question)
            self.items.set_value(iter, 2, item.answer)
        elif state == self.STATE_PROPERTY:
            if self.state_stack[-1] == self.STATE_ITEM:
                iter = self.items.get_iter(self.ref_stack[-1].get_path())
                item = self.items.get_value(iter, 0)
                # Check that property is supported
                if self.current_property in ('guid', 'start_date', 'creation_date', 'efficiency', 'repeat'):
                    setattr(item, self.current_property, self.buffer)
            elif self.state_stack[-1] == self.STATE_PREFERENCES:
                setattr(self.preferences, self.current_property, self.buffer)
    #@-node:eugene.20041103164710.5:endElement
    #@+node:eugene.20041103164710.6:characters
    def characters(self,  characters):
        if self.state_stack[-1] in (self.STATE_QUESTION, self.STATE_ANSWER):
            iter = self.items.get_iter(self.ref_stack[-1].get_path())
            item = self.items.get_value(iter, 0)
            if self.state_stack[-1] == self.STATE_QUESTION:
                item.question += characters
            elif self.state_stack[-1] == self.STATE_ANSWER:
                item.answer += characters
        elif self.state_stack[-1] == self.STATE_PROPERTY:
            self.buffer += characters
        else:
            pass # XXX: raise error if not whitespace
    #@nonl
    #@-node:eugene.20041103164710.6:characters
    #@-others
#@-node:eugene.20041103164710:class CardHandler
#@+node:eugene.20041112164453:class Preferences
class Preferences(object):
    __slots__ = ['question_font', 'answer_font']
    #@    @+others
    #@+node:eugene.20041112164453.1:__init__
    def __init__(self):
        self.question_font = None
        self.answer_font = None
    #@nonl
    #@-node:eugene.20041112164453.1:__init__
    #@-others
#@nonl
#@-node:eugene.20041112164453:class Preferences
#@+node:eugene.20041103164135:class SnakeStore
class SnakeStore(object):
    #@    @+others
    #@+node:eugene.20041103164311:__init__
    def __init__(self, path):
        self.observers = []
        self.path = path
    
        self.items = gtk.TreeStore(gobject.TYPE_PYOBJECT, str, str)
        self.preferences = Preferences()
    
        self._connect_handlers()
    #@-node:eugene.20041103164311:__init__
    #@+node:eugene.20041110164912:_connect_handlers
    def _connect_handlers(self):
        self.handlers = []
        self.handlers.append(self.items.connect_after('row-changed', self.notify))
        self.handlers.append(self.items.connect_after('row-deleted', self.notify))
        self.handlers.append(self.items.connect_after('row-inserted', self.notify))
    #@-node:eugene.20041110164912:_connect_handlers
    #@+node:eugene.20041110165218:_disconnect_handlers
    def _disconnect_handlers(self):
        for handler in self.handlers:
            self.items.disconnect(handler)
    #@nonl
    #@-node:eugene.20041110165218:_disconnect_handlers
    #@+node:eugene.20041109155428:attach
    def attach(self, observer):
        self.observers.append(observer)
    #@nonl
    #@-node:eugene.20041109155428:attach
    #@+node:eugene.20041109155522:notify
    def notify(self, store, path, iter=None):
        for observer in self.observers:
            observer.update(path, iter)
    #@nonl
    #@-node:eugene.20041109155522:notify
    #@+node:eugene.20041112172929:get_preferences
    def get_preferences(self):
        return self.preferences
    #@nonl
    #@-node:eugene.20041112172929:get_preferences
    #@+node:eugene.20041104155215:get_items
    def get_items(self):
        "Return gtk.TreeStore corresponding to items list."
        return self.items
    #@nonl
    #@-node:eugene.20041104155215:get_items
    #@+node:eugene.20041104120440:add_card
    def add_card(self, parent, sibling, item):
        row = (item, item.question, item.answer)
        if parent == None:
            return self.items.append(None, row)
        else:
            return self.items.insert_after(parent, sibling, row)
    #@nonl
    #@-node:eugene.20041104120440:add_card
    #@+node:eugene.20041121150918:remove
    def remove(self, refs):
        # Remove media files first
        for ref in refs:
            if not ref.valid():
                continue
            iter = self.items.get_iter(ref.get_path())
            self.remove_children(iter)
    
        for ref in refs:
            if not ref.valid():
                continue
            iter = self.items.get_iter(ref.get_path())
            item = self.items.get_value(iter, 0)
            self.items.remove(iter)
    #@-node:eugene.20041121150918:remove
    #@+node:eugene.20041127234342:remove_children
    def remove_children(self, iter):
        item = self.items.get_value(iter, 0)
        directory = os.path.join(self.path, item.guid)
        if os.path.exists(directory):
            shutil.rmtree(directory)
    
        child = self.items.iter_children(iter)
        while child != None:
            self.remove_children(child)
            child = self.items.iter_next(child)
    #@-node:eugene.20041127234342:remove_children
    #@+node:eugene.20041103164912:save
    def save(self):
        debug('SnakeStore.save')
    
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        cards = file(os.path.join(self.path, 'cards.tmp'), 'w')
        writer = XMLWriter(cards)
        writer.push('snakememory')
    
        writer.push('preferences')
        self.serialize_properties(writer, self.preferences, ('question_font', 'answer_font'))
        writer.pop()
    
        writer.push('items')
    
        sibling = self.items.get_iter_first()
        while sibling != None:
            self.serialize_items(writer, sibling)
            sibling = self.items.iter_next(sibling)
    
        writer.pop()
        writer.pop()
        cards.close()
        shutil.move(os.path.join(self.path, 'cards.tmp'),
                    os.path.join(self.path, 'cards.xml'))
    #@-node:eugene.20041103164912:save
    #@+node:eugene.20041105161449:serialize_items
    def serialize_items(self, writer, iter):
        writer.push('item')
        item = self.items.get_value(iter, 0)
        writer.elem('question', item.question)
        writer.elem('answer', item.answer)
    
        self.serialize_properties(writer, item,
            ('guid', 'start_date', 'scheduled_date', 'creation_date', 'efficiency', 'repeat'))
    
        child = self.items.iter_children(iter)
        while child != None:
            self.serialize_items(writer, child)
            child = self.items.iter_next(child)
        writer.pop()
    
    #@-node:eugene.20041105161449:serialize_items
    #@+node:eugene.20041110171435:serialize_properties
    def serialize_properties(self, writer, item, props):
        for prop_name in props:
            prop_value = getattr(item, prop_name, None)
            if prop_name in ('start_date', 'scheduled_date'):
                prop_value = prop_value.isoformat()
            elif prop_name in ('efficiency',):
                prop_value = ','.join([str(x) for x in prop_value])
            if prop_value:
                writer.elem('property', prop_value, {'name': prop_name})
    #@-node:eugene.20041110171435:serialize_properties
    #@+node:eugene.20041103164542:load
    def load(self):
        filename = os.path.join(self.path, 'cards.xml')
        if not os.path.exists(self.path) or not os.path.exists(filename):
            return
    
        # Don't call handlers while items are partially loaded
        self._disconnect_handlers()
        p = make_parser()
        ch = CardHandler(self)
        p.setContentHandler(ch)
    
        stream = file(filename, 'r')
        p.parse(stream)
        stream.close()
    
        self._connect_handlers()
        sibling = self.items.get_iter_first()
        while sibling != None:
            self.update_children(sibling)
            sibling = self.items.iter_next(sibling)
    #@-node:eugene.20041103164542:load
    #@+node:eugene.20041110165448:update_children
    def update_children(self, iter):
        path = self.items.get_path(iter)
        self.items.row_changed(path, iter)
        child = self.items.iter_children(iter)
        while child != None:
            self.update_children(child)
            child = self.items.iter_next(child)
    
    #@-node:eugene.20041110165448:update_children
    #@+node:eugene.20041120215720:set_question_audio
    def set_question_audio(self, guid, filename):
        self.save_media_object(guid, 'audio_question', filename)
    
    #@-node:eugene.20041120215720:set_question_audio
    #@+node:eugene.20041122231000:set_question_video
    def set_question_video(self, guid, filename):
        self.save_media_object(guid, 'video_question', filename)
    #@-node:eugene.20041122231000:set_question_video
    #@+node:eugene.20041120233045:set_answer_audio
    def set_answer_audio(self, guid, filename):
        self.save_media_object(guid, 'audio_answer', filename)
    
    #@-node:eugene.20041120233045:set_answer_audio
    #@+node:eugene.20041122231000.1:set_answer_video
    def set_answer_video(self, guid, filename):
        self.save_media_object(guid, 'video_answer', filename)
    #@-node:eugene.20041122231000.1:set_answer_video
    #@+node:eugene.20041121003332:get_question_audio
    def get_question_audio(self, guid):
        return self.get_media_object(guid, 'audio_question')
    #@-node:eugene.20041121003332:get_question_audio
    #@+node:eugene.20041122231000.2:get_question_video
    def get_question_video(self, guid):
        return self.get_media_object(guid, 'video_question')
    #@-node:eugene.20041122231000.2:get_question_video
    #@+node:eugene.20041121003332.1:get_answer_audio
    def get_answer_audio(self, guid):
        return self.get_media_object(guid, 'audio_answer')
    #@-node:eugene.20041121003332.1:get_answer_audio
    #@+node:eugene.20041122231000.3:get_answer_video
    def get_answer_video(self, guid):
        return self.get_media_object(guid, 'video_answer')
    #@-node:eugene.20041122231000.3:get_answer_video
    #@+node:eugene.20041120233045.1:save_media_object
    def save_media_object(self, guid, type, filename):
        root, ext = os.path.splitext(filename)
        if ext == '' or ext == '.':
            # XXX: fix that
            raise 'invalid filename'
        directory = os.path.join(self.path, guid)
        if not os.path.exists(directory):
            os.mkdir(directory)
        new_name = type + ext
        new_name = os.path.join(directory, new_name)
        shutil.copyfile(filename, new_name)
    
    #@-node:eugene.20041120233045.1:save_media_object
    #@+node:eugene.20041121003332.2:get_media_object
    def get_media_object(self, guid, type):
        directory = os.path.join(self.path, guid)
        if not os.path.exists(directory):
            return None
        objects = glob(os.path.join(directory, type + '.*'))
        if len(objects) != 1:
            return None
        return objects[0]
    
    #@-node:eugene.20041121003332.2:get_media_object
    #@-others
#@nonl
#@-node:eugene.20041103164135:class SnakeStore
#@+node:eugene.20041121125204:class GladeWindow
class GladeWindow(object):
    """This class loads glade description of the window and
    creates instance variables of specified widgets."""
    widgets = []
    #@    @+others
    #@+node:eugene.20041121125204.1:__init__
    def __init__(self, filename):
        self.widget_tree = gtk.glade.XML(filename)
        for widget in self.widgets:
            setattr(self, widget, self.widget_tree.get_widget(widget))
    #@-node:eugene.20041121125204.1:__init__
    #@-others
#@-node:eugene.20041121125204:class GladeWindow
#@+node:eugene.20041121130713:class GUIFactory
class GUIFactory(object):
    #@    @+others
    #@+node:eugene.20041121130713.1:get_window
    def get_window(name):
        if name == 'recall':
            return GladeRecallCardWindow()
        elif name == 'draw':
            return GladeDrawAnswerWindow()
        elif name == 'new_card':
            return GladeNewCardWindow()
        elif name == 'edit_card':
            return GladeEditCardWindow()
        elif name == 'snakememory':
            return GladeSnakememoryWindow()
        else:
            # XXX
            raise "There's no window with name %s" % name
    #@nonl
    #@-node:eugene.20041121130713.1:get_window
    #@-others
    get_window = staticmethod(get_window)


#@-node:eugene.20041121130713:class GUIFactory
#@+node:eugene.20041121143923:class MediaPlayer
class MediaPlayer(object):
    """This class plays media files."""
    #@    @+others
    #@+node:eugene.20041121143923.1:__init__
    def __init__(self, filename):
        self.filename = filename
    #@nonl
    #@-node:eugene.20041121143923.1:__init__
    #@+node:eugene.20041121143923.2:play
    def play(self):
        root, ext = os.path.splitext(self.filename)
        if ext == '.wav':
            os.system('artsplay %s' % self.filename)
    #@-node:eugene.20041121143923.2:play
    #@-others
#@-node:eugene.20041121143923:class MediaPlayer
#@+node:eugene.20041125154525:Draw answer window
#@+node:eugene.20041125154525.1:class DrawWindowController
class DrawWindowController(object):
    #@    @+others
    #@+node:eugene.20041125155228:__init__
    def __init__(self, view):
        self.view = view
        self.view.widget_tree.signal_autoconnect(self)
    #@-node:eugene.20041125155228:__init__
    #@+node:eugene.20041125164315:on_close_button_clicked
    def on_close_button_clicked(self, button):
        self.view.window.destroy()
    #@nonl
    #@-node:eugene.20041125164315:on_close_button_clicked
    #@+node:eugene.20041125220033:on_clear_button_clicked
    def on_clear_button_clicked(self, button):
        self.view.clear()
    #@nonl
    #@-node:eugene.20041125220033:on_clear_button_clicked
    #@-others
#@nonl
#@-node:eugene.20041125154525.1:class DrawWindowController
#@+node:eugene.20041125154525.2:class GladeDrawAnswerWindow
class GladeDrawAnswerWindow(GladeWindow):
    widgets = ['window', 'answer_area']
    #@    @+others
    #@+node:eugene.20041125154525.3:__init__
    def __init__(self):
        GladeWindow.__init__(self, 'draw_answer_window.glade')
        self.pixmap = None
    
        self.answer_area.connect('expose_event', self.expose_event)
        self.answer_area.connect('configure_event', self.configure_event)
        self.answer_area.connect('motion_notify_event', self.motion_notify_event)
        self.answer_area.connect('button_press_event', self.button_press_event)
    
        self.answer_area.set_events(gtk.gdk.EXPOSURE_MASK
                                    | gtk.gdk.LEAVE_NOTIFY_MASK
                                    | gtk.gdk.BUTTON_PRESS_MASK
                                    | gtk.gdk.POINTER_MOTION_MASK
                                    | gtk.gdk.POINTER_MOTION_HINT_MASK)
    
        self.window.show_all()
    
    
    #@-node:eugene.20041125154525.3:__init__
    #@+node:eugene.20041125172814:configure_event
    def configure_event(self, widget, event):
        x, y, width, height = widget.get_allocation()
        self.pixmap = gtk.gdk.Pixmap(widget.window, width, height)
        self.pixmap.draw_rectangle(widget.get_style().white_gc,
                                    True, 0, 0, width, height)
        return True
    #@nonl
    #@-node:eugene.20041125172814:configure_event
    #@+node:eugene.20041125172814.1:expose_event
    def expose_event(self, widget, event):
        x, y, width, height = event.area
        widget.window.draw_drawable(widget.get_style().fg_gc[gtk.STATE_NORMAL],
                                    self.pixmap, x, y, x, y, width, height)
        return False
    #@nonl
    #@-node:eugene.20041125172814.1:expose_event
    #@+node:eugene.20041125173059:draw_brush
    def draw_brush(self, widget, x, y):
        rect = (int(x)-3, int(y)-3, 6, 6)
        self.pixmap.draw_rectangle(widget.get_style().black_gc, True,
                                  rect[0], rect[1], rect[2], rect[3])
        widget.queue_draw_area(rect[0], rect[1], rect[2], rect[3])
    #@-node:eugene.20041125173059:draw_brush
    #@+node:eugene.20041125173254:button_press_event
    def button_press_event(self, widget, event):
        if event.button == 1 and self.pixmap != None:
            self.draw_brush(widget, event.x, event.y)
        return True
    
    #@-node:eugene.20041125173254:button_press_event
    #@+node:eugene.20041125173254.1:motion_notify_event
    def motion_notify_event(self, widget, event):
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state
    
        if state & gtk.gdk.BUTTON1_MASK and self.pixmap != None:
            self.draw_brush(widget, x, y)
    
        return True
    #@nonl
    #@-node:eugene.20041125173254.1:motion_notify_event
    #@+node:eugene.20041125220033.1:clear
    def clear(self):
        x, y, width, height = self.answer_area.get_allocation()
        self.pixmap.draw_rectangle(self.answer_area.get_style().white_gc,
                                    True, 0, 0, width, height)
        self.answer_area.queue_draw_area(0, 0, width, height)
    #@nonl
    #@-node:eugene.20041125220033.1:clear
    #@-others
#@nonl
#@-node:eugene.20041125154525.2:class GladeDrawAnswerWindow
#@-node:eugene.20041125154525:Draw answer window
#@+node:eugene.20041110135237:Recall card window
#@+node:eugene.20041110135237.1:class RecallCardWindowController
class RecallCardWindowController(object):
    #@    @+others
    #@+node:eugene.20041110135237.2:__init__
    def __init__(self, view, store, supermemo):
        self.view = view
        self.store = store
        self.supermemo = supermemo
    
        accelgroup = gtk.AccelGroup()
        for i in range(6):
            key, modifier = gtk.accelerator_parse('<Alt>%d' % i)
            accelgroup.connect_group(key, modifier, gtk.ACCEL_VISIBLE, lambda a,b,c,d,i=i: self.assess_quality(i))
        self.view.recall_card_window.add_accel_group(accelgroup)
    
        preferences = store.get_preferences()
    
        if preferences.question_font:
            font_desc = pango.FontDescription(preferences.question_font)
            self.view.question_label.modify_font(font_desc)
        if preferences.answer_font:
            font_desc = pango.FontDescription(preferences.answer_font)
            self.view.answer_label.modify_font(font_desc)
    
        self.view.widget_tree.signal_autoconnect(self)
    
        self.ready_cards = self.find_ready_items()
        self.continue_drill()
    #@-node:eugene.20041110135237.2:__init__
    #@+node:eugene.20041128192021:continue_drill
    def continue_drill(self):
        if len(self.ready_cards) == 0:
            self.view.recall_card_window.destroy()
            dlg = gtk.MessageDialog(None, buttons=gtk.BUTTONS_OK)
            dlg.set_markup(_("There're no more items to learn today"))
            dlg.run()
            dlg.destroy()
            return
        self.item = random.choice(self.ready_cards)
        self.ready_cards.remove(self.item)
    
        self.view.answer_label.set_text('')
        
        self.question_video = self.item.get_question_video()
        self.question_audio = self.item.get_question_audio()
        if self.question_video:
            self.view.question_label.hide()
            self.view.play_question_button.hide()
            self.show_video(self.view.question_image, self.question_video)
        elif self.question_audio:
            self.view.question_label.hide()
            self.view.question_image.hide()
        else:
            self.view.play_question_button.hide()
            self.view.question_image.hide()
            self.view.question_label.set_text(self.item.question)
    
        self.answer_video = self.item.get_answer_video()
        self.answer_audio = self.item.get_answer_audio()
        if self.answer_audio or self.answer_video:
            self.view.view_answer_button.set_label(_('Play answer'))
    
        self.view.quality_combo.set_active(0)
        
    #@nonl
    #@-node:eugene.20041128192021:continue_drill
    #@+node:eugene.20041111144752:find_ready_items
    def find_ready_items(self):
        ready_items = []
        store = self.store.get_items()
        sibling = store.get_iter_first()
        while sibling != None:
            ready_items.extend(self._find_ready_children(store, sibling))
            sibling = store.iter_next(sibling)
    
        return ready_items
    #@-node:eugene.20041111144752:find_ready_items
    #@+node:eugene.20041111145423:_find_ready_children
    def _find_ready_children(self, store, iter):
        children = []
        item = store.get_value(iter, 0)
        if item.scheduled_date == datetime.date.today() or item.repeat:
            # Do not use tree joints in drill
            if not store.iter_children(iter):
                children.append(item)
    
        child = store.iter_children(iter)
        while child != None:
            children.extend(self._find_ready_children(store, child))
            child = store.iter_next(child)
    
        return children
    
    #@-node:eugene.20041111145423:_find_ready_children
    #@+node:eugene.20041123231430:show_video
    def show_video(self, image, filename):
        root, ext = os.path.splitext(filename)
        if ext == '.gif':
            pixbufanim = gtk.gdk.PixbufAnimation(filename)
            image.set_from_animation(pixbufanim)
    #@-node:eugene.20041123231430:show_video
    #@+node:eugene.20041121143333:on_play_question_button_clicked
    def on_play_question_button_clicked(self, button):
        if self.question_audio:
            mplayer = MediaPlayer(self.question_audio)
            mplayer.play()
    
    
    
    #@-node:eugene.20041121143333:on_play_question_button_clicked
    #@+node:eugene.20041110135237.3:on_view_answer_button_clicked
    def on_view_answer_button_clicked(self, button):
        if self.answer_video:
            self.show_video(self.view.answer_image, self.answer_video)
        elif self.answer_audio:
            mplayer = MediaPlayer(self.answer_audio)
            mplayer.play()
        else:
            self.view.answer_label.set_text(self.item.answer)
    #@nonl
    #@-node:eugene.20041110135237.3:on_view_answer_button_clicked
    #@+node:eugene.20041110152618:on_evaluate_button_clicked
    def on_evaluate_button_clicked(self, button):
        quality = 5 - self.view.quality_combo.get_active()
        self.assess_quality(quality)
    #@-node:eugene.20041110152618:on_evaluate_button_clicked
    #@+node:eugene.20041125115009:on_draw_answer_button_clicked
    def on_draw_answer_button_clicked(self, button):
        draw_window = GUIFactory.get_window('draw')
        DrawWindowController(draw_window)
    #@-node:eugene.20041125115009:on_draw_answer_button_clicked
    #@+node:eugene.20041112160949:assess_quality
    def assess_quality(self, quality):
        if quality < 4:
            debug('bad quality, item "%s" will be repeated' % self.item.question)
            self.item.repeat = True
        else:
            self.item.repeat = False
    
        if self.item.scheduled_date == datetime.date.today():
            # Do not reschedule items that are repeated more than once
            self.supermemo.schedule_next_repetition(self.item, quality)
        self.store.save()
    
        self.continue_drill()
        
        return True # Accelgroup requirement
    
    #@-node:eugene.20041112160949:assess_quality
    #@-others
#@nonl
#@-node:eugene.20041110135237.1:class RecallCardWindowController
#@+node:eugene.20041110135237.4:class GladeRecallCardWindow
class GladeRecallCardWindow(GladeWindow):
    widgets = ['quality_combo', 'question_label', 'answer_label',
               'question_image', 'answer_image', 'play_question_button',
               'view_answer_button', 'recall_card_window']
    #@    @+others
    #@+node:eugene.20041110135237.5:__init__
    def __init__(self):
        GladeWindow.__init__(self, 'recall_card.glade')
        # Glade can't handle this task properly
        self.quality_combo.append_text(_('bright'))
        self.quality_combo.append_text(_('good'))
        self.quality_combo.append_text(_('pass'))
        self.quality_combo.append_text(_('fail'))
        self.quality_combo.append_text(_('bad'))
        self.quality_combo.append_text(_('null'))
    #@-node:eugene.20041110135237.5:__init__
    #@-others
#@-node:eugene.20041110135237.4:class GladeRecallCardWindow
#@-node:eugene.20041110135237:Recall card window
#@+node:eugene.20041109125829:Edit card window
#@+node:eugene.20041109125829.1:class EditCardWindowController
class EditCardWindowController(object):
    #@    @+others
    #@+node:eugene.20041109125856:__init__
    def __init__(self, view, store, reference):
        self.view = view
        self.store = store
        self.items = store.get_items()
        self.reference = reference
    
        iter = self.items.get_iter(reference.get_path())
        self.item = self.items.get_value(iter, 0)
    
        self.question_buffer = self.view.widget_tree.get_widget('question_textview').get_buffer()
        self.answer_buffer = self.view.widget_tree.get_widget('answer_textview').get_buffer()
        self.question_buffer.set_text(self.item.question)
        self.answer_buffer.set_text(self.item.answer)
    
        self.creation_date_label = self.view.widget_tree.get_widget('creation_date_label')
        self.schedule_date_label = self.view.widget_tree.get_widget('schedule_date_label')
        self.creation_date_label.set_text(self.item.creation_date.isoformat())
        self.schedule_date_label.set_text(self.item.scheduled_date.isoformat())
    
        self.view.widget_tree.signal_autoconnect(self)
    #@-node:eugene.20041109125856:__init__
    #@+node:eugene.20041109131943:on_ok_button_clicked
    def on_ok_button_clicked(self, button):
        start, end = self.question_buffer.get_bounds()
        question = self.question_buffer.get_text(start, end)
        start, end = self.answer_buffer.get_bounds()
        answer = self.answer_buffer.get_text(start, end)
    
        self.item.question = question
        self.item.answer = answer
    
        iter = self.items.get_iter(self.reference.get_path())
        self.items.set_value(iter, 1, self.item.question)
        self.items.set_value(iter, 2, self.item.answer)
        self.store.save()
    
        self.view.edit_card_window.destroy()
    #@-node:eugene.20041109131943:on_ok_button_clicked
    #@+node:eugene.20041109132042:on_cancel_button_clicked
    def on_cancel_button_clicked(self, button):
        self.view.edit_card_window.destroy()
    #@nonl
    #@-node:eugene.20041109132042:on_cancel_button_clicked
    #@-others
#@nonl
#@-node:eugene.20041109125829.1:class EditCardWindowController
#@+node:eugene.20041109131225:class GladeEditCardWindow
class GladeEditCardWindow(GladeWindow):
    widgets = ['question_audio_image', 'question_video_image',
               'answer_audio_image', 'answer_video_image',
               'edit_card_window']
    #@    @+others
    #@+node:eugene.20041109131225.1:__init__
    def __init__(self):
        GladeWindow.__init__(self, 'edit_card.glade')
        self.question_audio_image.set_from_file('icons/audio.png')
        self.question_video_image.set_from_file('icons/video.png')
        self.answer_audio_image.set_from_file('icons/audio.png')
        self.answer_video_image.set_from_file('icons/video.png')
    
    #@-node:eugene.20041109131225.1:__init__
    #@-others
#@nonl
#@-node:eugene.20041109131225:class GladeEditCardWindow
#@-node:eugene.20041109125829:Edit card window
#@+node:eugene.20041103171145:New card window
#@+node:eugene.20041103172037:class NewCardWindowController
class NewCardWindowController(object):
    #@    @+others
    #@+node:eugene.20041103172037.1:__init__
    def __init__(self, view, store, selection):
        self.view = view
        self.store = store
        self.selection = selection
    
        self.question_audio = None
        self.answer_audio = None
        self.question_video = None
        self.answer_video = None
    
        self.view.widget_tree.signal_autoconnect(self)
    
    #@-node:eugene.20041103172037.1:__init__
    #@+node:eugene.20041120234136:select_file
    def select_file(self, filter):
        dialog = gtk.FileChooserDialog(_('Open...'),
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
    
        dialog.add_filter(filter)
    
        filter = gtk.FileFilter()
        filter.set_name(_('All files'))
        filter.add_pattern('*')
        dialog.add_filter(filter)
    
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
        else:
            filename = None
        dialog.destroy()
    
        return filename
    #@-node:eugene.20041120234136:select_file
    #@+node:eugene.20041118230032:on_question_audio_clicked
    def on_question_audio_clicked(self, button):
        filter = gtk.FileFilter()
        filter.set_name(_('Audio'))
        filter.add_mime_type('audio/mpeg')
        filter.add_mime_type('audio/x-wav')
        filter.add_mime_type('audio/basic')
        filter.add_mime_type('application/ogg')
        filter.add_pattern('*.mp3')
        filter.add_pattern('*.ogg')
        filter.add_pattern('*.au')
        filter.add_pattern('*.wav')
    
        self.question_audio = self.select_file(filter)
    #@nonl
    #@-node:eugene.20041118230032:on_question_audio_clicked
    #@+node:eugene.20041118230032.1:on_answer_audio_clicked
    def on_answer_audio_clicked(self, button):
        filter = gtk.FileFilter()
        filter.set_name(_('Audio'))
        filter.add_mime_type('audio/mpeg')
        filter.add_mime_type('audio/x-wav')
        filter.add_mime_type('audio/basic')
        filter.add_mime_type('application/ogg')
        filter.add_pattern('*.mp3')
        filter.add_pattern('*.ogg')
        filter.add_pattern('*.au')
        filter.add_pattern('*.wav')
    
        self.answer_audio = self.select_file(filter)
    #@-node:eugene.20041118230032.1:on_answer_audio_clicked
    #@+node:eugene.20041122224617:on_question_video_clicked
    def on_question_video_clicked(self, button):
        filter = gtk.FileFilter()
        filter.set_name(_('Video'))
        filter.add_mime_type('video/mpeg')
        filter.add_mime_type('video/mp4')
        filter.add_mime_type('video/quicktime')
        filter.add_mime_type('video/x-ms-wmv')
        filter.add_mime_type('video/x-msvideo')
        filter.add_mime_type('image/gif')
    
        self.question_video = self.select_file(filter)
    #@-node:eugene.20041122224617:on_question_video_clicked
    #@+node:eugene.20041122224617.1:on_answer_video_clicked
    def on_answer_video_clicked(self, button):
        filter = gtk.FileFilter()
        filter.set_name(_('Video'))
        filter.add_mime_type('video/mpeg')
        filter.add_mime_type('video/mp4')
        filter.add_mime_type('video/quicktime')
        filter.add_mime_type('video/x-ms-wmv')
        filter.add_mime_type('video/x-msvideo')
        filter.add_mime_type('image/gif')
    
        self.answer_video = self.select_file(filter)
    #@-node:eugene.20041122224617.1:on_answer_video_clicked
    #@+node:eugene.20041103180138:on_ok_button_clicked
    def on_ok_button_clicked(self, button):
        q_buffer = self.view.question_textview.get_buffer()
        a_buffer = self.view.answer_textview.get_buffer()
        start, end = q_buffer.get_bounds()
        question = q_buffer.get_text(start, end)
        start, end = a_buffer.get_bounds()
        answer = a_buffer.get_text(start, end)
    
        item = Item(self.store, question, answer)
        if self.question_audio:
            item.set_question_audio(self.question_audio)
        if self.answer_audio:
            item.set_answer_audio(self.answer_audio)
        if self.question_video:
            item.set_question_video(self.question_video)
        if self.answer_video:
            item.set_answer_video(self.answer_video)
    
        parent = sibling = None
        model, paths = self.selection.get_selected_rows()
        if len(paths) == 1:
            sibling = model.get_iter(paths[0])
            parent = model.iter_parent(sibling)
            self.selection.unselect_iter(sibling)
    
        iter = self.store.add_card(parent, sibling, item)
        self.selection.select_iter(iter)
        self.store.save()
    
        self.view.new_card_window.destroy()
    #@nonl
    #@-node:eugene.20041103180138:on_ok_button_clicked
    #@+node:eugene.20041103175721:on_cancel_button_clicked
    def on_cancel_button_clicked(self, button):
        self.view.new_card_window.destroy()
    #@nonl
    #@-node:eugene.20041103175721:on_cancel_button_clicked
    #@-others
#@nonl
#@-node:eugene.20041103172037:class NewCardWindowController
#@+node:eugene.20041103171145.1:class GladeNewCardWindow
class GladeNewCardWindow(GladeWindow):
    widgets = ['question_audio_image', 'question_video_image',
               'answer_audio_image', 'answer_video_image',
               'new_card_window', 'question_textview',
               'answer_textview']
    #@    @+others
    #@+node:eugene.20041103171145.2:__init__
    def __init__(self):
        GladeWindow.__init__(self, 'new_card.glade')
        self.question_audio_image.set_from_file('icons/audio.png')
        self.question_video_image.set_from_file('icons/video.png')
        self.answer_audio_image.set_from_file('icons/audio.png')
        self.answer_video_image.set_from_file('icons/video.png')
    #@nonl
    #@-node:eugene.20041103171145.2:__init__
    #@-others
#@nonl
#@-node:eugene.20041103171145.1:class GladeNewCardWindow
#@-node:eugene.20041103171145:New card window
#@+node:eugene.20041113122546:Preferences Window
#@+node:eugene.20041113123359:class PreferencesWindowController
class PreferencesWindowController(object):
    #@    @+others
    #@+node:eugene.20041113123359.1:__init__
    def __init__(self, view, store):
        self.view = view
        self.store = store
        self.preferences = store.get_preferences()
    
        self.window = self.view.widget_tree.get_widget('preferences_window')
        self.view.widget_tree.signal_autoconnect(self)
    #@-node:eugene.20041113123359.1:__init__
    #@+node:eugene.20041113222040:on_question_font_set
    def on_question_font_set(self, font_button):
        self.preferences.question_font = font_button.get_font_name()
        self.store.save()
    #@nonl
    #@-node:eugene.20041113222040:on_question_font_set
    #@+node:eugene.20041113222555:on_answer_font_set
    def on_answer_font_set(self, font_button):
        self.preferences.answer_font = font_button.get_font_name()
        self.store.save()
    #@-node:eugene.20041113222555:on_answer_font_set
    #@+node:eugene.20041113123359.2:on_close_button_clicked
    def on_close_button_clicked(self, button):
        self.window.destroy()
    #@nonl
    #@-node:eugene.20041113123359.2:on_close_button_clicked
    #@-others
#@nonl
#@-node:eugene.20041113123359:class PreferencesWindowController
#@+node:eugene.20041113123359.3:class PreferencesWindow
class PreferencesWindow(object):
    #@    @+others
    #@+node:eugene.20041113123359.4:__init__
    def __init__(self):
        self.widget_tree = gtk.glade.XML('preferences.glade')
    #@-node:eugene.20041113123359.4:__init__
    #@-others
#@nonl
#@-node:eugene.20041113123359.3:class PreferencesWindow
#@-node:eugene.20041113122546:Preferences Window
#@+node:eugene.20041103171033:Main application Window
#@+node:eugene.20041103155300:class SnakeMemoryWindowController
class SnakeMemoryWindowController(object):
    #@    @+others
    #@+node:eugene.20041103155317:__init__
    def __init__(self, view):
        self.store = SnakeStore(os.path.expanduser('~/Snakememory'))
        self.view = view
        self.supermemo = SuperMemo()
    
        self.store.attach(self)
        self.store.load()
        self.view.items_treeview.set_model(self.store.get_items())
        self.view.widget_tree.signal_autoconnect(self)
        self.view.items_treeview.expand_all()
    #@-node:eugene.20041103155317:__init__
    #@+node:eugene.20041109155619:update
    def update(self, path, iter):
        "This is called whenever store changes."
        if not iter:
            # item(s) was deleted
            self.store.save()
            return
        store = self.store.get_items()
        item = store.get_value(iter, 0)
        # Sometimes None is passed even if I don't connect to the
        # 'row-inserted' signal
        if item:
            self.supermemo.schedule_item(item)
    #@-node:eugene.20041109155619:update
    #@+node:eugene.20041109125609:on_row_activated
    def on_row_activated(self, view, path, view_column):
        ref = gtk.TreeRowReference(self.store.get_items(), path)
        edit_card_window = GUIFactory.get_window('edit_card')
        EditCardWindowController(edit_card_window, self.store, ref)
    #@-node:eugene.20041109125609:on_row_activated
    #@+node:eugene.20041103170715:on_add_button_clicked
    def on_add_button_clicked(self, widget):
        selection = self.view.items_treeview.get_selection()
        new_card_window = GUIFactory.get_window('new_card')
        NewCardWindowController(new_card_window, self.store, selection)
    #@-node:eugene.20041103170715:on_add_button_clicked
    #@+node:eugene.20041103163321:on_learn_button_clicked
    def on_learn_button_clicked(self, widget):
        recall_window = GUIFactory.get_window('recall')
        RecallCardWindowController(recall_window, self.store, self.supermemo)
    #@-node:eugene.20041103163321:on_learn_button_clicked
    #@+node:eugene.20041111142758:on_delete_button_clicked
    def on_delete_button_clicked(self, button):
        # XXX: No confirmation dialog for now
        selection = self.view.items_treeview.get_selection()
        model, paths = selection.get_selected_rows()
        refs = [gtk.TreeRowReference(model, p) for p in paths]
        self.store.remove(refs)
    #@-node:eugene.20041111142758:on_delete_button_clicked
    #@+node:eugene.20041113122157:on_preferences_activate
    def on_preferences_activate(self, widget):
        PreferencesWindowController(PreferencesWindow(), self.store)
    #@-node:eugene.20041113122157:on_preferences_activate
    #@+node:eugene.20041103155350:on_delete_event
    def on_delete_event(self, widget, event):
        return gtk.FALSE
    #@-node:eugene.20041103155350:on_delete_event
    #@+node:eugene.20041103163226:on_quit_activate
    def on_quit_activate(self, widget, event=None):
        gtk.main_quit()
    #@nonl
    #@-node:eugene.20041103163226:on_quit_activate
    #@+node:eugene.20041103155434:on_destroy
    def on_destroy(self, widget):
        self.on_quit_activate(widget)
    #@nonl
    #@-node:eugene.20041103155434:on_destroy
    #@-others
#@nonl
#@-node:eugene.20041103155300:class SnakeMemoryWindowController
#@+node:eugene.20041103153955:class GladeSnakememoryWindow
class GladeSnakememoryWindow(GladeWindow):
    widgets = ['items_treeview']
    #@    @+others
    #@+node:eugene.20041103153955.1:__init__
    def __init__(self):
        GladeWindow.__init__(self, 'snakememory.glade')
        self.items_treeview = self.widget_tree.get_widget('items_treeview')
        selection = self.items_treeview.get_selection()
        selection.set_mode(gtk.SELECTION_MULTIPLE)
    
        column = gtk.TreeViewColumn(_('Question'), gtk.CellRendererText(), text=1)
        self.items_treeview.append_column(column)
        column = gtk.TreeViewColumn(_('Answer'), gtk.CellRendererText(), text=2)
        self.items_treeview.append_column(column)
    
    
    
    
    #@-node:eugene.20041103153955.1:__init__
    #@-others
#@nonl
#@-node:eugene.20041103153955:class GladeSnakememoryWindow
#@-node:eugene.20041103171033:Main application Window
#@+node:eugene.20041103153005:main
def main():
    window = GUIFactory.get_window('snakememory')
    SnakeMemoryWindowController(window)
    gtk.main()
#@nonl
#@-node:eugene.20041103153005:main
#@-others
if __name__ == '__main__':
    main()
#@-node:eugene.20041103145917:@thin snakememory.py
#@-leo

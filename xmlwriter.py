#@+leo-ver=4-thin
#@+node:eugene.20041029161735:@thin xmlwriter.py
#@@language python
#@<< xmlwriter declarations >>
#@+node:eugene.20041029161735.1:<< xmlwriter declarations >>
# A simple XML-generator# Originally Lars Marius Garshol, September 1998
# http://mail.python.org/pipermail/xml-sig/1998-September/000347.html
# Changes by Uche Ogbuji April 2003
# *  unicode support: accept encoding argument and use Python codecs
#    for correct character output
# *  switch from deprecated string module to string methods
# *  use PEP 8 style

import sys
import codecs

#@-node:eugene.20041029161735.1:<< xmlwriter declarations >>
#@nl
#@+others
#@+node:eugene.20041029161735.2:class XMLWriter
class XMLWriter:
    #@	@+others
    #@+node:eugene.20041029161735.3:__init__
    def __init__(self, out=sys.stdout, encoding="utf-8", indent=u"  "):
        """
        out      - a stream for the output
        encoding - an encoding used to wrap the output for unicode
        indent   - white space used for indentation
        """
        wrapper = codecs.lookup(encoding)[3]
        self.out = wrapper(out)
        self.stack = []
        self.indent = indent
        self.out.write(u'<?xml version="1.0" encoding="%s"?>\n' \
                       % encoding)
    #@-node:eugene.20041029161735.3:__init__
    #@+node:eugene.20041029161735.4:doctype
    def doctype(self, root, pubid, sysid):
        """
        Create a document type declaration (no internal subset)
        """
        if pubid == None:
            self.out.write(
                u"<!DOCTYPE %s SYSTEM '%s'>\n" % (root, sysid))
        else:
            self.out.write(
                u"<!DOCTYPE %s PUBLIC '%s' '%s'>\n" \
                % (root, pubid, sysid))
    #@-node:eugene.20041029161735.4:doctype
    #@+node:eugene.20041029161735.5:push
    def push(self, elem, attrs={}):
        """
        Create an element which will have child elements
        """
        self.__indent()
        self.out.write("<" + elem)
        for (a, v) in attrs.items():
            self.out.write(u" %s='%s'" % (a, self.__escape_attr(v)))
        self.out.write(u">\n")
        self.stack.append(elem)
    #@-node:eugene.20041029161735.5:push
    #@+node:eugene.20041029161735.6:elem
    def elem(self, elem, content, attrs={}):
        """
        Create an element with text content only
        """
        self.__indent()
        self.out.write(u"<" + elem)
        for (a, v) in attrs.items():
            self.out.write(u" %s='%s'" % (a, self.__escape_attr(v)))
        self.out.write(u">%s</%s>\n" \
                       % (self.__escape_cont(content), elem))
    #@-node:eugene.20041029161735.6:elem
    #@+node:eugene.20041029161735.7:empty
    def empty(self, elem, attrs={}):
        """
        Create an empty element
        """
        self.__indent()
        self.out.write(u"<"+elem)
        for a in attrs.items():
            self.out.write(u" %s='%s'" % a)
        self.out.write(u"/>\n")
    #@-node:eugene.20041029161735.7:empty
    #@+node:eugene.20041102153549:content
    def content(self, content):
        """
        Create simple text content as part of a mixed content element
        """
        self.out.write(self.__escape_cont(content))
    #@nonl
    #@-node:eugene.20041102153549:content
    #@+node:eugene.20041029161735.8:pop
    def pop(self):
        """
        Close an element started with the push() method
        """
        elem=self.stack[-1]
        del self.stack[-1]
        self.__indent()
        self.out.write(u"</%s>\n" % elem)
    #@-node:eugene.20041029161735.8:pop
    #@+node:eugene.20041029161735.9:__indent
    def __indent(self):
        self.out.write(self.indent * (len(self.stack) * 2))
    #@-node:eugene.20041029161735.9:__indent
    #@+node:eugene.20041029161735.10:__escape_cont
    def __escape_cont(self, text):
        text = str(text)
        return text.replace(u"&", u"&amp;")\
               .replace(u"<", u"&lt;")
    #@-node:eugene.20041029161735.10:__escape_cont
    #@+node:eugene.20041029161735.11:__escape_attr
    def __escape_attr(self, text):
        return text.replace(u"&", u"&amp;") \
               .replace(u"'", u"&apos;").replace(u"<", u"&lt;")
    #@-node:eugene.20041029161735.11:__escape_attr
    #@-others
#@-node:eugene.20041029161735.2:class XMLWriter
#@-others
#@-node:eugene.20041029161735:@thin xmlwriter.py
#@-leo

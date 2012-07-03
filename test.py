#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sigma
# Copyright 2011-2012 Grigory Petrov
# See LICENSE for details.

##  Simple tests.

import sys
sys.dont_write_bytecode = True

import sigma

assert sigma.parse( """
#!/usr/bin/python

##{ print( "foo" )
##}
##@ This is TOC.
""".strip() ) == [
  sigma.TagTxt( anchor = "##", raw = [ "#!/usr/bin/python", "" ] ),
  sigma.TagCode( anchor = "##", raw = [ "##{ print( \"foo\" )", "##}" ] ),
  sigma.TagToc( anchor = "##", raw = [ "##@ This is TOC." ] )
]

assert sigma.parse( """
#!/usr/bin/python

##{ print( "foo" )
##}
""".strip() )[ 1 ].codeLines() == [
  "print( \"foo\" )"
]

assert sigma.preprocess( """
#!/usr/bin/python

##{ print( "foo" )
##}
""".strip() ) == """
#!/usr/bin/python

##{ print( "foo" )
foo
##}
""".strip()

assert sigma.preprocess( """
#!/usr/bin/python

##{ print( "foo" )
foo
##}
""".strip() ) == """
#!/usr/bin/python

##{ print( "foo" )
foo
##}
""".strip()

assert sigma.preprocess( """
#!/usr/bin/python

##{ print( "foo" )
foo
bar
##}
""".strip() ) == """
#!/usr/bin/python

##{ print( "foo" )
foo
##}
""".strip()


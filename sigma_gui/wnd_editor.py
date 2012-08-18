#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pu
import pmq
import sigma

class WndEditor( pu.Wnd ) :

  def __init__( self ) :
    super( WndEditor, self ).__init__()
    with pu.Menu( parent = self ) :
      with pu.Menu() :
        pu.o.setText( "App" )
        with pu.MenuItem( name = 'settings' ) :
          pu.o.setText( "Settings" )
        with pu.MenuItem( name = 'exit' ) :
          pu.o.setText( "Exit" )
      with pu.Menu() :
        pu.o.setText( "File" )
        with pu.MenuItem( name = 'fopen' ) :
          pu.o.setText( "Open (C-O)" )
      with pu.Menu() :
        pu.o.setText( "Tools" )
        with pu.MenuItem( name = 'toc' ) :
          pu.o.setText( "TOC (C-S-F3)" )
    with pu.Rack( parent = self ) :
      with pu.Text( name = 'text' ) : pass
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.__updateCaption()
    self.bind( '<Control-o>', lambda _ : self.m_on_fopen() )
    self.bind( '<Control-Shift-F3>', lambda _ : self.m_on_toc() )

  def m_start( self ) :
    sName = "geometry_{0}".format( self.name() )
    sGeometry = pmq.request( 'm_cfg_get', sName )
    if sGeometry :
      self.geometry( sGeometry )
    else :
      self.setSize( 512, 384 )
      self.center()

  def m_shutdown( self ) :
    sName = "geometry_{0}".format( self.name() )
    pmq.post( 'm_cfg_set', sName, self.geometry() )

  def m_on_exit( self ) :
    pmq.stop()

  def __updateCaption( self, file = None ) :
    if file is None :
      self.setCaption( "Sigma: Editor" )
    else :
      self.setCaption( "Sigma: Editor: \"{0}\"".format( file ) )

  def m_on_fopen( self ) :
    sName = pu.askOpenFileName()
    try :
      with open( sName ) as oFile :
        self.o[ 'text' ].setText( oFile.read() )
        self.__updateCaption( sName )
    except IOError :
      pu.showMessage( "Failed to open file", type = 'error' )

  def m_on_toc( self ) :
    sText = self.o[ 'text' ].getText()
    lTags = [ o for o in sigma.parse( sText ) if o.isToc() ]
    pmq.post( 'm_toc', lTags )


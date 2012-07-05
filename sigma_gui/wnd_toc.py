#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys

if sys.platform == 'darwin' :
  import Cocoa

import pu
import pmq

class WndToc( pu.Wnd ) :

  def __init__( self ) :
    super( WndToc, self ).__init__()
    with pu.Rack( parent = self ) :
      with pu.Stack() as this :
        self.m_oStack = this
        with pu.Label( name = 'info' ) as this :
          this.setText( "Loading ..." )
          this.alignCenter()
        with pu.List( name = 'content' ) as this :
          self.m_oItems = this
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.setCaption( "Sigma: TOC" )
    self.bind( '<Return>', self.__onEnter )
    self.bind( '<Escape>', self.__onEscape )
    ##  Used with external editor.
    self.m_fEditor = False

  def m_startup( self ) :
    sGeometry = pmq.request( 'm_geometry_get', 'toc' )
    if sGeometry :
      self.geometry( sGeometry )
    else :
      self.center( 256, 256 )

  ##x Overloads |pu.Wnd|.
  def show( self, i_fShow = True ) :
    if self.m_fEditor :
      ##! Can't use |pmq.request()| since this will freeze GUI mainloop
      ##  and geometry retrieval enumerates HWND and requires main loop
      ##  to operate.
      pmq.post( 'm_editor_geometry_get' )
    else :
      super( WndToc, self ).show( i_fShow )

  def m_editor_geometry( self, gGeometry ) :
    if self.m_fEditor :
      if gGeometry is not None :
        nParentX, nParentY, nParentCx, nParentCy = gGeometry
        nCx = nParentCx / 2
        nCy = nParentCy / 2
        nX = nParentX + (nParentCx - nCx) / 2
        nY = nParentY + (nParentCy - nCy) / 2
        self.geometry( "{0}x{1}+{2}+{3}".format( nCx, nCy, nX, nY ) )
      super( WndToc, self ).show()
      ##  On OSX window will not get focus.
      if sys.platform == 'darwin' :
        pmq.post( 'm_wndtoc_activate' )

  def m_wndtoc_activate( self ) :
    Cocoa.NSApp.activateIgnoringOtherApps_( Cocoa.YES )

  def m_editor_use( self ) :
    self.m_fEditor = True

  def m_shutdown( self ) :
    pmq.post( 'm_geometry_set', 'toc', self.geometry() )

  def m_toc( self, i_lTags ) :
    for oTag in i_lTags :
      self.m_oItems.append( text = oTag.value(), baton = oTag )
    self.m_oStack.setCurrent( 'content' )
    self.m_oItems.focus_set()

  def __onEnter( self, i_oEvent ) :
    lItems = self.m_oItems.selection()
    if len( lItems ) :
      pmq.post( 'm_toc_select', self.m_oItems.idToBaton( lItems[ 0 ] ) )
      pmq.stop()

  def __onEscape( self, i_oEvent ) :
    pmq.stop()


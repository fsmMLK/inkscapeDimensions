# -*- coding: utf-8 -*-
#!/usr/bin/python

import inkex
import inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy_Draw as inkDraw
import math
import numpy as np

      
class lineSegment(inkBase.inkscapeMadeEasy):
  def __init__(self,Pstart,Pend,normalDirection='R'):
    self.Pstart=np.array(Pstart)
    self.Pend=np.array(Pend)
    [self.length,self.theta,self.t_versor,self.n_versor] = self.getSegmentFromPoints([Pstart,Pend],normalDirection)
    
    while self.theta<0:
      self.theta+=2.0*math.pi
    
      
  def getPointAtLength(self,length):
    return self.Pstart + length*self.t_versor

def getPosArc(versor1,versor2,deltaTheta1=None,deltaTheta2=None,flagInside=True):
  
  theta=math.acos(np.dot(versor1,versor2))
  if deltaTheta1 is None and deltaTheta2 is None:
    self.displayMsg('The two deltaThetas cannot be simultaneously None! Quitting...')
    return []
  
  if deltaTheta1 is not None and deltaTheta2 is not None:
    self.displayMsg('The two deltaThetas cannot be simultaneously not None! Quitting...')
    return []
  
  mat_A = np.row_stack((versor1,versor2))
  if abs(np.linalg.det(mat_A))<1e-9:
    if theta<0.1:
      if deltaTheta2 is None:
        if flagInside:
          w=rotateVector(versor1,+deltaTheta1)
        else:
          w=rotateVector(versor1,-deltaTheta1)
      if deltaTheta1 is None:
        if flagInside:
          w=rotateVector(versor2,-deltaTheta2)
        else:
          w=rotateVector(versor2,+deltaTheta2)
    if theta > 0.99*math.pi:
      if deltaTheta2 is None:
        if flagInside:
          w=rotateVector(versor1,-deltaTheta1)
        else:
          w=rotateVector(versor1,+deltaTheta1)
      if deltaTheta1 is None:
        if flagInside:
          w=rotateVector(versor2,+deltaTheta2)
        else:
          w=rotateVector(versor2,-deltaTheta2)
    return w

  if deltaTheta2 is None:
    if flagInside:
      vec_b= np.array([math.cos(deltaTheta1),math.cos(theta-deltaTheta1)])
    else:
      vec_b= np.array([math.cos(deltaTheta1),math.cos(theta+deltaTheta1)])
    
  
  if deltaTheta1 is None:
    if flagInside:
      vec_b= np.array([math.cos(theta-deltaTheta2),math.cos(deltaTheta2)])
    else:
      vec_b= np.array([math.cos(theta+deltaTheta2),math.cos(deltaTheta2)])
      
  w = np.linalg.solve(mat_A,vec_b)
  
  return w

def rotateVector(vector,theta):
  R=np.array([[math.cos(theta), -math.sin(theta)],[math.sin(theta), math.cos(theta)]])
  w=R.dot(vector)
  return w


#---------------------------------------------
class Dimensions(inkBase.inkscapeMadeEasy):
  def __init__(self):
    inkex.Effect.__init__(self)
    
    self.OptionParser.add_option("--tab",action="store", type="string",dest="tab", default="object") 
    
    self.OptionParser.add_option("--LINdirection",action="store", type="string",dest="LINdirection", default='none')
    self.OptionParser.add_option("--LINcontentsType",action="store", type="string",dest="LINcontentsType", default='none')
    self.OptionParser.add_option("--LINinvertSide", action="store", type="inkbool", dest="LINinvertSide", default=False)
    self.OptionParser.add_option("--LINinvertTextSide", action="store", type="inkbool", dest="LINinvertTextSide", default=False)
    self.OptionParser.add_option("--LINhorizontalText", action="store", type="inkbool", dest="LINhorizontalText", default=False)
    self.OptionParser.add_option("--LINsmalDimStyle", action="store", type="inkbool", dest="LINsmalDimStyle", default=False)
    
    self.OptionParser.add_option("--LINunit",action="store", type="string",dest="LINunit", default='none')
    self.OptionParser.add_option("--LINscaleDim", action="store", type="float", dest="LINscaleDim", default=1.0)
    self.OptionParser.add_option("--LINprecision", action="store", type="int", dest="LINprecision", default=2)
    self.OptionParser.add_option("--LINcustomContent",action="store", type="string",dest="LINcustomContent", default='none')

    self.OptionParser.add_option("--ANGdimPosition",action="store", type="string",dest="ANGdimPosition", default='center')
    self.OptionParser.add_option("--ANGannotationDistance", action="store", type="int", dest="ANGannotationDistance", default=50)
    self.OptionParser.add_option("--ANGcontentsType",action="store", type="string",dest="ANGcontentsType", default='none')    
    self.OptionParser.add_option("--ANGmarkCenter", action="store", type="inkbool", dest="ANGmarkCenter", default=False)
    self.OptionParser.add_option("--ANGinvertAngle", action="store", type="inkbool", dest="ANGinvertAngle", default=False)
    self.OptionParser.add_option("--ANGinvertTextSide", action="store", type="inkbool", dest="ANGinvertTextSide", default=False)
    self.OptionParser.add_option("--ANGhorizontalText", action="store", type="inkbool", dest="ANGhorizontalText", default=False)
    self.OptionParser.add_option("--ANGsmalDimStyle", action="store", type="inkbool", dest="ANGsmalDimStyle", default=False)
    
    self.OptionParser.add_option("--ANGunit",action="store", type="string",dest="ANGunit", default='none')
    self.OptionParser.add_option("--ANGprecision", action="store", type="int", dest="ANGprecision", default=2)
    self.OptionParser.add_option("--ANGcustomContent",action="store", type="string",dest="ANGcustomContent", default='none')

    self.OptionParser.add_option("--anotationScale", action="store", type="float", dest="anotationScale", default=1.0)
    self.OptionParser.add_option("--anotationText",action="store", type="string",dest="anotationText", default='none')
    self.OptionParser.add_option("--anotationFontSize", action="store", type="float", dest="anotationFontSize", default=1.0)
    
    self.OptionParser.add_option("--useLatex", action="store", type="inkbool", dest="useLatex", default=False)
    self.OptionParser.add_option("--removeAuxLine", action="store", type="inkbool", dest="removeAuxLine", default=False)
    
    self.OptionParser.add_option("--fontSize", action="store", type="float", dest="fontSize", default=1.0)
    self.OptionParser.add_option("--useDefaultProp", action="store", type="inkbool", dest="useDefaultProp", default=True)
    
    self.OptionParser.add_option("--lineWidthProp", action="store", type="float", dest="lineWidthProp", default=1.0)
    self.OptionParser.add_option("--arrowSizeProp", action="store", type="float", dest="arrowSizeProp", default=1.0)
    self.OptionParser.add_option("--auxLineOffsetProp", action="store", type="float", dest="auxLineOffsetProp", default=1.0)
    self.OptionParser.add_option("--auxLineExtensionProp", action="store", type="float", dest="auxLineExtensionProp", default=1.0)
    self.OptionParser.add_option("--textOffsetProp", action="store", type="float", dest="textOffsetProp", default=1.0)
    self.OptionParser.add_option("--dimSpacingProp", action="store", type="float", dest="dimSpacingProp", default=1.0)
    
    self.OptionParser.add_option("--textColor", action="store", type="string", dest="textColorOption", default='black')
    self.OptionParser.add_option("--colorPickerText", action="store", type="string", dest="colorPickerText", default='0') 
    self.OptionParser.add_option("--lineColor", action="store", type="string", dest="lineColorOption", default='black') 
    self.OptionParser.add_option("--colorPickerLine", action="store", type="string", dest="colorPickerLine", default='0') 
    
  def effect(self):
    
    so = self.options
    so.tab = so.tab.replace('"','')   # removes de exceding double quotes from the string
    
    #root_layer = self.current_layer
    root_layer = self.document.getroot()    
    
    # colors
    [self.textColor,alpha]=inkDraw.color.parseColorPicker(so.textColorOption,so.colorPickerText)
    [self.lineColor,alpha]=inkDraw.color.parseColorPicker(so.lineColorOption,so.colorPickerLine)
    
    # text size and font style
    if not inkDraw.useLatex:
      self.useLatex=False
    else:
      self.useLatex=so.useLatex
      inkDraw.useLatex=so.useLatex
       
    self.fontSize=so.fontSize
    if not so.useLatex:
      self.textStyle = inkDraw.textStyle.setSimpleColor(self.fontSize/0.75,justification='center',textColor=self.textColor)
    
    #dim configuration. All sizes are related to the text height
    if so.useDefaultProp:
      self.lineWidth = (so.fontSize/10.0)
      self.arrowSize = (so.fontSize)
      self.auxLineOffset = (so.fontSize/2.5)
      self.auxLineExtension = (so.fontSize/2.5)
      self.dimensionSpacing = (2.0*so.fontSize)
      self.textOffset = (so.fontSize/2.5)  # offset between symbol and text
    else:
      self.lineWidth = (so.fontSize/10.0)*so.lineWidthProp
      self.arrowSize = (so.fontSize)*so.arrowSizeProp
      self.auxLineOffset = (so.fontSize/2.5)*so.auxLineOffsetProp
      self.auxLineExtension = (so.fontSize/2.5)*so.auxLineExtensionProp
      self.dimensionSpacing = (2.0*so.fontSize)*so.dimSpacingProp
      self.textOffset = (so.fontSize/2.5)*so.textOffsetProp  # offset between symbol and text
    
    #linestyle
    self.auxiliaryLineStyle = inkDraw.lineStyle.set(lineWidth=self.lineWidth,lineColor=self.lineColor)

    renameMode = 1   # 0: do not create, , 1: overwrite  2: new name
    scaleMarker = 'scale (' + str(1.0/self.lineWidth) + ')'  # I have to scale it with respect to the lineWidth since marker's size is associated to width=1.0
    translateMarker ='translate (%s,0)' % self.arrowSize
    markerPath = 'M 0.0,0.0 L %f,%f L %f,%f L 0.0,0.0 z ' % (-self.arrowSize,self.arrowSize*math.tan(10*math.pi/180.0),-self.arrowSize,-self.arrowSize*math.tan(10*math.pi/180.0))
    arrowStart = inkDraw.marker.createMarker(self,'DimmArrow_Start',markerPath,renameMode,strokeColor=None,fillColor=self.lineColor,markerTransform= scaleMarker +'rotate(180)' + translateMarker)
    arrowEnd = inkDraw.marker.createMarker(self,'DimmArrow_End',markerPath,renameMode,strokeColor=None,fillColor=self.lineColor,markerTransform=scaleMarker + translateMarker)
    self.dimensionLineStyle = inkDraw.lineStyle.set(lineWidth=self.lineWidth,lineColor=self.lineColor,markerStart=arrowStart,markerEnd=arrowEnd)
    self.dimensionLineStyleSmall = inkDraw.lineStyle.set(lineWidth=self.lineWidth,lineColor=self.lineColor,markerEnd=arrowEnd)
    self.dimensionLineStyleSmall2 = inkDraw.lineStyle.set(lineWidth=self.lineWidth,lineColor=self.lineColor,markerStart=arrowStart)
      
    if so.tab=='Linear':
      # get points of selected object
      for id,element in self.selected.iteritems():
        [P1,P2] = self.getPointsLinDim(element,so.LINdirection)
        if not P1 or not P2:
          continue

        self.drawLinDim(root_layer,[P1,P2],direction=so.LINdirection,label='Dim',invertSide=so.LINinvertSide,textType=so.LINcontentsType,
                        customText=so.LINcustomContent,unit=so.LINunit,scale=so.LINscaleDim,precision=so.LINprecision,
                        horizontalText=so.LINhorizontalText,invertTextSide=so.LINinvertTextSide,smallDimension=so.LINsmalDimStyle)
        if so.removeAuxLine:
          self.removeElement(element)
    
    if so.tab=='Angular':
      # get points of selected object
      for id,element in self.selected.iteritems():
        self.drawAngDim(root_layer,element,label='Dim',invertAngle=so.ANGinvertAngle,textType=so.ANGcontentsType,
                        customText=so.ANGcustomContent,unit=so.ANGunit,precision=so.ANGprecision,horizontalText=so.ANGhorizontalText,
                        invertTextSide=so.ANGinvertTextSide,smallDimension=so.ANGsmalDimStyle,markCenter=so.ANGmarkCenter,
                        dimPosition=so.ANGdimPosition,dimDistance=so.ANGannotationDistance)
        if so.removeAuxLine:
          self.removeElement(element)

    if so.tab=='Arrow':
      for id,element in self.selected.iteritems():
        self.drawAnnotationArrow(root_layer,element,contents=so.anotationText,scale=so.anotationScale)
        self.removeElement(element)
   
  def drawAnnotationArrow(self,parent,auxElement,label='annotation',contents='textHere',nLines=1,scale=1.0):
    """ draws annotation Arrow
    
    parent: parent object
    auxElement: path with 3 points. the first will be the tip of the arrow, the next two demarks the area of the text
    label: label of the object (it can be repeated)
    contents: contents string
    nLines: number of lines of text
    scale: scale factor for the whole annotation (text, line width, marker size).  Default:  1.0
    """
    
    scaleMarker = 'scale (%f)' % (0.3)
    translateMarker ='translate (1.2,0)'
    markerPath = 'M 0.0,0.0 L 5.0,-5.0 L -12.5,0.0 L 5.0,5.0 L 0.0,0.0 z'
    arrowStart = inkDraw.marker.createMarker(self,'AnnArrow_Start',markerPath,RenameMode=1,strokeColor=None,fillColor=self.lineColor,markerTransform=translateMarker + scaleMarker )
      
    self.annotationLineStyle = inkDraw.lineStyle.set(lineWidth=self.lineWidth*scale,lineColor=self.lineColor,markerStart=arrowStart)
    
    group = self.createGroup(parent,label)
    
    [P1,P2,P3] = self.getPoints(auxElement)
    
    if P3[0]>P2[0]:
      justif='bl'
          
    else:
      justif='br'
        
    inkDraw.line.absCoords(group, [P1,P2,P3], offset=[0,0],label='dim', lineStyle=self.annotationLineStyle)
    
    if self.useLatex:
      pos=[P2[0],P2[1]-self.fontSize*scale/3.0]
    else:
      contents = contents.replace('\\\\', u'\\n')
      nLines=len(contents.split('\\n'))
      pos=[P2[0],P2[1]-self.fontSize*scale/3.0 - (nLines-1)*self.fontSize*scale*1.2]
    
    #text=inkDraw.text.write(self, contents, [P2[0],P2[1]-self.fontSize*scale/3.0 - (nLines-1)*self.fontSize*scale], group, fontSize=self.fontSize*scale, justification=justif)
    
    text=inkDraw.text.latex(self,group,contents,pos,textColor=self.textColor,fontSize=self.fontSize*scale,refPoint=justif)
    
    [Pmin,Pmax] =self.getBoundingBox(text)
    
    return group
    
  def centerMark(self,parent,pos):
      inkDraw.line.relCoords(parent, [ [-2.5,0], [5,0] ],offset=pos,lineStyle=self.auxiliaryLineStyle)
      inkDraw.line.relCoords(parent, [ [0,-2.5], [0,5] ],offset=pos,lineStyle=self.auxiliaryLineStyle)
 
  def drawAngDim(self,parent,auxElem,label='Dim',invertAngle=False,textType='dimension',customText='',
                 unit='deg',precision=2,horizontalText=False,invertTextSide=False,smallDimension=False,markCenter=False,dimPosition='exterior',dimDistance=50):
    """ draws angular dimension
    
    parent: parent object
    auxElem: element defining the angle. It must be a path with 3 or 4 vertices
    label: label of the object (it can be repeated)
    invertAngle: selects the complementary angle
    textType: type of text. values  'dimension' (default), 'custom'
    customText: text to be added. Used only if textType='custom'
    unit: dimmension unit. 'deg', 'rad', 'radPi'. Default: deg
    precision: number of decimals. Used only if textType='dimension'
    horizontalText: places text horizontally despite dimension orientation. Default: False
    invertTextSide: invert text placement (above, below the dimmension line
    markCenter: creates a mark at the center point
    dimPosition: position of the annotation arrow.  'interior', 'exterior'
    dimDistance: Distance along the segments where the dimension arrow will be placed. Values in percentage [0 to 100]. Used only if dimPosition='interior'
    """
    
    group = self.createGroup(parent,label)
    
    listPoints = self.getPoints(auxElem)

    if len(listPoints) == 3:
      auxElemType = '3points'
      segment1=lineSegment( listPoints[1], listPoints[0])
      segment2=lineSegment( listPoints[1], listPoints[2])
        
    if len(listPoints) == 4:
      auxElemType = '4points'
      segment1=lineSegment( listPoints[1], listPoints[0])
      segment2=lineSegment( listPoints[2], listPoints[3])

      
    #computes the center
    if auxElemType == '3points':
      centerPoint = segment1.Pstart.tolist()
        
    if auxElemType == '4points':
      mat_A = np.column_stack((segment1.t_versor,segment2.t_versor))
      if abs(np.linalg.det(mat_A))<1e-9:
        self.displayMsg('The two segments cannot be parallel! Quitting...')
        return
      
      [alpha,beta] = np.linalg.solve(mat_A,segment2.Pstart - segment1.Pstart)
      
      centerPoint = segment1.getPointAtLength(alpha)
      
      length1=segment1.length
      length2=segment2.length
      
      # recompute the segments, using the center point as starting point
      segment1=lineSegment( centerPoint, listPoints[0])
      segment2=lineSegment( centerPoint, listPoints[3])
            
    # makes sure the first segment has smaller theta
    if segment1.theta > segment2.theta:
      segment1 , segment2 = segment2 , segment1 # swaps variables
        
    if markCenter:
      inkDraw.line.relCoords(group, [ [-self.arrowSize/2.0,0], [self.arrowSize,0] ],offset=centerPoint,lineStyle=self.auxiliaryLineStyle)
      inkDraw.line.relCoords(group, [ [0,-self.arrowSize/2.0], [0,self.arrowSize] ],offset=centerPoint,lineStyle=self.auxiliaryLineStyle)
    
    
    if not invertAngle: # values between [0,pi] (closed interval)
      deltaTheta=math.acos(np.dot(segment1.t_versor,segment2.t_versor))
    else:
      deltaTheta=2.0*math.pi-math.acos(np.dot(segment1.t_versor,segment2.t_versor))

    # dimension position
    if dimPosition=='exterior':
      DimLineRadius=max(segment1.length,segment2.length) + self.auxLineOffset + self.dimensionSpacing
    if dimPosition=='interior':  
        DimLineRadius=max(max(segment1.length,segment2.length)*dimDistance/100.0, 2.5*self.arrowSize/deltaTheta) # the multiplicagtive factor MUST be > 2.0
    
    # text string 
    if textType=='dimension':
      
      if unit == 'rad':
        valueStr = '%.*f' % (precision, deltaTheta)
          
      if unit == 'radPi':
        deltaTheta=deltaTheta/math.pi
        valueStr = '%.*f' % (precision, deltaTheta)
        if self.useLatex:
          valueStr='$%s\pi$' % valueStr
        else:
          valueStr=valueStr + 'π'
      
      if unit == 'deg':
        deltaTheta*=180.0/math.pi
        valueStr = '%.*f' % (precision, deltaTheta)
        if self.useLatex:
          valueStr='\SI{%s}{\degree}' % valueStr
        else:
          valueStr=valueStr + '°'
          
    else:
      valueStr=customText

    #auxiliary lines
    if dimPosition=='exterior':
      L1start = segment1.getPointAtLength(segment1.length + self.auxLineOffset)
      L2start = segment2.getPointAtLength(segment2.length + self.auxLineOffset)
          
      L1end = segment1.getPointAtLength(DimLineRadius + self.auxLineExtension)
      L2end = segment2.getPointAtLength(DimLineRadius + self.auxLineExtension)
          
      inkDraw.line.absCoords(group, [L1start,L1end],offset=[0,0],lineStyle=self.auxiliaryLineStyle)
      inkDraw.line.absCoords(group, [L2start,L2end],offset=[0,0],lineStyle=self.auxiliaryLineStyle)
    
    if dimPosition=='interior':
      if DimLineRadius>segment1.length + self.auxLineOffset:
        L1start = segment1.getPointAtLength(segment1.length + self.auxLineOffset)
        L1end = segment1.getPointAtLength(DimLineRadius + self.auxLineExtension)
        inkDraw.line.absCoords(group, [L1start,L1end],offset=[0,0],lineStyle=self.auxiliaryLineStyle)
      if DimLineRadius>segment2.length + self.auxLineOffset:
        L2start = segment2.getPointAtLength(segment2.length + self.auxLineOffset)
        L2end = segment2.getPointAtLength(DimLineRadius + self.auxLineExtension)
        inkDraw.line.absCoords(group, [L2start,L2end],offset=[0,0],lineStyle=self.auxiliaryLineStyle)
      
      
    # draw dimension line
    theta_arrow=self.arrowSize/DimLineRadius
    theta_line=self.dimensionSpacing/DimLineRadius
          
    if not smallDimension:
        if invertAngle:
          flagInside=False
          if abs(segment2.theta-segment1.theta) == math.pi:
            flagLargeAngle=False
          else:
            flagLargeAngle=True
          if abs(segment2.theta-segment1.theta) < math.pi: 
            flagRightOf=True
          else:
            flagRightOf=False

        else:
          flagInside=True
          flagLargeAngle=False
          if abs(segment2.theta-segment1.theta) < math.pi:
            flagRightOf=False
          else:
            flagRightOf=True

        P1=getPosArc(segment1.t_versor,segment2.t_versor,deltaTheta1=theta_arrow,flagInside=flagInside)*DimLineRadius
        P2=getPosArc(segment1.t_versor,segment2.t_versor,deltaTheta2=theta_arrow,flagInside=flagInside)*DimLineRadius
          
        inkDraw.arc.startEndRadius(group, P1, P2, DimLineRadius, offset=centerPoint, lineStyle=self.dimensionLineStyle, flagRightOf=flagRightOf,largeArc=flagLargeAngle)
    else:
      if invertAngle:
        flagInside=True
      
      else:
        flagInside=False
        
      Pa1=getPosArc(segment1.t_versor,segment2.t_versor,deltaTheta1=theta_arrow+theta_line,flagInside=flagInside)*DimLineRadius
      Pa2=getPosArc(segment1.t_versor,segment2.t_versor,deltaTheta1=theta_arrow,flagInside=flagInside)*DimLineRadius
      Pb1=getPosArc(segment1.t_versor,segment2.t_versor,deltaTheta2=theta_arrow+theta_line,flagInside=flagInside)*DimLineRadius
      Pb2=getPosArc(segment1.t_versor,segment2.t_versor,deltaTheta2=theta_arrow,flagInside=flagInside)*DimLineRadius

      if abs(segment2.theta-segment1.theta) < math.pi:
        
        if invertAngle:
          flagRightOf=True
          line1=self.dimensionLineStyleSmall2
          line2=self.dimensionLineStyleSmall
        else:
          flagRightOf=False
          line1=self.dimensionLineStyleSmall
          line2=self.dimensionLineStyleSmall2

      else:
        if invertAngle:
          flagRightOf=False
          line1=self.dimensionLineStyleSmall
          line2=self.dimensionLineStyleSmall2
        else:
          flagRightOf=True
          line1=self.dimensionLineStyleSmall2
          line2=self.dimensionLineStyleSmall
        
      inkDraw.arc.startEndRadius(group, Pa1, Pa2, DimLineRadius, offset=centerPoint, lineStyle=line1, flagRightOf=flagRightOf)
      inkDraw.arc.startEndRadius(group, Pb1, Pb2, DimLineRadius, offset=centerPoint, lineStyle=line2, flagRightOf=not flagRightOf)

    #dimension
    
    #creates the segment structure passing at the center of the dimension line
    if np.dot(segment1.t_versor,segment2.t_versor)>=0.99:  # theta=0
      if invertAngle:
        bissectorVector=-segment1.t_versor
      else:
        bissectorVector=segment1.t_versor
        
    if np.dot(segment1.t_versor,segment2.t_versor)<=-0.99:  # theta=pi
      if invertAngle:
        bissectorVector=np.array( [-segment1.t_versor[1],segment1.t_versor[0]])
      else:
        bissectorVector=np.array( [segment1.t_versor[1],-segment1.t_versor[0]])
        
    if -0.99<np.dot(segment1.t_versor,segment2.t_versor)<0.99:  # 0<theta<pi
      if invertAngle:
        bissectorVector=-(segment1.t_versor+segment2.t_versor)
      else:
        bissectorVector=segment1.t_versor+segment2.t_versor

    segmentCenter=lineSegment( centerPoint, [ centerPoint[0]+bissectorVector[0] , centerPoint[1]+bissectorVector[1] ])
      
    if valueStr!='':
      if not smallDimension:  # regular dimension style
        if invertTextSide:
          posDim=segmentCenter.getPointAtLength(DimLineRadius - self.textOffset)
        else:
          posDim=segmentCenter.getPointAtLength(DimLineRadius + self.textOffset)
          
      else:  # small dimension style
        posDim=segmentCenter.getPointAtLength(DimLineRadius)
      
      #self.centerMark(group,posDim)
      #inkDraw.text.write(self, '1) %.*f' % (0,segment1.theta*180/math.pi), segment1.Pend, group, fontSize=self.fontSize, justification='center', angleDeg=0.0)
      #inkDraw.text.write(self, '2) %.*f' % (0,segment2.theta*180/math.pi), segment2.Pend, group, fontSize=self.fontSize, justification='center', angleDeg=0.0)
      #inkDraw.circle.centerRadius(group, centerPoint, radius=1.0)
      
      #inkDraw.text.write(self, '%.*f' % (1,theta*180/math.pi), posDim, group, fontSize=self.fontSize, justification='center', angleDeg=0.0)
      
      if horizontalText:
        angle=0
        
        if not smallDimension:  # regular dimension style
          theta_deg=segmentCenter.theta*(180.0/math.pi)

          justifRL='c'
          justifTB='c'
            
          if invertTextSide:
            if theta_deg<=80 or theta_deg>=280:
              justifRL='r'
            if 100<=theta_deg<=260:
              justifRL='l'

            if 10<=theta_deg<=170:
              justifTB='b'
            if 190<=theta_deg<=350:
              justifTB='t'
          else:
            if theta_deg<=80 or theta_deg>=280:
              justifRL='l'
            if 100<=theta_deg<=260:
              justifRL='r'

            if 10<=theta_deg<=170:
              justifTB='t'
            if 190<=theta_deg<=350:
              justifTB='b'
                
          justif = justifTB + justifRL
        else:
          justif='cc'
          
      else:
        if segmentCenter.t_versor[1]<0:
          angle=-(segmentCenter.theta+math.pi/2.0)*180/math.pi
        else:
          angle=-(segmentCenter.theta+3.0*math.pi/2.0)*180/math.pi
          
        if not smallDimension:  # regular dimension style
          if invertTextSide:
            if segmentCenter.t_versor[1]<0:
              justif='tc'
            else:
              justif='bc'
          else:
            if segmentCenter.t_versor[1]<0:
              justif='bc'
            else:
              justif='tc'
        else:
          justif='cc'

      inkDraw.text.latex(self,group,valueStr,posDim,fontSize=self.fontSize,refPoint=justif,textColor=self.textColor,LatexCommands=' ',angleDeg=angle)
      
  def drawLinDim(self,parent,points,direction,label='Dim',invertSide=False,textType='dimension',customText='',
                 unit=None,scale=1.0,precision=2,horizontalText=False,invertTextSide=False,smallDimension=False):
    """ draws linear dimension
    
    parent: parent object
    points: list of points [P1,P2]
    direction: dimension direction. values: 'vertical','horizontal','parallel'
    label: label of the object (it can be repeated)
    invertSide: invert side of the dimmension annotation. False (default): above(horiz./paral.),left (vert.)  True: below(horiz./paral.),right (vert.)
    textType: type of text. values  'dimension' (default), 'custom'
    customText: text to be added. Used only if textType='custom'
    unit: dimmension unit. Used only if textType='dimension'. use None to ignore. Default: None
    scale: scale factor for the dimension. Used only if textType='dimension'. Default: 1.0
    precision: number of decimals. Used only if textType='dimension'
    horizontalText: places text horizontally despite dimension orientation. Default: False
    invertTextSide: invert text placement. False (default): above line(horiz./paral.),left (vert.)  True: below line (horiz./paral.),right (vert.)
    
    """
    
    P1=np.array(points[0])
    P2=np.array(points[1])
    maxX=max(P1[0],P2[0])
    minX=min(P1[0],P2[0])
    
    maxY=max(P1[1],P2[1])
    minY=min(P1[1],P2[1])
    
    
    # tangent vector: from P1 to P2
    t_vector=P2-P1
    if direction=='horizontal':
      t_vector=np.array([t_vector[0],0])
      DeltaY=abs(P2[1]-P1[1])
    if direction=='vertical':
      t_vector=np.array([0,t_vector[1]])
      DeltaX=abs(P2[0]-P1[0])
      
    # normal vector: counter-clockwise with respect to tangent vector
    n_vector=np.array([t_vector[1],-t_vector[0]])
    
    #normalization  
    t_versor=t_vector/np.linalg.norm(t_vector) 
    n_versor=n_vector/np.linalg.norm(n_vector)
    
    #inkDraw.line.relCoords(parent, [(0.5*n_vector).tolist()],offset=P1.tolist(), lineStyle=inkDraw.lineStyle.setSimpleBlack(0.5))
    #inkDraw.line.relCoords(parent, [(0.5*t_vector).tolist()],offset=P1.tolist(), lineStyle=inkDraw.lineStyle.setSimpleBlack(0.5))
    
    # text string 
    if textType=='dimension':
      value=np.linalg.norm(n_vector)
      valueStr = '%.*f' % (precision, value*scale)
      
      if unit and unit !='none':
        if self.useLatex:
          valueStr='\SI{%s}{%s}' %(valueStr,unit)
        else:
          valueStr=valueStr + ' ' + unit
    else:
      valueStr=customText
        

    group = self.createGroup(parent,label)
    
    # auxiliary lines
    if invertSide:
      L1start= P1-n_versor*self.auxLineOffset
      L2start= P2-n_versor*self.auxLineOffset
    else:
      L1start= P1+n_versor*self.auxLineOffset
      L2start= P2+n_versor*self.auxLineOffset
    
    if direction=='horizontal':
      if invertSide:  # below
        if P1[1]<P2[1]:
          L1endRel=-n_versor*(DeltaY + self.dimensionSpacing+self.auxLineExtension)
          L2endRel=-n_versor*(self.dimensionSpacing+self.auxLineExtension)
        else:
          L1endRel=-n_versor*(self.dimensionSpacing+self.auxLineExtension)
          L2endRel=-n_versor*(DeltaY + self.dimensionSpacing+self.auxLineExtension)

      else:  #above
        if P1[1]<P2[1]:
          L1endRel=n_versor*(self.dimensionSpacing+self.auxLineExtension)
          L2endRel=n_versor*(DeltaY + self.dimensionSpacing+self.auxLineExtension)
        else:
          L1endRel=n_versor*(DeltaY + self.dimensionSpacing+self.auxLineExtension)
          L2endRel=n_versor*(self.dimensionSpacing+self.auxLineExtension)
    
    if direction=='vertical':
      if invertSide:  # to the right
        if P1[0]<P2[0]:
          L1endRel=-n_versor*(DeltaX + self.dimensionSpacing+self.auxLineExtension)
          L2endRel=-n_versor*(self.dimensionSpacing+self.auxLineExtension)
        else:
          L1endRel=-n_versor*(self.dimensionSpacing+self.auxLineExtension)
          L2endRel=-n_versor*(DeltaX + self.dimensionSpacing+self.auxLineExtension)

      else:  # to the left
        if P1[0]<P2[0]:
          L1endRel=n_versor*(self.dimensionSpacing+self.auxLineExtension)
          L2endRel=n_versor*(DeltaX + self.dimensionSpacing+self.auxLineExtension)
        else:
          L1endRel=n_versor*(DeltaX + self.dimensionSpacing+self.auxLineExtension)
          L2endRel=n_versor*(self.dimensionSpacing+self.auxLineExtension)
          
    if direction=='parallel':
      if invertSide:  # below
        L1endRel = -n_versor*(self.dimensionSpacing+self.auxLineExtension)
      else:  #above
        L1endRel =  n_versor*(self.dimensionSpacing+self.auxLineExtension)
      L2endRel = L1endRel

    inkDraw.line.relCoords(group, [L1endRel.tolist()],offset=L1start.tolist(),lineStyle=self.auxiliaryLineStyle)
    inkDraw.line.relCoords(group, [L2endRel.tolist()],offset=L2start.tolist(),lineStyle=self.auxiliaryLineStyle)


    # draw dimension line
    if not smallDimension:
      if invertSide:  # hor.:below    ver.:to the right    paral.:above
        Pstart=L1start+L1endRel+n_versor*(self.auxLineExtension)+t_versor*self.arrowSize
        Pend  =L2start+L2endRel+n_versor*(self.auxLineExtension)-t_versor*self.arrowSize
      else:  # hor.:above    ver.:to the left    paral.:above
        Pstart=L1start+L1endRel-n_versor*(self.auxLineExtension)+t_versor*self.arrowSize
        Pend  =L2start+L2endRel-n_versor*(self.auxLineExtension)-t_versor*self.arrowSize
  
      inkDraw.line.absCoords(group, [Pstart.tolist(),Pend.tolist()], offset=[0,0],label='dim', lineStyle=self.dimensionLineStyle)
    else:
      if invertSide:  # hor.:below    ver.:to the right    paral.:above
        Pstart=L1start+L1endRel+n_versor*(self.auxLineExtension)-t_versor*self.arrowSize
        Pend  =L2start+L2endRel+n_versor*(self.auxLineExtension)+t_versor*self.arrowSize
      else:  # hor.:above    ver.:to the left    paral.:above
        Pstart=L1start+L1endRel-n_versor*(self.auxLineExtension)-t_versor*self.arrowSize
        Pend  =L2start+L2endRel-n_versor*(self.auxLineExtension)+t_versor*self.arrowSize
      
      PextStart=Pstart-t_versor*self.dimensionSpacing
      PextEnd=Pend+t_versor*self.dimensionSpacing
        
      inkDraw.line.absCoords(group, [PextStart.tolist(),Pstart.tolist()], offset=[0,0],label='dim', lineStyle=self.dimensionLineStyleSmall)
      inkDraw.line.absCoords(group, [PextEnd.tolist(),Pend.tolist()], offset=[0,0],label='dim', lineStyle=self.dimensionLineStyleSmall)
      
      
    #dimension
    if valueStr!='':
      if not smallDimension:  # regular dimension style
        if invertTextSide:
          posDim=((Pstart+Pend)/2.0)-n_versor*self.textOffset
        else:
          posDim=((Pstart+Pend)/2.0)+n_versor*self.textOffset
      else:  # small dimension style
        if invertTextSide:
          posDim=((Pstart+Pend)/2.0)
        else:
          posDim=((Pstart+Pend)/2.0)
        
      if horizontalText:
        angle=0
        
        if not smallDimension:  # regular dimension style
          if direction=='vertical':
            posDim=posDim-t_versor*self.fontSize/2.0
          
          if direction=='horizontal':
            if invertTextSide:
              posDim=posDim-n_versor*self.fontSize
            
          if direction=='parallel':
            if n_versor[1]==0:
              posDim=posDim-t_versor*self.fontSize/2.0
            if n_versor[0]==0 and invertTextSide:
              posDim=posDim-n_versor*self.fontSize
            if n_versor[0]!=0 and n_versor[1]!=0:
              if invertTextSide:
                posDim=posDim-n_versor*self.fontSize/1.5

          if invertTextSide:
            if n_versor[0]<0:
                justif='bl'
            if n_versor[0]>0:
                justif='br'
            if n_versor[0]==0:
                justif='bc'
          else:
            if n_versor[0]<0:
                justif='br'
            if n_versor[0]>0:
                justif='bl'
            if n_versor[0]==0:
                justif='bc'
        else:
          justif='cc'
      else:
        angle=(180/math.pi)*math.atan2(-t_vector[1],t_vector[0])
        if not smallDimension:  # regular dimension style
          if invertTextSide:
            justif='tc'
          else:
            justif='bc'
        else:
          justif='cc'
          
      inkDraw.text.latex(self,group,valueStr,posDim,fontSize=self.fontSize,refPoint=justif,textColor=self.textColor,LatexCommands=' ',angleDeg=angle)

    return group
  
  
  def getPointsLinDim(self,element,LINdirection):
    """ Extracts the 2 end points from the Obj.
    
    Also checks if distance is zero and reorder the points so that

      - if LINdirection=='horizontal'  -> P1 is to the left
      - if LINdirection=='vertical'  -> P1 is below
      - if LINdirection=='parallel'  -> P1 is to the left. If line is vertical, ensures that P1 is below.
    
    :param element: element object
    :type element: element object
    :param LINdirection: orientation of the dimension: horizontal, vertical, parallel
    :type LINdirection: string

    
    :returns: [pointsList]
    
      - pointsList: list of points with the coordinates
    :rtype: list of list
    
    If the element does not have any transformation attribute, this function returns:
        transfAttrib=''
        transfMatrix=identity matrix
        
    **Example**
    
    >>> for id_elem,element in self.selected.iteritems():                    # iterates through all selected elements
    >>>   pointsList = self.getPointsLinDim(self,element,'horizontal')
    """

    [P1,P2] = self.getPoints(element)

    # sets the position to the viewport center
    position=self.getCenter(element)
    root_layer = self.document.getroot()  
    
    #inkDraw.text.write(self,'P1='+str(P1),position,root_layer,fontSize=self.fontSize,justification='center')
    #inkDraw.text.write(self,'P2='+str(P2),position,root_layer,fontSize=self.fontSize,justification='center')
    
    # check whether the line segment is valid and reorder if necessary
    if LINdirection=="horizontal":
      if P1[0]==P2[0]:
        inkDraw.text.write(self,'Error: horizontal dimension is zero.',position,root_layer,fontSize=self.fontSize,justification='center')
        return [None,None];
      if P2[0]<P1[0]: # makes sure P1 has smallest xcoords
        temp=P1
        P1=P2
        P2=temp
        
    if LINdirection=="vertical":
      if P1[1]==P2[1]:
        inkDraw.text.write(self,'Error: vertical dimension is zero.',position,root_layer,fontSize=self.fontSize,justification='center')
        return [None,None];
      if P2[1]>P1[1]: # makes sure P1 has smallest ycoords
        temp=P1
        P1=P2
        P2=temp
            
    if LINdirection=="parallel":
      if P1[0]==P2[0] and P1[1]==P2[1]:
        inkDraw.text.write(self,'Error: dimension is zero.',position,root_layer,fontSize=self.fontSize,justification='center')
        return [None,None];
      if P2[0]<P1[0]: # makes sure P1 has smallest xcoords
        temp=P1
        P1=P2
        P2=temp
        
      if P2[0]==P1[0]:
        if P2[1]>P1[1]:
          temp=P1
          P1=P2
          P2=temp
        
    return [P1,P2]
    

if __name__ == '__main__':
  dimension = Dimensions()
  dimension.affect()
    

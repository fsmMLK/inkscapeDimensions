# -*- coding: utf-8 -*-

# !/usr/bin/python

import math

import numpy as np

import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw


class lineSegment(inkBase.inkscapeMadeEasy):
    def __init__(self, Pstart, Pend, normalDirection='R'):
        self.Pstart = np.array(Pstart)
        self.Pend = np.array(Pend)
        [self.length, self.theta, self.t_versor, self.n_versor] = self.getSegmentFromPoints([Pstart, Pend], normalDirection)

        while self.theta < 0:
            self.theta += 2.0 * math.pi

    def getPointAtLength(self, length):
        return self.Pstart + length * self.t_versor


def getPosArc(versor1, versor2, deltaTheta1=None, deltaTheta2=None, flagInside=True):
    theta = math.acos(np.dot(versor1, versor2))
    if deltaTheta1 is None and deltaTheta2 is None:
        self.displayMsg('The two deltaThetas cannot be simultaneously None! Quitting...')
        return []

    if deltaTheta1 is not None and deltaTheta2 is not None:
        self.displayMsg('The two deltaThetas cannot be simultaneously not None! Quitting...')
        return []

    mat_A = np.row_stack((versor1, versor2))
    if abs(np.linalg.det(mat_A)) < 1e-9:
        if theta < 0.1:
            if deltaTheta2 is None:
                if flagInside:
                    w = rotateVector(versor1, +deltaTheta1)
                else:
                    w = rotateVector(versor1, -deltaTheta1)
            if deltaTheta1 is None:
                if flagInside:
                    w = rotateVector(versor2, -deltaTheta2)
                else:
                    w = rotateVector(versor2, +deltaTheta2)
        if theta > 0.99 * math.pi:
            if deltaTheta2 is None:
                if flagInside:
                    w = rotateVector(versor1, -deltaTheta1)
                else:
                    w = rotateVector(versor1, +deltaTheta1)
            if deltaTheta1 is None:
                if flagInside:
                    w = rotateVector(versor2, +deltaTheta2)
                else:
                    w = rotateVector(versor2, -deltaTheta2)
        return w

    if deltaTheta2 is None:
        if flagInside:
            vec_b = np.array([math.cos(deltaTheta1), math.cos(theta - deltaTheta1)])
        else:
            vec_b = np.array([math.cos(deltaTheta1), math.cos(theta + deltaTheta1)])

    if deltaTheta1 is None:
        if flagInside:
            vec_b = np.array([math.cos(theta - deltaTheta2), math.cos(deltaTheta2)])
        else:
            vec_b = np.array([math.cos(theta + deltaTheta2), math.cos(deltaTheta2)])

    w = np.linalg.solve(mat_A, vec_b)

    return w


def rotateVector(vector, theta):
    R = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
    w = R.dot(vector)
    return w


# ---------------------------------------------
class Dimensions(inkBase.inkscapeMadeEasy):
    def __init__(self):
        inkBase.inkscapeMadeEasy.__init__(self)

        self.arg_parser.add_argument("--tab", type=str, dest="tab", default="object")
        self.arg_parser.add_argument("--LinContents_subtab", type=str, dest="LinContents_subtab", default="object")
        self.arg_parser.add_argument("--AngContents_subtab", type=str, dest="AngContents_subtab", default="object")

        self.arg_parser.add_argument("--LINdirection", type=str, dest="LINdirection", default='none')
        self.arg_parser.add_argument("--LINinvertSide", type=self.bool, dest="LINinvertSide", default=False)
        self.arg_parser.add_argument("--LINinvertTextSide", type=self.bool, dest="LINinvertTextSide", default=False)
        self.arg_parser.add_argument("--LINhorizontalText", type=self.bool, dest="LINhorizontalText", default=False)
        self.arg_parser.add_argument("--LINsmalDimStyle", type=self.bool, dest="LINsmalDimStyle", default=False)

        self.arg_parser.add_argument("--LINunit", type=str, dest="LINunit", default='none')
        self.arg_parser.add_argument("--LINunitSymbol", type=self.bool, dest="LINunitSymbol", default=False)
        self.arg_parser.add_argument("--LINscaleDim", type=float, dest="LINscaleDim", default=1.0)
        self.arg_parser.add_argument("--LINprecision", type=int, dest="LINprecision", default=2)
        self.arg_parser.add_argument("--LINcustomContent", type=str, dest="LINcustomContent", default='none')

        self.arg_parser.add_argument("--ANGdimPosition", type=str, dest="ANGdimPosition", default='center')
        self.arg_parser.add_argument("--ANGannotationDistance", type=int, dest="ANGannotationDistance", default=50)
        self.arg_parser.add_argument("--ANGcontentsType", type=str, dest="ANGcontentsType", default='none')
        self.arg_parser.add_argument("--ANGmarkCenter", type=self.bool, dest="ANGmarkCenter", default=False)
        self.arg_parser.add_argument("--ANGinvertAngle", type=self.bool, dest="ANGinvertAngle", default=False)
        self.arg_parser.add_argument("--ANGinvertTextSide", type=self.bool, dest="ANGinvertTextSide", default=False)
        self.arg_parser.add_argument("--ANGhorizontalText", type=self.bool, dest="ANGhorizontalText", default=False)
        self.arg_parser.add_argument("--ANGsmalDimStyle", type=self.bool, dest="ANGsmalDimStyle", default=False)

        self.arg_parser.add_argument("--ANGunit", type=str, dest="ANGunit", default='none')
        self.arg_parser.add_argument("--ANGprecision", type=int, dest="ANGprecision", default=2)
        self.arg_parser.add_argument("--ANGcustomContent", type=str, dest="ANGcustomContent", default='none')

        self.arg_parser.add_argument("--anotationScale", type=float, dest="anotationScale", default=1.0)
        self.arg_parser.add_argument("--anotationText", type=str, dest="anotationText", default='none')
        self.arg_parser.add_argument("--anotationFontSize", type=float, dest="anotationFontSize", default=1.0)

        self.arg_parser.add_argument("--useLatex", type=self.bool, dest="useLatex", default=False)
        self.arg_parser.add_argument("--removeAuxLine", type=self.bool, dest="removeAuxLine", default=False)
        self.arg_parser.add_argument("--markerStyle", type=str, dest="markerStyle", default=False)

        self.arg_parser.add_argument("--fontSize", type=float, dest="fontSize", default=1.0)
        self.arg_parser.add_argument("--useDefaultProp", type=self.bool, dest="useDefaultProp", default=True)

        self.arg_parser.add_argument("--lineWidthProp", type=float, dest="lineWidthProp", default=1.0)
        self.arg_parser.add_argument("--arrowSizeProp", type=float, dest="arrowSizeProp", default=1.0)
        self.arg_parser.add_argument("--auxLineOffsetProp", type=float, dest="auxLineOffsetProp", default=1.0)
        self.arg_parser.add_argument("--auxLineExtensionProp", type=float, dest="auxLineExtensionProp", default=1.0)
        self.arg_parser.add_argument("--textOffsetProp", type=float, dest="textOffsetProp", default=1.0)
        self.arg_parser.add_argument("--dimSpacingProp", type=float, dest="dimSpacingProp", default=1.0)

        self.arg_parser.add_argument("--textColor", type=str, dest="textColorOption", default='black')
        self.arg_parser.add_argument("--colorPickerText", type=str, dest="colorPickerText", default='0')
        self.arg_parser.add_argument("--lineColor", type=str, dest="lineColorOption", default='black')
        self.arg_parser.add_argument("--colorPickerLine", type=str, dest="colorPickerLine", default='0')

    def effect(self):

        so = self.options
        so.tab = so.tab.replace('"', '')  # removes de exceding double quotes from the string

        self.documentUnit = self.getDocumentUnit()

        # root_layer = self.current_layer
        # root_layer = self.document.getroot()
        root_layer = self.getcurrentLayer()

        # colors
        self.textColor = inkDraw.color.parseColorPicker(so.textColorOption, so.colorPickerText)
        self.lineColor = inkDraw.color.parseColorPicker(so.lineColorOption, so.colorPickerLine)

        # text size and font style
        if not inkDraw.useLatex:
            self.useLatex = False
        else:
            self.useLatex = so.useLatex
            inkDraw.useLatex = so.useLatex

        self.fontSize = so.fontSize

        if not so.useLatex:
            self.textStyle = inkDraw.textStyle.setSimpleColor(self.fontSize / 0.75, justification='center', textColor=self.textColor)

        # dim configuration. All sizes are related to the text height
        if so.useDefaultProp:
            self.lineWidth = (self.fontSize / 10.0)
            self.arrowSize = (self.fontSize)
            self.auxLineOffset = (self.fontSize / 2.5)
            self.auxLineExtension = (self.fontSize / 2.5)
            self.dimensionSpacing = (2.0 * self.fontSize)
            self.textOffset = (self.fontSize / 2.5)  # offset between symbol and text
        else:
            self.lineWidth = (self.fontSize / 10.0) * so.lineWidthProp
            self.arrowSize = (self.fontSize) * so.arrowSizeProp
            self.auxLineOffset = (self.fontSize / 2.5) * so.auxLineOffsetProp
            self.auxLineExtension = (self.fontSize / 2.5) * so.auxLineExtensionProp
            self.dimensionSpacing = (2.0 * self.fontSize) * so.dimSpacingProp
            self.textOffset = (self.fontSize / 2.5) * so.textOffsetProp  # offset between symbol and text

        # linestyles
        self.auxiliaryLineStyle = inkDraw.lineStyle.set(lineWidth=self.lineWidth, lineColor=self.lineColor)

        renameMode = 2  # 0: do not create, , 1: overwrite  2: new name

        # I have to scale it with respect to the lineWidth since marker's size is associated to width=1.0
        scaleMarker = 'scale (' + str(1.0 / self.lineWidth) + ')'

        translateMarker = 'translate (%s,0)' % self.arrowSize
        markerPath = 'M 0.0,0.0 L %f,%f L %f,%f L 0.0,0.0 z ' % (
            -self.arrowSize, self.arrowSize * math.tan(10 * math.pi / 180.0), -self.arrowSize, -self.arrowSize * math.tan(10 * math.pi / 180.0))

        arrowStart = inkDraw.marker.createMarker(self, 'DimmArrow_Start', markerPath, renameMode, strokeColor=None, fillColor=self.lineColor,
                                                 markerTransform=scaleMarker + 'rotate(180)' + translateMarker)
        arrowEnd = inkDraw.marker.createMarker(self, 'DimmArrow_End', markerPath, renameMode, strokeColor=None, fillColor=self.lineColor,
                                               markerTransform=scaleMarker + translateMarker)

        if so.markerStyle == 'arrow':
            self.LINdimensionLineStyle = inkDraw.lineStyle.set(lineWidth=self.lineWidth, lineColor=self.lineColor, markerStart=arrowStart,
                                                               markerEnd=arrowEnd)

        if so.markerStyle == 'circle':
            marker = inkDraw.marker.createDotMarker(self, 'DimmCircle', renameMode, scale=0.05 / self.lineWidth * self.arrowSize, strokeColor=None,
                                                    fillColor=self.lineColor)
            self.LINdimensionLineStyle = inkDraw.lineStyle.set(lineWidth=self.lineWidth, lineColor=self.lineColor, markerStart=marker,
                                                               markerEnd=marker)

        if so.markerStyle == 'serif':
            markerPath = 'M -%f,%f L %f,-%f' % (0.5 * self.arrowSize, 0.5 * self.arrowSize, 0.5 * self.arrowSize, 0.5 * self.arrowSize)
            marker = inkDraw.marker.createMarker(self, 'DimmSerif', markerPath, renameMode, strokeColor=self.lineColor, lineWidth=self.lineWidth * 2,
                                                 markerTransform=scaleMarker)
            self.LINdimensionLineStyle = inkDraw.lineStyle.set(lineWidth=self.lineWidth, lineColor=self.lineColor, markerStart=marker,
                                                               markerEnd=marker)

        self.ANGdimensionLineStyle = inkDraw.lineStyle.set(lineWidth=self.lineWidth, lineColor=self.lineColor, markerStart=arrowStart,
                                                           markerEnd=arrowEnd)

        # used with smalldimension
        self.ANGdimensionLineStyleSmall = inkDraw.lineStyle.set(lineWidth=self.lineWidth, lineColor=self.lineColor, markerEnd=arrowEnd)
        self.ANGdimensionLineStyleSmall2 = inkDraw.lineStyle.set(lineWidth=self.lineWidth, lineColor=self.lineColor, markerStart=arrowStart)
        self.annotationLineStyle = inkDraw.lineStyle.set(lineWidth=self.lineWidth * so.anotationScale, lineColor=self.lineColor,
                                                         markerStart=arrowStart)

        if so.tab == 'Linear':
            # get points of selected object
            for id, element in self.svg.selected.items():
                [P1, P2] = self.getPointsLinDim(element, so.LINdirection)

                if P1 is None or P2 is None:
                    continue

                self.drawLinDim(root_layer, [P1, P2], direction=so.LINdirection, label='Dim', invertSide=so.LINinvertSide,
                                textType=so.LinContents_subtab, customText=so.LINcustomContent, unit=so.LINunit, unitSymbol=so.LINunitSymbol,
                                scale=so.LINscaleDim, precision=so.LINprecision, horizontalText=so.LINhorizontalText,
                                invertTextSide=so.LINinvertTextSide, smallDimension=so.LINsmalDimStyle)
                if so.removeAuxLine:
                    self.removeElement(element)

        if so.tab == 'Angular':
            # get points of selected object
            for id, element in self.svg.selected.items():
                self.drawAngDim(root_layer, element, label='Dim', invertAngle=so.ANGinvertAngle, textType=so.AngContents_subtab,
                                customText=so.ANGcustomContent, unit=so.ANGunit, precision=so.ANGprecision, horizontalText=so.ANGhorizontalText,
                                invertTextSide=so.ANGinvertTextSide, smallDimension=so.ANGsmalDimStyle, markCenter=so.ANGmarkCenter,
                                dimPosition=so.ANGdimPosition, dimDistance=so.ANGannotationDistance)
                if so.removeAuxLine:
                    self.removeElement(element)

        if so.tab == 'Arrow':
            for id, element in self.svg.selected.items():
                self.drawAnnotationArrow(root_layer, element, contents=so.anotationText, scale=so.anotationScale)
                self.removeElement(element)

    def drawAnnotationArrow(self, parent, auxElement, label='annotation', contents='textHere', nLines=1, scale=1.0):
        """ draws annotation Arrow

        parent: parent object
        auxElement: path with 3 points. the first will be the tip of the arrow,
                    the next two demarks the area of the text
        label: label of the object (it can be repeated)
        contents: contents string
        nLines: number of lines of text
        scale: scale factor for the whole annotation (text, line width, marker size).  Default:  1.0
        """

        group = self.createGroup(parent, label)

        [P1, P2, P3] = self.getPoints(auxElement)

        if P3[0] > P2[0]:
            justif = 'bl'
        else:
            justif = 'br'

        inkDraw.line.absCoords(group, [P1, P2, P3], offset=[0, 0], label='dim', lineStyle=self.annotationLineStyle)

        if self.useLatex:
            pos = [P2[0], P2[1] - self.fontSize * scale / 3.0]
            contents = r'\noindent ' + contents.replace('\\n', '\\newline ')
        else:
            contents = contents.replace('\\\\', '\\n')
            nLines = len(contents.split('\\n'))
            pos = [P2[0], P2[1] - self.fontSize * scale / 3.0 - (nLines - 1) * self.fontSize * scale * 1.2]

        text = inkDraw.text.latex(self, group, contents, pos, textColor=self.textColor, fontSize=self.fontSize * scale, refPoint=justif)

        [Pmin, Pmax] = self.getBoundingBox(text)

        return group

    def centerMark(self, parent, pos):
        inkDraw.line.relCoords(parent, [[-2.5, 0], [5, 0]], offset=pos, lineStyle=self.auxiliaryLineStyle)
        inkDraw.line.relCoords(parent, [[0, -2.5], [0, 5]], offset=pos, lineStyle=self.auxiliaryLineStyle)

    def drawAngDim(self, parent, auxElem, label='Dim', invertAngle=False, textType='dimension', customText='', unit='deg', precision=2,
                   horizontalText=False, invertTextSide=False, smallDimension=False, markCenter=False, dimPosition='exterior', dimDistance=50):
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
        dimDistance: Distance along the segments where the dimension arrow will be placed.
                     Values in percentage [0 to 100]. Used only if dimPosition='interior'
        """

        group = self.createGroup(parent, label)

        listPoints = self.getPoints(auxElem)

        if len(listPoints) == 3:
            auxElemType = '3points'
            segment1 = lineSegment(listPoints[1], listPoints[0])
            segment2 = lineSegment(listPoints[1], listPoints[2])

        if len(listPoints) == 4:
            auxElemType = '4points'
            segment1 = lineSegment(listPoints[1], listPoints[0])
            segment2 = lineSegment(listPoints[2], listPoints[3])

        # computes the center
        if auxElemType == '3points':
            centerPoint = segment1.Pstart.tolist()

        if auxElemType == '4points':
            mat_A = np.column_stack((segment1.t_versor, segment2.t_versor))
            if abs(np.linalg.det(mat_A)) < 1e-9:
                self.displayMsg('The two segments cannot be parallel! Quitting...')
                return

            [alpha, beta] = np.linalg.solve(mat_A, segment2.Pstart - segment1.Pstart)

            centerPoint = segment1.getPointAtLength(alpha)

            length1 = segment1.length
            length2 = segment2.length

            # recompute the segments, using the center point as starting point
            segment1 = lineSegment(centerPoint, listPoints[0])
            segment2 = lineSegment(centerPoint, listPoints[3])

        # makes sure the first segment has smaller theta
        if segment1.theta > segment2.theta:
            segment1, segment2 = segment2, segment1  # swaps variables

        if markCenter:
            inkDraw.line.relCoords(group, [[-self.arrowSize / 2.0, 0], [self.arrowSize, 0]], offset=centerPoint, lineStyle=self.auxiliaryLineStyle)
            inkDraw.line.relCoords(group, [[0, -self.arrowSize / 2.0], [0, self.arrowSize]], offset=centerPoint, lineStyle=self.auxiliaryLineStyle)

        if not invertAngle:  # values between [0,pi] (closed interval)
            deltaTheta = math.acos(np.dot(segment1.t_versor, segment2.t_versor))
        else:
            deltaTheta = 2.0 * math.pi - math.acos(np.dot(segment1.t_versor, segment2.t_versor))

        # dimension position
        if dimPosition == 'exterior':
            DimLineRadius = max(segment1.length, segment2.length) + self.auxLineOffset + self.dimensionSpacing
        if dimPosition == 'interior':
            DimLineRadius = max(max(segment1.length, segment2.length) * dimDistance / 100.0,
                                2.5 * self.arrowSize / deltaTheta)  # the multiplicagtive factor MUST be > 2.0

        # text string
        if textType == 'dimension':

            if unit == 'rad':
                valueStr = '%.*f' % (precision, deltaTheta)

            if unit == 'radPi':
                deltaTheta = deltaTheta / math.pi
                valueStr = '%.*f' % (precision, deltaTheta)
                if self.useLatex:
                    valueStr = '$%s\pi$' % valueStr
                else:
                    valueStr = valueStr + 'π'

            if unit == 'deg':
                deltaTheta *= 180.0 / math.pi
                valueStr = '%.*f' % (precision, deltaTheta)
                if self.useLatex:
                    valueStr = '\SI{%s}{\degree}' % valueStr
                else:
                    valueStr = valueStr + '°'

        else:
            if self.useLatex:
                valueStr = r'\noindent ' + customText.replace('\\n', '\\newline ')
            else:
                valueStr = customText.replace('\\\\', '\\n')

        # auxiliary lines
        if dimPosition == 'exterior':
            L1start = segment1.getPointAtLength(segment1.length + self.auxLineOffset)
            L2start = segment2.getPointAtLength(segment2.length + self.auxLineOffset)

            L1end = segment1.getPointAtLength(DimLineRadius + self.auxLineExtension)
            L2end = segment2.getPointAtLength(DimLineRadius + self.auxLineExtension)

            inkDraw.line.absCoords(group, [L1start, L1end], offset=[0, 0], lineStyle=self.auxiliaryLineStyle)
            inkDraw.line.absCoords(group, [L2start, L2end], offset=[0, 0], lineStyle=self.auxiliaryLineStyle)

        if dimPosition == 'interior':
            if DimLineRadius > segment1.length + self.auxLineOffset:
                L1start = segment1.getPointAtLength(segment1.length + self.auxLineOffset)
                L1end = segment1.getPointAtLength(DimLineRadius + self.auxLineExtension)
                inkDraw.line.absCoords(group, [L1start, L1end], offset=[0, 0], lineStyle=self.auxiliaryLineStyle)
            if DimLineRadius > segment2.length + self.auxLineOffset:
                L2start = segment2.getPointAtLength(segment2.length + self.auxLineOffset)
                L2end = segment2.getPointAtLength(DimLineRadius + self.auxLineExtension)
                inkDraw.line.absCoords(group, [L2start, L2end], offset=[0, 0], lineStyle=self.auxiliaryLineStyle)

        # draw dimension line
        theta_arrow = self.arrowSize / DimLineRadius
        theta_line = self.dimensionSpacing / DimLineRadius

        if not smallDimension:
            if invertAngle:
                flagInside = False
                if abs(segment2.theta - segment1.theta) == math.pi:
                    flagLargeAngle = False
                else:
                    flagLargeAngle = True
                if abs(segment2.theta - segment1.theta) < math.pi:
                    flagRightOf = True
                else:
                    flagRightOf = False

            else:
                flagInside = True
                flagLargeAngle = False
                if abs(segment2.theta - segment1.theta) < math.pi:
                    flagRightOf = False
                else:
                    flagRightOf = True

            P1 = getPosArc(segment1.t_versor, segment2.t_versor, deltaTheta1=theta_arrow, flagInside=flagInside) * DimLineRadius
            P2 = getPosArc(segment1.t_versor, segment2.t_versor, deltaTheta2=theta_arrow, flagInside=flagInside) * DimLineRadius

            inkDraw.arc.startEndRadius(group, P1, P2, DimLineRadius, offset=centerPoint, lineStyle=self.ANGdimensionLineStyle,
                                       flagRightOf=flagRightOf, largeArc=flagLargeAngle)
        else:
            if invertAngle:
                flagInside = True

            else:
                flagInside = False

            Pa1 = getPosArc(segment1.t_versor, segment2.t_versor, deltaTheta1=theta_arrow + theta_line, flagInside=flagInside) * DimLineRadius
            Pa2 = getPosArc(segment1.t_versor, segment2.t_versor, deltaTheta1=theta_arrow, flagInside=flagInside) * DimLineRadius
            Pb1 = getPosArc(segment1.t_versor, segment2.t_versor, deltaTheta2=theta_arrow + theta_line, flagInside=flagInside) * DimLineRadius
            Pb2 = getPosArc(segment1.t_versor, segment2.t_versor, deltaTheta2=theta_arrow, flagInside=flagInside) * DimLineRadius

            if abs(segment2.theta - segment1.theta) < math.pi:

                if invertAngle:
                    flagRightOf = True
                    line1 = self.ANGdimensionLineStyleSmall2
                    line2 = self.ANGdimensionLineStyleSmall
                else:
                    flagRightOf = False
                    line1 = self.ANGdimensionLineStyleSmall
                    line2 = self.ANGdimensionLineStyleSmall2

            else:
                if invertAngle:
                    flagRightOf = False
                    line1 = self.ANGdimensionLineStyleSmall
                    line2 = self.ANGdimensionLineStyleSmall2
                else:
                    flagRightOf = True
                    line1 = self.ANGdimensionLineStyleSmall2
                    line2 = self.ANGdimensionLineStyleSmall

            inkDraw.arc.startEndRadius(group, Pa1, Pa2, DimLineRadius, offset=centerPoint, lineStyle=line1, flagRightOf=flagRightOf)
            inkDraw.arc.startEndRadius(group, Pb1, Pb2, DimLineRadius, offset=centerPoint, lineStyle=line2, flagRightOf=not flagRightOf)

        # dimension

        # creates the segment structure passing at the center of the dimension line
        if np.dot(segment1.t_versor, segment2.t_versor) >= 0.99:  # theta=0
            if invertAngle:
                bissectorVector = -segment1.t_versor
            else:
                bissectorVector = segment1.t_versor

        if np.dot(segment1.t_versor, segment2.t_versor) <= -0.99:  # theta=pi
            if invertAngle:
                bissectorVector = np.array([-segment1.t_versor[1], segment1.t_versor[0]])
            else:
                bissectorVector = np.array([segment1.t_versor[1], -segment1.t_versor[0]])

        if -0.99 < np.dot(segment1.t_versor, segment2.t_versor) < 0.99:  # 0<theta<pi
            if invertAngle:
                bissectorVector = -(segment1.t_versor + segment2.t_versor)
            else:
                bissectorVector = segment1.t_versor + segment2.t_versor

        segmentCenter = lineSegment(centerPoint, [centerPoint[0] + bissectorVector[0], centerPoint[1] + bissectorVector[1]])





        if valueStr != '':
            if not smallDimension:  # regular dimension style
                if invertTextSide:
                    posDim = segmentCenter.getPointAtLength(DimLineRadius - self.textOffset)
                else:
                    posDim = segmentCenter.getPointAtLength(DimLineRadius + self.textOffset)

            else:  # small dimension style
                posDim = segmentCenter.getPointAtLength(DimLineRadius)

            if horizontalText:
                angle = 0

                if not smallDimension:  # regular dimension style
                    theta_deg = segmentCenter.theta * (180.0 / math.pi)

                    justifRL = 'c'
                    justifTB = 'c'

                    if invertTextSide:
                        if theta_deg <= 80 or theta_deg >= 280:
                            justifRL = 'r'
                        if 100 <= theta_deg <= 260:
                            justifRL = 'l'

                        if 10 <= theta_deg <= 170:
                            justifTB = 'b'
                        if 190 <= theta_deg <= 350:
                            justifTB = 't'
                    else:
                        if theta_deg <= 80 or theta_deg >= 280:
                            justifRL = 'l'
                        if 100 <= theta_deg <= 260:
                            justifRL = 'r'

                        if 10 <= theta_deg <= 170:
                            justifTB = 't'
                        if 190 <= theta_deg <= 350:
                            justifTB = 'b'

                    justif = justifTB + justifRL
                else:
                    justif = 'cc'

            else:
                if segmentCenter.t_versor[1] < 0:
                    angle = -(segmentCenter.theta + math.pi / 2.0) * 180 / math.pi
                else:
                    angle = -(segmentCenter.theta + 3.0 * math.pi / 2.0) * 180 / math.pi

                if not smallDimension:  # regular dimension style
                    if invertTextSide:
                        if segmentCenter.t_versor[1] < 0:
                            justif = 'tc'
                        else:
                            justif = 'bc'
                    else:
                        if segmentCenter.t_versor[1] < 0:
                            justif = 'bc'
                        else:
                            justif = 'tc'
                else:
                    justif = 'cc'

            inkDraw.text.latex(self, group, valueStr, posDim, fontSize=self.fontSize, refPoint=justif, textColor=self.textColor, LatexCommands=' ',
                               angleDeg=angle)

    def drawLinDim(self, parent, points, direction, label='Dim', invertSide=False, textType='dimension', customText='', unit=None, unitSymbol=False,
                   scale=1.0, precision=2, horizontalText=False, invertTextSide=False, smallDimension=False):
        """ draws linear dimension

        parent: parent object
        points: list of points [P1,P2]
        direction: dimension direction. values: 'vertical','horizontal','parallel'
        label: label of the object (it can be repeated)
        invertSide: invert side of the dimmension annotation.
                    False (default): above(horiz./paral.),left (vert.)
                    True: below(horiz./paral.),right (vert.)
        textType: type of text. values  'dimension' (default), 'custom'
        customText: text to be added. Used only if textType='custom'
        unit: dimmension unit. Used only if textType='dimension'. use None to ignore. Default: None
        unitSymbol: add unit symbol to the text. Default: False
        scale: scale factor for the dimension. Used only if textType='dimension'. Default: 1.0
        precision: number of decimals. Used only if textType='dimension'
        horizontalText: places text horizontally despite dimension orientation. Default: False
        invertTextSide: invert text placement.
                        False (default): above line(horiz./paral.),left (vert.)
                        True: below line (horiz./paral.),right (vert.)

        """

        P1 = np.array(points[0])
        P2 = np.array(points[1])
        maxX = max(P1[0], P2[0])
        minX = min(P1[0], P2[0])

        maxY = max(P1[1], P2[1])
        minY = min(P1[1], P2[1])

        # tangent vector: from P1 to P2
        t_vector = P2 - P1
        if direction == 'horizontal':
            t_vector = np.array([t_vector[0], 0])
            DeltaY = abs(P2[1] - P1[1])
        if direction == 'vertical':
            t_vector = np.array([0, t_vector[1]])
            DeltaX = abs(P2[0] - P1[0])

        # normal vector: counter-clockwise with respect to tangent vector
        n_vector = np.array([t_vector[1], -t_vector[0]])

        # normalization
        t_versor = t_vector / np.linalg.norm(t_vector)
        n_versor = n_vector / np.linalg.norm(n_vector)

        # inkDraw.line.relCoords(parent, [(0.5 * n_vector).tolist()], offset=P1.tolist(),
        #                        lineStyle=inkDraw.lineStyle.setSimpleBlack(0.5))
        # inkDraw.line.relCoords(parent, [(0.5 * t_vector).tolist()], offset=P1.tolist(),
        #                        lineStyle=inkDraw.lineStyle.setSimpleBlack(0.5))

        # text string

        if unit == 'doc':
            unit = self.documentUnit

        if textType == 'dimension':
            value = np.linalg.norm(n_vector)

            # ssss
            # doc_scale = self.getDocumentScaleFactor()
            # value = self.unit2unit(value, self.documentUnit, unit) / doc_scale
            # ssss

            value = self.userUnit2unit(value, unit)

            valueStr = '%.*f' % (precision, value * scale)

            if unitSymbol:
                if unit and unit != 'none':
                    if self.useLatex:
                        valueStr = '\SI{%s}{%s}' % (valueStr, unit)
                    else:
                        valueStr = valueStr + ' ' + unit
        else:
            if self.useLatex:
                valueStr = r'\noindent ' + customText.replace('\\n', '\\newline ')
            else:
                valueStr = customText.replace('\\\\', '\\n')

        group = self.createGroup(parent, label)

        # auxiliary lines
        if invertSide:
            L1start = P1 - n_versor * self.auxLineOffset
            L2start = P2 - n_versor * self.auxLineOffset
        else:
            L1start = P1 + n_versor * self.auxLineOffset
            L2start = P2 + n_versor * self.auxLineOffset

        if direction == 'horizontal':
            if invertSide:  # below
                if P1[1] < P2[1]:
                    L1endRel = -n_versor * (DeltaY + self.dimensionSpacing + self.auxLineExtension)
                    L2endRel = -n_versor * (self.dimensionSpacing + self.auxLineExtension)
                else:
                    L1endRel = -n_versor * (self.dimensionSpacing + self.auxLineExtension)
                    L2endRel = -n_versor * (DeltaY + self.dimensionSpacing + self.auxLineExtension)

            else:  # above
                if P1[1] < P2[1]:
                    L1endRel = n_versor * (self.dimensionSpacing + self.auxLineExtension)
                    L2endRel = n_versor * (DeltaY + self.dimensionSpacing + self.auxLineExtension)
                else:
                    L1endRel = n_versor * (DeltaY + self.dimensionSpacing + self.auxLineExtension)
                    L2endRel = n_versor * (self.dimensionSpacing + self.auxLineExtension)

        if direction == 'vertical':
            if invertSide:  # to the right
                if P1[0] < P2[0]:
                    L1endRel = -n_versor * (DeltaX + self.dimensionSpacing + self.auxLineExtension)
                    L2endRel = -n_versor * (self.dimensionSpacing + self.auxLineExtension)
                else:
                    L1endRel = -n_versor * (self.dimensionSpacing + self.auxLineExtension)
                    L2endRel = -n_versor * (DeltaX + self.dimensionSpacing + self.auxLineExtension)

            else:  # to the left
                if P1[0] < P2[0]:
                    L1endRel = n_versor * (self.dimensionSpacing + self.auxLineExtension)
                    L2endRel = n_versor * (DeltaX + self.dimensionSpacing + self.auxLineExtension)
                else:
                    L1endRel = n_versor * (DeltaX + self.dimensionSpacing + self.auxLineExtension)
                    L2endRel = n_versor * (self.dimensionSpacing + self.auxLineExtension)

        if direction == 'parallel':
            if invertSide:  # below
                L1endRel = -n_versor * (self.dimensionSpacing + self.auxLineExtension)
            else:  # above
                L1endRel = n_versor * (self.dimensionSpacing + self.auxLineExtension)
            L2endRel = L1endRel

        inkDraw.line.relCoords(group, [L1endRel.tolist()], offset=L1start.tolist(), lineStyle=self.auxiliaryLineStyle)
        inkDraw.line.relCoords(group, [L2endRel.tolist()], offset=L2start.tolist(), lineStyle=self.auxiliaryLineStyle)

        # draw dimension line
        if self.options.markerStyle == 'arrow':
            extraDist = t_versor * self.arrowSize

        if self.options.markerStyle == 'circle':
            extraDist = 0

        if self.options.markerStyle == 'serif':
            extraDist = 0

        if not smallDimension:
            if invertSide:  # hor.:below    ver.:to the right    paral.:above
                Pstart = L1start + L1endRel + n_versor * (self.auxLineExtension) + extraDist
                Pend = L2start + L2endRel + n_versor * (self.auxLineExtension) - extraDist
            else:  # hor.:above    ver.:to the left    paral.:above
                Pstart = L1start + L1endRel - n_versor * (self.auxLineExtension) + extraDist
                Pend = L2start + L2endRel - n_versor * (self.auxLineExtension) - extraDist

            inkDraw.line.absCoords(group, [Pstart.tolist(), Pend.tolist()], offset=[0, 0], label='dim', lineStyle=self.LINdimensionLineStyle)
        else:
            if invertSide:  # hor.:below    ver.:to the right    paral.:above
                Pstart = L1start + L1endRel + n_versor * (self.auxLineExtension) - extraDist
                Pend = L2start + L2endRel + n_versor * (self.auxLineExtension) + extraDist
            else:  # hor.:above    ver.:to the left    paral.:above
                Pstart = L1start + L1endRel - n_versor * (self.auxLineExtension) - extraDist
                Pend = L2start + L2endRel - n_versor * (self.auxLineExtension) + extraDist

            PextStart = Pstart - t_versor * self.dimensionSpacing
            PextEnd = Pend + t_versor * self.dimensionSpacing

            inkDraw.line.absCoords(group, [PextStart.tolist(), Pstart.tolist()], offset=[0, 0], label='dim',
                                   lineStyle=self.ANGdimensionLineStyleSmall)
            inkDraw.line.absCoords(group, [PextEnd.tolist(), Pend.tolist()], offset=[0, 0], label='dim', lineStyle=self.ANGdimensionLineStyleSmall)

        # dimension
        if valueStr != '':
            if not smallDimension:  # regular dimension style
                if invertTextSide:
                    posDim = ((Pstart + Pend) / 2.0) - n_versor * self.textOffset
                else:
                    posDim = ((Pstart + Pend) / 2.0) + n_versor * self.textOffset
            else:  # small dimension style
                if invertTextSide:
                    posDim = ((Pstart + Pend) / 2.0)
                else:
                    posDim = ((Pstart + Pend) / 2.0)

            if horizontalText:
                angle = 0

                if not smallDimension:  # regular dimension style
                    if direction == 'vertical':
                        posDim = posDim - t_versor * self.fontSize / 2.0

                    if direction == 'horizontal':
                        if invertTextSide:
                            posDim = posDim - n_versor * self.fontSize

                    if direction == 'parallel':
                        if n_versor[1] == 0:
                            posDim = posDim - t_versor * self.fontSize / 2.0
                        if n_versor[0] == 0 and invertTextSide:
                            posDim = posDim - n_versor * self.fontSize
                        if n_versor[0] != 0 and n_versor[1] != 0:
                            if invertTextSide:
                                posDim = posDim - n_versor * self.fontSize / 1.5

                    if invertTextSide:
                        if n_versor[0] < 0:
                            justif = 'bl'
                        if n_versor[0] > 0:
                            justif = 'br'
                        if n_versor[0] == 0:
                            justif = 'bc'
                    else:
                        if n_versor[0] < 0:
                            justif = 'br'
                        if n_versor[0] > 0:
                            justif = 'bl'
                        if n_versor[0] == 0:
                            justif = 'bc'
                else:
                    justif = 'cc'
            else:
                angle = (180 / math.pi) * math.atan2(-t_vector[1], t_vector[0])
                if not smallDimension:  # regular dimension style
                    if invertTextSide:
                        justif = 'tc'
                    else:
                        justif = 'bc'
                else:
                    justif = 'cc'

            inkDraw.text.latex(self, group, valueStr, posDim, fontSize=self.fontSize, refPoint=justif, textColor=self.textColor, LatexCommands=' ',
                               angleDeg=angle)

        return group

    def getPointsLinDim(self, element, LINdirection):
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

        **Example**

        >>> for id_elem,element in self.selected.iteritems():                # iterates through all selected elements
        >>>   pointsList = self.getPointsLinDim(self,element,'horizontal')
        """

        listPoints = self.getPoints(element)

        if len(listPoints)!=2:
            return [None,None]
        else:
            P1=listPoints[0]
            P2=listPoints[1]

        # sets the position to the viewport center
        position = self.getCenter(element)
        root_layer = self.document.getroot()

        # inkDraw.text.write(self,'P1='+str(P1),position,root_layer,fontSize=self.fontSize,justification='center')
        # inkDraw.text.write(self,'P2='+str(P2),position,root_layer,fontSize=self.fontSize,justification='center')

        # check whether the line segment is valid and reorder if necessary
        if LINdirection == "horizontal":
            if P1[0] == P2[0]:
                inkDraw.text.write(self, 'Error: horizontal dimension is zero.', position, root_layer, fontSize=self.fontSize, justification='center')
                return [None, None]
            if P2[0] < P1[0]:  # makes sure P1 has smallest xcoords
                temp = P1
                P1 = P2
                P2 = temp

        if LINdirection == "vertical":
            if P1[1] == P2[1]:
                inkDraw.text.write(self, 'Error: vertical dimension is zero.', position, root_layer, fontSize=self.fontSize, justification='center')
                return [None, None]
            if P2[1] > P1[1]:  # makes sure P1 has smallest ycoords
                temp = P1
                P1 = P2
                P2 = temp

        if LINdirection == "parallel":
            if P1[0] == P2[0] and P1[1] == P2[1]:
                inkDraw.text.write(self, 'Error: dimension is zero.', position, root_layer, fontSize=self.fontSize, justification='center')
                return [None, None]
            if P2[0] < P1[0]:  # makes sure P1 has smallest xcoords
                temp = P1
                P1 = P2
                P2 = temp

            if P2[0] == P1[0]:
                if P2[1] > P1[1]:
                    temp = P1
                    P1 = P2
                    P2 = temp

        return [P1, P2]


if __name__ == '__main__':
    dimension = Dimensions()
    dimension.run()

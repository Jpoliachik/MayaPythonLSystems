#------------------------------------------------------------------------------
#Creates tree-like shapes made from cylinders
#Uses an L-system derived recursive function
#
#For use with 
#
#Justin Poliachik
#12/11/13
#------------------------------------------------------------------------------

from pymel.all import *
import maya.cmds as mc
import random as r
import math as m
from maya.OpenMaya import MVector

#Initialize
branches
angle
angleVariance
lengthFactor
lengthVariance
radiusFactor
radiusVariance

#Draws a tree using an L-system derived algorithm
#First sets the globals from user specifications
#Sets the starting length and radius
#Calls the recursive function to build the branches
def drawTree(bran, ang, angleVar, lengthFac, lengthVar, radiusFac, radiusVar):
	global branches
	global angle
	global angleVariance
	global lengthFactor
	global lengthVariance
	global radiusFactor
	global radiusVariance
	branches = bran
	angle = ang
	angleVariance = angleVar
	lengthFactor = lengthFac/100.0
	lengthVariance = lengthVar/100.0
	radiusFactor = radiusFac/100.0
	radiusVariance = radiusVar/100.0
	
	startingLength = 8
	startingRadius = 1
	drawBranch(0, 0, 0, 0, 0, 1, 0, startingRadius, startingLength)


#Recursive function for creating branches. 
#Creates a circle with radius
#Extrudes circle out
#Calculates new attributes based on user input plus random logic
def drawBranch(iteration, cX, cY, cZ, nrX, nrY, nrZ, radius, length):
	if(iteration < branches):
		iteration = iteration + 1
		
		#Draw circle and extrude based on parameters
		shape = circle( nr=(nrX, nrY, nrZ), c=(cX, cY, cZ), r=radius)
		extrude (shape, et=0, d= (nrX, nrY, nrZ), l= length)
		#Delete the base circle, keep the cylinder
		delete(shape)
		
		#Define direction vector and normalize
		vector = MVector(nrX, nrY, nrZ)
		vector.normalize()
		
		cX = cX + (length*vector.x)
		cY = cY + (length*vector.y)
		cZ = cZ + (length*vector.z)
		
		randX = r.randint(0, 1)*2 -1
		randY = r.randint(0, 1)*2 -1
		randZ = r.randint(0, 1)*2 -1
		
		#Random direction vector
		#For X, Y, Z, ( -1 or 1 )*angle + (randint from -angleVariance to +angleVariance)
		nrX = nrX + ((angle*randX) + r.randint(0, angleVariance*2) - angleVariance)/100.0
		nrY = nrY + ((angle*randY) + r.randint(0, angleVariance*2) - angleVariance)/100.0
		nrZ = nrZ + ((angle*randZ) + r.randint(0, angleVariance*2) - angleVariance)/100.0

		#Length and Radius based on factor + (randint from -variance to +variance)
		length = length * (lengthFactor + (r.randint(0, lengthVariance*2*100)/100.0) - lengthVariance)
		radius = radius * (radiusFactor + (r.randint(0, radiusVariance*2*100)/100.0) - radiusVariance)
		
		#Draw first branch
		drawBranch(iteration, cX, cY, cZ, nrX, nrY, nrZ, radius, length)
		
		#Use opposite base angle from previous branch
		nrX = nrX + ((angle*randX*-1) + r.randint(0, angleVariance*2) - angleVariance)/100.0
		nrY = nrY + ((angle*randY*-1) + r.randint(0, angleVariance*2) - angleVariance)/100.0
		nrZ = nrZ + ((angle*randZ*-1) + r.randint(0, angleVariance*2) - angleVariance)/100.0

		length = length * (lengthFactor + (r.randint(0, lengthVariance*2*100)/100.0) - lengthVariance)
		radius = radius * (radiusFactor + (r.randint(0, radiusVariance*2*100)/100.0) - radiusVariance)
		
		#Draw second branch
		drawBranch(iteration, cX, cY, cZ, nrX, nrY, nrZ, radius, length)
	


""" Create simple Maya interface window. """
myWindow = mc.window(title="Parameters", wh=(180,400))
mc.columnLayout()

mc.text(label="Number of branches (2-15): ")
branchesText= mc.intField( minValue=2, value=9, maxValue=15 )

mc.text(label="Branch Base Angle (0-90): ")
angleText= mc.intField( minValue=0, value=35, maxValue=90 )

mc.text(label="Angle Variance (0-50)")
angleVarianceText= mc.intField( minValue=0, value=6, maxValue=50 )

mc.text(label="Length Factor Percentage (0-200): ")
lengthFactorText= mc.intField( minValue=0, value=85, maxValue=200 )

mc.text(label="Length Variance Percentage (0-100): ")
lengthVarianceText= mc.intField( minValue=0, value=15, maxValue=100 )

mc.text(label="Radius Factor Percentage (0-200): ")
radiusFactorText= mc.intField( minValue=0, value=90, maxValue=200 )

mc.text(label="Radius Variance Percentage (0-100): ")
radiusVarianceText= mc.intField( minValue=0, value=10, maxValue=100 )

commandString = ("drawTree(mc.intField(branchesText, query=True, value=True),"
		"mc.intField(angleText, query=True, value=True),"
		"mc.intField(angleVarianceText, query=True, value=True),"
		"mc.intField(lengthFactorText, query=True, value=True),"
		"mc.intField(lengthVarianceText, query=True, value=True),"
		"mc.intField(radiusFactorText, query=True, value=True),"
		"mc.intField(radiusVarianceText, query=True, value=True))")
		
mc.button(label="Draw", command=commandString)

mc.showWindow(myWindow)


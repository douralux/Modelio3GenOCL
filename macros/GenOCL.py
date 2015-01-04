"""
=========================================================
                       GenOCL.py
 Generate a USE OCL specification from a UML package
=========================================================

FILL THIS SECTION AS SHOWN BELOW AND LINES STARTING WITH ###
@author Xuan Shong TI WONG SHI <xuan.ti@mydomain.com>
@author Maria Shohie CEZAR LOPEZ DE ANDERA <maria.cezar@ujf-grenoble.fr>
@group  G17

Current state of the generator
----------------------------------
FILL THIS SECTION 
Explain which UML constructs are supported, which ones are not.
What is good in your generator?
What are the current limitations?

Current state of the tests
--------------------------
FILL THIS SECTION 
Explain how did you test this generator.
Which test are working? 
Which are not?

Observations
------------
Additional observations could go there
"""


#---------------------------------------------------------
#   Helpers on the source metamodel (UML metamodel)
#---------------------------------------------------------
# The functions below can be seen as extensions of the
# modelio metamodel. They define useful elements that 
# are missing in the current metamodel but that allow to
# explorer the UML metamodel with ease.
# These functions are independent from the particular 
# problem at hand and could be reused in other 
# transformations taken UML models as input.
#---------------------------------------------------------

# example
def isAssociationClass(clazz):
	""" 
	Return True if and only if the element is an association 
	that have an associated class, or if this is a class that
	has a associated association. (see the Modelio metamodel
	for details)
	"""
	if clazz.linkToAssociation is None:
		return False
	
	return True
    
 
#---------------------------------------------------------
#   Application dependent helpers on the source metamodel
#---------------------------------------------------------
# The functions below are defined on the UML metamodel
# but they are defined in the context of the transformation
# from UML Class diagramm to USE OCL. There are not
# intended to be reusable. 
#--------------------------------------------------------- 

# example
def associationsInPackage(package):
    """
    Return the list of all associations that start or
    arrive to a class which is recursively contained in
    a package.
    """

def inheritance(clazz):
	'''
	Check if a class is subclass of another class 
	then return the representation in OCL format
	'''
	parents = clazz.parent
	if len(parents) > 0:
		p = parents.get(0)
		return ' < ' + p.superType.name
	
	return ''

def abstract(clazz):
	'''
	Return 'abstract' if clazz is abstract
	'''
	if clazz.isIsAbstract():
		return 'abstract '
	
	return ''
	
def associationRoleName(asso):
	'''
	Get the association end role name
	'''
	if len(asso.name) > 0:
		return ' role ' + asso.name.capitalize()
		
	return ''

def isAssociationRelationship(asso):
	'''
	Return true if asso is an association relationship, false if not
	Is merely the same as isAssociation class !
	'''
	if asso.linkToClass is None:
		return False
		
	return True
	
def associationClassString(asso):
	'''
	Return 'associationClass' if asso is an association class or 'association' if not
	'''
	if isAssociationRelationship(asso):
		return 'associationclass '
		
	return 'association '
	

    
#---------------------------------------------------------
#   Helpers for the target representation (text)
#---------------------------------------------------------
# The functions below aims to simplify the production of
# textual languages. They are independent from the 
# problem at hand and could be reused in other 
# transformation generating text as output.
#---------------------------------------------------------


# for instance a function to indent a multi line string if
# needed, or to wrap long lines after 80 characters, etc.

#---------------------------------------------------------
#           Transformation functions: UML2OCL
#---------------------------------------------------------
# The functions below transform each element of the
# UML metamodel into relevant elements in the OCL language.
# This is the core of the transformation. These functions
# are based on the helpers defined before. They can use
# print statement to produce the output sequentially.
# Another alternative is to produce the output in a
# string and output the result at the end.
#---------------------------------------------------------



# examples

def umlEnumeration2OCL(enumeration):
	"""
	Generate USE OCL code for the enumeration
	"""
	i = 0
	values = enumeration.value
	n = len(values) 
	
	print 'enum ' + enumeration.name 
	print '{'
	
	while i < (n - 1):
		print '\t' + values.get(i).name + ','
		i = i + 1
	print '\t' + values.get(i).name
			
	print '}\n'
    

def umlBasicType2OCL(basicType):
	"""
	Generate USE OCL basic type. Note that
	type conversions are required.
	"""
	if basicType == 'float':
		return 'Real'
	return basicType.capitalize()
	
def paramater2OCL(parameter):
	"""
	Parameter representation in OCL
	"""
	# TODO

def umlAttribute2OCL(attribute):
	"""
	UML attribute generation
	"""
	print '\t' + attribute.name + ' : ' + umlBasicType2OCL(attribute.type.name)
	
def umlOperation2OCL(operation):
	"""
	UML operation generation
	"""
	print '\t' + operation.name + '() : ' + operation.return.type.name # TO COMPLETE !!!
	
def umlClass2OCL(clazz):
	"""
	UML class generation
	"""
	attributes = clazz.ownedAttribute
	operations = clazz.ownedOperation
	
	if not isAssociationClass(clazz):
		print abstract(clazz) + 'class ' + clazz.name + inheritance(clazz)	
		commonUmlClass2OCL(clazz)			
		print 'end\n'
	# else:
	# The else is handled by association generation
	# see umlAssociation2OCL(clazz)
	
	
	# UML association handling
	umlAssociation2OCL(clazz)

def commonUmlClass2OCL(clazz):
	'''
	Common class handling (association class or normal class) :
	<< Essentially class attributes and operations >>
	'''
	attributes = clazz.ownedAttribute
	operations = clazz.ownedOperation
	
	if len(attributes) > 0:
		print 'attributes'
		for attr in attributes:
			umlAttribute2OCL(attr)
	
	if len(operations) > 0:
		print 'operations'
		for op in operations:
			umlOperation2OCL(op)
	
def umlAssociation2OCL(clazz):
	'''
	UML association to OCL
	'''
	targetingEnds = clazz.targetingEnd
		
	# For all targetingEnd 
	for target in targetingEnds: 
		# Get the association
		asso = target.association 
			
		# Checking if association isn't treat yet
		if not (asso.name in targetAlreadyTreated):
			# Add the name to the list
			targetAlreadyTreated.append(asso.name)
			
			print associationClassString(asso) + asso.name + ' between'
			
			for end in asso.end:
				print '\t' + end.owner.name + '[' + end.multiplicityMin + '..' + end.multiplicityMax + ']' + associationRoleName(end)			
			
			if isAssociationRelationship(asso):
				# handle association class there
				commonUmlClass2OCL(asso.linkToClass.classPart)
				print 'end\n'
				# handle recursively asso's class association
				umlAssociation2OCL(asso.linkToClass.classPart)
			else:
				print 'end\n'			

# etc.

def package2OCL(package):
	"""
    Generate a complete OCL specification for a given package.
    The inner package structure is ignored. That is, all
    elements useful for USE OCL (enumerations, classes, 
    associationClasses, associations and invariants) are looked
    recursively in the given package and output in the OCL
    specification. The possibly nested package structure that
    might exist is not reflected in the USE OCL specification
    as USE is not supporting the concept of package.
    """
	elements = package.ownedElement
				
	for element in elements:		
		if isinstance(element, Class):
			umlClass2OCL(element)
		if isinstance(element, Package):
			package2OCL(element) # Handling other packages


def enumPackageGeneration(package):
	'''
	Generate enumerations for all packages : This allows us to have 
	enum declaration at the top of generated OCL code 
	(Mandatory in USE specs)
	'''
	elements = package.ownedElement
	
	for element in elements:
		if isinstance(element, Enumeration):
			umlEnumeration2OCL(element)
		if isinstance(element, Package):
			enumPackageGeneration(element) # Handle other packages

#---------------------------------------------------------
#           User interface for the Transformation 
#---------------------------------------------------------
# The code below makes the link between the parameter(s)
# provided by the user or the environment and the 
# transformation functions above.
# It also produces the end result of the transformation.
# For instance the output can be written in a file or
# printed on the console.
#---------------------------------------------------------

# (1) computation of the 'package' parameter
# (2) call of package2OCL(package)
# (3) do something with the result

# Elements selected by user in Modelio
elements = selectedElements

# Check if a user has selected a package
isPackageSelected = False

# Contains associations whose OCL declaration are already generated
# Avoid duplicate declaration
targetAlreadyTreated = []

if len(elements) > 0:
	print 'model CyberResidences\n'

	for e in elements:
		if isinstance(e, Package):
			isPackageSelected = True
			# Generate enumerations first
			enumPackageGeneration(e)
			# Generate the rest
			package2OCL(e)
	
	if isPackageSelected == False:
		print '-- No selected valide package !'
else:
		print '-- No selected element !\n-- Please select one !'
				
	
	
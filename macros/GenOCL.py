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
def isAssociationClass(element):
    """ 
    Return True if and only if the element is an association 
    that have an associated class, or if this is a class that
    has a associated association. (see the Modelio metamodel
    for details)
    """
    # TODO
    
 
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
	print 'enum', enumeration.name, '\n{'
	for val in enumeration.value:
		print '\t', val.name
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
	

def umlAttribute2OCL(attribute):
	"""
	UML attribute generation
	"""
	print '\t', attribute.name, ':', umlBasicType2OCL(attribute.type.name)
	
def umlOperation2OCL(operation):
	"""
	UML operation generation
	"""
	print '\t', operation.name+'() :', operation.return.type.name
	
def umlClass2OCL(clazz):
	"""
	UML class generation
	"""
	attributes = clazz.ownedAttribute
	operations = clazz.ownedOperation
	
	print abstract(clazz) + ' class ' + clazz.name + inheritance(clazz)
	if len(attributes) > 0:
		print 'attributes'
		for attr in attributes:
			umlAttribute2OCL(attr)
	
	if len(operations) > 0:
		print 'operations'
		for op in operations:
			umlOperation2OCL(op)
			
	print 'end\n'
	
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
	if clazz.isIsAbstract:
		return 'abstract'
	
	return ''
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
		if isinstance(element, Enumeration):
			umlEnumeration2OCL(element)
		if isinstance(element, Class):
			umlClass2OCL(element)
		if isinstance(element, Package):
			package2OCL(element) # Récursion sur les sous packages




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

elements = selectedElements
isPackageSelected = False
if len(elements) > 0:
	print 'model CyberResidences\n'

	for e in elements:
		if isinstance(e, Package):
			isPackageSelected = True
			package2OCL(e)
	
	if isPackageSelected == False:
		print '-- No selected valide package !'
else:
		print '-- No selected element !\n-- Please select one !'
				
	
	
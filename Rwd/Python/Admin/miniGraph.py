#!/usr/bin/env python
"""
miniGraph: ported from xayacore of 20060224 by Mishtu Banerjee to work with TeseraAnalytics
CurrentRevisionDate:20120907

FROM ORIGINAL XAYASTATS VERSION
BeginDate:20040902
CurrentRevisionDate:20060202
Development Version : core 001
Release Version: pre-release
# 20050818 -- Xayacore_001 is renamed simply xayacore -- and a xayaVersion fn is added

Author(s): Mishtu Banerjee, Tyler Mitchell
Contact: mishtu@harmeny.com

Copyright: The Authors
License: Distributed under MIT License
    [http://opensource.org/licenses/mit-license.html]
    
Environment: Programmed and tested under Python 2.3.3 on Windows 2000.
    Database Access: Psycopg and Postgres 7.4
    
Dependencies:
    Python Interpreter and base libraries.
    Psycopg [website]
    Postgres [website] test X



==============================================
XAYAcore_001 A Language for Thinking with Data
==============================================


XAYAcore is a Pythonic implementation of the Graph Abstraction Logic (GAL)
design principles. GAL relationally models information as graphs (an old idea
originating in modern logic) as a "little language" that can embedded
or embellished. It provides a basis for modelling and querying data from
complex systems. Data---> Information--> Knowledge (but wisdom is golden).

GAL was inspired by Robert Ulanowicz's ecological network theory of Ascendency,
Stan Salthe's developmental theory of Hierarchical Systems,
and Charles Peirce's Existential Graphs (a visual method of doing logic).
Hopefully beautiful ideas can lead to pragmatic working code ;-} ...

Xayacore goes frominstances to ontologies,and points inbetween.
One graph to rule them all! And some common sense to bind them ...

Send bugs, fixes, suggestions to mishtu@harmeny.com (Thanks). 



USAGE EXAMPLE: (see examples under individual functions)

ALGORITHMs:
    AlgorithmName -- Reference

CODE SOURCES:
    Guido Code. [webref]
    Graphlib Code
    Pydot Code
    Graphpath Code
    Python Cookbook
    Djikstra's
    Algorithms in Python

REFERENCES:
    Ascendency book.
    Salthe Hierarchy Book.
    Peirce Book (Reasoning and the Logic of Things)
    Graph Algorithms Reference
    Information Flow Book
    Foundations of Logic.
    Tools for Thought book
    
"""


# KNOWN BUGS
# None Known at this point

# UNITTESTS
# Unittests are below fn/obj being tested

# DESIGN CONTRACTS
# Design Contract for each fn/obj is right after docstring

#DOCTESTS
# Used sparingly where they illustrate code above and beyond unittest

import shelve
# import sets
import string
import copy

# To allow the code to use built-in set fns in Python 2.4 or the sets module in Python 2.3
try :
    set
except NameError:
    from sets import Set as set

def xayacoreVersion():
    return "Current version is xayacore_001 (development branch), updated August 18, 2005"

def readGraph(filepath = ""):
    """
    Reads An Ascii Format Graph File and Converts to Python Dictionary
    The lines of the file are of the general format:
    'Key : value1, value2, value3, .... valueN'
    or alternatively
    'Key : [value1, value2, value3, .... valueN]'
    roughly corresponding to YAML format http://www.yaml.org/
    unittests are in the file test_readgraph.py in the test directory
    The keys represent Nodes, specifically Parent Nodes
    The values represent Child Nodes
    So each key: values pairing defines a set of edges from Parent Node to
    Child Nodes.
    Preconditions: Input matches above format
    Postconditions: Returns a graph where format translated to key : list pairs
    
    Usage:
    >>> testgraph = readGraph('/XAYA/devcore/DataFiles_X001.txt')
    -------------------------------
    

    Opening file /XAYA/devcore/DataFiles_X001.txt
    >>> testgraph
    {'XAYA001': ['DataFiles_X001.txt', 'Models_X001.txt', 'Objects_X001.txt', 'ObjectOntology_X001.txt', 'Map_ObjectsToData_X001.txt', 'Map_ObjectAttributesToMeasures_X001.txt', 'Schema_X001.txt', 'Measures_X001.txt', 'MeasureTypes_001', 'MeasureUnits_X001', 'DataDictionary_X001.txt', 'datStandStructures_X001.txt', 'datPolygons_X001.txt', 'datProtocols_X001.txt', 'datPlotStructures_X001.txt', 'datPlots_X001.txt', 'datTrees_X001.txt', 'datMeasurements_X001.txt']}
    >>> 
    
    Algorithm (see pseudocode below)
    #Open a file holding the graphData (Check that the file is there)
        # Set Up a Graph data structure to hold nodes and edges
        #Set Up a KeyString to hold the keys for a graph
        #Set Up a ValueString to hold the values for a graph
        # Read each line of the file
            # Separating KeyString and ValueString for each line
            # Reading the KeyString into the Graph's Key -- strip extra spaces
            # Reading the ValueString into the Graph's Value
        # Convert the ValueString to a List, stripping extra space and newlines
            #Test for and handle case where string ends in NewLine
            #Test for and handle case where string does not end in NewLine
        # The end result should be a Graph data structure where every key is \
        # associated with a list of values.

    """
    
    
    #Open a file holding the graphData (#Check that the file is there)
    try:
        graphData = open(filepath, 'r')
    except IOError:
        return "File not opened, could not find" + filepath
    else:
        # print "-------------------------------"
        # print
        # print "Opening file", filepath -- Disabled as adds to much "gibberish" to interpreter session
                
        # Set Up a Graph data structure to hold nodes and edges
        graphDict = {}
        
        #Set Up a KeyString to hold the keys for a graph
        keyString = ''
        
        #Set Up a ValueString to hold the values for a graph
        valueString = ''
        
        # Read each line of the file
            # Separating KeyString and ValueString for each line
            # Reading the KeyString into the Graph's Key -- strip extra spaces
            # Reading the ValueString into the Graph's Value
        for line in graphData:
            if len(line) > 1: # Add lines with data to graph
                lineList = line.split(':')
                keyString = lineList[0]
                try: # Check line has a second item post splitting on the :, skip if IndexError
                    valueString = lineList[1]
                    graphDict[keyString.strip()] = valueString
                except IndexError: continue
                
            else: continue # Silently ignore blank lines. 

            
            
        # Convert the ValueString to a List, stripping extra space and newlines
        for key in graphDict:
            #Test for and handle case where string ends in NewLine
            if graphDict[key][:-1] == "\n":
                graphDict[key] = [column.strip() for column in graphDict[key][:-1].split(",")]
            
            #Test for and handle case where string does not end in NewLine
            if graphDict[key][:-1] != "\n":
                graphDict[key] = [column.strip() for column in graphDict[key].split(",")]
            # original graphDict[key] = [column.strip() for column in graphDict[key][:-1].split("'")]
            # Work out case to handle List Parenthesis -- present, missing, partial. 
        graphData.close()
        
        # The end result should be a Graph data structure where every key is \
        # associated with a list of values.
        return graphDict
    
    # Future -- read from DB, read from XML via testing for what's at a filepath
    
    # Iteration 002: Add the following Sanity Checks and Psycopg support
        # Allow YAML style value lists, with opening [ and closing ] tokens
        # Test that a file is ascii or unicode before reading
        # Test for "end of line" characters, and handle if missing (i.e.)
        # Add param -- so "filepath" can be either a file locn or DB session string
            #Initially add support for Postgres only -- via Psycopg
            # Note -- this breaks the model that only Python Standard Libs used
                # So consider putting this code in another module
        # Add ability to read "standard ascii data files" which have values only
        # Break fn down to sub-fns that can be used again. Such as the \n
        # value string cleanup code -- that could be used for any value string.
    


def writeGraph(graph = {}, filepath = "defaultFilePath", append=0):
    """ Inverse of readGraph. Stores a XAYA format dictGraph as a text file"""
    transList = transGraphToList(graph)
    if append != 0:
        fileObject = open(filepath, 'a+')
    else: 
        fileObject = open(filepath, 'w+')
    fileObject.writelines(transList)
    fileObject.flush()
    return fileObject


def shelveGraph(graph = {},filepath = "defaultFilePath"):
    """ Stores via the Graph at the filepath location e.g '/apath/file.xay'
    Preconditions: Takes a graph
    Postconditions: Returns a shelf object with stored graph
    
    Usage:
    >>> agraph = {'Key1': ['Value1', 'Value2'], 'Key2':['Value3',4]}
    >>> shelveGraph(agraph,'storeagraph')
    {'Key2': ['Value3', 4], 'Key1': ['Value1', 'Value2']}
    >>>

    Algorithms (see pseudocode below)
    #Open a shelfObject
    #read graph into shelfObject; deal with case of emptygraph via get fn
    #return shelfObject

    """
    #Open a shelfObject
    shelfObject = shelve.open(filepath)
    #read graph into shelfObject; deal with case of emptygraph via get fn
    for key in graph:
        shelfObject[key] = graph.get(key,'')    #graph[key] causes error if no such key
    #return shelfObject
    return shelfObject





 
def transGraphToList(graph={}):
    """ Transforms a graph to a list of strings
    of the form -- ["key1: v11, v12, v13", "key2: v21, v22, v23 ...."]
    Preconditions: Takes a graph
    Postconditions: Returns a list of strings
    
    Usage:
    >>> numbergraph
    {1: [2, 3, 4], 2: [5, 6, 9]}
    >>> agraph
    {'a': ['b', 'c', 'd'], 'c': ['e', 'f', 'g']}
    >>> transGraphToList(numbergraph)
    ['1:2, 3, 4\n', '2:5, 6, 9\n']
    >>> transGraphToList(agraph)
    ['a:b, c, d\n', 'c:e, f, g\n']

    Algorithms (see pseudocode below)
    # For each key in the input graph
        # render the Key as a string, and add the ':' key delimiter
        # render the value list as a comma delimited string
        # add the Key as String and Value as String together and tag with newline
        # The resulting string is appended to a list
    # return the list of strings
    
    """
    transList = []
    for key in graph:
        keyString = str(key) + ':'
        # render the value list as a comma delimited string.
            # Run a list comprehension for values to create a list of strings
            # join the strings together into a single string of comma delimted values
            # strip off the final comma
        valueString = " ".join([str(x) + ',' for x in graph[key]]).rstrip(',')
        newline = '\n'
        finalString = keyString + valueString + newline
        transList.append(finalString)
    return transList


def transListToGraph(list=[]):
    """ Transforms a List to a Graph in Xaya format"""
    graph = {}
    for item in list:
        graph[str(item)] = [item]
    return graph
    # Future -- add explicit type checking if not a list


def transValueToKey(graph = {},key = ""):
    """Given a Graph,a Key outputs graph with value as key; value-index as value
        Usage:
        Preconditions: A graph in Xaya format
        PostConditions: Returns a Graph 
        Invariants:
        
        Usage:
        
        Algorithms:
        # Define graph to hold indexed items
        # For the selected key, place all items into an indexed graph where
            #indexed graph's keys are the original values in the value list
            #indexed graph's values are the index positions in the value list
              
    
    """
    # Define graph to hold indexed items
    itemgraph = {}
    # For the selected key, place all items into an indexed graph where
        #indexed graph's keys are the original values in the value list
        #indexed graph's values are the index positions in the value list
    for item in graph.get(key,''):
            itemgraph[item] = graph.get(key,'').index(item)
    return itemgraph



    
def bindGraphsByValues (parentgraph = {}, parentkey = "", parentvalue = "", childgraph = {}, ):
    """ Given a ParentGraph and Parentkey, bind to all Values of a ChildGraph
        Preconditions: parentgraph and childgraphs in Xaya format
        Postconditions: returns a graph with same keys as childgraph and "selected" column
        Invariants:
        
        Usage:
        
        Algorithm:
        #Use function transValueToKey to create a linkgraph indexing values in parentkey
            #Note childgraph approximates a data table -- key and tuple
            #Note parentgraph approximates a dbs catalogue -- a list of all tables(keys) and columns(values
        #define graph linking parent to child.
            #Note linkgraph is like the column indexing in a relational db
        #define graph that will have selected data
        # for each key in childgraph, extract data for parentvalue only via linkgraph
        #Approximates very simplified version of selecting a single "column" from a "table"
        
    """
        #Note childgraph approximates a data table -- key and tuple
        #Note parentgraph approximates a dbs catalogue -- a list of all tables(keys) and columns(values)
    #define graph linking parent to child. 
    linkgraph = transValueToKey(parentgraph,parentkey)
    #Note linkgraph is like the column indexing in a relational db
    #define graph that will have selected data
    selectgraph = {}
    # for each key in childgraph, extract data for parentvalue only via linkgraph
    for key in childgraph:
        selectgraph[key] = childgraph[key][linkgraph[parentvalue]]
    # Resulting graph has same keys as childgraph, but only the selected parentvalues
    #Approximates very simplified version of selecting a single "column" from a "table"
    return selectgraph

# Future -- support selecting multi-columns. Constraints via Value criteria
    #This will approximate a generalized "Select From Where" clause in a single table
    
def findAllPathsAsLists(graph={}, startnode='', endnode='', pathList=[ ]):
    """ Header: Find all paths from startnode to endnode
        Preconditions:
        Postconditions:
        
        Usage:
        
        Algorithm: Based on 'find_all_paths' example by GvR at
        http://www.python.org/doc/essays/graphs.html
        Other variations can be found at:
            Python Cookbook on Dijkstra's Shortest Path (classic CS Graph Algorithm):
                http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/119466
            Graph and Graph Algorithms section in Bruno R Preiss' book on Python DS and Alg:
                http://www.brpreiss.com/books/opus7/html/book.html
            Graphlib module of general graph routines in python by Istvan Albert:
                http://www.personal.psu.edu/staff/i/u/iual/python/graphlib/html/public/graphlib-module.html
        
        # --- SETUP ---
        # Set up a pathList and add the start node to it
        # Check if Start Node and End Node Equal. If so return pathList converted to a graph
        # If start node not in graph, return an empty graph
        # Set Up 'allpathsList' which is a list of all paths found
        # --- Finding Paths ---
        # For childedges in startnode
            #If childedge not in path
                # Recursively call 'findAllPaths'
                    # Append new paths found to the 'allPathsList'
        # Return the 'allPathsList' as the function's value
        
    """
    pathList = pathList + [startnode]
    if startnode == endnode:
        return [pathList]
    if not graph.has_key(startnode):
        return []
    allpathsList = []
    for childnode in graph[startnode]:
        if childnode not in pathList:
            newpathsList = findAllPathsAsLists(graph, childnode, endnode, pathList)
            for newpath in newpathsList:
                allpathsList.append(newpath)
    return allpathsList
   
    
def findAllPaths(graph={}, startnode='', endnode='', pathList=[ ]):
    """ Wraps results from findAllPathsAsLists as a Graph with Keys having String Rep of each PathList """
    allpathsList = findAllPathsAsLists(graph, startnode, endnode, pathList)
    allpathsGraph = { }
    if allpathsList == [['']]: #Case of no parameters entered so empty strings for startnode, endnode
        return { }
    for path in allpathsList:
        allpathsGraph[str(path)] = path
    return allpathsGraph
    # Alternative -- Use Nested scope. But then no direct access to 'findAllPathsAsLists
    

 
def findPathsUp(graph={}, endnode='', operator='==', pathlength=None):
    """ Given a Graph, Endnode, Operator and Pathlength, find all paths that match.
    Preconditions: Graph in Xaya Format
    Postconditions: Returns a Graph where keys are startnodes, and values are paths
        to an endnode beginning with the startnode. 
        Invariants: No changes to the input Graph
        
        Usage:
        
        Algorithm:
        # Define operators that can be used for pathlength comparisons
        # Check that only valid operators are input by user
        # Check that pathlength is an integer
        # For each key in the input graph find all paths between the key (starnode)
            # and the endnode
            # Ignore the case where key == endnode
        # Check that resulting list of paths is not empty
        # Filter non-empty paths
            # If pathlength == None -- no Filter is applied and path entered in output graph for key(startnode)
            # For all valid (positive integer) pathlengths:
                # apply the user input operator and pathlength info to filter paths
                # Check that remaining valid paths results in a non-empty list.
                # Apply valid non-empty paths to output graph for key (startnode)
        
        
    """ 
    pathsUpGraph ={}
    # Define operators that can be used for pathlength comparisons
    operatorDict = {'<': '<', '<=': '<=',
                    '>' : '>', '>=': '>=',
                    '==': '==', '!=': '!=',
                    '<>' : '<>'}
    # Check that only valid operators are input by user
    if not operatorDict.has_key(operator):
        return "Operator must  be one of -- '<', '<=', '>', '>=', '==', '!=', '<>'"
    if pathlength <> None:
        # Check that pathlength is an integer
        try:
            int(pathlength)
        except ValueError:
            return "Pathlength must be an integer"
    # For each key in the input graph find all paths between the key (starnode) and endnode
    for key in graph:
        # Ignore the case where key (i.e. startnode)  == endnode -- path to self
        if key == endnode:
            continue
        pathsList = findAllPathsAsLists(graph, key, endnode)
        # Check that resulting list of paths is not empty
        if len (pathsList) <> 0:
            # If pathlength == None -- no Filter is applied and path entered
            # in output graph for key(startnode)
            if pathlength == None:
                pathsUpGraph[key] = pathsList
            else:
                 # apply the user input operator and pathlength info to filter paths
                validpathsList = [path for path in
                                  pathsList if
                                  eval('len(path)' + operatorDict[operator] + 'pathlength')]
                # Check that remaining valid paths results in a non-empty list.
                if len(validpathsList) > 0:
                    # Apply valid non-empty paths to output graph for key (startnode)
                    pathsUpGraph[key] = validpathsList
                else:
                    continue
        else:
            continue
    return pathsUpGraph


def findPathsDown(graph={}, startnode='', operator='==', pathlength=None):
    """ Given a Graph, Startnode, Operator and Pathlength, find all paths that match.
    Preconditions: Graph in Xaya Format
    Postconditions: Returns a Graph where keys are endnodes, and values are paths
        form a startnode to the endnode. 
        Invariants: No changes to the input Graph
        
        Usage:
        
        Algorithm:
        # Define operators that can be used for pathlength comparisons
        # Check that only valid operators are input by user
        # Check that pathlength is an integer
        # Create a list of unique endnodes (for iteration and will become keys in output graph)
        # For each unique endnode find all paths between the startnode and endnodes
            # Ignore case where startnode == endnode
        # Check that resulting list of paths is not empty
        # Filter non-empty paths
            # If pathlength == None -- no Filter is applied and path entered in output graph for key(startnode)
            # For all valid (positive integer) pathlengths:
                # apply the user input operator and pathlength info to filter paths
                # Check that remaining valid paths results in a non-empty list.
                # Apply valid non-empty paths to output graph for key (startnode)
        
        
    """ 
    pathsDownGraph ={}
    # Define operators that can be used for pathlength comparisons
    operatorDict = {'<': '<', '<=': '<=',
                    '>' : '>', '>=': '>=',
                    '==': '==', '!=': '!=',
                    '<>' : '<>'}
    # Check that only valid operators are input by user
    if not operatorDict.has_key(operator):
        return "Operator must  be one of -- '<', '<=', '>', '>=', '==', '!=', '<>'"
    if pathlength <> None:
        # Check that pathlength is an integer
        try:
            int(pathlength)
        except ValueError:
            return "Pathlength must be an integer"
    # Create a list of unique endnodes (for iteration and will become keys in output graph)
    endnodesList = graph.values()
    uniqueendnodesList = [ ]
    for nodeList in endnodesList:
        for node in nodeList:
            if node not in uniqueendnodesList:
                uniqueendnodesList.append(node)
        # For each unique endnode find all paths between the startnode and endnodes
        for endnode in uniqueendnodesList:
            # Ignore case where endnode == startnode -- path to self
            if endnode == startnode:
                continue
            pathsList = findAllPathsAsLists(graph, startnode, endnode)
            # Check that resulting list of paths is not empty
            if len (pathsList) <> 0:
                # If pathlength == None -- no Filter is applied and path entered
                # in output graph for key(startnode)
                if pathlength == None:
                    pathsDownGraph[endnode] = pathsList
                else:
                    # apply the user input operator and pathlength info to filter paths
                    validpathsList = [path for path in
                                      pathsList if
                                      eval('len(path)' + operatorDict[operator] + 'pathlength')]
                    # Check that remaining valid paths results in a non-empty list.
                    if len(validpathsList) > 0:
                        # Apply valid non-empty paths to output graph for key (startnode)
                        pathsDownGraph[endnode] = validpathsList
                    else:
                        continue
            else:
                continue
    return pathsDownGraph

#Future -- PathsUp and PathsDown could be incorporated into a single function
#Future -- Use PathsUp/PathsDown to build a NodesUp and NodesDown function
    # PathsUp and PathsDown return the complete paths. A typical Prolog-like query
    # would be to simply return the node that satisfies a target. For example,
    #if the base predicate were parent(Parent, Child) and a derived rule were
    # grandparent(X,Y) <-- parent(X,Z), parent(Z,Y) and the query were something like
    # grandparent(X, lot)? -- then we are looking for the individual nodes that satisfy
    # the relation grandparent of Lot.
    # In XAYA terms this would be satisfied by a function similar to findPathsUp, but
        # which returns only the startnodes.
        # Something like:
        # grandparentsOfLot= findNodesUp(graph=parents, endnode='Lot', operator='==', pathlength=2)

   

    
def findRootsLeaves(graph = {}):
    """Given a Graph, finds Root and Leaf Nodes for the Graph
    Preconditions: Graph in Xaya Format
    Postconditions: Returns a Graph with two keys: "Roots" and "Leaves", each with their valuelist. 
    Invariants:
        
    Usage:
        
    Definition:
        # A "keyset" is the set of Keys in a Graph.
        # A "valueset' is the set of unique values in a Graph
        # A "Root" is a member of keyset that is not a member of valueset = 'rootset'
        # A "Leaf" is a member of valueset that is not a member of keyset = 'leafset'
        
    """
    # A "keyset" is the set of Keys in a Graph.
    # A "valueset' is the set of unique values in a Graph
    keyset = set(graph.keys())
    valuelist = []
    for key in graph:
        for value in graph[key]:
            valuelist.append(value)
    valueset = set(valuelist)
    # A "Root" is a member of keyset that is not a member of valueset = 'rootset'
    rootset = keyset.difference(valueset)
    # A "Leaf" is a member of valueset that is not a member of keyset = 'leafset'
    leafset = valueset.difference(keyset)
    # An "Interior" is the difference of "AllNodes" minus UnionRootSetLeafSet
    allNodes = keyset.union(leafset)
    unionLeavesRoots = leafset.union(rootset)
    # Note: Allnodes is now partitioned into 3 disjoint sets:rootset, leafset, interiorset. 
    interiorset = allNodes.difference(unionLeavesRoots)
    # 'rootset' and 'leafset' in graph via keys "Roots" and "Leaves" = 'rootleaves'
    rootleaves = {}
    rootleaves['Roots'] = list(rootset)
    rootleaves['Leaves'] = list(leafset)
    rootleaves['Interior'] = list(interiorset)
    rootleaves['AllNodes'] = list(allNodes)
    return rootleaves

# Future -- Actually a Leaf Set is a member of valueset that is not a member of
    # keyset OR is a member of member of Keyset whose ValueList = []
    # Also add internodeset (interior nodes) all remaining nodes not in keyset or leafset
    
    
def findPathsToRoot(graph={}, selections={}):
    """ Given a Graph and Selections, find all Paths from Selections to Root
    Preconditions: Graph in Xaya Format, Selections as a Graph in XAYA format
        Keys are selections -- a name meaningful to the user
        Values are the selected nodes -- in Xaya format: ['n1', 'n2', n3' ..]
    Postconditions: Returns a Graph where keys are combinations of selections, roots
        and values are list of paths to root. 
    Invariants: No changes to the input Graph and Selections
        
    Usage:
        
    Algorithm:
        # Find all roots in a Graph
        # For each selection, fore each root, for each node in a selection
        # Find paths to roots via
            # each root represents startnode in a path
            # each selected node represents endnode in a path
        # Return a graph where for every combination of Selection/root
            values are the paths to root
        # 
        
    """ 
    pathstorootGraph = {}
    # Find all roots in a Graph
    rootsleavesGraph = findRootsLeaves(graph)
    # For each selection, for each root, for each node in a selection
    for selectedpathkey in selections:
        for root in rootsleavesGraph['Roots']:
            pathList = [ ]
            for selectedpaths in selections[selectedpathkey]:
                # Find the path from each root to the selected node
                pathList = pathList + findAllPathsAsLists(graph, root, selectedpaths)
            # Return a graph where for every combo of selection/root values are paths to root
            pathstorootGraph[str(selectedpathkey) + '/' + str(root)] = pathList
    return pathstorootGraph



def findUniquePathsToRoot(graph={}, selections={}):
    """ Given a Graph and Selections, find all Paths from Selections to Root.
    Wraps the functions findPathsToRoot and filterSubPaths
    """
    return filterSubPaths(findPathsToRoot(graph, selections))


def filterSubPaths(pathGraph={}):
    """ Given a Graph of Paths, filter out SubPaths
    What is a SubPath?
        In this graph {'query1': ['a', 'b'], ['a', 'c'], ['a', 'b','c','d']]
        ['a','b'] is a SubPath of ['a','b','c','d']
    Preconditions: Graph in Xaya Format
        Keys are selections -- a name meaningful to the user
        Values are pathlists -- in Xaya format: [['n1', 'n2', n3'] ['n1', 'n5] ..]
        Postconditions: Returns a Graph where for a key, any SubPaths have been removed. 
        Invariants: No changes to the input Graph and Selections
        
        Usage:
        
        Algorithm:
        #For each key, values are paths. 
        # A path is a list of nodes, which defines the path.
        # Desired output is a graph with SubPaths filtered, subpathsGraph
        # for each key, create a new list with string representation of paths
            # This is so we can do string comparisons to find SubPaths
            # And also, so we can deal with multiple object types in the paths
        # There will be two copies of this list.
            # filteredpathsList is the copy we will delete SubPaths from
            # testpathsList is the copy we will use to iterate over
            # We sort testpathsList for efficiency.
            # we make copies because iterating over a list while changing it
                # is like doing brain surgery on yourself -- not recommended
        # If there is a single path for a key, no filter is needed
        # If there are > 1 paths, we need to compare paths
            # Iterate over the paths list shifted right and shifted left
                # This creates a matrix of path comparisons
                # For N paths, there are N(N-1)/2 comparisons
                # The item being compared for SubPathhood is from the left shift
            # For each comparison of the leftpath as a subpath of the rightpath
                # Convert the paths to a string representation to make comparison
                # If leftpath is a subpath of rightpath
                    # remove leftpathsList from the filteredpathsList and
                    # break out of loop, to compare the next leftpath
            # Place the filtered filteredpathsList into a dictionary
            # Return the dictionary with all the filtered paths
                
        
    """ 
    # Desired output is a graph with SubPaths filtered, subpathsGraph
    subpathsGraph = { }
    # for each key, create a new list with string representation of paths
    for key in pathGraph:
        filteredpathsList = [ ]
        for path in pathGraph[key]:
            strpathList = [ ]
            for node in path:
                strpathList.append(str(node))
            filteredpathsList.append(strpathList)
        # filteredpathsList is the copy we will delete SubPaths from
        # testpathsList is the copy we will use to iterate over
        testpathsList = copy.deepcopy(filteredpathsList)
        testpathsList.sort()
        # If there is a single path for a key, no filter is needed
        if len(testpathsList) == 1:
            subpathsGraph[key] = filteredpathsList
        # If there are > 1 paths, we need to compare paths
        # Iterate over the paths list shifted right and shifted left
        for rightpath in testpathsList[1: ]:
            for leftpath in testpathsList[ testpathsList.index(rightpath) -1 : -1] :
                # Convert the paths to a string representation to make comparison
                strleftpath = "".join(leftpath)
                strrightpath= "".join(rightpath)
                # If leftpath is a subpath of rightpath
                if strrightpath.startswith(strleftpath):
                    # remove leftpathsList from the filteredpathsList
                    filteredpathsList.remove(leftpath)
                # break out of loop, to compare the next leftpath
                break
        # Place the filtered filteredpathsList into a dictionary
        subpathsGraph[key] = filteredpathsList
    return subpathsGraph

# Future -- Simplify and Clarify. Possibly use sets module for membership tests




def unionGraphs(graph1={}, graph2={}):
    """Given two Graphs, create a new Graph that is their Relational Union
    Preconditions: Graph in Xaya Format
        Postconditions: returns a graph in XAYA format  with all keys and values
        Invariants: The input graphs do not change
        
        Usage:
        
        Definition:
        # A "keyset" is the set of Keys in a Graph.
        # To Union Two graphs, you must
                # Add keys and values that are unique to each graph
                # Add keys that intersect for the two graphs and
                    #Union the values associated with  these keys
        
    """
    # A "keyset" is the set of Keys in a Graph
    keyset1 = set(graph1)
    keyset2 = set(graph2)
    unionGraph = {}
    # Add keys and values that are unique to each graph
    for key in keyset1.difference(keyset2):
        unionGraph[key] = graph1[key]
    for key in keyset2.difference(keyset1):
        unionGraph[key] = graph2[key]
    # Add keys that intersect for the two graphs and
    for key in keyset1.intersection(keyset2):
        #Union the values of these keys
        unionGraph[key] = list(set(graph1[key]).union(set(graph2[key])))
    return unionGraph


def intersectGraphs(graph1={}, graph2={}):
    """Given two Graphs, create a new Graph that is their Relational Intersection
    `   Preconditions: Graph in Xaya Format
        Postconditions: returns a graph in XAYA format with intersecting keys and values 
        Invariants: The input graphs do not change
        
        Usage:
        
        Definition:
        # A "keyset" is the set of Keys in a Graph.
        # To Intersect Two graphs, you must
                # Add keys that intersect for the two graphs and
                    #intersect the values associated with the  keys
        
    """
    # A "keyset" is the set of Keys in a Graph
    keyset1 = set(graph1)
    keyset2 = set(graph2)
    intersectionGraph = {}
    # Add keys that intersect for the two graphs and
    for key in keyset1.intersection(keyset2):
        #intersect the values associated with the  keys
        intersectionGraph[key] = list(set(graph1[key]).intersection(set(graph2[key])))
    return intersectionGraph


def differenceGraphs(graph1={}, graph2={}):
    """Given two Graphs, create a new Graph that is their Relational Difference
    Preconditions: Graph in Xaya Format
        Postconditions: returns a graph in XAYA format  with differnce in "edges"
        Invariants: The input graphs do not change
        
        Usage:
        
        Definition:
        # A "keyset" is the set of Keys in a Graph.
        # To Difference (the edges of) two graphs, you must 
                # Add keys and values that are unique to the first graph
                # Add keys that intersect for the two graphs and
                    #difference the values associated with  these keys
                    # Remove intersecting keys, with empty list as difference
                    (i.e. no edges left after taking the difference)
                    # result is only those "nozero" valued differences
    """
    keyset1 = set(graph1)
    keyset2 = set(graph2)
    differenceGraph = {}
    for key in keyset1.difference(keyset2):
        differenceGraph[key] = graph1[key]
    for key in keyset1.intersection(keyset2):
        differenceGraph[key] = list(set(graph1[key]).difference(set(graph2[key])))
        # Remove intersecting keys, with empty list as difference
    nozerodifferenceGraph = {}
    for key in differenceGraph:
        if differenceGraph[key] <> []:
            nozerodifferenceGraph[key] = differenceGraph[key]
    
    return nozerodifferenceGraph




def addNode(graph={}, node=''):
    """ From input Graph, creates output Graph with new node with an empty list as the value.
    Wraps unionGraphs for simple node addition functionality.
    
    """
    graph1 = graph
    graph2 = {node :[ ]}
    return unionGraphs(graph1, graph2)

#Future -- Note -- use of set operations means order of value list items can change.
    # This might cause complications if another function assumes list order stable
 
    
def addEdge(graph={}, startnode='',endnode=''):
    """ From input Graph, creates Output Graph with new edge added.
    Wraps unionGraphs for simple edge addition functionality.
    
    """
    graph1 = graph
    graph2 = {startnode:[endnode]}
    return unionGraphs(graph1, graph2)

#Future -- again note that use of set operations may cause complications if
    # the order of value list is important. 

    
def dropNode(graph={}, node=''):
    """ From input Graph, creates output Graph that excludes the selected node
    
    """
    graph2 = {}
    for key in graph:
        if key <> node:
            graph2[key] = graph[key]
    return graph2
    
    
def dropEdge(graph={}, startnode='',endnode=''):
    """ From input Graph creates output Graph which excludes the selected edge.
    Wraps differenceGraphs.
    
    """
    graph1 = graph
    graph2 = {startnode:[endnode]}
    return differenceGraphs(graph1, graph2)

def reverseGraph (graph = {}):
    """
    Reverses the direction of arrows on a graph, so all Parent Nodes become Child Nodes.
    A node with no childs, is left alone.
    
    Preconditions: A XAYA format graph
    
    Postconditions: A XAYA format graph with arcs reversed from the original
    
    Invariants: No Changes to the input graph
    
    Usage:
    
    Definition:
        Every Node with No Parents and No Childs remains the same
        Every Child Node becomes a Parent Node and
            All its parents become its childs
        If a node has no children and is a terminal node
            it dissapears in the graph reversal process. 
    
    """
    copygraph = copy.deepcopy(graph) # Prevents changes to the submitted graph
    revgraph = {}
    for node in copygraph:
        if copygraph[node] == []:
            # Every Node with No Parents and No Childs remains the same
            if not revgraph.has_key(node):
                revgraph[node]= copygraph[node]
            else:
                continue # If a node has no children and is a terminal node it dissapears
        elif copygraph[node] != []:
            # Every Child Node becomes a Parent Node and
            # All its parents become its childs
            for childnode in copygraph[node]:
                if revgraph.has_key(childnode): # If the arc exists, add a new item
                    revgraph[childnode].append(node)
                else:
                    
                    revgraph[childnode] = [node] # If the arc does not exist, create it
    return revgraph
                
            


    
    
# Functions to do --------------------------------------------------------------
#                 --------------------------------------------------------------
    
  
    
#runs doctests of usage examples -- confirms examples still valid. 
if __name__ == '__main__':
    import doctest, sys
    doctest.testmod(sys.modules[__name__])    

 

# REVISION HISTORY
# Revised XXX by YYY

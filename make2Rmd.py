# make2Rmd 0.2
# ==============

# make2Rmd pretends to be a tool to transform a makefile into a (Rstudio) Markdown literate programming script. 
# Version 0.1 is just a parser that linearly wraps the makefile into a Rstudio file. 
# Version 0.2 order the makefile according to the dependency graph 

filename = "./makefile" #the test file 

#OPTIONS 

LINEAR = True 
    

import re

#The expected structure of a makefile is that of comment->rule->code. 

# 1. Parse the Makefile to obtain the dependency graph of the rules and the comment_code graph associated. 

input_file = open(filename, "r")

comment = "" 
code = ""

dependency_graph = dict()
comment_code_graph = dict()
makefile_rule_order = list()  # the order in which the rules appear in the file 

#Regex 
#unixFile = "[\w.]+"  #simple version. Improve!
rule = re.compile('^([\w.]+)\s*\:\s*(.*)')



for linea in input_file:
	linea = linea.lstrip("\n") # remove blank lines 
	if len(linea)>0:
		if linea[0]=="#": # The line is a comment			
			linea = linea.lstrip("#")   # Remove the comment mark
			linea = linea.lstrip(" ")   # Remove the spaces 
			comment += linea	    
			if code!="":		    #If code has been detected previuously
				code +="```\n"	    #Close the chunk 
				#output_file.write(code)  #write in the file 
				comment_code_graph[target]["code"] = code
				print target, code
				code = ""		 #Initializes the code 

		else:		 # The line is code (= not comment)		
			isRule = re.search(rule, linea)
			# is it a rule?
			if isRule:
				if code!="":
					code +="```\n"	    #Close the chunk 
					comment_code_graph[target]["code"] = code
					code = ""
				target = isRule.group(1)  #take the target
				dependencies = isRule.group(2).split()  #take the dependencies
				#print target, dependencies  
				dependency_graph[target] = dependencies  #actualize graph
				makefile_rule_order.append(target)
				comment_code_graph[target]= {comment : "", code : ""}
					
				
			else: 
				if code=="":		#if it is the first line of code
					code = "```{r, engine='bash', eval=FALSE}\n" # open the chunk
					code += linea
				else:
	 				code += linea

			if comment!="":  	#If there a previous comment 
				#output_file.write(comment + "\n")  #write the comment
				comment_code_graph[target]["comment"] = comment
				comment = "" 			# initializes it 


comment_code_graph[target]["comment"] = comment
comment_code_graph[target]["code"] = code

print comment_code_graph["kbd.o"].get("code", "")



input_file.close()

#print comment_code_graph["DivideByCellLine"][1]

## 2. Sort the graph topologically 

if not LINEAR: 
	pass

# 3. Write the output file according to the graph 




# 3.1. The linear parser 
output_file =  open(filename + "_wrapped.Rmd", "w")

if LINEAR:
	#nrule = 1
	for target in makefile_rule_order:
		#print nrule	
		output_file.write(comment_code_graph[target].get("comment", ""))
		output_file.write("\n")
		if len(comment_code_graph[target])>1:
			output_file.write(comment_code_graph[target].get("code", ""))
			output_file.write("\n") 
		#nrule +=1

#3.2. Topologically sorted 

else: 

	targets = dependency_graph.keys()

	Values = dependency_graph.values()
	files = [x for sublist in Values for x in sublist]
	files = list(set(files))





output_file.close()




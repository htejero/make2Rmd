# make2Rmd 0.1
# ==============

# make2Rmd pretends to be a tool to transform a makefile into a (Rstudio) Markdown literate programming script. 
# Version 0.1 is just a parser that linearly wraps the makefile into a Rstudio file. 

filename = "../Garnett/exome/Makefile" #the test file 

input_file = open(filename, "r")    
output_file =  open(filename + "_wrapped.Rmd", "w")


#The expected structure of a makefile is that of comment->rule->code. In version 0.1 the dependency
#graph of the makefile is not used. The script just parses the file lienarly detecting comments and including the rule in the code. Each time it detects a change from comment to code, write the comment an then initializes it. Each time it detects a change from code to comment, writes the code and initialized it. 

comment = "" 
code = ""
for linea in input_file:
	linea = linea.lstrip("\n") # remove blank lines 
	if len(linea)>0:
		if linea[0]=="#": # The line is a comment			
			linea = linea.lstrip("#")   # Remove the comment mark
			linea = linea.lstrip(" ")   # Remove the spaces 
			comment += linea	    
			if code!="":		    #If code has been detected previuously
				code +="```\n"	    #Close the chunk 
				output_file.write(code)  #write in the file 
				code = ""		 #Initializes the code 
		else:		 # The line is code 
			if comment!="":  	#If there a previous comment 
				output_file.write(comment + "\n")  #write the comment
				comment = "" 			# initializes it 
			if code=="":		#if it is the first line of code
				code = "```{r, engine='bash', eval=FALSE}\n" # open the chunk
				code += linea
			else:
	 			code += linea
	


input_file.close()
output_file.close()

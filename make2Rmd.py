filename = "../Garnett/exome/Makefile"

input_file = open(filename, "r")
output_file =  open(filename + "_wrapped.Rmd", "w")

comment = ""
code = ""
for linea in input_file:
	linea = linea.lstrip("\n")
	if len(linea)>0:
		if linea[0]=="#": # Es un comentario de Make			
			linea = linea.lstrip("#")
			linea = linea.lstrip(" ")
			comment += linea
			if code!="":
				code +="```\n"
				output_file.write(code)
				code = ""
		else:
			if comment!="":
				output_file.write(comment + "\n")
				comment = ""
			if code=="":
				code = "```{r, engine='bash', eval=FALSE}\n"
				#linea = linea.lstrip("\n")
				code += linea
			else:
				#linea = linea.lstrip("\n")
	 			code += linea
	


input_file.close()
output_file.close()

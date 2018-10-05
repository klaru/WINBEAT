#! python3
import os, sys

print('Input file name : ', end='')
infilename = input()
print('Output file name : ', end='')
outfilename = input()

linenew = '1'
lineout = ''
comment = False
commentend = False
with open(infilename, 'r') as infile, open(outfilename, 'w') as outfile :        
    for line in (infile) :
        if line[:2] == '(*' :
            comment = True
            if line[len(line)-3:len(line)] == '*)\n' \
			or line[len(line)-4:len(line)] == '*);\n' :			
                commentend = True
        else:
            if line[len(line)-3:len(line)] == '*)\n' \
			or line[len(line)-4:len(line)] == '*);\n' :
                commentend = True    
            else:
                pass  
				
        if comment == True :
	        lineout = '#' + line
        else:
	        lineout = line		
			
        if commentend == True :
            comment = False
            commentend = False
		 

        lineout = lineout.replace('#(*', '#')
        lineout = lineout.replace('*)', '')
        lineout = lineout.replace('end;', '#end')
        lineout = lineout.replace('end ','#end ')
        lineout = lineout.replace(' end', ' #end')
        lineout	= lineout.replace('begin', '#begin')
        if lineout.find('#') == -1 :
            lineout = lineout.replace('(*', '#')	
        else:
            lineout = lineout.replace('(*', '')
        lineout = lineout.replace('ClrScr', "os.system('cls')")
        lineout = lineout.replace('<>', '!=')
        lineout = lineout.replace(' =', ' ==')		
        lineout = lineout.replace('procedure', 'def')
        lineout = lineout.replace('function', 'def')
        lineout = lineout.replace('var', '#var')
        lineout = lineout.replace('const', '#const')
        lineout = lineout.replace('unit', '#unit')
        lineout = lineout.replace('interface', '#interface')
        lineout = lineout.replace('implementation', '#implementation')
        lineout = lineout.replace('uses', 'import')
        lineout = lineout.replace('then', ':')
        lineout = lineout.replace('do ', ': ')
        lineout = lineout.replace('else', 'else:')
        lineout = lineout.replace('writeln ;', r"rint('\n')")
        lineout = lineout.replace('writeln;', r"print('\n')")
        lineout = lineout.replace('writeln', 'print')
        lineout = lineout.replace(':= 1 to', 'in range(1, ')
        lineout = lineout.replace('sqrt(', 'math.sqrt(')
        lineout = lineout.replace('true', 'True')
        lineout = lineout.replace('TRUE', 'True')
        lineout = lineout.replace('false', 'False')
        lineout = lineout.replace('FALSE', 'False')
        lineout = lineout.replace('ln(', 'math.log(')
        lineout = lineout.replace('sqr(', 'math.pow(')
		
        lineout = lineout.replace(':=1',' = 1')
        lineout = lineout.replace(':=', '=')
        lineout = lineout.replace(';', '') 
        lineout = lineout.replace('##', '#')
		
        outfile.write(lineout)	
					
infile.close()
outfile.close()
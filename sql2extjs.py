#convert mysql dump to ExtJS model files
#does not support data types yet

import os
import re

def search_file(dump, models_to):
    i = 0
    for line in dump:
        i += 1
        if "CREATE" in line:
            tokens = re.findall(r"[\w']+|[.,!?;]", line)
            name = tokens[len(tokens)-1]
            j = i
            model = []
            while ";" not in dump[j]: 
                model.append( re.sub('[`,]', '', dump[j].lstrip()) )
                j += 1
            create_model(name, model, models_to)
       
       
def create_model(name, model, models_to):
    member = []
    for item in model:
        member.append(item.partition(' ')[0])
    
    print 'Parsing model:', name + '...'
    
    model_file = open(models_to + ('\\' + name + '.js'), 'w')
    
    model_file.write('Ext.define(\'app.' + name + '\', {\n\t')
    model_file.write('extend: \'Ext.data.Model\',\n\t')
    model_file.write('fields: [\n\t\t')
    
    for item in member[:-1]:
        model_file.write('{ name: \'' + item + '\' },\n\t\t')
        
    model_file.write('{ name: \'' + member[-1] + '\' }\n\t]\n});')
    

def main():
    target = raw_input("Enter the path of your file:\n>")
    
    assert os.path.exists(target), "I did not find the file at, " + str(target)
    print '\nFile found - ' + str(target) + '\n'
    
    models_to = raw_input("Where would you like to store the models?\n>")
   
    assert os.path.exists(models_to), "Invalid path"
    print '\n'
    
    lines = [line.strip('\n') for line in open(target, 'r')]   # will this cause issues ?
    search_file(lines, models_to)
    
    print '\nFinished\n'
    
if __name__ == "__main__":
    main()
output = ""
compile_error_list = []#List for compile errors.
runtime_error_list = []#List for runtime errors
var_dict = {}#Dict for variables for during compile error finding.
def main():
    # DO NOT CHANGE
    global output
    handle = open('input.tup',encoding="utf-8")
    code = handle.read()
    handle.close()
    splitted_lines = code.splitlines()#Splitted the code line by line.
    #Checking Programı Başlat and Programı Bitir lines.
    if lower_turkish(splitted_lines[0]) != "programı başlat.":
        compile_error_list.append(1)
    if lower_turkish(splitted_lines[-1]) != "programı bitir.":
        compile_error_list.append(len(splitted_lines))
    #Checking end of the lines.
    for i in range(1,len(splitted_lines)-1):
        if not lines(splitted_lines[i].split()) :     
            compile_error_list.append(i+1)
    #Counting words and spaces of the each line by paying attention to the exclamation points.
    for i in range(len(splitted_lines)):
        lines_word = splitted_lines[i]
        space_count = count_(lines_word)
        if space_count != word_count(lines_word)-1:
            compile_error_list.append(i+1)
    #Cheking line structure of olsun line.
    for j in range(1,len(splitted_lines)-1):
        lines_word = splitted_lines[j].split()
        if lower_turkish(splitted_lines[j].split()[-1])== "olsun.":
            if not (lines_word[1] == "bir" or lower_turkish(lines_word[1]) == "değeri"):
                compile_error_list.append(j+1)
    #Assigning variables' type and type's line number to dict. 
    for j in range(1,len(splitted_lines)-1):
        lines_word = splitted_lines[j].split()
        if lower_turkish(splitted_lines[j].split()[-1])== "olsun.":
            if lines_word[1] == "bir" :
                if len(lines_word)==4:
                    if var_check(lines_word):
                        var_dict[lower_turkish(lines_word[0])] = [["type","satır"],["değer","satır"]]
                        var_dict[lower_turkish(lines_word[0])][0][0] = lines_word[2]
                        var_dict[lower_turkish(lines_word[0])][0][1] = j+1
                    else :
                        compile_error_list.append(j+1)
                else :
                    compile_error_list.append(j+1)
    #Checking value assign line.
    for j in range(1,len(splitted_lines)-1):
        lines_word = splitted_lines[j].split()
        if lower_turkish(splitted_lines[j].split()[-1])== "olsun.":
            if lower_turkish(lines_word[1]) == "değeri": 
                if olsun(lines_word) :
                    if not olsun_value(lines_word):
                        compile_error_list.append(j+1)
                    else :
                        new_list = []
                        for k in range(2,len(lines_word)-1):
                            new_list.append(lines_word[k])
                        if not ce_calculation(new_list):
                            compile_error_list.append(j+1)
                        else :
                            var_dict[lower_turkish(lines_word[0])][1][1] = j+1
                            if len(new_list) == 1 :
                                var_dict[lower_turkish(lines_word[0])][1][0] = lines_word[2]
                else :
                    compile_error_list.append(j+1)
    
    for j in range(1,len(splitted_lines)-1):
        lines_word = splitted_lines[j].split()
        if lower_turkish(splitted_lines[j].split()[-1])== "yazdır.":#Checking yazdır line's structure.
            if olsun(splitted_lines[j].split()):
                if not yazdır_value(lines_word):
                    compile_error_list.append(j+1)
                else :
                    new_list = []
                    for k in range(len(lines_word)-1):
                        new_list.append(lines_word[k])
                    if not ce_calculation(new_list):
                        compile_error_list.append(j+1)
            else :
                compile_error_list.append(j+1)
        elif lower_turkish(lines_word[-1]) == "zıpla.":#Checking zıpla line's structure.
            if (lower_turkish(lines_word[-2]) == "satıra" and zıpla(lines_word)):
                if not zıpla_value(lines_word):
                    compile_error_list.append(j+1)
                else :
                    new_list = []
                    for k in range(len(lines_word)-2):
                        new_list.append(lines_word[k])
                    if len(new_list) == 1 :
                        if type_determine(new_list[0]) == "reel-sayı":
                            if not float(reel_sayı_without_dot(new_list[0])) == int(float(reel_sayı_without_dot(new_list[0]))):
                                compile_error_list.append(j+1)
                            elif int(float(reel_sayı_without_dot(new_list[0]))) > len(splitted_lines) or int(float(reel_sayı_without_dot(new_list[0])))<=0:
                                compile_error_list.append(j+1)
                        elif type_determine(new_list[0]) == "tam-sayı":
                            if int(new_list[0])> len(splitted_lines) or 0>=int(new_list[0]):
                                compile_error_list.append(j+1)
                        elif type_determine(new_list[0]) == "variable":
                            continue
                        elif type_determine(new_list[0]) == "metin":
                            if not zıpla_odd(new_list[0]) :
                                compile_error_list.append(j+1)
                            if zıpla_odd(new_list[0]) == "tam-sayı":
                                if not (10000>=tam_sayı_without_dot(metin_convert(new_list[0]))>=-10000) :
                                    compile_error_list.append(j+1)
                                if tam_sayı_without_dot(metin_convert(new_list[0]))> len(splitted_lines) or 0>= tam_sayı_without_dot(metin_convert(new_list[0])):
                                    compile_error_list.append(j+1)
                            if zıpla_odd(new_list[0])=="reel-sayı":
                                if not float(reel_sayı_without_dot(metin_convert(new_list[0]))) == int(float(reel_sayı_without_dot(metin_convert(new_list[0])))):
                                    compile_error_list.append(j+1)
                                if  int(float(reel_sayı_without_dot(metin_convert(new_list[0]))))> len(splitted_lines) or 0>= int(float(reel_sayı_without_dot(metin_convert(new_list[0])))):
                                    compile_error_list.append(j+1)
                    elif not z_ce_calculation(new_list):
                        compile_error_list.append(j+1)
            else :
                compile_error_list.append(j+1)


    if len(compile_error_list)>0:#If there is a compile error , program won+t execute.
        output = (f"Compile error at line {min(compile_error_list)}.")
    else :#If there is no compile error , program will execute.
        var2_dict = dict()
        j = 0
        while j < len(splitted_lines) and len(runtime_error_list) == 0 :
            lines_word = splitted_lines[j].split()
            if lower_turkish(splitted_lines[j].split()[-1])== "olsun.":
                if lines_word[1] == "bir" :
                    var2_dict[lower_turkish(lines_word[0])] = [["type","satır"],["değer","satır"]]
                    var2_dict[lower_turkish(lines_word[0])][0][0] = lines_word[2]
                    var2_dict[lower_turkish(lines_word[0])][0][1] = j+1             
                elif lower_turkish(lines_word[1]) == "değeri":
                    if lower_turkish(lines_word[0]) not in var2_dict :
                        runtime_error_list.append(j+1)
                    else :
                        new_list = []
                        var2_dict[lower_turkish(lines_word[0])][1][1] = j+1
                        for i in range(2,len(lines_word)-1):
                            new_list.append(lines_word[i])
                        if len(new_list) == 1 :
                            if type_determine(new_list[0])== "variable":
                                if lower_turkish(new_list[0]) not in var2_dict :
                                    runtime_error_list.append(j+1)
                                elif var2_dict[lower_turkish(new_list[0])][1][0]== "değer":
                                    runtime_error_list.append(j+1)
                                else :
                                    new_value = var2_dict[lower_turkish(new_list[0])][1][0]
                                    var2_dict[lower_turkish(lines_word[0])][1][0] = new_value
                            else :
                                var2_dict[lower_turkish(lines_word[0])][1][0] = lines_word[2]
                        else :
                            if not rte_calculation(new_list,var2_dict):
                                runtime_error_list.append(j+1)
                            else :
                                if not son_değer_hesaplama(new_list,var2_dict):
                                    runtime_error_list.append(j+1)
                                else :
                                    var2_dict[lower_turkish(lines_word[0])][1][0] = son_değer_hesaplama(new_list,var2_dict)
                        if rte_var_type(lower_turkish(lines_word[0]),var2_dict) != type_determine(rte_value_(lower_turkish(lines_word[0]),var2_dict)):
                            runtime_error_list.append(j+1)
            elif lower_turkish(lines_word[-1])== "yazdır.":
                var_list = []
                op_list = []
                new_list = []
                for i in range(len(lines_word)-1):
                    new_list.append(lines_word[i])
                    if i%2 == 0 :
                        var_list.append(lines_word[i])
                    else :
                        op_list.append(lines_word[i])
                for k in range(len(var_list)):
                    if type_determine(var_list[k]) == "variable":
                        if lower_turkish(var_list[k]) not in var2_dict :
                            runtime_error_list.append(j+1)
                        elif var2_dict[lower_turkish(var_list[k])][1][0]== "değer":
                            runtime_error_list.append(j+1)
                if j+1 not in runtime_error_list:
                    if not rte_calculation(new_list,var2_dict):
                        runtime_error_list.append(j+1)
                    else :
                        if  not son_değer_hesaplama(new_list,var2_dict):
                            runtime_error_list.append(j+1)
                        elif len(runtime_error_list) == 0 :
                            if type_determine(son_değer_hesaplama(new_list,var2_dict)) == "metin":
                                output += metin_convert(son_değer_hesaplama(new_list,var2_dict)) + "\n"
                            else :
                                output += (son_değer_hesaplama(new_list,var2_dict)) + "\n"   
            elif lower_turkish(lines_word[-1]) == "zıpla.":
                new_list = []
                var_list = []
                op_list = []
                for i in range(len(lines_word)-2):
                    if lines_word[i][-1] == ".":
                        new_list.append(lines_word[i][:-1])
                        if i%2 == 0 :
                            var_list.append(lines_word[i][:-1])
                        else :
                            op_list.append(lines_word[i][:-1])
                    else :
                        new_list.append(lines_word[i])
                        if i%2 == 0 :
                            var_list.append(lines_word[i])
                        else :
                            op_list.append(lines_word[i])
                for k in range(len(var_list)):
                    if type_determine(var_list[k]) == "variable":
                        if lower_turkish(var_list[k]) not in var2_dict :
                            runtime_error_list.append(j+1)
                        if var2_dict[lower_turkish(var_list[k])][1][0]== "değer":
                            runtime_error_list.append(j+1)
                if j+1 not in runtime_error_list:
                    if not rte_calculation(new_list,var2_dict):
                        runtime_error_list.append(j+1)
                    else :
                        if not son_değer_hesaplama(new_list,var2_dict):
                            runtime_error_list.append(j+1) 
                        else :
                            if type_determine(son_değer_hesaplama(new_list,var2_dict)) == "reel-sayı":
                                if float(reel_sayı_without_dot(son_değer_hesaplama(new_list,var2_dict)))!=int(float(reel_sayı_without_dot(son_değer_hesaplama(new_list,var2_dict)))):
                                    runtime_error_list.append(j+1)
                                elif int(float(reel_sayı_without_dot(son_değer_hesaplama(new_list,var2_dict)))) <=0 or int(float(reel_sayı_without_dot(son_değer_hesaplama(new_list,var2_dict))))>len(splitted_lines):
                                    runtime_error_list.append(j+1)
                                else :
                                    j = int(float(reel_sayı_without_dot(son_değer_hesaplama(new_list,var2_dict))))-2
                            elif type_determine(son_değer_hesaplama(new_list,var2_dict)) == "tam-sayı":
                                if int(float(reel_sayı_without_dot(son_değer_hesaplama(new_list,var2_dict)))) <=0 or int(float(reel_sayı_without_dot(son_değer_hesaplama(new_list,var2_dict))))>len(splitted_lines):
                                    runtime_error_list.append(j+1)
                                else :
                                    j =  int(tam_sayı_without_dot(son_değer_hesaplama(new_list,var2_dict)))-2
                            elif type_determine(son_değer_hesaplama(new_list,var2_dict)) == "metin":
                                if not zıpla_odd(son_değer_hesaplama(new_list,var2_dict)) :
                                    runtime_error_list.append(j+1)
                                if zıpla_odd(son_değer_hesaplama(new_list,var2_dict)) == "tam-sayı":
                                    if not (10000>=tam_sayı_without_dot(metin_convert(son_değer_hesaplama(new_list,var2_dict)))>=-10000) :
                                        runtime_error_list.append(j+1)
                                    elif tam_sayı_without_dot(metin_convert(son_değer_hesaplama(new_list,var2_dict)))> len(splitted_lines) or 0>= tam_sayı_without_dot(metin_convert(son_değer_hesaplama(new_list,var2_dict))):
                                        runtime_error_list.append(j+1)
                                    else :
                                        j =  int(tam_sayı_without_dot(metin_convert(son_değer_hesaplama(new_list,var2_dict))))-2
                                if zıpla_odd(son_değer_hesaplama(new_list,var2_dict))=="reel-sayı":
                                    if not float(reel_sayı_without_dot(metin_convert(son_değer_hesaplama(new_list,var2_dict)))) == int(float(reel_sayı_without_dot(metin_convert(son_değer_hesaplama(new_list,var2_dict))))):
                                        runtime_error_list.append(j+1)
                                    elif  int(float(reel_sayı_without_dot(metin_convert(son_değer_hesaplama(new_list,var2_dict)))))> len(splitted_lines) or 0>= int(float(reel_sayı_without_dot(metin_convert(son_değer_hesaplama(new_list,var2_dict))))):
                                        runtime_error_list.append(j+1)
                                    else :
                                        j =  int(float(reel_sayı_without_dot(metin_convert(son_değer_hesaplama(new_list,var2_dict)))))-2

                            else :
                                runtime_error_list.append(j+1)

            j += 1
        if len(runtime_error_list) > 0 :
            output += (f"Runtime error at line {min(runtime_error_list)}.") +"\n"
  
    # DO NOT CHANGE
    handle = open('output.txt','w')
    handle.write(output)
    handle.close()

def lower_turkish(text):
    replacements = {
        "I": "ı",
        "İ": "i",
        "Ç": "ç",
        "Ğ": "ğ",
        "Ö": "ö",
        "Ş": "ş",
        "Ü": "ü"
    }
    result = ""
    for char in text:
        if char in replacements:
            result += replacements[char]
        elif char in numbers or char  in other_chr :
            result += char
        else:
            result += char.lower()
    return result
#Türkçe karakterler 
turkish_alphabet = ["a","b","c","ç","d","e","f","g","ğ","h","ı","i","j","k","l","m","n","o","ö","p","r","s","ş","t","u","ü","v","y","z",
                    "A","B","C","Ç","D","E","F","G","Ğ","H","I","İ","J","K","L","M","N","O","Ö","P","R","S","Ş","T","U","Ü","V","Y","Z"]
numbers =          ["0","1","2","3","4","5","6","7","8","9"]
other_chr =        [",",".",":",";"," "]
all_list = turkish_alphabet+numbers+other_chr
#3 2 ve 1 basamaklı sayılar için 
def num(num):
    for i in range(len(num)):
        if num[i] not in numbers:
            return False 
    return True
#Türkçe karakter kontrol eden fonksiyon
def turkish_chr(word):
    for i in range(len(word)):
        if word[i] not in turkish_alphabet :
            return False
    return True
#Son kelimeler sınırlı olduğu için onları kontrol ediyor noktalarla beraber.
def lines(line):
    if lower_turkish(line[-1]) in ["yazdır.","olsun.","zıpla."]:
        return True
    return False 

def olsun(line):
    if len(line)%2 == 0 :
        return True
    return False

def zıpla(line):
    if len(line)%2 == 1 :
        return True
    return False

def count_(line):#riskli
    new_list = []
    for i in range(len(line)):
        if line[i] == "!":
            new_list.append(i)
    if len(new_list) == 2 :
        str_ = line[:new_list[0]+1]+line[new_list[1]+1:]
    else :
        str_ = line
    return str_.count(" ")

def word_count(line):#riskli
    new_list = []
    for i in range(len(line)):
        if line[i] == "!":
            new_list.append(i)
    if len(new_list) == 2 :
        str_ = line[:new_list[0]+1]+line[new_list[1]+1:]
    else :
        str_ = line
    return len(str_.split())

def var_check(lines_word):
    if not olsun(lines_word):
        return False
    if not (20>=len(lines_word[0]) and turkish_chr(lines_word[0])):
        return False
    if lower_turkish(lines_word[0]) in ["artı", "eksi", "çarp", "bölü", "metin","tam-sayı","reel-sayı"]:
        return False
    if lower_turkish(lines_word[2]) not in ["tam-sayı","reel-sayı","metin"]:
        return False
    return True
#metinin karakter sayınısını ve doğru yazılıp yazılmadığını kontrol ediyor.
def metin(metin):
    if len(metin)-2 > 50 :
        return False
    if not(metin[0] == "!" and metin[-1] == "!"):
        return False 
    for i in range(1,len(metin)-1):
        if metin[i] not in all_list:
            return False
    return True
#ondalıklı kısmı buluyor
def find_decimal_point(reelsayı):
    find_ = reelsayı.find(",")
    decimal_position = len(reelsayı)-find_-1
    return decimal_position
#reel sayının olması gereken hali 
def reel_sayı_without_dot(reelsayı) :
    sayı_list = list(reelsayı)
    new_list = []
    if new_list.count(",") > 1 :
        return False 
    for j in range(len(sayı_list)):
        if sayı_list[j] == ".":
            continue
        if sayı_list[j] == ",":
            new_list.append(".")
        else :
            new_list.append(sayı_list[j])
    sayı = "".join(new_list)
    if sayı[0] == ".":
        sayı = "0"+ sayı
    return sayı
#reel sayının doğru yazılıp yazılmadığını kontrol ediyor
def reel_sayı_yazılış(reelsayı) :
    str_ = ""
    decimal_pos = find_decimal_point(reelsayı)
    sayı_list = list(reelsayı)
    new_list = []
    for j in range(len(sayı_list)):
        if sayı_list[j] == "." or sayı_list[j] == "," :
            continue
        else :
            new_list.append(sayı_list[j])
    sayı = "".join(new_list)
    for i in range(len(sayı)):
        index = len(sayı)-1-i
        if i == decimal_pos-1:
            str_ =","+sayı[index] + str_
        elif index == 0 :
            str_ = sayı[0]+ str_ 
        elif (len(sayı)-decimal_pos-index) % 3 == 0 :
            str_ ="."+sayı[index] + str_
        else :
            str_ = sayı[index] + str_
    return str_
#reel sayının aralığını ve doğru yazılıp yazılmadığını kontrol ediyor.
def reel_sayı(reelsayı):
    if reel_sayı_without_dot == False :
        return False  
    if find_decimal_point(reelsayı)>3 :
        return False 
    if reelsayı != reel_sayı_yazılış(reelsayı):
        return False
    if not (10000.000>=float(reel_sayı_without_dot(reelsayı))>=-10000.000):
        return False 
    return True

#Tam sayının doğru yazılıp yazılmadığını kontrol ediyor
def tam_sayı_yazılış(sayı) :
    str_ = ""
    sayı_list = list(sayı)
    new_list = []
    for j in range(len(sayı_list)):
        if sayı_list[j] == ".":
            continue
        else :
            new_list.append(sayı_list[j])
    sayı = "".join(new_list)

    for i in range(len(sayı)):
        index = len(sayı)-1-i
        if index == 0 :
            str_ = sayı[0]+ str_
        elif (len(sayı)-index) % 3 == 0 :
            str_ ="."+sayı[index] + str_
        else :
            str_ = sayı[index] + str_
    return str_

#Noktayla ayrılmış sayıyı normal haline çevirir
def tam_sayı_without_dot(sayı) :
    sayı_list = list(sayı)
    new_list = []
    for j in range(len(sayı_list)):
        if sayı_list[j] == ".":
            continue
        else :
            new_list.append(sayı_list[j])
    sayı = "".join(new_list)
    return int(sayı)
#Tam sayının aralığını ve  doğru yazılıp yazılmadığını yukarıdaki fonksiyonlarla kontrol ediyor.
def tam_sayı(tamsayı):
    if tamsayı != tam_sayı_yazılış(tamsayı):
        return False 
    if not (10000>=tam_sayı_without_dot(tamsayı)>=-10000):
        return False
    return True
def yazdır_value(line):
    for i in range(len(line)-1):
        if i%2 == 1:
            if lower_turkish(line[i]) not in ["artı", "eksi", "çarp", "bölü"]:
                return False
        if i%2 == 0 :
            if line[i][0]== "!" and line[i][-1] == "!":#metin
                if not metin(line[i]):
                    return False
            elif "," in line[i] :#reel sayı
                for j in range(len(line[i])):
                    if line[i][j] not in [".",",","1","2","3","4","5","6","7","8","9","0"] :
                        return False   
                if not reel_sayı(line[i]):
                    return False
            elif "," not in line[i] and ("." in line[i] or num(line[i])) :#tamsayı
                for j in range(len(line[i])):
                    if line[i][j] not in [".","1","2","3","4","5","6","7","8","9","0"] :
                        return False
                if not tam_sayı(line[i]):
                    return False
            else  :
                if lower_turkish(line[i]) not in var_dict:
                    return False
    return True

def olsun_value(line):
    value_list = []
    if lower_turkish(line[0]) not in var_dict:
        return False
    else:
        for i in range(2,len(line)-1):
            value_list.append(lower_turkish(line[i]))
        if len(value_list) % 2 == 1 :
            for k in range(len(value_list)):
                if k%2 == 1 :
                    if lower_turkish(value_list[k]) not in ["artı", "eksi", "çarp", "bölü"]:
                        return False
                elif k%2 == 0 :
                    if value_list[k][0]== "!" and value_list[k][-1] == "!":#metin
                        if not metin(value_list[k]):
                            return False
                    elif "," in value_list[k]:#reel-sayı
                        for j in range(len(value_list[k])):
                            if value_list[k][j] not in [".",",","1","2","3","4","5","6","7","8","9","0"] :
                                return False 
                        if not reel_sayı(value_list[k]):
                            return False
                    elif "," not in value_list[k] and ("." in value_list[k] or num(value_list[k])) :#tam-sayı
                        for j in range(len(value_list[k])):
                            if value_list[k][j] not in [".","1","2","3","4","5","6","7","8","9","0"]:
                                return False 
                        if not tam_sayı(value_list[k]):
                            return False
                    else  :
                        if lower_turkish(value_list[k]) not in var_dict:#variable
                            return False
        else :
            return False
    return True

def zıpla_value(line):
    for i in range(len(line)-2):
        if line[-3][-1] != ".":
            return False 
        else :
            if i%2 == 1:
                if lower_turkish(line[i]) not in ["artı", "eksi", "çarp", "bölü"]:
                    return False
            if i%2 == 0 :
                if line[i]==line[-3]:
                    line[i] =line[-3][:-1]
                    if line[i][0]== "!" and line[i][-1] == "!":#metin
                        if not metin(line[i]):
                            return False
                    elif "," in line[i] :#reel sayı
                        for j in range(len(line[i])):
                            if line[i][j] not in [".",",","1","2","3","4","5","6","7","8","9","0"] :
                                return False   
                        if not reel_sayı(line[i]):
                            return False
                    elif "," not in line[i] and ("." in line[i] or num(line[i])) :#tamsayı
                        for j in range(len(line[i])):
                            if line[i][j] not in [".","1","2","3","4","5","6","7","8","9","0"] :
                                return False
                        if not tam_sayı(line[i]):
                            return False
                    else  :
                        if lower_turkish(line[i]) not in var_dict:
                            return False
                else :
                    if line[i][0]== "!" and line[i][-1] == "!":#metin
                        if not metin(line[i]):
                            return False
                    elif "," in line[i] :#reel sayı
                        for j in range(len(line[i])):
                            if line[i][j] not in [".",",","1","2","3","4","5","6","7","8","9","0"] :
                                return False
                        if not reel_sayı(line[i]):
                            return False
                    elif "," not in line[i] and ("." in line[i] or num(line[i])) :#tamsayı
                        for j in range(len(line[i])):
                            if line[i][j] not in [".","1","2","3","4","5","6","7","8","9","0"] :
                                return False
                        if not tam_sayı(line[i]):
                            return False
                    else  :
                        if lower_turkish(line[i]) not in var_dict:
                            return False
    return True


def type_determine(value):
    if value[0]== "!" and value[-1] == "!":#metin
        if  metin(value):
            return "metin"
    elif "," in value :#reel sayı
        for j in range(len(value)):
            if value[j] not in [".",",","1","2","3","4","5","6","7","8","9","0"] :
                return False
        if reel_sayı(value):
            return "reel-sayı"
    elif ","  not in value and ("." in value or num(value)) :#tamsayı
        for j in range(len(value)):
            if value[j] not in [".","1","2","3","4","5","6","7","8","9","0"] :
                    return False
        if tam_sayı(value):
            return "tam-sayı"
    else  :
        return "variable"

#ilk sts sonra true ise type sts.for döngüsü içinde 
def sts(a,b,operator):
    if (a == "tam-sayı" and b == "tam-sayı") and (operator == "artı" or operator == "eksi"):
        return True
    if (a == "tam-sayı" and b == "reel-sayı") and (operator == "artı" or operator == "eksi"):
        return False
    if (a == "tam-sayı" and b == "metin") and (operator == "artı" or operator == "eksi"):
        return True
    

    if (a == "reel-sayı" and b == "tam-sayı") and (operator == "artı" or operator == "eksi"):
        return False
    if (a == "reel-sayı" and b == "reel-sayı") and (operator == "artı" or operator == "eksi"):
        return True
    if (a == "reel-sayı" and b == "metin") and (operator == "artı" or operator == "eksi"):
        return True
    

    if (a == "metin" and b == "tam-sayı") and (operator == "artı" or operator == "eksi"):
        return True
    if (a == "metin" and b == "reel-sayı") and (operator == "artı" or operator == "eksi"):
        return True
    if (a == "metin" and b == "metin") and (operator == "artı" or operator == "eksi"):
        return True
    
    if (a == "tam-sayı" and b == "tam-sayı") and (operator == "çarp" or operator == "bölü"):
        return True
    if (a == "tam-sayı" and b == "reel-sayı") and (operator == "çarp" or operator == "bölü"):
        return False
    if (a == "tam-sayı" and b == "metin") and (operator == "çarp" or operator == "bölü"):
        return True
    
    

    if (a == "reel-sayı" and b == "tam-sayı") and (operator == "çarp" or operator == "bölü"):
        return False
    if (a == "reel-sayı" and b == "reel-sayı") and (operator == "çarp" or operator == "bölü"):
        return True
    if (a == "reel-sayı" and b == "metin") and (operator == "çarp" or operator == "bölü"):
        return True
    
    if (a == "metin" and b == "tam-sayı") and (operator == "çarp" or operator == "bölü"):
        return True
    if (a == "metin" and b == "reel-sayı") and (operator == "çarp" or operator == "bölü"):
        return True
    if (a == "metin" and b == "metin") and (operator == "çarp" or operator == "bölü"):
        return False   
    if (a not in ["tam-sayı","metin","reel-sayı"]) or (b not in ["tam-sayı","metin","reel-sayı"]):
        return True 
    return False
def type_sts(x,y,operator):
    if (x == "tam-sayı" and y == "tam-sayı") and (operator == "artı" or operator == "eksi"):
        return "tam-sayı"
    if (x == "tam-sayı" and y == "metin") and (operator == "artı" or operator == "eksi"):
        return "tam-sayı"
    if (x == "reel-sayı" and y == "reel-sayı") and (operator == "artı" or operator == "eksi"):
        return "reel-sayı"
    if (x == "reel-sayı" and y == "metin") and (operator == "artı" or operator == "eksi"):
        return "reel-sayı"
    if (x == "metin" and y == "tam-sayı") and (operator == "artı" or operator == "eksi"):
        return "tam-sayı"
    if (x == "metin" and y == "reel-sayı") and (operator == "artı" or operator == "eksi"):
        return "reel-sayı"
    if (x == "metin" and y == "metin") and (operator == "artı" or operator == "eksi"):
        return "metin"
    if (x == "tam-sayı" and y == "tam-sayı") and (operator == "çarp" or operator == "bölü"):
        return "reel-sayı"
    if (x == "tam-sayı" and y == "metin") and (operator == "çarp"):
        return "metin"
    if (x == "reel-sayı" and y == "reel-sayı") and (operator == "çarp" or operator == "bölü"):
        return "reel-sayı"
    if (x == "reel-sayı" and y == "metin") and (operator == "çarp" or operator == "bölü"):
        return "reel-sayı"
    if (x == "metin" and y == "tam-sayı") and (operator == "çarp"):
        return "metin"
    if (x == "metin" and y == "reel-sayı") and (operator == "çarp" or operator == "bölü"):
        return "reel-sayı"
    if (x == "metin" and y == "tam-sayı") and (operator == "bölü"):
        return "reel-sayı"
    if (x == "tam-sayı" and y == "metin") and (operator == "bölü"):
        return "reel-sayı"
    

def ce_calculation(line):
    op_list = []
    varr_list = []
    for i in range(len(line)):
        if i%2 == 1 :
            op_list.append(line[i])
        if i%2 == 0 :
            varr_list.append(line[i])
    a = type_determine(varr_list[0])
    for j in range(len(op_list)):
        operator = op_list[j]
        b = type_determine(varr_list[j+1])
        if sts(a,b,operator) :
            a = type_sts(a,b,operator)
        else :
            return False
    return True

def z_ce_calculation(line):
    op_list = []
    varr_list = []
    for i in range(len(line)):
        if i%2 == 1 :
            op_list.append(line[i])
        if i%2 == 0 :
            varr_list.append(line[i])
                
    a = type_determine(varr_list[0])
    for j in range(len(op_list)):
        operator = op_list[j]
        b = type_determine(varr_list[j+1])
        if sts(a,b,operator) :
            a == type_sts(a,b,operator)
        else :
            return False
    return True
def metin_convert(metin):
    str = ""
    for i in range(1,len(metin)-1):
        str += metin[i]
    return str

def zıpla_odd(metin):
    new_metin = metin_convert(metin)
    if "," not in new_metin: 
        for j in range(len(new_metin)):
            if new_metin[j] not in [".","1","2","3","4","5","6","7","8","9","0"] :
                    return False
        if tam_sayı(new_metin) == True :
            return "tam-sayı"
    if "," in new_metin:
        for j in range(len(new_metin)):
            if new_metin[j] not in [".",",","1","2","3","4","5","6","7","8","9","0"] :
                    return False
        if reel_sayı(new_metin) == True : 
            return "reel-sayı"
    return False 

def rte_value_line(var,dict):
    value_line = dict[var][1][1]
    return value_line #bu değer yazıldığı satırdan büyükse rte
def rte_var_line(var,dict):
    var_line = dict[var][0][1]
    return var_line

def rte_value_(var,dict):
    value = dict[var][1][0]
    return value #bu değer yazıldığı satırdan büyükse rte
def rte_var_type(var,dict):
    var= dict[var][0][0]
    return var

def rte_calculation(lst,dict):
    value_list = []
    op_list = []
    for i in range(len(lst)):
        if i%2 == 0 :
            if type_determine(lst[i]) == "variable" :
                if lower_turkish(lst[i]) not in dict :
                    return False
                elif dict[lower_turkish(lst[i])][1][0] == "değer":
                    return False 
            value_list.append(lst[i])
        else :
            op_list.append(lst[i])
    a = type_determine(value_list[0])
    for j in range(len(op_list)):
        b = type_determine(value_list[j+1])
        if a == "variable":
            a = type_determine(rte_value_(lower_turkish(value_list[0]),dict))
        if b =="variable":
            b = type_determine(rte_value_(lower_turkish(value_list[j+1]),dict))
        operator = op_list[j]
        if sts(a,b,operator):
            a = type_sts(a,b,operator)#!!!!!!!!!!!!!
        else : 
            return False 
    return True
def rte_type_sts(x,a,y,b,operator):
    if (x == "tam-sayı" and y == "tam-sayı") and (operator == "artı"):
        return tam_sayı_tam_sayı(a,b,operator)
    if (x == "tam-sayı" and y == "tam-sayı") and (operator == "eksi"):
        return tam_sayı_tam_sayı(a,b,operator)
    if (x == "tam-sayı" and y == "metin") and (operator == "artı"):
        return tam_sayı_metin(a,b,operator)
    if (x == "tam-sayı" and y == "metin") and (operator == "eksi"):
        return tam_sayı_metin(a,b,operator)
    if (x == "reel-sayı" and y == "reel-sayı") and (operator == "artı"):
        return reel_reel(a,b,operator)
    if (x == "reel-sayı" and y == "reel-sayı") and (operator == "eksi"):
        return reel_reel(a,b,operator)
    if (x == "reel-sayı" and y == "metin") and (operator == "artı"):
        return reel_metin(a,b,operator)
    if (x == "reel-sayı" and y == "metin") and (operator == "eksi"):
        return reel_metin(a,b,operator)
    if (x == "metin" and y == "tam-sayı") and (operator == "artı"):
        return metin_tam_sayı(a,b,operator)
    if (x == "metin" and y == "tam-sayı") and (operator == "eksi"):
        return metin_tam_sayı(a,b,operator)
    if (x == "metin" and y == "reel-sayı") and (operator == "artı"):
        return metin_reel(a,b,operator)
    if (x == "metin" and y == "reel-sayı") and (operator == "eksi"):
        return metin_reel(a,b,operator)
    if (x == "metin" and y == "metin") and (operator == "artı"):
        return metin_artı(a,b)
    if (x == "metin" and y == "metin") and (operator == "eksi"):
        return metin_eksi(a,b)
    

    if (x == "tam-sayı" and y == "tam-sayı") and (operator == "çarp"):
        return tam_sayı_çarp_böl(a,b,operator)
    if (x == "tam-sayı" and y == "tam-sayı") and (operator == "bölü"):
        return tam_sayı_çarp_böl(a,b,operator)
    if (x == "tam-sayı" and y == "metin") and (operator == "çarp"):
        return tam_metin_çarp(a,b)
    if (x == "reel-sayı" and y == "reel-sayı") and (operator == "çarp"):
        return reel_reel_çarp_böl(a,b,operator)
    if (x == "reel-sayı" and y == "reel-sayı") and (operator == "bölü"):
        return reel_reel_çarp_böl(a,b,operator)
    if (x == "reel-sayı" and y == "metin") and (operator == "çarp"):
        return reel_metin_çarp_böl(a,b,operator)
    if (x == "reel-sayı" and y == "metin") and (operator == "bölü"):
        return reel_metin_çarp_böl(a,b,operator)
    if (x == "metin" and y == "tam-sayı") and (operator == "çarp"):
        return metin_tam_çarp(a,b)
    if (x == "metin" and y == "reel-sayı") and (operator == "çarp"):
        return metin_reel_çarp_böl(a,b,operator)
    if (x == "metin" and y == "reel-sayı") and (operator == "bölü"):
        return metin_reel_çarp_böl(a,b,operator)
    if (x == "metin" and y == "tam-sayı") and (operator == "bölü"):
        return metin_tam_bölü(a,b)
    if (x == "tam-sayı" and y == "metin") and (operator == "bölü"):
        return tam_metin_bölü(a,b)

def tam_sayı_noktalı_yazma(sayı):
    str_ = ""
    for i in range(len(sayı)):
        index = len(sayı)-1-i
        if index == 0 :
            str_ = sayı[0]+ str_
        elif (len(sayı)-index) % 3 == 0 :
            str_ ="."+sayı[index] + str_
        else :
            str_ = sayı[index] + str_
    return str_

def reel_sayı_virgüllü_yazma(sayı):#noktaları da koymalıyım.
    str = ""
    for i in range(len(sayı)):
        if sayı[i]==".":
            str += ","
        else :
            str+= sayı[i]
    decimal = find_decimal_point(str)
    str_ = ""
    for i in range(len(str)):
        index = len(str)-i-1
        if i>decimal and i%3 == decimal%3 :
            str_ = "." + str[index] + str_
        else :
            str_ = str[index] + str_
    return str_

def find_decimal_point2(reelsayı):
    find_ = reelsayı.find(".")
    decimal_position = len(reelsayı)-find_-1
    return decimal_position

def tam_sayı_tam_sayı(a,b,op):
    if op == "artı":
        x = tam_sayı_without_dot(a)+tam_sayı_without_dot(b)
        if x > 10000 or x < -10000 :
            return False 
        else :
            return tam_sayı_noktalı_yazma(str(x))
    if op == "eksi":
        x = tam_sayı_without_dot(a)-tam_sayı_without_dot(b)
        if x < -10000:
            return False 
        else :
            return tam_sayı_noktalı_yazma(str(x))

def tam_sayı_metin(a,b,op):
    if zıpla_odd(b) != "tam-sayı":
        return False
    if op == "artı":
        metin_int = tam_sayı_without_dot(metin_convert(b))
        a_fl = tam_sayı_without_dot(a)
        if a_fl+metin_int>10000:
            return False 
        else :
            return tam_sayı_noktalı_yazma(str(a_fl+metin_int))
    if op == "eksi":
        metin_int = tam_sayı_without_dot(metin_convert(b))
        a_fl = tam_sayı_without_dot(a)
        if a_fl-metin_int<-10000:
            return False 
        else :
            return tam_sayı_noktalı_yazma(str(a_fl-metin_int))

def reel_reel(a,b,op):
    if op == "artı":
        a_fl = float(reel_sayı_without_dot(a))*1000
        b_fl = float(reel_sayı_without_dot(b))*1000
        result = (a_fl+b_fl)/1000
        if result > 10000.000:
            return False 
        if find_decimal_point2(str(result))>3:
            return False 
        return reel_sayı_virgüllü_yazma(str(result))
    if op == "eksi":
        a_fl = float(reel_sayı_without_dot(a))*1000
        b_fl = float(reel_sayı_without_dot(b))*1000
        result = (a_fl-b_fl)/1000
        if (result) < -10000.000:
            return False 
        if find_decimal_point2(str(result))>3:
            return False 
        return reel_sayı_virgüllü_yazma(str(result))
    
def reel_metin(a,b,op):
    if zıpla_odd(b) != "reel-sayı":
        return False
    if op == "artı":
        metin_fl = float(reel_sayı_without_dot(metin_convert(b)))*1000
        a_fl = float(reel_sayı_without_dot(a))*1000
        result = (metin_fl+a_fl)/1000
        if result>10000.000:
            return False 
        if find_decimal_point2(str(result))> 3 :
            return False  
        else :
            return reel_sayı_virgüllü_yazma(str(result))
    if op == "eksi":
        metin_fl = float(reel_sayı_without_dot(metin_convert(b)))*1000
        a_fl = float(reel_sayı_without_dot(a))*1000
        result = (metin_fl-a_fl)/1000
        if result<-10000.000:
            return False 
        if find_decimal_point2(str(result))> 3 :
            return False  
        else :
            return reel_sayı_virgüllü_yazma(str(result))

def metin_tam_sayı(a,b,op):
    if zıpla_odd(a) != "tam-sayı":
        return False
    if op == "artı":
        metin_int = tam_sayı_without_dot(metin_convert(a))
        b_fl = tam_sayı_without_dot(b)
        if b_fl+metin_int>10000:
            return False 
        else :
            return tam_sayı_noktalı_yazma(str(b_fl+metin_int))
    if op == "eksi":
        metin_int = tam_sayı_without_dot(metin_convert(a))
        b_fl = tam_sayı_without_dot(b)
        if b_fl-metin_int<-10000:
            return False 
        else :
            return tam_sayı_noktalı_yazma(str(b_fl+metin_int))
        
def metin_reel(a,b,op):
    if zıpla_odd(a) != "reel-sayı":
        return False
    if op == "artı":
        metin_fl = float(reel_sayı_without_dot(metin_convert(a)))*1000
        b_fl = float(reel_sayı_without_dot(b))*1000
        result = (metin_fl+b_fl)/1000
        if result>10000.000:
            return False 
        if find_decimal_point2(str(result))> 3 :
            return False  
        else :
            return reel_sayı_virgüllü_yazma(str(result))
    if op == "eksi":
        metin_fl = float(reel_sayı_without_dot(metin_convert(a)))*1000
        b_fl = float(reel_sayı_without_dot(b))*1000
        result = (metin_fl-b_fl)/1000
        if result<-10000.000:
            return False 
        if find_decimal_point2(str(result))> 3 :
            return False  
        else :
            return  reel_sayı_virgüllü_yazma(str(result))
        
def metin_artı(a,b):
    a_ = metin_convert(a)
    b_ = metin_convert(b)
    if len(a_+b_)>50:
        return False 
    return "!"+a_+b_+"!"

def metin_eksi(a,b):
    a_ = metin_convert(a)
    b_ = metin_convert(b)
    loc = -1
    new_list = []
    while True:
        loc = a_.find(b_,loc+1)
        if loc == -1 :
            break
        for i in range(len(b_)):
            if loc+i in new_list :
                continue
            new_list.append(loc+i)
    str_ = ""
    for j in range(len(a_)):
        if j in new_list :
            continue
        str_ += a_[j]
    return "!"+ str_ + "!"

def tam_sayı_çarp_böl(a,b,op):
    if op == "çarp":
        if (tam_sayı_without_dot(a)*tam_sayı_without_dot(b)) > 10000 or (tam_sayı_without_dot(a)*tam_sayı_without_dot(b))<-10000:
            return False 
        result = str(tam_sayı_without_dot(a)*tam_sayı_without_dot(b))
        return tam_sayı_noktalı_yazma(result) + ",0"
    if op == "bölü":
        result = str(tam_sayı_without_dot(a)/tam_sayı_without_dot(b))
        if find_decimal_point2(result) > 3 :
            return False 
        return reel_sayı_virgüllü_yazma(result)
    
def tam_metin_çarp(a,b):
    new_str = metin_convert(b)*tam_sayı_without_dot(a)
    if len(new_str)>50:
        return False 
    return "!" + new_str + "!"

def tam_metin_bölü(a,b):
    if zıpla_odd(b) != "tam-sayı":
        return False
    result = str(tam_sayı_without_dot(a)/tam_sayı_without_dot(metin_convert(b)))
    if find_decimal_point2(result) > 3 :
        return False 
    return reel_sayı_virgüllü_yazma(result)

def reel_reel_çarp_böl(a,b,operator):
    if operator == "çarp":
        a_fl = float(reel_sayı_without_dot(a))*1000
        b_fl = float(reel_sayı_without_dot(b))*1000
        result = (a_fl*b_fl/1000000)
        if result > 10000.000 or result < -10000.000:
            return False 
        if find_decimal_point2(str(result))>3 :
            return False 
        return reel_sayı_virgüllü_yazma(str(result))
    if operator == "bölü":
        a_fl = float(reel_sayı_without_dot(a))*1000
        b_fl = float(reel_sayı_without_dot(b))*1000
        result = (a_fl/b_fl)
        if result > 10000.000 or result < -10000.000:
            return False 
        if find_decimal_point2(str(result))>3 :
            return False 
        return reel_sayı_virgüllü_yazma(str(result))
    
def reel_metin_çarp_böl(a,b,operator):
    if zıpla_odd(b) != "reel-sayı":
        return False 
    if operator == "çarp":
        a_fl = float(reel_sayı_without_dot(a))*1000
        b_fl = float(reel_sayı_without_dot(metin_convert(b)))*1000
        result = (a_fl*b_fl/1000000)
        if result > 10000.000 or result < -10000.000:
            return False 
        if find_decimal_point2(str(result))>3 :
            return False 
        return reel_sayı_virgüllü_yazma(str(result))
    if operator == "bölü":
        a_fl = float(reel_sayı_without_dot(a))*1000
        b_fl = float(reel_sayı_without_dot(metin_convert(b)))*1000
        result = (a_fl/b_fl)
        if result > 10000.000 or result < -10000.000:
            return False 
        if find_decimal_point2(str(result))>3 :
            return False 
        return reel_sayı_virgüllü_yazma(str(result))
    
def metin_tam_çarp(a,b):
    new_str = metin_convert(a)*tam_sayı_without_dot(b)
    if len(new_str)>50:
        return False 
    return "!" + new_str + "!"

def metin_tam_bölü(a,b):
    if zıpla_odd(a) != "tam-sayı":
        return False
    result = str(tam_sayı_without_dot(metin_convert(a))/tam_sayı_without_dot(b))
    a = (tam_sayı_without_dot(metin_convert(a))/tam_sayı_without_dot(b))
    if find_decimal_point2(result) > 3 :
        return False 
    if a > 10000.000 or a<-10000.000 :
        return False 
    return reel_sayı_virgüllü_yazma(result)

def metin_reel_çarp_böl(a,b,operator):
    if zıpla_odd(a) != "reel-sayı":
        return False 
    if operator == "çarp":
        a_fl = float(reel_sayı_without_dot(metin_convert(a)))*1000
        b_fl = float(reel_sayı_without_dot(b))*1000
        result =(a_fl*b_fl/1000000)
        if result > 10000.000 or result < -10000.000:
            return False 
        if find_decimal_point2(str(result))>3 :
            return False 
        return reel_sayı_virgüllü_yazma(str(result))
    if operator == "bölü":
        a_fl = float(reel_sayı_without_dot(metin_convert(a)))*1000
        b_fl = float(reel_sayı_without_dot(b))*1000
        result = (a_fl/b_fl)
        if result > 10000.000 or result < -10000.000:
            return False 
        if find_decimal_point2(str(result))>3 :
            return False 
        return reel_sayı_virgüllü_yazma(str(result))
    
def son_değer_hesaplama(line,dict):
    value_list = []
    op_list = []
    for i in range(len(line)):
        if i%2 == 0 :
            value_list.append(line[i])
        if i%2 == 1 :
            op_list.append(line[i])
    if type_determine(value_list[0]) == "variable":
        x = dict[lower_turkish(value_list[0])][0][0]#türü
        a = dict[lower_turkish(value_list[0])][1][0]#değeri
    else :
        x = type_determine(value_list[0])
        a = value_list[0]
    for j in range(len(op_list)):
        op = op_list[j]
        if type_determine(value_list[j+1]) == "variable":            
            y = dict[lower_turkish(value_list[j+1])][0][0]#türü
            b = dict[lower_turkish(value_list[j+1])][1][0]#değeri
        else :
            y = type_determine(value_list[j+1])
            b = value_list[j+1]
        a = rte_type_sts(x,a,y,b,op)
        x = type_sts(x,y,op)
        if not a : 
            return False 
    return a 
main()
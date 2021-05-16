import window

var_name_list = [" "]
var_value_list = [" "]

#Parse code
#解析はじめ
def lexer(code):
    read_now = ""   #今読んでいる文字変数
    code_read = ""  #今読んでいる途中の文字
    code_read_mode = 1  #コードを読むか読まないか1読む0読まない
    read_list = []
    read_stop = [";","=",">",",","{","}"]   #この記号があったらリストを区切る
    command_fin = 0     #コマンドの終わり1おわりじゃない0
    for n in range(len(code)):
        read_now = code[n]

        for i in range(len(read_stop)):
            if read_now == read_stop[i]: #いま読んでいる文字がリストを区切る記号だったら
                command_fin = 1     #コマンド終わり
                            
        if command_fin == 1:#プログラム終わりまたは記号なら
            if code_read != "":  #読んでいるcommandが空白でなければ
                
                #記号をstr型としてよみこめるようにする
                if code_read.count('"') == 0 and code_read.count("'") == 0:     #クオーテーションがないなら
                    read_list.append(code_read) #リストに追加
                    read_list.append(read_now)
                    code_read = ""  #初期化
                
                elif code_read.count('"') >= 2 or code_read.count("'") >= 2:    #クオーテーションが2つ(strの終わり)なら
                    read_list.append(code_read) #リストに追加
                    read_list.append(read_now)
                    code_read = ""  #初期化
                    print("ok!")
                elif code_read.count('"') == 1 or code_read.count("'") == 1:    #クオーテーションが1つ(strの読み込み途中)なら
                    code_read = code_read + read_now

                        
            else:   #空白だったら除外
                read_list.append(read_now)
            command_fin = 0
        else:   #改行などを削除
            if read_now != "\n" and read_now != "\r" and read_now != " " and read_now != "  ":
                code_read = code_read + read_now
    return read_list

#解析終了

#Run code
def code(code):
    global var_name_list
    global var_value_list
    if_fin_pos = 0
    loop_start_pos = 0
    loop_start = 0
    loop_read = ""
    code_jmp = 0    #コードを読み飛ばす
    if_mode = 0     #if文の処理を実行1 if文ではない0 条件式2
    for n in range(len(code)):  #関数の引数を取得
        if code_jmp == 0:
            
            if code[n] == ";":  #commandの終わりなら初期化
                var = 0
            
            elif code[n] == "=":  #変数宣言またはif文の条件式(==)
                if if_mode == 2:
                    if var_list(code[n-1]) == var_list(code[n+1]):
                        if_mode = 1
                    else:
                        if_mode = 0
                else:
                    var_dec_return = var_dec(code[n-1],var_list(code[n+1]))
                    print(var_dec_return[0])
                    print(var_dec_return[1])
            
            elif code[n] == "<" and if_mode == 2:   #if文条件式(<)
                if var_list(code[n-1]) < var_list(code[n+1]):
                    if_mode = 1
                else:
                    if_mode = 0
            
            elif code[n] == ">" and if_mode == 2:   #if文条件式(>)
                if var_list(code[n-1]) > var_list(code[n+1]):
                    if_mode = 1
                else:
                    if_mode = 0
            
            elif code[n] == "if":
                if_mode = 2
            elif code[n] == "{":
                if if_mode == 1:
                    pass
                elif loop_start == 1:
                    loop_start_pos = n+1
                    code_jmp = 1
                else:
                    code_jmp = 1
            elif code[n] == "loop":
                loop_start = 1
            elif code[n] == "print":
                window.write(var_list(code[n+2]))
            elif code[n] == "text_color":
                window.text_color_c(var_list(code[n+2]))
            elif code[n] == "background":
                window.background(var_list(code[n+2]))
        elif code[n] == "}":
            if_fin_pos = n
            code_jmp = 0
            if_mode = 0
            if loop_start == 1:
                if if_mode == 0:
                    loop(code[loop_start_pos:if_fin_pos],int(var_list(code[loop_start_pos-2])))
        
   
#Make a list of values ​​and perform calculations, etc.
#値をリストにして計算などをする
def var_list(var_value):
    global var_name_list
    global var_value_list
    value_list = []
    read = ""
    for n in range(len(var_value)): #記号で区切ってリストに収納
        if var_value[n] == '"' or var_value[n] == "'" or var_value[n] == "+" or var_value[n] == "-" or var_value[n] == "*" or var_value[n] == "+" or var_value[n] == "/":
            if read != "":
                value_list.append(read)
                value_list.append(var_value[n])
                read = ""
            else:
                value_list.append(var_value[n])
        else:
            read = read + var_value[n]
            if n == len(var_value)-1:
                value_list.append(read)
    if value_list.count("'") == 0 and value_list.count('"') == 0:  #これが文字列ではないなら
        var_value = calc(var2value(value_list))
    else:   #strなら
        var_value = var_str(var2value(value_list))
    print(value_list)
    return var_value

#Variable declaration
#変数宣言
def var_dec(var_name,var_value):
    global var_name_list
    global var_value_list
    if var_name_list.count(var_name) == 0:  #この変数を読み込んだことがないなら
        var_name_list.append(var_name)  #変数名を追加
        var_value_list.append(var_value)    #値を追加
    else:   #読み込んだことがあるなら
        var_pos = var_name_list.index(var_name) #(リストの中で)変数の位置を取得
        var_value_list[var_pos] = var_value     #値を追加
    return var_name_list,var_value_list

#calc    
#四則演算
def calc(calc):
    var = int(calc[0])     #変数を一時的に保存する変数
    for n in range(len(calc)):
        if calc[n] == "+":
            var = var + int(calc[n+1])
        elif calc[n] == "-":
            var = var - int(calc[n+1])
        elif calc[n] == "*":
            var = var * int(calc[n+1])
        elif calc[n] == "/":
            var = var / int(calc[n+1])
    return str(var)

#variable declaration of str type
#str型の変数宣言
def var_str(i_value):
    s_loop = 0  #クオーテーション検索時のループ回数
    q = ""
    o_value = ""
    temp = ""
    start_pos = 0
    if i_value.count("'") == 0:    #'が含まれてないなら
        q = '"' #クオーテーション
        s_loop = int(i_value.count('"')/2)  #クオーテーションの数/2
    elif i_value.count('"') == 0: #"が含まれていないなら
        q = "'" #クオーテーション
        s_loop = int(i_value.count("'")/2)
    
    for n in range(s_loop):
        start_pos = i_value.index(q)
        temp = i_value[start_pos+1]
        i_value = i_value[start_pos+3:]
        o_value = o_value + temp
    return o_value

#Make the value a variable
#配列ををまとめて変数にする
def var2value(value_list):
    global var_name_list
    global var_value_list
    print(value_list)
    for n in range(len(value_list)):
        
        for i in range(len(var_name_list)):
            
            if value_list[n] == var_name_list[i]:    #変数が存在したなら
                var_pos = var_name_list.index(value_list[n])
                if value_list.count('"') != 0 or value_list.count("'") != 0:   #str型なら

                    if len(value_list[n:]) == 1:    #これでおしまいなら
                        
                        if value_list.count('"') != 0:  #区切りがダブルクォーテーションなら
                            
                            value_list[n] = var_value_list[var_pos]     #この場所を読み込んだ変数の値にする
                            value_list.insert(n,'"')    #この場所の前にクォーテーションを追加
                            value_list.insert(n+2,'"')  #この場所の後ろにクォーテーションを追加
                        else:   #区切りがクォーテーションなら
                            
                            value_list[n] = var_value_list[var_pos]     #この場所を読み込んだ変数の値にする
                            value_list.insert(n,"'")    #この場所の前にクォーテーションを追加
                            value_list.insert(n+2,"'")  #この場所の後ろにクォーテーションを追加
                        pass
                    else:
                        if value_list[n+1] != '"' and value_list[n+1] != "'":   #クオーテーションに囲まれていないなら
                            value_list[n] = var_value_list[var_pos]     #この場所を読み込んだ変数の値にする
                    
                else:   #strではないなら
                    value_list[n] = var_value_list[var_pos]     #この場所を読み込んだ変数の値にする
                    
                
    return value_list

def loop(source,loop_num):  #loop文
    for n in range(loop_num):
        code(source)
    
##############run
print(lexer("""
            background>"#ff0000";
            print>"hello,world!";"""))

##プログラム
code(lexer("""
            print>"hello,world!";
            """))  #ここにコードを書く yor code write here
window.root.mainloop()

    

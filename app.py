from flask import Flask, render_template
from flask import request, url_for, redirect
import os, re, string, random
from ocr import classify
import sys
import json
import io
import base64
import time
import datetime

# sys.getdefaultencoding()
# reload(sys)
# sys.setdefaultencoding('utf-8')

app = Flask(__name__)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def solve_redirect(request):
    form = request.form.to_dict()
    choice = form.get('selection')  # get the value of name 'selection' in form

    if choice == 'recognition':
        folder = './static/base/temp/'
        dirs = os.listdir(folder)
        if len(dirs) > 20:
            for file in dirs:
                os.remove(folder + file)

        img = request.files.get('image_uploader')
        fname = id_generator() + img.filename
        img.save(folder + fname)
        return redirect(url_for('recognition', filename=fname))

    else:
        id = form.get('ID')  # get the value of name 'ID' in form
        if choice == 'script':
            return redirect(url_for('search_script', id=id))
        elif choice == 'chinese':
            return redirect(url_for('search_character', id=id))

    return None


# url-redirect (based on form info in html)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ret = solve_redirect(request)
        if ret:
            return ret
    return render_template('index.html')

# url-redirect (based on form info in html)
@app.route('/script/', methods=['GET', 'POST'])
def index_script():
    if request.method == 'POST':
        ret = solve_redirect(request)
        if ret:
            return ret
    return render_template('index_script.html')


# url for certain script ID
@app.route('/search_script/<id>', methods=['GET', 'POST'])
def search_script(id):
    if request.method == 'POST':
        ret = solve_redirect(request)
        if ret:
            return ret

    folder = './static/oracle/%05d' % (int(id))

    if not os.path.exists(folder):
        return redirect(url_for('index'))

    pics = os.listdir(folder)
    pics = [os.path.join('.' + folder, pic) for pic in pics if 'jpg' in pic or 'png' in pic]  # context
    oracle = os.path.join(folder, '1')  # characters
    chn = oracle[:-1] + '2'
    char_list = [oracle, chn]

    # url_script means oracle characters' context
    img_info = {'id': id, 'url_script': pics, 'len': 0}
    
    for char_path in char_list:
        def getKey(x):
            id_list = x[:-4].split('-')
            # solve XX-YY+.png
            id3 = re.findall("\d+", id_list[3])[0]
            id4 = id_list[3].replace(id3, '')
            return int(id_list[0]), int(id_list[1]), int(id_list[2]), int(id3), len(id4)
        
        chars = os.listdir(char_path) if os.path.exists(char_path) else []
        chars.sort(key=getKey)
        name_trans = {'1': 'oracle', '2': 'words'}
        img_info[name_trans[char_path[-1]]] = ['.' + char_path + '/' + ch for ch in chars]

    return render_template('result_script.html', **img_info)


# url for certain character
@app.route('/search_character/<id>', methods=['GET', 'POST'])
def search_character(id):
    if request.method == 'POST':
        ret = solve_redirect(request)
        if ret:
            return ret

    img_info = {'id': id}

    folder = './static/oracle-book/'
    char_dict = {}
    scripts = {}

    # Chinese character input / out of range
    if not os.path.exists(folder+id):
        f = io.open(folder+'map.txt', 'r', encoding='utf-8')
        char_dict = json.load(fp=f)
        f.close()
        if id in char_dict.keys():
            id = char_dict[id]
        else:
            return redirect(url_for('index'))

    # glyph set
    folder = folder + id
    pics = os.listdir(folder)
    pics = [os.path.join('.' + folder, pic) for pic in pics if 'jpg' in pic or 'png' in pic]  # context

    img_info['url_character'] = pics

    # alignment with documents
    f = io.open('./static/oracle-book/zid2script.txt', 'r', encoding='utf-8')
    script_dict = eval(f.read())
    f.close()
    if id in script_dict.keys():
        for pid in script_dict[id]:
            pdir = './static/oracle/%05d' % (int(pid))
            if os.path.exists(pdir):
                pfolder = os.listdir(pdir)
                pfolder = [folder for folder in pfolder if 'jpg' in folder or 'png' in folder]
                if pfolder:
                    scripts[pid] = pfolder[0]
                else:
                    print('pfolder is Non for:', pid)
    
    img_info['url_script'] = scripts
    print(scripts)
    return render_template('result_character.html', **img_info)


# url for oracle recognition
@app.route('/recognition/<filename>', methods=['GET', 'POST'])
def recognition(filename):
    if request.method == 'POST':        
        ret = solve_redirect(request)
        if ret:
            return ret

    result1, result2 = classify('./static/base/temp/' + filename)
    result1 = ['base/temp/' + filename] + result1
    # result = [(file+'.jpg', os.listdir('./static/oracle-book/'+file)[0]) for file in topk]
    img_info = {'upload': filename, 'result': [result1, result2]}

    return render_template('result_recognition.html', **img_info)


# url for handa information of oracle recognition
@app.route('/recognition/<filename>/<id>', methods=['GET', 'POST'])
def recognition_to_handa(filename):
    if request.method == 'POST':
        ret = solve_redirect(request)
        if ret:
            return ret

    result1, result2 = classify('./static/base/temp/' + filename)
    result1 = ['base/temp/' + filename] + result1
    # result = [(file+'.jpg', os.listdir('./static/oracle-book/'+file)[0]) for file in topk]
    img_info = {'upload': filename, 'result': [result1[id], result2[id]]}

    return render_template('result_recognition2handa.html', **img_info)



def random_name():
    time_token = (int)(time.time())
    num_token = (int)(random.random()*100000)
    return (str)(time_token)+"_"+(str)(num_token)+".jpg"

@app.route('/uploadcanvas', methods=["POST"])
def uploadFromCanvas():
    if request.method == "POST":
        recv_data = request.get_json()
 
        if recv_data is None:
            print("request.get_json() is None")
            recv_data = request.get_data()
 
        json_re = json.loads(recv_data)
        imgRes = json_re['uploadImg']
 
        imgdata = base64.b64decode(imgRes)

        filename = random_name()
 
        file = open('./static/base/temp/' + filename, "wb")
        file.write(imgdata)
        file.close()

        return filename

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    #app.run(port=5050)

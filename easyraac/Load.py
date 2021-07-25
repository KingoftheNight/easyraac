# import package
import os
import numpy as np
import urllib.request
file_path = os.path.dirname(__file__)
import tarfile


# read svm file
def read_svmfile(file):
    with open(file, 'r') as f1:
        file = f1.readlines()
    # 提取特征list
    features = []
    features_label = []
    for i in file:
        line = i.strip('\n').split(' ')
        fs_box = line[1:]
        mid_box = []
        for j in fs_box:
            mid_box.append(float(j.split(':')[-1]))
        features.append(mid_box)
        features_label.append(int(line[0]))
    # 转换为数组
    np_data = np.array(features)
    np_label = np.array(features_label)
    return np_data, np_label


# read sequence data set
def read_fasta(file, out=None):
    with open(file, 'r') as u:
        lines = u.readlines()
    result = ''
    for i in lines:
        i = i.strip('\n')
        if i and i[0] == '>':
            result = result + '\n' + i + '\n'
        else:
            result = result + i
    result = result[1:].split('\n')
    sq_dic = {}
    for i in range(len(result)-1):
        if '>' in result[i]:
            sq_dic[result[i]] = result[i+1]
    if out == None:
        return sq_dic
    else:
        t = 0
        path = []
        for i in range(len(result)-1):
            if '>' in result[i]:
                t += 1
                line = result[i] + '\n' + result[i+1]
                path.append(os.path.join(out, str(t) + '.fasta'))
                with open(os.path.join(out, str(t) + '.fasta'), 'w') as f:
                    f.write(line)
        return path


# read raac dictionary
def read_raac(file):
    with open(file, 'r') as code:
        raacode = code.readlines()
    raa_dict = {}
    raa_index = []
    for eachline in raacode:
        each_com = eachline.strip('\n').split()
        raa_com = each_com[-1].split('-')
        raa_ts = 't' + each_com[1] + 's' + each_com[3]
        raa_dict[raa_ts] = raa_com
        raa_index.append(raa_ts)
    return raa_dict, raa_index


# read pssm matrix
def read_pssm(path):
    with open(path, 'r') as f:
        data = f.readlines()
    matrix = []
    aa_id = []
    end_matrix = 0
    for j in data:
        if 'Lambda' in j and 'K' in j:
            end_matrix = data.index(j)
            break
    for eachline in data[3:end_matrix - 1]:
        row = eachline.split()
        newrow = row[0:22]
        for k in range(2, len(newrow)):
            newrow[k] = int(newrow[k])
        nextrow = newrow[2:]
        matrix.append(nextrow)
        aa_id.append(newrow[1])
    return matrix, aa_id


# extract selected feature of svm file
def extract_svm_feature(file, filter_index, number, out=None):
    # 读取特征排序以及特征文件
    with open(filter_index, 'r', encoding='UTF-8') as f:
        data = f.readlines()
    index = data[0].split(' ')[1:-1]
    with open(file, 'r', encoding='UTF-8') as f:
        data = f.readlines()
    # 提取矩阵特征
    type_f = []
    matrix = []
    for line in data:
        line = line.split(' ')
        type_f.append(line[0])
        mid_box = line[1:]
        for i in range(len(mid_box)):
            mid_box[i] = mid_box[i].split(':')[-1]
        matrix.append(mid_box)
    # 提取数组
    out_type = np.zeros(len(type_f))
    out_matrix = np.zeros([len(matrix), number])
    for i in range(len(type_f)):
        out_type[i] = int(type_f[i])
        for j in range(number):
            out_matrix[i][j] = float(matrix[i][int(index[j])-1])
    if out == None:
        return out_matrix, out_type
    else:
        content = ''
        for i in range(len(out_matrix)):
            line = out_matrix[i]
            mid = str(out_type[i])
            for j in range(number):
                mid += ' ' + str(j+1) + ':' + str(line[j])
            content += mid + '\n'
        with open(out, 'w') as f:
            f.write(content[:-1])
        return out_matrix, out_type


# extract selected feature of numpy
def extract_numpy_feature(matrix, type_f, number, index=None, out=None):
    if index == None:
        out_type = np.zeros(len(type_f))
        out_matrix = np.zeros([len(matrix), number])
        for i in range(len(type_f)):
            out_type[i] = type_f[i]
            for j in range(number):
                out_matrix[i][j] = matrix[i][j]
    else:
        out_type = np.zeros(len(type_f))
        out_matrix = np.zeros([len(matrix), number])
        for i in range(len(type_f)):
            out_type[i] = type_f[i]
            for j in range(number):
                out_matrix[i][j] = matrix[i][index[j]]
    if out == None:
        return out_matrix, out_type
    else:
        content = ''
        for i in range(len(out_matrix)):
            line = out_matrix[i]
            mid = str(out_type[i])
            for j in range(number):
                mid += ' ' + str(j+1) + ':' + str(line[j])
            content += mid + '\n'
        with open(out, 'w') as f:
            f.write(content[:-1])
        return out_matrix, out_type


# read hyperparameters file
def read_hys(file):
    with open(file, 'r') as f:
        data = f.readlines()
    cg_box = {}
    for i in data:
        cg_box[i.split('\t')[0]] = [i.split('\t')[1].split(': ')[-1], i.split('\t')[2].split(': ')[-1]]
    return cg_box


# read raac of different types
def read_ssc(raa_file, type_r):
    with open(raa_file, "r") as f:
        data = f.readlines()
    out_box = []
    for line in data:
        line = line.strip("\n").split(" ")
        if line[1] == type_r:
            out_box.append(line[4])
    all_sq = ""
    for i in out_box[0]:
        if i != "-":
            all_sq += i + "-"
    out_box.append(all_sq[:-1])
    for i in range(len(out_box)):
        out_box[i] = out_box[i].split("-")
    return out_box[::-1]


# read pssm weblogo
def read_weblogo_main(matrix):
    def line_score(newrow):
        out_box = []
        a = 0
        for i in newrow:
            if i > 0:
                a += i
        for i in newrow:
            if i > 0:
                out_box.append(i * 100 / a)
            else:
                out_box.append(0)
        return out_box
    # main
    out = []
    for eachline in matrix:
        newrow = line_score(eachline)
        for i in range(len(newrow)):
            newrow[i] = int(newrow[i])
        out.append(newrow)
    return out


# load blast database
def load_pdbaa():
    if 'pdbaa.pdb' not in os.listdir(os.path.join(file_path, 'blastDB')):
        url = 'https://ftp.ncbi.nlm.nih.gov/blast/db/pdbaa.tar.gz'
        save_path = os.path.join(file_path, 'pdbaa')
        urllib.request.urlretrieve(url, filename=save_path)
        t = tarfile.open(save_path)
        t.extractall(path=os.path.join(file_path, 'blastDB'))
    


























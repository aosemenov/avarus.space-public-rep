import subprocess
import os
import re
import shutil
from itertools import groupby

def module_col_factor(ds):
    #command = '../R-4.0.4/bin/Rscript'
    command = 'Rscript'
    path2script = "col.r"
    args = [ds, '1']
    cmd = [command, path2script] + args
    try:
        x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        success = True
    except subprocess.CalledProcessError as e:
        x = e.output
        success = True
    z = re.sub(r'"', r'', x)
    y = z.split()[1::2]
    return y

def module_jacquard(ds):
    #command = '../R-4.0.4/bin/Rscript'
    command = 'Rscript'
    path2script = "jaccard.r"
    args = [ds, '1']
    cmd = [command, path2script] + args
    try:
        x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        success = True
    except subprocess.CalledProcessError as e:
        x = e.output
        success = True
    info_dataset = 'Dataset: ' + str(ds) + '\n'
    file = open("media/testRjacquard.txt", "w")
    file.write(info_dataset)
    file.close()
    file = open("media/testRjacquard.txt", "a")
    file.write(str(x))
    file.close()
    return x

def module_factor(ds, length, columns):
    #command = '../R-4.0.4/bin/Rscript'
    command = 'Rscript'
    path2script = "factor.r"
    args = [ds, '1', length] + columns
    cmd = [command, path2script] + args
    print(cmd)
    try:
        x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        success = True
    except subprocess.CalledProcessError as e:
        x = e.output
        success = True
    info_dataset = 'Dataset: ' + str(ds) + ' Columns: ' + str(columns) + '\n'
    file = open("media/Factor.txt", "w")
    file.write(info_dataset)
    file.close()
    file = open("media/Factor.txt", "a")
    file.write(str(x))
    file.close()
    return x


def module_col_comp(ds):
    #command = '../R-4.0.4/bin/Rscript'
    command = 'Rscript'
    path2script = "col.r"
    args = [ds, '1']
    cmd = [command, path2script] + args
    try:
        x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        success = True
    except subprocess.CalledProcessError as e:
        x = e.output
        success = True
    z = re.sub(r'"', r'', x)
    y = z.split()[1::2]
    return y


def module_col(ds):
    #command = '../R-4.0.4/bin/Rscript'
    command = 'Rscript'
    path2script = "col.r"
    args = [ds, '1']
    cmd = [command, path2script] + args

    try:
        x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        success = True
    except subprocess.CalledProcessError as e:
        x = e.output
        success = True
    z = re.sub(r'"', r'', x)
    y = z.split()[1::2]
    y = y[3::]
    return y


def module_statistics(ds, length, columns):
    #command = '../R-4.0.4/bin/Rscript'
    command = 'Rscript'
    path2script = "subset.r"
    args = [ds, '1', length, 'PASL.TAXON.SCIENTIFIC.NAME.NO.AUTHOR(S)'] + columns
    cmd = [command, path2script] + args

    try:
        x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        success = True
    except subprocess.CalledProcessError as e:
        x = e.output
        success = True
    return x


def module_statistics_env(ds, length, columns):
    #command = '../R-4.0.4/bin/Rscript'
    command = 'Rscript'
    path2script = "subset_env.r"
    args = [ds, '1', length, 'SITE_MOIST'] + columns
    cmd = [command, path2script] + args

    try:
        x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        success = True
    except subprocess.CalledProcessError as e:
        x = e.output
        success = True
    return x


def module_col_statistics(ds):
    #command = '../R-4.0.4/bin/Rscript'
    command = 'Rscript'
    path2script = "znach.r"
    args = [ds, '1']
    cmd = [command, path2script] + args

    try:
        x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        success = True
    except subprocess.CalledProcessError as e:
        x = e.output
        success = True
    y = x.split('"')[1::2]
    y = y[3::]
    return y


def module_col_statistics_env(ds):
    #command = '../R-4.0.4/bin/Rscript'
    command = 'Rscript'
    path2script = "znach_poch.r"
    args = [ds, '1']
    cmd = [command, path2script] + args

    try:
        x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        success = True
    except subprocess.CalledProcessError as e:
        x = e.output
    z = re.sub(r'"', r'', x)
    y = z.split()[1::2]
    y = y[1::]
    y = list(set(y))
    return y


def module_comp(ds, length, columns):
    #command = '../R-4.0.4/bin/Rscript'
    command = 'Rscript'
    path2script = "PCA.r"
    args = [ds, '1', length] + columns
    cmd = [command, path2script] + args
    print(cmd)
    try:
        x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        success = True
    except subprocess.CalledProcessError as e:
        x = e.output
        success = True
    info_dataset = 'Dataset: ' + str(ds) + ' Columns: ' + str(columns) + '\n'
    file = open("media/testRcomp.txt", "w")
    file.write(info_dataset)
    file.close()
    file = open("media/testRcomp.txt", "a")
    file.write(str(x))
    file.close()
    return x


def module(ds, columns):
    #command = '../R-4.0.4/bin/Rscript'
    command = 'Rscript'
    path2script = "cor.r"
    args = [ds, '1'] + columns
    cmd = [command, path2script] + args
    try:
        x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        success = True
    except subprocess.CalledProcessError as e:
        x = e.output
        success = True
    info_dataset = 'Dataset: ' + str(ds) + ' Columns: ' + str(columns) + '\n'
    file = open("media/testR.txt", "w")
    file.write(info_dataset)
    file.close()
    file = open("media/testR.txt", "a")
    file.write(str(x))
    file.close()
    return x

def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('PyCharm')


def module_plants(ds):
    #command = '../R-4.0.4/bin/Rscript'
    command = 'Rscript'
    path2script = "Classify_by_groups.R"
    args = [ds, '1']
    cmd = [command, path2script] + args
    try:
        x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        success = True
    except subprocess.CalledProcessError as e:
        x = e.output
        success = True
    info_dataset = 'Dataset: ' + str(ds) + '\n'
    file = open("media/testRplants.txt", "w")
    file.write(info_dataset)
    file.close()
    file = open("media/testRplants.txt", "a")
    file.write(str(x))
    file.close()
    return x


def module_species(ds, gr):
    #command = '../R-4.0.4/bin/Rscript'
    command = 'Rscript'
    path2script = "charts_for_groups.R"
    args = [ds, '1', gr]
    cmd = [command, path2script] + args
    try:
        x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        success = True
    except subprocess.CalledProcessError as e:
        x = e.output
        success = True
    info_dataset = 'Dataset: ' + str(ds) + '\n'
    file = open("media/testRsp.txt", "w")
    file.write(info_dataset)
    file.close()
    file = open("media/testRsp.txt", "a")
    file.write(str(x))
    file.close()
    return x
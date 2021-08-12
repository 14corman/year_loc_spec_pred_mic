# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 18:11:08 2020

@author: Cory Kromer-Edwards
"""

import csv
import os
import numpy as np
import xlsxwriter

gene_headers = ["ampC-like ", "CMH-1-like ", "CMH-2-like ", "CMH-3-like ",
                "CTX-M-206 ", "CTX-M-27-like ", "EC-12-like ", "LEN-13-like ",
                "LEN-2-like ", "LEN-5-like ", "MAL-1-like ", "OXA-17-like ",
                "OXA-232-like ", "CMY-151 ", "CMY-152 ", "CMY-152-like ",
                "CMY-141 ", "MOX-12-like ", "PER-1-like ", "PER-7-like ",
                "SED-1-like ", "SHV-100-like ", "SHV-133-like ",
                "SHV-148-like ", "SHV-155-like ", "SHV-16-like ",
                "SHV-187-like ", "SHV-198 ", "SRT ", "SRT-2-like ",
                "SRT-like ", "SST-1-like ", "TEM-110-like ", "TEM-12-like ",
                "CARB-1-like ", "CARB-2_PSE-1 ", "CTX-M-1 ", "CTX-M-10 ",
                "CTX-M-12 ", "CTX-M-123 ", "CTX-M-15 ", "CTX-M-15-like ",
                "CTX-M-22 ", "CTX-M-3 ", "CTX-M-30 ", "CTX-M-32 ",
                "CTX-M-33 ", "CTX-M-36 ", "CTX-M-55 ", "CTX-M-55-like ",
                "CTX-M-64 ", "CTX-M-71 ", "CTX-M-115 ", "CTX-M-2 ",
                "CTX-M-75 ", "CTX-M-8 ", "CTX-M-91 ", "CTX-M-134 ",
                "CTX-M-14 ", "CTX-M-174 ", "CTX-M-19 ", "CTX-M-24 ",
                "CTX-M-27 ", "CTX-M-65 ", "CTX-M-9 ", "GES-1 ",
                "GES-17 ", "GES-7 ", "PER-2 ", "IMI-1 ", "KPC-12 ",
                "KPC-2 ", "KPC-2-like ", "KPC-3 ", "KPC-3-like ", "KPC-4 ",
                "KPC-6 ", "SME-4 ", "SHV-1 ", "SHV-100 ", "SHV-106 ",
                "SHV-108 ", "SHV-108-like ", "SHV-11 ", "SHV-110 ",
                "SHV-111 ", "SHV-11-like ", "SHV-12 ", "SHV-120 ", "SHV-121 ",
                "SHV-12-like ", "SHV-14 ", "SHV-144 ", "SHV-146-like ",
                "SHV-148 ", "SHV-154 ", "SHV-155 ", "SHV-157 ", "SHV-168 ",
                "SHV-187 ", "SHV-1-like ", "SHV-2 ", "SHV-25 ", "SHV-26 ",
                "SHV-27 ", "SHV-28 ", "SHV-28-like ", "SHV-2A ",
                "SHV-2-like ", "SHV-30 ", "SHV-31 ", "SHV-32 ", "SHV-33 ",
                "SHV-33-like ", "SHV-36 ", "SHV-38 ", "SHV-40 ", "SHV-5 ",
                "SHV-52 ", "SHV-55 ", "SHV-5-like ", "SHV-60 ",
                "SHV-60-like ", "SHV-61 ", "SHV-62 ", "SHV-7 ", "SHV-71 ",
                "SHV-75 ", "SHV-76 ", "SHV-77 ", "SHV-9 ", "TEM-1 ",
                "TEM-10 ", "TEM-110 ", "TEM-12 ", "TEM-135 ", "TEM-15 ", 
                "TEM-155 ", "TEM-166 ", "TEM-169 ", "TEM-176 ", "TEM-181 ",
                "TEM-19 ", "TEM-190 ", "TEM-1-like ", "TEM-2 ", "TEM-206 ",
                "TEM-210 ", "TEM-212 ", "TEM-214 ", "TEM-215 ", "TEM-24 ",
                "TEM-26 ", "TEM-29 ", "TEM-30 ", "TEM-32 ", "TEM-33 ",
                "TEM-34 ", "TEM-35 ", "TEM-4 ", "TEM-40 ", "TEM-52 ",
                "TEM-54 ", "TEM-57 ", "TEM-84 ", "TEM-92 ", "VEB-1 ",
                "VEB-6 ", "VEB-9 ", "IMP-27 ", "IMP-4 ", "IMP-8 ",
                "NDM-1 ", "NDM-4 ", "NDM-5 ", "NDM-6 ", "NDM-7 ",
                "VIM-1 ", "VIM-12 ", "VIM-23 ", "VIM-4 ", "ACC-1 ",
                "ACC-4 ", "CMY-13 ", "CMY-16 ", "CMY-2 ", "CMY-2-like ",
                "CMY-4 ", "CMY-42 ", "CMY-42-like ", "CMY-44 ",
                "CMY-44-like ", "CMY-48-like ", "CMY-4-like ",
                "CMY-6 ", "DHA-1 ", "DHA-23 ", "DHA-7 ", "FOX-5 ",
                "FOX-5-like ", "FOX-7 ", "NMC-A ", "OXA-1_OXA-30 ",
                "OXA-1_OXA-30-like ", "OXA-224 ", "OXA-256-like ",
                "OXA-320 ", "OXA-392 ", "OXA-4 ", "OXA-74 ", "OXA-9 ",
                "OXA-9-like ", "OXA-10 ", "OXA-10-like ", "OXA-23 ",
                "OXA-2 ", "OXA-2-like ", "OXA-163 ", "OXA-181 ", "OXA-232 ",
                "OXA-244 ", "OXA-370 ", "OXA-48 ", "OXA-48-like ", "LAP-1 ",
                "LAP-2 ", "LEN-11 ", "LEN-16 ", "LEN-17 ", "LEN-2 ", "LEN-9 ",
                "MAL-1 ", "ORN-1 ", "OXA-534 ", "SCO-1 ", "SRT-2 ", "TLA-1 "]

#cefe_col_remove = ['CTX-M-15 ']
cefe_col_remove = []

def translate_pm1(y_test, y_pred):
    """
    Checks if the prediction is +-1 dilution from actual.
    If it is, then it changes prediction to actual to show it is correct.
  
    Parameters
    ----------
    y_test : float list
      List of actual labels
    y_pred : float list
      List of predicted labels
  
    Returns
    -------
    New list of changed predicted labels
  
    """
    y_new = []
    for i in range(0, len(y_test)):
        if y_test[i] == (y_pred[i] * 2) or y_test[i] == (y_pred[i] * 0.5):
            y_new.append(y_test[i])
        else:
            y_new.append(y_pred[i])
          
    return y_new

def get_data(path, cell_num, file_name):
    """
    Collect a csv file and return a useful data structure for knn
  
    Parameters
    ----------
    path : string
      Path to file
    cell_num : int
      Cell number that labels are located at (between 0 and 47)
    file_name : string
      Filename of csv to use
  
    Returns
    -------
    None.
  
    """
    X, y, _, collection_ids = get_year_data(path, file_name, cell_num, 49)
    return X, y, collection_ids
  
def get_year_data(path, file_name, cell_num, data_start_cell):
    """
    Collect a csv file and return a useful data structure for knn
  
    Parameters
    ----------
    path : string
      Path to file
    file_name : string
      Filename of csv to use
    cell_num : int
      Cell number that labels are located at (between 0 and 47)
    data_start_cell: int
      Cell input data starts at
  
    Returns
    -------
    None.
  
    """
    
    #Take into account that column 0 is the collection number
    cell_num += 1
    if not path.endswith(os.path.sep):
      path += os.path.sep
      
    with open(path + file_name) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        X = []
        y = []
        collection_ids = []
        for index, row in enumerate(csvReader):
            if index == 0:
                col_header = row[cell_num]
                if col_header == "Cefepime":
                    cols_to_remove = [gene_headers.index(x) for x in cefe_col_remove]
                else:
                    cols_to_remove = []
                    
            elif row[cell_num] != '-1.0' and row[cell_num] != '-1' and row[cell_num] != -1.0  and row[cell_num] != -1:
                x_values = []
                for i in range(data_start_cell, len(row)):
                    if (i - data_start_cell) in cols_to_remove:
                        continue
                  
                    x_values.append(row[i])
                
                y.append(row[cell_num])
                X.append(x_values)
                collection_ids.append(row[0])
                
          
    X = np.asarray(X, dtype=np.int32)
    y = np.asarray(y, dtype=np.float32)
    return X, y, col_header, collection_ids
  
def save_results_knn(k, file_name, output, pm1_output, separators):
    """
    Takes in 2 dictionaries and rights their results out to an excel file
  
    Parameters
    ----------
    k : int
      value used for knn
    file_name : string
      name to give file
    output : dict of string:float pairs
      f1-score of predicted results
    pm1_output : dict of string:float pairs
      f1-score of +-1 dilution predicted results
    separators : list of string
      list of separators for excel sheet
      
  
    Returns
    -------
    None.
  
    """
    save_results(file_name, output, pm1_output, 'knn', separators, k)
    
def save_results_rf(file_name, output, pm1_output, separators):
    """
    Takes in 2 dictionaries and rights their results out to an excel file
  
    Parameters
    ----------
    file_name : string
      name to give file
    output : dict of string:float pairs
      f1-score of predicted results
    pm1_output : dict of string:float pairs
      f1-score of +-1 dilution predicted results
    separators : list of string
      list of separators for excel sheet
      
  
    Returns
    -------
    None.
  
    """
    save_results(file_name, output, pm1_output, 'rf', separators)
    
def save_results_xgb(file_name, output, pm1_output, separators):
    """
    Takes in 2 dictionaries and rights their results out to an excel file
  
    Parameters
    ----------
    file_name : string
      name to give file
    output : dict of string:float pairs
      f1-score of predicted results
    pm1_output : dict of string:float pairs
      f1-score of +-1 dilution predicted results
    separators : list of string
      list of separators for excel sheet
      
  
    Returns
    -------
    None.
  
    """
    save_results(file_name, output, pm1_output, 'xgb', separators)
  
def save_results(file_name, output, pm1_output, algorithm, separators, k=None):
    if algorithm == 'knn':
        file = file_name + '_knn_' + str(k) + '.xlsx'
    elif algorithm == 'rf':
        file = file_name + '_rf_' + '.xlsx'
    else:
        file = file_name + '_xgb_' + '.xlsx'
        
    # print(output)
    # print()
    # print(separators)
    # print()
        
    
    with xlsxwriter.Workbook(file) as workbook:
        formatted = workbook.add_worksheet('f1 actual')
        formatted.write(0, 0, "Separator")
        for i, k in enumerate(output.keys()):
            formatted.write(0, i + 1, k)
            #print(output[k])
        
            row_num = 1
            for separator in separators:
                formatted.write(row_num, 0, separator.replace(".csv", ""))
                
                if separator in output[k]:
                    formatted.write(row_num, i + 1, output[k][separator])
                    
                row_num += 1
                
        formatted = workbook.add_worksheet('f1 +-1')
        formatted.write(0, 0, "Separator")
        for i, k in enumerate(pm1_output.keys()):
            formatted.write(0, i + 1, k)
        
            row_num = 1
            for separator in separators:
                formatted.write(row_num, 0, separator.replace(".csv", ""))
                
                if separator in pm1_output[k]:
                    formatted.write(row_num, i + 1, pm1_output[k][separator])
                    
                row_num += 1
                
def save_genotypes(file_name, correct, incorrect, algorithm):
    """
    Save the corectly predicted and not correctly predicted genotypes of inputs
    to an excel file for further analysis.
  
    Parameters
    ----------
    file_name : str
      What to make the pre part of the name of the output file.
    correct : array
      Array of genotypes (arrays).
    incorrect : array
      Array of genotypes (arrays).
    algorithm : str
      Name of algorithm used.
  
    Returns
    -------
    None.
  
    """
    file = file_name + '_' + algorithm + '.xlsx'
    
    with xlsxwriter.Workbook(file) as workbook:
        formatted = workbook.add_worksheet('correct')
        for row_num, geno in enumerate(correct):
            formatted.write(row_num, 0, geno.get("id"))
            for col_num, gene in enumerate(geno.get("value")):
                formatted.write(row_num, col_num + 1, gene)
                
        formatted = workbook.add_worksheet('incorrect')
        for row_num, geno in enumerate(incorrect):
            formatted.write(row_num, 0, geno.get("id"))
            for col_num, gene in enumerate(geno.get("value")):
                formatted.write(row_num, col_num + 1, gene)
                
def save_pred_mic_distro(file_name, collection, algorithm):
    """
    
  
    Parameters
    ----------
    file_name : TYPE
      DESCRIPTION.
    collection : TYPE
      DESCRIPTION.
    algorithm : TYPE
      DESCRIPTION.
  
    Returns
    -------
    None.
  
    """
    file = file_name + '_' + algorithm + '.xlsx'
    
    with xlsxwriter.Workbook(file) as workbook:
        output = workbook.add_worksheet('output')
        mics = list(collection.keys())
        mics.sort()
        for i, mic in enumerate(mics):
            section = collection.get(mic)
            output.write(0, i, mic)
            output.write(1, i, section["amount"])
            #if not os.path.exists("+-genotypes\\" + str(mic) + "_" + algorithm + ".csv"):
                
            
            with open("+-genotypes\\" + str(mic) + "_" + algorithm + ".csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(list(filter(lambda x : x not in cefe_col_remove, gene_headers)))
                writer.writerows(section['genos'])
    
def get_labels(path, file_name, train_antibiotic):
    """
  

    Parameters
    ----------
    path : str
      Path to labels csv file
    file_name : str
      Labels csv file name (with extension)
    train_antibiotic : int
      Antibioitic number to use from file (starts at 0)
  
    Returns
    -------
    List of labels for that antibiotic
  
    """
    if not path.endswith(os.path.sep):
      path += os.path.sep
    
    labels = []
    row_num = 0
    with open(path + file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row_num != 0 and row[train_antibiotic] != '':
                labels.append(float(row[train_antibiotic]))
                
            row_num += 1
    
    labels = np.asarray(labels, dtype=np.float32)
    return labels
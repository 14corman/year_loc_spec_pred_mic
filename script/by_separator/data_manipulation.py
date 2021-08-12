# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 13:03:24 2020

@author: Cory Kromer-Edwards
"""

import csv
import os
import numpy as np
import xlsxwriter

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
    X, y, _ = get_year_data(path, file_name, cell_num, 48)
    return X, y
  
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
    if not path.endswith(os.path.sep):
      path += os.path.sep
      
    with open(path + file_name) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        X = []
        y = []
        row_num = 0
        for row in csvReader:
            if row_num == 0:
                col_header = row[cell_num]
            elif row[cell_num] != '-1.0' and row[cell_num] != '-1' and row[cell_num] != -1.0  and row[cell_num] != -1:
                y.append(row[cell_num])
                X.append(row[data_start_cell:])
            
            row_num += 1
          
    X = np.asarray(X, dtype=np.int32)
    y = np.asarray(y, dtype=np.float32)
    return X, y, col_header
  
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
  
def save_results(file_name, output, pm1_output, algorithm, separators, k=None):
    if algorithm == 'knn':
        file = file_name + '_knn_' + str(k) + '.xlsx'
    else:
        file = file_name + '_rf_' + '.xlsx'
    
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
    
def get_labels(path, file_name, train_antibiotic):
    """
  

    Parameters
    ----------
    path : string
      Path to labels csv file
    file_name : string
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
    with open(path + file_name) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        for row in csvReader:
            if row_num != 0 and row[train_antibiotic] != '':
                labels.append(float(row[train_antibiotic]))
                
            row_num += 1
    
    labels = np.asarray(labels, dtype=np.float32)
    return labels
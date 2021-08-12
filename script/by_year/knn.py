# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 18:41:47 2020

@author: Cory Kromer-Edwards
"""

from argparse import ArgumentParser
from collections import Counter
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from imblearn.combine import SMOTEENN
from imblearn.over_sampling import RandomOverSampler
import os
from data_manipulation import get_data, translate_pm1, save_results_knn, get_year_data, get_labels, save_genotypes, save_pred_mic_distro
import csv
import math

# The uncommented drug will be what drug results are kept
#EXTRACT_DRUG = "Cefepime"
#EXTRACT_DRUG = "Ceftriaxone"
#EXTRACT_DRUG = "Meropenem"
EXTRACT_DRUG = "Ceftazidime"

# The uncommented species csv will be what is kept from run
#ORGANISM_SELECTED = "Escherichia_coli.csv"
ORGANISM_SELECTED = "Klebsiella_pneumoniae.csv"

def main():
    """
    Collects input arguements, creates key, and outputs to file.
    """
    parser = build_parser()
    options = parser.parse_args()
    
    output_all = dict()
    pm1_output_all = dict()
    separators = os.listdir(options.data_path)
    for train_antibiotic in [3, 6, 13, 21, 32, 34, 41]:
        X_train, y_train, col_header, collection_ids = get_year_data(os.getcwd(), options.training_file, train_antibiotic, 49)
        print("Using antibiotic: %s" % (col_header))
        #print("Original y shape: %s" % Counter(y_train))
        
        if X_train.size < 100 or len(set(y_train)) < 2:
            print("not enough data for antibiotic... skipping...")
            continue
    
        labels = get_labels(os.getcwd(), 'labels.csv', train_antibiotic)
        labels.sort()
        le = preprocessing.LabelEncoder()
        le.fit(labels)
        print(labels)
        print(set(y_train))
        y_train = le.transform(y_train)
        
        temp_y_dict = Counter(y_train)
        for key, value in temp_y_dict.items():
            if value < 6:
                temp_y_dict[key] = 6
        
        #Make sure every class has at least 6 elements to be able to do KNN in SMOTE.
        ros = RandomOverSampler(sampling_strategy = temp_y_dict)
        X_train, y_train = ros.fit_resample(X_train, y_train)
        #print("New y shape: %s" % Counter(y_train))
        
        
        #SMOTE is a a way to over sample minority classes by creating synthetic data
        #EEN is a way to under sample by using Edited Nearest Neighbors
        #https://github.com/scikit-learn-contrib/imbalanced-learn/blob/b861b3a8e3414c52f40a953f2e0feca5b32e7460/imblearn/combine/_smote_enn.py#L25
        sme = SMOTEENN(n_jobs = 5)
        print("Original y shape: %s" % Counter(y_train))
        X_train, y_train = sme.fit_resample(X_train, y_train)
        print("New y shape: %s" % Counter(y_train))
        
        # gsc = GridSearchCV(estimator=KNeighborsClassifier(),
        #                     param_grid = {
        #                       'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        #                       },
        #                     scoring='f1_micro')
        
        # gsc.fit(X_train, y_train)
        # print("Best parameters set found on development set:")
        # print()
        # print(gsc.best_params_)
        # # print()
        # # print("Grid scores on development set:")
        # # print()
        # means = gsc.cv_results_['mean_test_score']
        # stds = gsc.cv_results_['std_test_score']
        # with open("grid_search\\knn_" + col_header + ".csv", 'w', newline='\n', encoding='utf-8') as csv_file:
        #     writer = csv.writer(csv_file)
        #     for mean, std, params in zip(means, stds, gsc.cv_results_['params']):
        #         writer.writerow([params['n_neighbors'], "%0.3f" % mean, "%0.3f" % (std * 2)])
        #         #print("%0.3f \t %0.03f \t %i"
        #         #      % (mean, std * 2, params['n_neighbors']))
        #     #     print("%0.3f"
        #     #           % (mean))
        #     # print()
        
        #Create and fit the model with best hyperparameter
        #classifier = KNeighborsClassifier(n_neighbors=gsc.best_params_['n_neighbors'])
        classifier = KNeighborsClassifier(n_neighbors=1)
        classifier.fit(X_train, y_train)
        
        output = dict()
        pm1_output = dict()
        correct = []
        incorrect = []
        correct_mics = []
        incorrect_mics = []
        for file in separators:
            #print(file)
            X_test, y_test, collection_ids = get_data(options.data_path, train_antibiotic, file)
            if len(y_test) < 10:
                #print("skipping...")
                #separators.remove(file)
                continue
                  
            y_test = le.transform(y_test)
            y_pred = classifier.predict(X_test)
            y_labels = list(set(y_pred))
            y_names = [str(labels[i]) for i in y_labels]
            y_pm1_pred = translate_pm1(y_test, y_pred)
            
            metric_dict = classification_report(y_test, y_pred, labels = y_labels, target_names=y_names, zero_division = 0, output_dict=True)
            metric_pm1_dict = classification_report(y_test, y_pm1_pred, labels = y_labels, target_names=y_names, zero_division = 0, output_dict=True)
            
            if 'micro avg' not in metric_dict:
                metrics = metric_dict['weighted avg']
            else:
                metrics = metric_dict['micro avg']
                
            if 'micro avg' not in metric_pm1_dict:
                metrics_pm1 = metric_pm1_dict['weighted avg']
            else:
                metrics_pm1 = metric_pm1_dict['micro avg']
                
            output[file] = metrics['f1-score']
            pm1_output[file] = metrics_pm1['f1-score']
            
            if file == ORGANISM_SELECTED and col_header == EXTRACT_DRUG:
                for y, x, y_pred_value, col_id in zip(y_test, X_test, y_pred, collection_ids):
                    if y == y_pred_value:
                        correct.append({"id": col_id, "value": x})
                        correct_mics.append({"id": col_id, "value": [round(labels[y], 3), round(labels[y_pred_value], 3)]})
                    else:
                        incorrect.append({"id": col_id, "value": x})
                        incorrect_mics.append({"id": col_id, "value": [round(labels[y], 3), round(labels[y_pred_value], 3)]})
            
        output_all[col_header] = output
        pm1_output_all[col_header] = pm1_output
        
        if col_header == EXTRACT_DRUG:
            save_genotypes('saved_genotypes', correct, incorrect, 'knn')
            save_genotypes('saved_genotypes_mics', correct_mics, incorrect_mics, 'knn')
            
            correction_output = {-14: {"amount": 0, "genos": []}, -13: {"amount": 0, "genos": []}, -12: {"amount": 0, "genos": []}, -11: {"amount": 0, "genos": []}, -10: {"amount": 0, "genos": []}, -9: {"amount": 0, "genos": []}, -8: {"amount": 0, "genos": []}, -7: {"amount": 0, "genos": []}, -6: {"amount": 0, "genos": []}, -5: {"amount": 0, "genos": []}, -4: {"amount": 0, "genos": []}, -3: {"amount": 0, "genos": []}, -2: {"amount": 0, "genos": []}, -1: {"amount": 0, "genos": []}, 0: {"amount": 0, "genos": []}, 
                                  14: {"amount": 0, "genos": []}, 13: {"amount": 0, "genos": []}, 12: {"amount": 0, "genos": []}, 11: {"amount": 0, "genos": []}, 10: {"amount": 0, "genos": []}, 9: {"amount": 0, "genos": []}, 8: {"amount": 0, "genos": []}, 7: {"amount": 0, "genos": []}, 6: {"amount": 0, "genos": []}, 5: {"amount": 0, "genos": []}, 4: {"amount": 0, "genos": []}, 3: {"amount": 0, "genos": []}, 2: {"amount": 0, "genos": []}, 1: {"amount": 0, "genos": []} }
            
            for geno, cor in zip(correct, correct_mics):
                actual = cor.get("value")[0]
                pred = cor.get("value")[1]
                if actual > pred:
                    #Below zero
                    #amount below -> 2^x = actual/pred -> x = log_2(actual/pred)
                    amount = -int(math.floor(math.log(actual/pred, 2.0)))
                elif actual < pred:
                    #Above zero
                    #amount above -> 2^x = actual/pred -> x = log_2(pred/actual)
                    amount = int(math.floor(math.log(pred/actual, 2.0)))
                else:
                    #Correct (0)
                    amount = 0
                    
                if amount in correction_output:
                    correction_output[amount]["amount"] += 1
                    correction_output[amount]["genos"].append(geno.get("value"))
                else:
                    correction_output[amount] = {"amount": 1, "genos": [geno.get("value")]}
                    
            for geno, incor in zip(incorrect, incorrect_mics):
                actual = incor.get("value")[0]
                pred = incor.get("value")[1]
                if actual > pred:
                    #Below zero
                    #amount below -> 2^x = actual/pred -> x = log_2(actual/pred)
                    amount = -int(math.floor(math.log(actual/pred, 2.0)))
                elif actual < pred:
                    #Above zero
                    #amount above -> 2^x = actual/pred -> x = log_2(pred/actual)
                    amount = int(math.floor(math.log(pred/actual, 2.0)))
                else:
                    #Correct (0)
                    amount = 0
                    
                if amount in correction_output:
                    correction_output[amount]["amount"] += 1
                    correction_output[amount]["genos"].append(geno.get("value"))
                else:
                    correction_output[amount] = {"amount": 1, "genos": [geno.get("value")]}
                    
            save_pred_mic_distro("prediction_distro", correction_output, 'knn')
            
    save_results_knn(1, options.data_path, output_all, pm1_output_all, separators)

def build_parser():
    """
    Author Cory Kromer-Edwards
    Builds the parser based on input variables from the command line.
    """
    parser = ArgumentParser()
    
    parser.add_argument('data_path', type=str,
                        help='The path to all data files from current directory', 
                        metavar='D')
    
    parser.add_argument('training_file', type=str, 
                        help='The csv training file year to use',
                        metavar='T')
    
    # parser.add_argument('k', type=int, 
    #                     help='Number of neighbors to use (-1 = use best)',
    #                     metavar='K')
    
    # parser.add_argument('train_antibiotic', type=int, 
    #                     help='Antibiotic  cell number to use for training (starts at 0)',
    #                     metavar='A')
    
    
    return parser


if __name__ == '__main__':
    main()


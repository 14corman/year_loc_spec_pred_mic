# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 18:44:33 2020

@author: Cory Kromer-Edwards
"""

import csv
import os
from itertools import zip_longest

#Different locations in csv file for data
#NOTE: Country now means continent
#NOTE: Species now means organism, and only E. coli & Kleb p. are used.
year_cell = 3
country_cell = 6
species_cell = 11
passing_organisms = ['Escherichia coli', 'Klebsiella pneumoniae']
antibiotic_start_cell = 16
num_antibiotics = 48
gene_start_cell = 64
#num_genes = 409  #All beta-lactam (OLD)
num_genes = 237

#The antibiotic that will be used for country and species separation
#separation_antibiotic = 2   #Ampicillin-sulbactam
#separation_antibiotic = 18   #Ceftobiprole
#separation_antibiotic = 25   #Colistin
#separation_antibiotic = 27   #Doripenem
#separation_antibiotic = 35   #Meropenem-vaborbactam

#The os paths required to build the files
start_path = os.getcwd() + os.path.sep
species_path = start_path + "species_separator"
country_path = start_path + "country_separator"
drug_path = start_path + "drug_separator"
all_path = start_path + "no_separator"

#For debuging csv
debug = False

def get_mics(row):
    """
    Collect all MIC values for the given isolate
  
    Parameters
    ----------
    row : list
      Row from CSV file
  
    Returns
    -------
    array of mic values for row. No MIC=-1
  
    """
    mics = []
    for i in range(antibiotic_start_cell, antibiotic_start_cell + num_antibiotics):
        mic = str(row[i])
        if "<=" in mic:
            mic = float(mic[2:])
        elif ">" in mic:
            mic = float(mic[1:])
        elif mic == "":
            mic = -1.0
        else:
            mic = float(mic)
            
        mics.append(mic)
        
    return mics
  
def get_genes(row):
    """
    Collect all gene acuisition results for isolate
  
    Parameters
    ----------
    row : list
        Row from CSV file
  
    Returns
    -------
    array of GA values for row. No gene = 0, gene found = 1
  
    """
  
    genes = []
    for i in range(gene_start_cell, gene_start_cell + num_genes):
        if row[i] == "":
            genes.append(0)
        else:
            genes.append(1)
            
    return genes
  
def write_csv(data_dict, header, path):
    """
    Takes a dictionary and header list and writes them out to a csv files
  
    Parameters
    ----------
    data_dict : dict
      Key:Value where Key tells which csv file to write to and Value is data row
      
    header : list
      A data row for the header
      
    path : string
      Folder to place csv files
  
    Returns
    -------
    None.
  
    """
    for name, data in data_dict.items():
        with open(path + os.path.sep + name + ".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)
    

def load_dataset():
    """
    Author Cory Kromer-Edwards
    The main method to preprocessing. This method will open the dataset csv
    file, and send each row to the preprocessing steps.
    """
    
    if not os.path.exists(species_path):
        os.mkdir(species_path)
    else:
        [os.remove(species_path + os.path.sep + f) for f in os.listdir(species_path)]
        
    if not os.path.exists(country_path):
        os.mkdir(country_path)
    else:
        [os.remove(country_path + os.path.sep + f) for f in os.listdir(country_path)]
        
    if not os.path.exists(drug_path):
        os.mkdir(drug_path)
    else:
        [os.remove(drug_path + os.path.sep + f) for f in os.listdir(drug_path)]
        
    if not os.path.exists(all_path):
        os.mkdir(all_path)
    else:
        [os.remove(all_path + os.path.sep + f) for f in os.listdir(all_path)]
    
    #Collect all information from dataset
    all_rows = []
    with open(start_path + 'dataset.csv') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        lineCount = 0
        for row in csvReader:
            if lineCount == 0:
                #Names for headers of output csv files
                antibiotic_names = [row[i] for i in range(antibiotic_start_cell, antibiotic_start_cell + num_antibiotics)]
                gene_names = [row[i] for i in range(gene_start_cell, gene_start_cell + num_genes)]
                
                if debug:
                    print(f'Column names are:\n{", ".join(row)}')
                    
                    #Used to test if the range for gene cells are correct
                    #print(", ".join([row[x] for x in range(gene_start_cell, gene_start_cell + num_genes)]))
                lineCount += 1
            elif lineCount > 5 and debug:
                break
            else:
                if row[species_cell] in passing_organisms:
                    mics = get_mics(row)
                    genes = get_genes(row)
                    if debug:
                        print("\nRow number " + str(lineCount))
                        print("\nSpecies: " + row[species_cell])
                        print("\nCountry: " + row[country_cell])
                        print("\nMIC's': " + ", ".join([str(m) for m in mics]))
                        print("\n")
                        
                    row_data = dict()
                    row_data["s"] = row[species_cell]
                    row_data["c"] = row[country_cell]
                    row_data["m"] = mics
                    row_data["g"] = genes
                    all_rows.append(row_data)
                
            print(f'Processed {lineCount} lines.')
            lineCount += 1
    
    species = {}
    countries = {}
    antibiotics = {}
    labels = {"labels": [set() for _ in range(num_antibiotics)]}
    
    #Start separating it out into data structures
    for r in all_rows:
        m = r.get('m')
        
        for i, a in enumerate(m):
            if a != '-1.0' and a != -1.0:
                labels["labels"][i].add(a)
                
        
        # data_point = [m[separation_antibiotic]]
        # [data_point.append(i) for i in r.get('g')]
        
        data_point = []
        for a in m:
            data_point.append(a)
        
        for g in r.get('g'):
            data_point.append(g)
        
        #Separate species data points
        s = r.get('s')
        if s in species:
            species[s].append(data_point)
        else:
            species[s] = [data_point]
            
        #Separate country data points
        c = r.get('c')
        if c in countries:
            countries[c].append(data_point)
        else:
            countries[c] = [data_point]
            
        #Separate antibiotic data points
        for i, a in enumerate(m):
            data_point = [a]
            [data_point.append(i) for i in r.get('g')]
            if antibiotic_names[i] in antibiotics:
                antibiotics[antibiotic_names[i]].append(data_point)
            else:
                antibiotics[antibiotic_names[i]] = [data_point]
                
    #Set up header file for species and country
    header = []
    [header.append(x) for x in antibiotic_names]
    [header.append(x) for x in gene_names]
    
    # header = []
    # header.append(antibiotic_names[separation_antibiotic])
    # [header.append(x) for x in gene_names]
                
    #Send data structures to csv files
    write_csv(species, header, species_path)
    write_csv(countries, header, country_path)
    
    #Header for antibiotics
    header = ['Antibioitc']
    [header.append(x) for x in gene_names]
    write_csv(antibiotics, header, drug_path)
        
    #Labels for each antibiotic
    labels_transpose = {'labels' : zip_longest(*labels['labels'], fillvalue = '')}
    write_csv(labels_transpose, antibiotic_names, os.getcwd())
    
  
def main():
    load_dataset()

if __name__ == '__main__':
    main()


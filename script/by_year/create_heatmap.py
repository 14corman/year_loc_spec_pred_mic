# -*- coding: utf-8 -*-
"""
Created on Sun May 10 08:32:00 2020

@author: Cory
"""

from argparse import ArgumentParser
import graphviz
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def main():
    parser = build_parser()
    algorithm = parser.parse_args().algorithm_name
    correct = []
    incorrect = []
    incorrect_org = []
    correct_org = []
    features = []
    
    with open('saved_genotypes_' + algorithm + '_processed.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_num = 1
        for row in csv_reader:
            if row_num != 1:
                if row[-1] == '1':
                    correct.append(row[:-1])
                else:
                    incorrect.append(row[:-1])
            else:
                features = row[:-1]
                row_num += 1
        
    #Remove all genes that have all 0's to make graph readable. 
    #Then, remove those same genes from feature list.
    correct = np.array(correct).astype(float)
    correct_features = [features[x] for x in np.where(correct.any(axis=0))[0]]
    correct = correct[:, ~np.all(correct == 0, axis = 0)]
    
    incorrect = np.array(incorrect).astype(float)
    incorrect_features = [features[x] for x in np.where(incorrect.any(axis=0))[0]]
    incorrect = incorrect[:, ~np.all(incorrect == 0, axis = 0)]
        
    for i, org in enumerate(correct):
        correct_org.append('Organism ' + str(i))
      
    for i, org in enumerate(incorrect):
        incorrect_org.append('Organism ' + str(i))
        
    ############################################################################
    # Code modified from: https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html
    plt.rcParams.update({'font.size': 8}) #default is 10
    fig, ax = plt.subplots()
    
    #Need aspect auto so make sure graph is properly proportioned with axis text
    im = ax.imshow(correct, aspect='auto')
    
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(correct_features)))
    #ax.set_yticks(np.arange(len(incorrect_org)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(correct_features)
    #ax.set_yticklabels(incorrect_org)
    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
              rotation_mode="anchor")
    
    # Loop over data dimensions and create text annotations.
    # for i in range(len(incorrect_org)):
    #     for j in range(len(features)):
    #         text = ax.text(j, i, incorrect[i, j],
    #                         ha="center", va="center", color="w")
    
    #ax.set_title("Harvest of local farmers (in tons/year)")
    fig.tight_layout()
    #plt.show()
    ############################################################################
    
    #Remove borders since they can overlap with cells
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    #dpi of at least 400 because any lower and some cells will not be shown
    plt.savefig(algorithm + '_heatmap.pdf', dpi=400)

def build_parser():
    """
    Author Cory Kromer-Edwards
    Builds the parser based on input variables from the command line.
    """
    parser = ArgumentParser()
    
    parser.add_argument('algorithm_name', type=str,
                        help='Name of algorithm to look up input file.', metavar='D')
    
    return parser


if __name__ == '__main__':
    main()
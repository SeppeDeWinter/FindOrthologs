def _nan_to(a, b):
    import numpy as np
    try:
        if a == (np.nan, np.nan):
            return b
        else:
            return a
    except:
            return a

def FindOrthologs(features_file_path, homology_table_file_path, out_file_path):
    import pandas as pd
    import numpy as np

    df_features = pd.read_csv(features_file_path, sep = '\t', names = ['Spec_A_gid', 'Spec_A_symbol', 'type'])
    df_homol = pd.read_csv(homology_table_file_path, sep = '\t')
    df_homol.columns = ['Spec_A_gid', 'Spec_A_symbol', 'Spec_B_gid', 'Spec_B_symbol']
    df_homol.index = df_homol['Spec_A_gid']

    print('Mapping ... \n')
    
    mapping_dict = {
                    spec_A_geneID: 
                    _nan_to((df_homol.loc[spec_A_geneID]['Spec_B_gid'], df_homol.loc[spec_A_geneID]['Spec_B_symbol']), ('NO_ORTH', 'NO_ORTH'))
                    if spec_A_geneID in df_homol.index else ('NOT_IN_DB', 'NOT_IN_DB')
                    for spec_A_geneID in df_features['Spec_A_gid'].values
                   }
    
    converted_gid_symb_list = [
                                mapping_dict[spec_A_geneID] 
                                if np.ndim(mapping_dict[spec_A_geneID]) == 1 else ('MULTI_MAP', 'MULTI_MAP')
                                for spec_A_geneID in df_features['Spec_A_gid'].values
                              ]
    #calculate statistics:
    n_features_specA = len(converted_gid_symb_list)
    n_not_in_db = converted_gid_symb_list.count(('NOT_IN_DB', 'NOT_IN_DB'))
    n_multi_map = converted_gid_symb_list.count(('MULTI_MAP', 'MULTI_MAP'))
    n_no_orth = converted_gid_symb_list.count(('NO_ORTH', 'NO_ORTH'))
    n_prop_converted = n_features_specA - n_not_in_db - n_multi_map - n_no_orth
    
    print('+-----------------------------------------------------------------------------------------------+')
    print('|' + str(n_not_in_db) + '\tfeatures were not found in the provided ortholog database\t' + str(np.round(n_not_in_db/n_features_specA * 100, 1)) + ' %\t(NOT_IN_DB)\t|')
    print('|' + str(n_multi_map) + '\tfeatures were not 1 to 1 orthologues\t\t\t\t' + str(np.round(n_multi_map/n_features_specA * 100, 1)) + ' %\t(MULTI_MAP)\t|')
    print('|' + str(n_no_orth) + '\tfeatures for which no orthologue was found\t\t\t' + str(np.round(n_no_orth/n_features_specA * 100, 1)) + ' %\t(NO_ORTH)\t|')
    print('|' + str(n_prop_converted) + '\tfeatures were properly mapped, 1 to 1\t\t\t\t' + str(np.round(n_prop_converted/n_features_specA * 100, 1)) + ' %\t\t\t|')
    print('|\t\t\t\t\t\t\t\t\t\t\t\t|')
    print('|' +str(n_features_specA) + '\tTOTAL FEATURES\t\t\t\t\t\t\t\t\t\t|')
    print('+-----------------------------------------------------------------------------------------------+')

    print('\n Writing file ... ' + out_file_path)

    df_features_converted = pd.DataFrame(data = {
                                                    'Spec_B_gid':[feature[0] for feature in converted_gid_symb_list],
                                                    'Spec_B_symbol':[feature[1] for feature in converted_gid_symb_list],
                                                    'type':['Gene Expression' for i in range(n_features_specA)]
                                                }
                                        )
    df_features_converted.to_csv(out_file_path, sep = '\t', header = False, index = False, compression = 'gzip')

    print('\n Done!')

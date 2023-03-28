from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from pathlib import Path
import pickle

# Store the labels for main clusters and sub clusters inside 
predicted_labels = ["Strategic Product Planning","Product & Service Development", "Production System Development"]
sub_cluster0 = ["Idea Generation", "Market Analysis", "Technology Analysis", "Product Manangement"]
sub_cluster1 = ["Testing", "Product Design", "Requirements Management"]
sub_cluster3 = ["Production System Planning", "Production System Implementation"]

# We used the hugging face's sentence transformer for embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create path to the pickle_files directory with pathlib library so that it is accessible through all OS
pickle_folder = Path("../pickle_files")

# Files to be open in pickle_files directory

spp_file = pickle_folder / "spp_embeddings.sav"
pd_file =  pickle_folder / "pd_embeddings.sav"
psd_file =  pickle_folder / "psd_embeddings.sav"

ig_file =  pickle_folder / "idea_generation_embeddings.sav"
ma_file =  pickle_folder / "market_analysis_embeddings.sav"
ta_file =  pickle_folder / "technology_analysis_embeddings.sav"
pm_file =  pickle_folder / "product_management_embeddings.sav"

te_file =  pickle_folder / "testing_embeddings.sav"
pde_file =  pickle_folder / "product_design_embeddings.sav"
rm_file =  pickle_folder / "requirements_management_embeddings.sav"

psp_file =  pickle_folder / "production_system_planning_embeddings.sav"
psi_file =  pickle_folder / "production_system_implementation_embeddings.sav"

# We load the embeddings of main clusters and sub-clusters using the pickle Python module
pickled_spp_embeddings = pickle.load(open(spp_file, 'rb'))
pickled_pd_embeddings = pickle.load(open(pd_file, 'rb'))
pickled_psd_embeddings = pickle.load(open(psd_file, 'rb'))

idea_generation_embeddings = pickle.load(open(ig_file, 'rb'))
market_analysis_embeddings = pickle.load(open(ma_file, 'rb'))
technology_analysis_embeddings = pickle.load(open(ta_file, 'rb'))
product_manangement_embeddings = pickle.load(open(pm_file, 'rb'))

testing_embeddings = pickle.load(open(te_file, 'rb'))
product_design_embeddings = pickle.load(open(pde_file, 'rb'))
requirements_management_embeddings = pickle.load(open(rm_file, 'rb'))

production_system_planning_embeddings = pickle.load(open(psp_file, 'rb'))
production_system_implementation_embeddings = pickle.load(open(psi_file, 'rb'))

# Function to find cosine similarity scores between two vectors
def find_cosine_sim(vector1,vector2):
    return(cosine_similarity(vector1.reshape(1, -1),vector2.reshape(1, -1))[0][0])

# Function to find the maximum among the similarity scores passed in a list
def cycle_result(list1):
    maximum = max(list1)
    return list1.index(maximum)

# Function to find main cluster and sub-clusters of AI companies passed to the function inside a dataframe
# It returns two lists contains the main clusters and sub-clusters
def find_clusters(dataframe):
    main_cluster_labels = []
    sub_cluster_labels = []
    main_cluster = -1
    sub_cluster = -1
    for index, row in dataframe.iterrows():
        data_emebeddings = model.encode(row["Keywords"])
        list1=[ find_cosine_sim(pickled_spp_embeddings, data_emebeddings),
                find_cosine_sim(pickled_pd_embeddings, data_emebeddings),
                find_cosine_sim(pickled_psd_embeddings, data_emebeddings)]
        main_cluster = predicted_labels[cycle_result(list1)]
        if main_cluster == "Strategic Product Planning":
            list2 = [find_cosine_sim(idea_generation_embeddings, data_emebeddings),
            find_cosine_sim(market_analysis_embeddings, data_emebeddings),
            find_cosine_sim(technology_analysis_embeddings, data_emebeddings),
            find_cosine_sim(product_manangement_embeddings, data_emebeddings)]
            sub_cluster = sub_cluster0[cycle_result(list2)]
        elif main_cluster == "Product & Service Development":
            list2 = [find_cosine_sim(testing_embeddings, data_emebeddings),
                find_cosine_sim(product_design_embeddings, data_emebeddings),
                find_cosine_sim(requirements_management_embeddings, data_emebeddings)]
            sub_cluster = sub_cluster1[cycle_result(list2)]
        else:
            list2 = [find_cosine_sim(production_system_planning_embeddings, data_emebeddings),
            find_cosine_sim(production_system_implementation_embeddings, data_emebeddings)]
            sub_cluster = sub_cluster3[cycle_result(list2)]      
        main_cluster_labels.append(main_cluster)
        sub_cluster_labels.append(sub_cluster)            
    return main_cluster_labels, sub_cluster_labels

# Function to find the main cluster of a company given its keywords
def find_clusters_for_individual_company(keywords):
    data_emebeddings = model.encode(keywords)
    list1=[ find_cosine_sim(pickled_spp_embeddings, data_emebeddings),
            find_cosine_sim(pickled_pd_embeddings, data_emebeddings),
            find_cosine_sim(pickled_psd_embeddings, data_emebeddings)]
    main_cluster = predicted_labels[cycle_result(list1)]
    sub_cluster = find_sub_cluster_for_individual_company(data_emebeddings, main_cluster)
    return main_cluster, sub_cluster

# Function to find the sub-cluster of a company given its embedded webdata and tha main_cluser information
def find_sub_cluster_for_individual_company(data_emebeddings, main_cluster):
    if main_cluster == "Strategic Product Planning":
        list2 = [find_cosine_sim(idea_generation_embeddings, data_emebeddings),
        find_cosine_sim(market_analysis_embeddings, data_emebeddings),
        find_cosine_sim(technology_analysis_embeddings, data_emebeddings),
        find_cosine_sim(product_manangement_embeddings, data_emebeddings)]
        sub_cluster = sub_cluster0[cycle_result(list2)]
    elif main_cluster == "Product & Service Development":
        list2 = [find_cosine_sim(testing_embeddings, data_emebeddings),
            find_cosine_sim(product_design_embeddings, data_emebeddings),
            find_cosine_sim(requirements_management_embeddings, data_emebeddings)]
        sub_cluster = sub_cluster1[cycle_result(list2)]
    else:
        list2 = [find_cosine_sim(production_system_planning_embeddings, data_emebeddings),
            find_cosine_sim(production_system_implementation_embeddings, data_emebeddings)]
        sub_cluster = sub_cluster3[cycle_result(list2)] 
    return sub_cluster
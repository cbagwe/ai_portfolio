from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pickle

predicted_labels = ["Strategy Product Planning","Product Development", "Production System Development"]
sub_cluster0 = ["Idea Generation", "Customer Market Analysis", "Product Manangement"]
sub_cluster1 = ["Testing", "Product Design", "Requirements Management"]
sub_cluster3 = ["Process Optimization", "Maintenance"]

model = SentenceTransformer('all-MiniLM-L6-v2')

pickled_spp_embeddings = pickle.load(open('spp_embeddings.sav', 'rb'))
pickled_pd_embeddings = pickle.load(open('pd_embeddings.sav', 'rb'))
pickled_psd_embeddings = pickle.load(open('psd_embeddings.sav', 'rb'))

idea_generation_embeddings = pickle.load(open('idea_generation_embeddings.sav', 'rb'))
customer_market_analysis_embeddings = pickle.load(open('customer_market_analysis_embeddings.sav', 'rb'))
product_manangement_embeddings = pickle.load(open('product_manangement_embeddings.sav', 'rb'))

testing_embeddings = pickle.load(open('testing_embeddings.sav', 'rb'))
product_design_embeddings = pickle.load(open('product_design_embeddings.sav', 'rb'))
requirements_management_embeddings = pickle.load(open('requirements_management_embeddings.sav', 'rb'))

process_optimization_embeddings = pickle.load(open('process_optimization_embeddings.sav', 'rb'))
maintenance_embeddings = pickle.load(open('maintenance_embeddings.sav', 'rb'))

def find_cosine_sim(vector1,vector2):
    return(cosine_similarity(vector1.reshape(1, -1),vector2.reshape(1, -1))[0][0])

def cycle_result(list1):
    maximum = max(list1)
    return list1.index(maximum)

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
        if main_cluster == "Strategy Product Planning":
            list2 = [find_cosine_sim(idea_generation_embeddings, data_emebeddings),
            find_cosine_sim(customer_market_analysis_embeddings, data_emebeddings),
            find_cosine_sim(product_manangement_embeddings, data_emebeddings)]
            sub_cluster = sub_cluster0[cycle_result(list2)]
        elif main_cluster == "Product Development":
            list2 = [find_cosine_sim(testing_embeddings, data_emebeddings),
                find_cosine_sim(product_design_embeddings, data_emebeddings),
                find_cosine_sim(requirements_management_embeddings, data_emebeddings)]
            sub_cluster = sub_cluster1[cycle_result(list2)]
        else:
            list2 = [find_cosine_sim(process_optimization_embeddings, data_emebeddings),
                find_cosine_sim(maintenance_embeddings, data_emebeddings)]
            sub_cluster = sub_cluster3[cycle_result(list2)]      
        main_cluster_labels.append(main_cluster)
        sub_cluster_labels.append(sub_cluster)            
    return main_cluster_labels, sub_cluster_labels
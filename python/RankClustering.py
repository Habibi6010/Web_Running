import joblib
import os
import numpy as np
import pandas as pd
from scipy.fftpack import fft
class RankClustering:
    models_folder = "ClusterModels/"
    art_model = None
    pca_transform = None
    normalization_transform = None

    def __init__(self, data: dict):
        # Initialize with data dictionary
        gender = data.get('gender', 'men')
        season = data.get('season', 'outdoor')
        category = data.get('category', 'NCAA Div I')
        event = data.get('event', '100m')
        # Make model path
        path_seleceted_model = f"{self.models_folder}{gender}/{event}/{season}"
        # print(f"Model path: {self.path_seleceted_model}")
        # Load models
        art_model_path = f"{path_seleceted_model}/art_{season}.pkl"
        pca_transform_path = f"{path_seleceted_model}/pca_transform_{season}.pkl"
        normalization_transform_path = f"{path_seleceted_model}/normalization_transform_{season}.pkl"
        self.pca_transform = self.load_model(pca_transform_path)
        self.normalization_transform = self.load_model(normalization_transform_path)
        self.art_model = self.load_model(art_model_path)
        
    def load_model(self, path: str):
        if os.path.exists(path):
            with open(path, 'rb') as file:
                model = joblib.load(file)
                print(f"Loaded model from {path}")
                return model
        else:
            print(f"Model file not found: {path}")
            return None
    
    def predict_cluster(self,scores: list):
        if not self.art_model or not self.pca_transform or not self.normalization_transform:
            print("One or more models are not loaded properly.")
            return None
        
        if len(scores) < 5:
            print(f"Lenght Scores provided for prediction: {len(scores)}")
            print("No enough scores provided for prediction.")
            return None
        
        # Reshape scores for processing
        scores_array = np.array(scores)
        best_score = np.min(scores_array)
        avg_score = np.mean(scores_array)
        var_score = np.var(scores_array)
        cv= np.std(scores_array)/np.mean(scores_array) if np.mean(scores_array)!=0 else 0
        mean_fft = fft(scores_array).real.mean()
        test_df = pd.DataFrame({'200m_best_score_indoor': [best_score],
                        '200m_avg_score_indoor': [avg_score],
                        '200m_var_score_indoor': [var_score],
                        '200m_mean_fft_indoor': [mean_fft],
                        '200m_cv_indoor': [cv]})
        # Normalize the data
        normalized_data = self.normalization_transform.transform(test_df)
        # Apply PCA transformation
        pca_data = self.pca_transform.transform(normalized_data)
        pca_data_df = pd.DataFrame(pca_data, columns=[f'PC{i+1}' for i in range(pca_data.shape[1])])
        # Predict cluster using ART2 model
        test_label=[]
        for index,row in pca_data_df.iterrows():
            self.art_model.set_train_mode(False)
            test_label.append([self.art_model.find_label(row)+1,float(row.values[0])])  
        return test_label
    
class ART2:
    # Initialize ART2 parameters
    def __init__(self, max_clusters, vigilance_threshold,train_mode=True, do_normalization=False):
        self.max_clusters = max_clusters
        self.vigilance_threshold = vigilance_threshold
        self.cluster_centers = []
        self.do_normalization = do_normalization
        self.cluster_sample = {}
        self.train_mode = train_mode

    def set_train_mode(self, train_mode):
        self.train_mode = train_mode

    # calculate Manhattan distance
    def manhattan_distance(self, vector1, vector2):
        return np.sum(np.abs(vector1 - vector2))

    # normalize the vector
    def normalize(self, vector):
        return np.array(vector / np.linalg.norm(vector))

    # find closest cluster center to vector
    def find_closest_cluster_center(self, vector):
        min_distance = float('inf')
        closest_center = None
        for center in self.cluster_centers:
            distance = self.manhattan_distance(center,vector)
            if distance < min_distance:
                min_distance = distance
                closest_center = center
        return closest_center, min_distance

    # find label for input x
    def find_label(self, x):
        x = np.array(x)
        if self.do_normalization:
            x = self.normalize(x)
        if len(self.cluster_centers) == 0:
            self.cluster_centers.append(x)
            self.cluster_sample[0]=list(x)
            return 0
        else:
            closest_center, distance = self.find_closest_cluster_center(x)
            if distance < self.vigilance_threshold:
                # Find the index using np.allclose
                index = next(i for i, center in enumerate(self.cluster_centers) if np.allclose(center, closest_center))
                # calculate number of sample belong to that cluster
                n = len(self.cluster_sample[index])

                # Update the cluster center
                self.cluster_centers[index] = ((n *self.cluster_centers[index]) + x)/ (n+1)
                self.cluster_sample[index].append(list(x))

                return index
            else:
                if len(self.cluster_centers) < self.max_clusters and self.train_mode:
                    self.cluster_centers.append(x)
                    self.cluster_sample[len(self.cluster_centers)-1]=list(x)
                    return len(self.cluster_centers) - 1
                else:
                    # print("Maximum number of clusters reached. Cannot classify new input.")
                    return -1


if __name__ == "__main__":
    # Example usage
    data = {"gender":"women","season":"indoor","event":"400m"}
    scores = [52.5, 51.3, 50.7, 49.9, 49.5, 48.7, 48.2]
    rc = RankClustering(data)
    cluster = rc.predict_cluster(scores)
    print(f"Predicted cluster: {cluster}")

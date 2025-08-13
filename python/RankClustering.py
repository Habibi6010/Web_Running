import joblib
import os
import numpy as np
import pandas as pd
from scipy.fftpack import fft
import json,io, base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid GUI issues
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.cm as cm


class RankClustering:
    models_folder = "ClusterModels/"
    plot_output_folder = "static/plots/"
    plot_output_folder_comparison_same = "static/plots/plots_comparison_same/"
    plot_output_folder_comparison_individual = "static/plots/plots_comparison_individual/"
    path_seleceted_model = None
    art_model = None
    pca_transform = None
    normalization_transform = None
    boxplot_summary = None
    def __init__(self, data: dict):
        # Initialize with data dictionary
        gender = data.get('gender', 'men')
        season = data.get('season', 'outdoor')
        category = data.get('category', 'NCAA Div I')
        event = data.get('event', '100m')
        # Make model path
        self.path_seleceted_model = f"{self.models_folder}{gender}/{event}/{season}"
        # print(f"Model path: {self.path_seleceted_model}")
        # Load models
        art_model_path = f"{self.path_seleceted_model}/art.pkl"
        pca_transform_path = f"{self.path_seleceted_model}/pca_transform.pkl"
        normalization_transform_path = f"{self.path_seleceted_model}/normalization_transform.pkl"
        self.pca_transform = self.load_model(pca_transform_path)
        self.normalization_transform = self.load_model(normalization_transform_path)
        self.art_model = self.load_model(art_model_path)
        # Load the summary statistics
        with open(f"{self.path_seleceted_model}/boxplot_summary.json", "r") as f:
            self.boxplot_summary = json.load(f)
            print(f"Loaded boxplot summary")


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
        test_df = pd.DataFrame({'best_score': [best_score],
                        'avg_score': [avg_score],
                        'var_score': [var_score],
                        'mean_fft': [mean_fft],
                        'cv': [cv]})
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
    
    def draw_boxpolt(self,predicte_label, plot_name="ranking_boxplot.png",plot_title = "Ranking Prediction",is_comparison=False):
        fig, ax = plt.subplots(figsize=(10, 6))

        # Colors and labels
        box_color = (0.2, 0.4, 0.8, 0.2)         # more transparent blue
        line_color = (0, 0, 0, 1)               # semi-transparent black for lines
        outlier_color = (0.8, 0.2, 0.2, 0.6)      # semi-transparent red
        median_color = (0.8, 0.2, 0.2, 0.7)        # red for median line
        predict_color = (0.2, 0.8, 0.2, 0.6)       # semi-transparent green for predicted cluster

        labels = ['A', 'B', 'C', 'D', 'E']
        
        
        positions = list(range(len(self.boxplot_summary)))

        for stat, pos in zip(self.boxplot_summary, positions):
            q1 = stat["q1"]
            median = stat["median"]
            q3 = stat["q3"]
            low = stat["whisker_low"]
            high = stat["whisker_high"]
            outliers = stat["outliers"]

            # Draw box
            rect = Rectangle((pos - 0.3, q1), 0.6, q3 - q1, facecolor=box_color, edgecolor=line_color, linewidth=1.2)
            ax.add_patch(rect)

            # Median line
            ax.plot([pos - 0.3, pos + 0.3], [median, median], color=median_color, linewidth=1)

            # Whiskers
            ax.plot([pos, pos], [low, q1], color=line_color, linewidth=1)
            ax.plot([pos, pos], [q3, high], color=line_color, linewidth=1)

            # Whisker caps
            ax.plot([pos - 0.1, pos + 0.1], [low, low], color=line_color, linewidth=1)
            ax.plot([pos - 0.1, pos + 0.1], [high, high], color=line_color, linewidth=1)

            # Outliers
            # ax.plot([pos] * len(outliers), outliers, 'o', color=outlier_color, markersize=4)
            

        # Final formatting
        ax.set_xticks(positions)
        ax.set_xticklabels(labels)
        ax.set_yticks([])
        ax.set_ylabel("")
        ax.set_xlabel("Performance Clusters", fontsize=12)
        ax.set_title(plot_title, fontsize=16)
        ax.grid(True)

        # Highlight predicted cluster
        if predicte_label and predicte_label[0][0] != -1:
            pred_cluster = predicte_label[0][0]
            pred_value = predicte_label[0][1]
            ax.plot([pred_cluster], [pred_value], 'o', color=predict_color, markersize=12, label='Predicted Cluster')
        # invert y-axis
        ax.invert_yaxis()

        if not is_comparison:
            os.makedirs(self.plot_output_folder, exist_ok=True)
            file_path = os.path.join(self.plot_output_folder, plot_name)
        else:
            os.makedirs(self.plot_output_folder_comparison_individual, exist_ok=True)
            file_path = os.path.join(self.plot_output_folder_comparison_individual, plot_name)
        # Save the plot
        plt.savefig(file_path, format='png', bbox_inches='tight')
        plt.close()
        return file_path
    
    def draw_boxplot_comparison_same_season_evet_category_gender(self, predict_name_lable_dict, plot_name="boxplot_comparison.png", plot_title = "Comparison of Runners"):
        fig, ax = plt.subplots(figsize=(10, 6))

        # Colors and labels
        box_color = (0.2, 0.4, 0.8, 0.2)         # more transparent blue
        line_color = (0, 0, 0, 1)               # semi-transparent black for lines
        outlier_color = (0.8, 0.2, 0.2, 0.6)      # semi-transparent red
        median_color = (0.8, 0.2, 0.2, 0.7)        # red for median line

        labels = ['A', 'B', 'C', 'D', 'E']
        positions = list(range(len(self.boxplot_summary)))

        for stat, pos in zip(self.boxplot_summary, positions):
            q1 = stat["q1"]
            median = stat["median"]
            q3 = stat["q3"]
            low = stat["whisker_low"]
            high = stat["whisker_high"]
            outliers = stat["outliers"]

            # Draw box
            rect = Rectangle((pos - 0.3, q1), 0.6, q3 - q1, facecolor=box_color, edgecolor=line_color, linewidth=1.2)
            ax.add_patch(rect)

            # Median line
            ax.plot([pos - 0.3, pos + 0.3], [median, median], color=median_color, linewidth=1)

            # Whiskers
            ax.plot([pos, pos], [low, q1], color=line_color, linewidth=1)
            ax.plot([pos, pos], [q3, high], color=line_color, linewidth=1)

            # Whisker caps
            ax.plot([pos - 0.1, pos + 0.1], [low, low], color=line_color, linewidth=1)
            ax.plot([pos - 0.1, pos + 0.1], [high, high], color=line_color, linewidth=1)

            # Outliers
            # ax.plot([pos] * len(outliers), outliers, 'o', color=outlier_color, markersize=4)
            
        # Runner predictions
        runner_names = [item["name"] for item in predict_name_lable_dict]
        color_map = cm.get_cmap('tab10', len(runner_names))  # Use 'tab10' colormap for up to 10 unique runners
        for idx, pred_data in enumerate(predict_name_lable_dict):
            name = pred_data["name"]
            pred_label = pred_data["predict_info"]

            if pred_label and pred_label[0][0] != -1:
                cluster_id = pred_label[0][0]
                cluster_value = pred_label[0][1]
                ax.scatter(cluster_id, cluster_value, s=100, color=color_map(idx), label=name, edgecolors='black')

        # Final formatting
        ax.set_xticks(positions)
        ax.set_xticklabels(labels)
        ax.set_yticks([])
        ax.set_ylabel("")
        ax.set_xlabel("Performance Clusters", fontsize=12)
        ax.set_title(plot_title, fontsize=16)
        ax.grid(True)
        ax.legend(title="Runner Predictions", bbox_to_anchor=(1.05, 1), loc='upper left')
        # invert y-axis
        ax.invert_yaxis()
        # Save the plot        
        os.makedirs(self.plot_output_folder_comparison_same, exist_ok=True)
        file_path = os.path.join(self.plot_output_folder_comparison_same, plot_name)
        plt.savefig(file_path, format='png', bbox_inches='tight')
        plt.close()
        return file_path    


    def get_cluster_summary(self):
        df = pd.read_csv(f"{self.path_seleceted_model}/class_summary.csv")
        # print(f"Cluster summary:\n{df.columns}")
        df_selected = df[['Cluster', 'Max Best Score', 'Min Best Score', 'Mean Best', 'Max Avg','Min Avg', 'Mean Avg']]
        # Map cluster numbers to letters
        cluster_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
        df_selected['Cluster'] = df_selected['Cluster'].map(cluster_map)
        df_selected = df_selected.round(2)
        return df_selected


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
                    if self.train_mode:
                        print("Maximum number of clusters reached. Cannot classify new input.")
                        return -1
                    else:
                        # If not in training mode, return the closest cluster index
                        return len(self.cluster_centers)-1 if self.cluster_centers else self.max_clusters


if __name__ == "__main__":
    # Example usage
    data = {"gender":"women","season":"indoor","event":"400m"}
    scores = [52.5, 51.3, 50.7, 49.9, 49.5, 48.7, 48.2]
    rc = RankClustering(data)
    cluster = rc.predict_cluster(scores)
    print(f"Predicted cluster: {cluster}")
    ax = rc.darw_boxpolt(cluster)


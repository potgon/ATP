from utils.config import SNR_PRICE_RANGE, SNR_BREAKOUT_FACTOR
from utils.logger import make_log


class SNRDetector:
    def __init__(self, data):
        self.data = data
        self.price_range_threshold = SNR_PRICE_RANGE
        self.breakout_factor = SNR_BREAKOUT_FACTOR

    def detect_clusters(self):
        make_log("CLUSTER", 20, "clusters.log", "Initializing cluster variables")
        clusters = []
        current_cluster = []
        in_cluster = False
        cluster_max_price = cluster_min_price = None

        make_log("CLUSTER", 20, "clusters.log", "Starting iteration")
        for index, row in self.data.iterrows():
            if not in_cluster:
                make_log("CLUSTER", 20, "clusters.log", "Not in cluster")
                in_cluster = True
                cluster_max_price = cluster_min_price = row["Close"]
                current_cluster = [row]
            else:
                make_log(
                    "CLUSTER", 20, "clusters.log", "In cluster, setting price range"
                )
                cluster_max_price = max(cluster_max_price, row["Close"])
                cluster_min_price = min(cluster_min_price, row["Close"])

                if self.is_breakout(row["Close"], cluster_max_price, cluster_min_price):
                    make_log("CLUSTER", 20, "clusters.log", "Breakout detected")
                    clusters.append(current_cluster)
                    in_cluster = False
                    current_cluster = []
                else:
                    make_log("CLUSTER", 20, "clusters.log", "Cluster appended")
                    current_cluster.append(row)
        return clusters

    def is_breakout(self, current_price, cluster_max, cluster_min):
        range_size = cluster_max - cluster_min
        upper_bound = cluster_max + range_size * self.breakout_factor
        lower_bound = cluster_min - range_size * self.breakout_factor
        return current_price > upper_bound or current_price < lower_bound

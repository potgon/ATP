from utils.logger import make_log


class SNRDetector:
    def __init__(self, fetcher):
        self.fetcher = fetcher

    def close_cluster(self, cluster, min_cluster_size):
        if len(cluster) >= min_cluster_size:
            make_log("CLUSTER", 10, "workflow.log", f"Cluster detected: {cluster}")

    def detect_cluster(self):
        with self.fetcher.data_lock:
            data = self.fetcher.current_data.copy()

        cluster_threshold = 0.5
        min_cluster_size = 3

        cluster_start = None
        current_cluster = []
        current_average = 0

        for index, row in data.iterrows():
            sign_change = row["Sign Change"]

            if index == 0:
                continue

            if sign_change == 0:
                if cluster_start is not None:
                    current_cluster.append(row["Close"])

                    current_timestamp = row.name.to_pydatetime()
                    previous_timestamp = data.index[index - 1].to_pydatetime()

                    timestamp_diff = (
                        current_timestamp - previous_timestamp
                    ).total_seconds()

                    current_average = (
                        current_average * len(current_cluster) + abs(timestamp_diff)
                    ) / (len(current_cluster) + 1)

                    if current_average > cluster_threshold:
                        self.close_cluster(current_cluster, min_cluster_size)
                        cluster_start = None
                        current_cluster = []
                        current_average = 0
            elif abs(sign_change) == 2:
                if cluster_start is not None:
                    self.close_cluster(current_cluster, min_cluster_size)

                cluster_start = row["Close"]
                current_cluster = [cluster_start]
                current_average = 0
            else:
                self.close_cluster(current_cluster, min_cluster_size)
                cluster_start = None
                current_cluster = []
                current_average = 0

        self.close_cluster(current_cluster, min_cluster_size)

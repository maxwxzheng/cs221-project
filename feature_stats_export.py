from collections import Counter
import csv
import json


def export_stats_for_file(data_file, csv_filename, features_counter_csv_filename):
    data = json.load(open(data_file))
    with open(csv_filename, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['rating', 'feature_count', 'features'])
        for id, features in data.iteritems():
            csv_writer.writerow([
                id,
                features['rating'],
                len(features['features'])
            ])

    with open(features_counter_csv_filename, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['feature', 'count'])
        counter = Counter([])
        for id, features in data.iteritems():
            for feature_key in features['features'].keys():
                counter[feature_key] += 1

        feature_index = 0
        for feature_key, feature_count in counter.iteritems():
            feature_index += 1
            csv_writer.writerow([
                "feature_%s" % feature_index,
                feature_count
            ])

export_stats_for_file('data/features_with_cross.json', "data/features_with_cross_stats.csv", "data/features_counter_with_cross_stats.csv")
export_stats_for_file('data/features_without_cross.json', "data/features_without_cross_stats.csv", "data/features_counter_without_cross_stats.csv")
import pandas as pd
import json

from Extract_features.ExtractFeatures import getDomain
from Extract_features.ExtractFeatures_NamLe import getTLD
from Environment.path import extracted_url_dataset_csv

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)

input1 = extracted_url_dataset_csv

# Load CSV
data1 = pd.read_csv(input1)
data1['domain'] = data1['url'].apply(getDomain)
data1['tld'] = data1['url'].apply(getTLD)
data1 = data1
print(data1.head())

documents = []
for _, row in data1.iterrows():
    document = {
        "url": row["url"],
        "domain": row["domain"],
        "features": {
            "url_length": row["url_length"],
            "hostname_length": row["hostname_length"],
            "count-www": row["count-www"],
            "count-https": row["count-https"],
            "count-http": row["count-http"],
            "count.": row["count."],
            "count%": row["count%"],
            "count?": row["count?"],
            "count-": row["count-"],
            "count=": row["count="],
            "count@": row["count@"],
            "count_dir": row["count_dir"],
            "count_embed_domain": row["count_embed_domian"],
            "short_url": row["short_url"],
            "fd_length": row["fd_length"],
            "tld": row["tld"],
            "tld_length": row["tld_length"],
            "sus_url": row["sus_url"],
            "count-digits": row["count-digits"],
            "count-letters": row["count-letters"],
            "abnormal_url": row["abnormal_url"],
            "use_of_ip_address": row["use_of_ip_address"],
            "google_index": row["google_index"]
        }
    }
    documents.append(document)

with open("mali_urls.json", "w") as f:
    json.dump(documents, f, indent=4)

print("JSON file created successfully!")

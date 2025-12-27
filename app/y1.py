import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- PART 1: SALES DATA ANALYSIS --- #
# Creating the Sales DataFrame
data = {
    "2014": [100.5, 150.8, 200.9, 30000, 40000],
    "2015": [12000, 18000, np.nan, 30000, 45000],
    "2016": [20000, 50000, 70000, 100000, np.nan],
    "2017": [50000, 60000, 70000, 80000, 90000]
}
sales_df = pd.DataFrame(data, index=["Madhu", "Kasam", "Kin", "Ankit", "Shruti"])

# a. Finding total NaN values
total_nan = sales_df.isna().sum().sum()
print(f"Total NaN values in dataset: {total_nan}")

# b. Replace NaN in '2015' column with previous value
sales_df["2015"] = sales_df["2015"].ffill()

# c. Predict sales for 2018 (10% increase)
sales_df["2018"] = sales_df["2017"] * 1.10

# Pie Chart: Sales distribution in 2018
plt.figure(figsize=(6,6))
plt.pie(sales_df["2018"], labels=sales_df.index, autopct='%1.1f%%', startangle=140)
plt.title("Sales Distribution in 2018")
plt.show()





## ans 2

import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
import pandas as pd

# Load the dataset
file_path = "FP_growth__Market_Basket_Optimisation.csv"
df = pd.read_csv(file_path, header=None)

# Convert dataset into a list of transactions
transactions = df.apply(lambda row: row.dropna().tolist(), axis=1).tolist()

# Step 1: Build Frequency Table
def get_frequency_table(transactions, min_support):
    frequency = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            frequency[item] += 1
    return {k: v for k, v in frequency.items() if v >= min_support}

# Step 2: Build FP-Tree
class FPTreeNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.link = None  # Used for header table links

    def increment(self, count):
        self.count += count

def build_fp_tree(transactions, min_support):
    frequency_table = get_frequency_table(transactions, min_support)
    if not frequency_table:
        return None, None

    # Sorting items in each transaction by frequency
    sorted_transactions = []
    for transaction in transactions:
        sorted_items = [item for item in transaction if item in frequency_table]
        sorted_items.sort(key=lambda x: frequency_table[x], reverse=True)
        sorted_transactions.append(sorted_items)

    root = FPTreeNode(None, 1, None)
    header_table = {}

    # Insert transactions into FP-Tree
    for transaction in sorted_transactions:
        current_node = root
        for item in transaction:
            if item in current_node.children:
                current_node.children[item].increment(1)
            else:
                new_node = FPTreeNode(item, 1, current_node)
                current_node.children[item] = new_node

                if item in header_table:
                    last_node = header_table[item]
                    while last_node.link:
                        last_node = last_node.link
                    last_node.link = new_node
                else:
                    header_table[item] = new_node

            current_node = current_node.children[item]

    return root, header_table

# Step 3: Mine Frequent Patterns
def find_prefix_paths(base_node):
    conditional_patterns = []
    node_counts = []
    while base_node:
        path = []
        parent = base_node.parent
        while parent and parent.item:
            path.append(parent.item)
            parent = parent.parent
        if path:
            conditional_patterns.append(path)
            node_counts.append(base_node.count)  # Store counts separately
        base_node = base_node.link
    return conditional_patterns, node_counts

def mine_fp_tree(header_table, min_support):
    frequent_patterns = {}

    for item in header_table:
        conditional_patterns, node_counts = find_prefix_paths(header_table[item])
        frequent_patterns[(item,)] = sum(node_counts)  # Fixed sum issue

        conditional_tree, conditional_header = build_fp_tree(conditional_patterns, min_support)
        if conditional_tree:
            sub_patterns = mine_fp_tree(conditional_header, min_support)
            for pattern, count in sub_patterns.items():
                frequent_patterns[tuple(sorted(pattern + (item,)))] = count  # Fixed tuple concatenation issue

    return frequent_patterns

# Step 4: Generate Association Rules
def generate_association_rules(frequent_patterns, min_confidence):
    rules = []
    for itemset in frequent_patterns.keys():
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    consequent = tuple(sorted(set(itemset) - set(antecedent)))
                    if antecedent and consequent:
                        antecedent_support = frequent_patterns.get(antecedent, 0)  # Get support safely
                        if antecedent_support > 0:  # Prevent division by zero
                            confidence = frequent_patterns[itemset] / antecedent_support
                            if confidence >= min_confidence:
                                rules.append((antecedent, consequent, frequent_patterns[itemset], confidence))
    return rules

# Run FP-Growth Algorithm
min_support = 20  # Adjust based on dataset
min_confidence = 0.5

fp_root, header_table = build_fp_tree(transactions, min_support)
frequent_patterns = mine_fp_tree(header_table, min_support)
rules = generate_association_rules(frequent_patterns, min_confidence)

# Display Frequent Itemsets
print("\nFrequent Itemsets:")
for pattern, support in frequent_patterns.items():
    print(f"{pattern}: {support}")

# Display Association Rules
print("\nAssociation Rules:")
for antecedent, consequent, support, confidence in rules:
    print(f"{antecedent} => {consequent} (Support: {support}, Confidence: {confidence:.2f})")

# Step 5: Scatter Plot (Support vs Confidence)
supports = [support for _, _, support, _ in rules]
confidences = [confidence for _, _, _, confidence in rules]

plt.figure(figsize=(8, 6))
plt.scatter(supports, confidences, color="blue", alpha=0.6)
plt.xlabel("Support")
plt.ylabel("Confidence")
plt.title("Support vs Confidence Scatter Plot")
plt.grid()
plt.show()

import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_chart(data):
    df = pd.DataFrame(data)
    names = df['name'].to_list()
    success_counts = df['success'].to_list()
    no_success_counts = df['no_success'].to_list()
    x = np.arange(len(names))
    width = 0.35
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width / 2, success_counts, width, label="Ko'tarilgan qo'ng'iroqlar", color='skyblue',
                    edgecolor='grey')
    rects2 = ax.bar(x + width / 2, no_success_counts, width, label="Ko'tarilmagan qo'ng'iroqlar", color='salmon',
                    edgecolor='grey')

    ax.set_xlabel('Xodimlar', fontsize=12, fontweight='bold')
    ax.set_ylabel("Qo'ng'iroqlar soni", fontsize=12, fontweight='bold')
    ax.set_title("Ko'tarilgan va ko'tarilmagan qo'ng'iroqlar xodimlar kesimida", fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=10, fontweight='medium')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    fig.tight_layout()

    for rect in rects1 + rects2:
        height = rect.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='medium')

    plt.savefig('calls.png', dpi=300)

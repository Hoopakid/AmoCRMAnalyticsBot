import matplotlib.pyplot as plt
import numpy as np


def plot_chart(data):
    names = [item['name'] for item in data]
    success_counts = [item['success'] for item in data]
    no_success_counts = [item['no_success'] for item in data]

    x = np.arange(len(names))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, success_counts, width, label="Ko'tarilgan qo'ng'iroqlar")
    rects2 = ax.bar(x + width / 2, no_success_counts, width, label="Ko'tarilmagan qo'ng'iroqlar")

    ax.set_xlabel('Xodimlar')
    ax.set_ylabel("Qo'ng'iroqlar soni")
    ax.set_title("Ko'tarilgan va ko'tarilmagan qo'ng'iroqlar xodimlar kesimida")
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.legend()

    fig.tight_layout()
    plt.xticks(rotation=45, ha='right')
    plt.savefig('calls_chart.png')

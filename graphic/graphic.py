from collections import OrderedDict

import seaborn as sns
import matplotlib.pyplot as plt
from generator import run


def create_graphic():
    yes, no, yes_without_ans, index_base_arr, max_code_smell_base, gpt_bad_smells = run("gpt_data")
    ordered_dict = OrderedDict(sorted(gpt_bad_smells.items(), key=lambda x: x[1], reverse=True))
    ax = sns.barplot(x=list(ordered_dict.keys())[:9], y=list(ordered_dict.values())[:9])
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    plt.xlabel('BAD SMELL')
    plt.ylabel('QUANTIDADE')
    plt.title('TOTAL, POR TIPO, DE BADSMELLS IDENTIFICADO PELO GPT')
    plt.show()


if __name__ == '__main__':
    create_graphic()

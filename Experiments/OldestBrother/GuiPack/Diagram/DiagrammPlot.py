import matplotlib.pyplot as plt
from Experiments.OldestBrother.GuiPack.Interface import child_house
import math

child_h = child_house
label_values = {}
for i in child_h.get_value_family():
    if i[0] == 1:
        label_values["Семьи с 1 ребенком"] = i[1]
    else:
        label_values[f"Семьи с {i[0]} детьми"] = i[1]

values_family = tuple(label_values.values())
labels_family = tuple(label_values.keys())

child_items = child_h.get_child_distribution()
label_child = tuple(child_items.keys())
values_child = tuple(child_items.values())


def get_pie(values, labels):
    fig, ax = plt.subplots(figsize=(4, 5))
    colors = ["yellow", "red", "blue", "green", "black"]
    wedges, _ = ax.pie(
        values,
        labels=None,  # отключаем подписи на секторах
        startangle=90,
        colors=colors,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
    )

    box = ax.get_position()  # текущая позиция: Bbox(x0, y0, x1, y1)
    ax.set_position([box.x0, box.y0 + 0.17, box.width, box.height * 1])

    # создаём легенду с процентами
    total = sum(values)
    legend_labels = [f"{label} — {value} ({value / total * 100:.1f}%)"
                     for label, value in zip(labels, values)]

    ax.legend(
        wedges, legend_labels,
        title="Сектора",
        loc="lower center",
        bbox_to_anchor=(0.5, -0.5),
        ncol=1
    )

    ax.axis('equal')  # круг
    plt.show()


get_pie(values=values_child, labels=label_child)

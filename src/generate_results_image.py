import os
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy.control as ctrl


def generate_report_images():
    os.makedirs("../results", exist_ok=True)

    error = ctrl.Antecedent(np.arange(-100, 101, 1), "Error (RPM)")
    delta_error = ctrl.Antecedent(np.arange(-50, 51, 1), "Delta Error (RPM/s)")
    voltage_change = ctrl.Consequent(
        np.arange(-0.5, 0.51, 0.01), "Voltage Change (V)"
    )

    names = ["NB", "NS", "ZE", "PS", "PB"]
    error.automf(names=names)
    delta_error.automf(names=names)
    voltage_change.automf(names=names)

    fig, ax = plt.subplots(figsize=(8, 4))
    error.view(sim=None, ax=ax)
    ax.set_title("Membership Functions - Error (RPM)", fontweight="bold")
    plt.tight_layout()
    plt.savefig("../results/mf_error.png", dpi=300)
    plt.close()

    fig, ax = plt.subplots(figsize=(8, 4))
    delta_error.view(sim=None, ax=ax)
    ax.set_title("Membership Functions - Delta Error (RPM/s)", fontweight="bold")
    plt.tight_layout()
    plt.savefig("../results/mf_delta_error.png", dpi=300)
    plt.close()

    fig, ax = plt.subplots(figsize=(8, 4))
    voltage_change.view(sim=None, ax=ax)
    ax.set_title("Membership Functions - Voltage Change (V)", fontweight="bold")
    plt.tight_layout()
    plt.savefig("../results/mf_voltage_change.png", dpi=300)
    plt.close()

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.axis("off")

    rules = [
        ["NB", "NB", "NB", "NS", "ZE"],
        ["NB", "NS", "NS", "ZE", "PS"],
        ["NS", "NS", "ZE", "PS", "PS"],
        ["NS", "ZE", "PS", "PB", "PB"],
        ["ZE", "PS", "PB", "PB", "PB"],
    ]

    cols = ["de: NB", "de: NS", "de: ZE", "de: PS", "de: PB"]
    rows = ["e: NB", "e: NS", "e: ZE", "e: PS", "e: PB"]

    colors = {
        "NB": "#ff9999",
        "NS": "#ffcc99",
        "ZE": "#ffffcc",
        "PS": "#cce5ff",
        "PB": "#99ccff",
    }

    table = ax.table(
        cellText=rules,
        rowLabels=rows,
        colLabels=cols,
        loc="center",
        cellLoc="center",
    )

    table.scale(1, 2.5)
    table.set_fontsize(12)

    for (i, j), cell in table.get_celld().items():
        if i == 0 or j == -1:
            cell.set_facecolor("#e6e6e6")
            cell.get_text().set_weight("bold")
        else:
            text = cell.get_text().get_text()
            if text in colors:
                cell.set_facecolor(colors[text])
                cell.get_text().set_weight("bold")

    plt.title(
        "Fuzzy Inference Matrix (Error × ΔError → Voltage)",
        fontweight="bold",
        pad=15,
    )
    plt.tight_layout()
    plt.savefig("../results/rule_table.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("Images successfully generated in '../results/'")


if __name__ == "__main__":
    generate_report_images()
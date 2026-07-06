import math
import tkinter as tk
from tkinter import ttk, messagebox

# https://rateyourmusic.com/~Networking
# very much assisted by GPT
# sonic density = S
# structural unity = G
# enjoyability = X
# lyrical performance = L
# vocal performance = W
# S, G, X, L, W ∈ [0, 1]
# heteronomy = H
# H ∈ (0, 1]

def clamp(x, low, high):
    return max(low, min(high, x))


def compute_Q(S, G, X, L, W):
    """
    S, G, X, L, W ∈ [0, 1]

    원래 Q:
    S^1.3 + G^1.1 + X + (L+W)^0.75

    최대값:
    1 + 1 + 1 + 2^0.75
    """
    raw_Q = S**1.3 + G**1.1 + X + (L + W)**0.75
    max_Q = 3 + 2**0.75

    normalized_Q = raw_Q / max_Q
    scaled_Q = normalized_Q * 5

    return scaled_Q


def compute_rating(S, G, X, L, W, H):
    """
    H ∈ [0, 1]
    Heteronomy는 감점항.

    Q가 높고 H가 낮을수록 평점 상승.
    """
    Q = compute_Q(S, G, X, L, W)

    penalty = H * 2.0
    effective_score = Q - penalty

    if effective_score <= 0:
        return Q, effective_score, 0.5, "anti-object / valueless"

    rating = 5 * (effective_score / 5) ** 0.85
    rating = clamp(rating, 0.5, 5.0)

    return Q, effective_score, rating, ontology_zone(rating)


def ontology_zone(x):
    if x < 1.5:
        return "arbitrary object"
    elif x < 2.5:
        return "structured object"
    elif x < 3.3:
        return "unified object"
    elif x < 4.0:
        return "luminous object"
    elif x < 4.6:
        return "exceptional object"
    else:
        return "dimensional object"


def calculate():
    try:
        values = {}

        for key, entry in entries.items():
            value = float(entry.get())

            if not (0 <= value <= 1):
                raise ValueError(f"{key} must be between 0 and 1.")

            values[key] = value

        Q, effective, rating, ontology = compute_rating(
            values["S"],
            values["G"],
            values["X"],
            values["L"],
            values["W"],
            values["H"]
        )

        result_text.set(
            f"Q = {Q:.4f} / 5\n"
            f"Effective Score = {effective:.4f}\n"
            f"Final Rating = {rating:.4f} / 5\n"
            f"Ontology = {ontology}"
        )

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


root = tk.Tk()
root.title("Rating System")
root.geometry("460x560")
root.resizable(False, False)

title = ttk.Label(
    root,
    text="Rating Calculator",
    font=("Arial", 16, "bold")
)
title.pack(pady=18)

subtitle = ttk.Label(
    root,
    text="All values must be between 0 and 1.",
    font=("Arial", 10)
)
subtitle.pack(pady=2)

frame = ttk.Frame(root)
frame.pack(pady=18)

labels = {
    "S": "Sonic Density",
    "G": "Structural Unity",
    "X": "Enjoyability",
    "L": "Lyrical Performance",
    "W": "Vocal Performance",
    "H": "Heteronomy"
}

entries = {}

for i, (key, label) in enumerate(labels.items()):
    ttk.Label(frame, text=f"{label} ({key})").grid(
        row=i,
        column=0,
        padx=12,
        pady=9,
        sticky="w"
    )

    entry = ttk.Entry(frame, width=16)
    entry.grid(row=i, column=1, padx=12, pady=9)
    entry.insert(0, "0.5")

    entries[key] = entry

button = ttk.Button(root, text="Calculate", command=calculate)
button.pack(pady=15)

result_text = tk.StringVar()
result_label = ttk.Label(
    root,
    textvariable=result_text,
    font=("Arial", 12),
    justify="left"
)
result_label.pack(pady=20)

root.mainloop()

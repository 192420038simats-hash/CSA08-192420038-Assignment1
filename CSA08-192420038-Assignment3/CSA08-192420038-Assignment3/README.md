# CSA0806 – Python Programming | Assignment 3 (CO3)
## Data structures: lists, tuples, dictionaries, sets, comprehensions and nested data

- Name: Dhatri
- Register number: 192420038
- Course: CSA0806 – Python Programming
- Python version: 3.12
- Libraries: standard library only; `matplotlib` 3.10 only for `Q4/venn.py` (see `requirements.txt`)
- GitHub repository name: `CSA08-192420038-Assignment3`

Run every program from inside its own folder (`cd Q3`, then the command shown).

| Question | Run | Result in one line |
|---|---|---|
| Q1 Lists, rainfall | `python rainfall.py`, `python measure.py`, `python alternatives.py` | 52 weekly totals; running sum needs n−1 additions against 6(n−6) for the naive method |
| Q2 Tuples, copying | `python complete_code.py` (TODO 1), `python busstops.py`, `python measure.py` | list used as key → `TypeError`; grid bug fixed with a comprehension; list and tuple of 10⁶ items differ by 16 bytes |
| Q3 Dictionaries | `python complete_code.py` (TODO 1, 2), `python kisan.py`, `python experiments.py` | `[('seeds', 3), ('price', 2), ('received', 2)]`; dictionary/Counter 6× faster than `list.count` at 100,000 complaints |
| Q4 Sets | `python complete_code.py` (TODO 1), `python electives.py`, `python experiments.py`, `python venn.py` | clash 2 students; `x in set` up to 95,000× faster than `x in list` |
| Q5 Comprehension | `python sensors.py`, `python measure.py` | three versions identical; generator uses 208 bytes against 8.4 MB for the list |
| Q6 Nested data | `python railway.py`, `python experiments.py` | station index makes queries 43–80× faster |
| Q7 Contact merging | `python test_contacts.py`, `python experiments.py` | 10 contacts → 6 people; 100,000 contacts in 1.7 s; pairwise needs about 7 minutes |

Each folder contains `output_<program>.txt` (captured output), the diagrams (`Q2/memory_diagram.png`, `Q4/venn_diagrams.png`, `Q6/nested_structure.png`) and a `screenshots/` folder (rendered images of the program output; replace them with screenshots of your own runs).

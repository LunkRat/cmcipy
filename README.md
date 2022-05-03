# `cmci.py`

Cousineau-Morey confidence intervals ([Morey 2008](https://web.archive.org/web/20180720084728id_/http://www.tqmp.org/Content/vol04-2/p061/p061.pdf)) calculated with a Python implementation. Based on Jarrod Blinch's [2014 blog tutorial](https://motorbehaviour.wordpress.com/2014/10/31/confidence-intervals-in-within-participant-design-a-tutorial-on-the-cousineau-morey-method/),
I coded this Python implementation to aid my own learning on the topic. Thank you Jarrod; your tutorial helped me a lot.

## Usage

`python3 cmci.py` runs the script, outputs all values calculated using the sample data, and shows four plots.

`python3 cmci.py --datafile=/path/to/your/datafile.tsv` runs the script using _your_ data. It assumes the data layout in the format of the table in the [blog entry](https://motorbehaviour.wordpress.com/2014/10/31/confidence-intervals-in-within-participant-design-a-tutorial-on-the-cousineau-morey-method/)

`python3 cmci.py --datafile=/path/to/your/datafile.tsv --ylabel="My quantitative measurement"` allows you to specify the `y` axis label.

## Installation

Requires `pandas`, `matplotlib`, and `scipy`. A pip `requirements.txt` file is included, so you can install by running:

```bash
python3 -m pip install -r requirements.txt
```

## Author

Link Swanson
# Create a venv and activate it

`python3 -m venv tetris-venv`
`source tetris-venv/bin/activate`

# To install requirements

`python -m pip install -r requirements.txt`

# To save requirements

`python -m pip freeze > requirements.txt`

# To train

`python src/dominator.py _epochs_ _opt-chkpt_`

-1 epochs means run until fitness threshold.

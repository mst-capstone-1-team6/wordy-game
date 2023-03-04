# wordy-game
Our Boggle/Scrabble-like game for Capstone 1

## Setting up
On your machine, run these commands:

```shell
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

You should run the above commands before launching an IDE of your choice.
After running the above commands, your IDE (such as VS Code or Pycharm)
should pick up the created virtual environment.

## Running
Once you are setup, you can run the game like so:

```shell
python3 -m wordy
```

Alternatively, you can open up [`__main__.py`](wordy/__main__.py) in your IDE and click the run button at the bottom.

## Writing code
All code will go inside of the [wordy](wordy) directory.
You can write unit tests inside the [tests/unit](tests/unit) directory.

## Testing
```shell
python3 -m tests.unit.basic_test
```

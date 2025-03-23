# Fastnote migration/convertion

Migrate (convert) android app [fastnotepad](https://play.google.com/store/apps/details?id=net.fast_notepad_notes_app.fastnotepad&hl=en) notes from previous version format to latest version format. Earlier app version stored notes in plain text files. Latest app version stores notes in a single file with specific structure. Program takes folder of 

# How to run

You can either download compiled program from [release section](https://github.com/aleksandrasd/fastnotepad-migration/releases) or, if you have installed python, run script in python.

## Release

Download program from [release section](https://github.com/aleksandrasd/fastnotepad-migration/releases).

Open prompt.

Migrate (convert) [fastnotepad](https://play.google.com/store/apps/details?id=net.fast_notepad_notes_app.fastnotepad&hl=en) notes that exists in folder `fastnotes`:

```bash
migrate fastnotes/ backup
```

This will create file `backup` containing notes in the newest format.

## Python

Script works with any python3 interpreter.

First, clone git repository:

```bash
git clone https://github.com/aleksandrasd/fastnotepad-migration.git
```

Migrate (convert) [fastnotepad](https://play.google.com/store/apps/details?id=net.fast_notepad_notes_app.fastnotepad&hl=en) notes that exists in folder `fastnotes`:

```bash
python migrate fastnotes/ backup
```

This will create file `backup` containing notes in the newest format

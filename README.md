# Find Case Law Analysis / Data Science repo

This contains various utilities for analysis and evaluation of the search functionality.

To get started, first install pre-commit (this needs to be outside your virtualenv):

> pip install pre-commit jupyter
> pre-commit install

This is important, as we use a pre-commit hook to strip the output from our ipython notebooks - given some of the data we work with here is sensitive, we absolutely do not want it leaking into the git repository.

**Ensure all your data files are kept within the gitignored `tmp/` or `data/`, and your notebook output is properly sanitised before commiting anything!

Then set up a virtualenv and install the dependencies:

> virtualenv venv
> . venv/bin/activate
> pip install -r requirements.txt

Finally, run jupyter:

> jupyter notebook

# Getting data to work with

Now you'll need some data to work with. Ask one of the dxw folks for a sample of the cloudfront logs - they will give you a folder full of .gz compressed log files which you can place within `data/`

First, pre-process these to create one log file:

./scripts/concatenate_cloudfront_logs.sh DIRECTORY_CONTAINING_LOGS data/cloudfront_logs_concatenated.log

Then extract the search queries and results from these logs:
python ./scripts/make_search_sessions.py data/cloudfront_logs_concatenated.log data/searches_nov_23.json

You can then delete the folder of gzipped logs and `data/cloudfront_logs_concatenated.log`.

# Reproducing the search evaluation.

You'll need first to step through the notebook `Parse cloudfront logs`, following the instructions, and then the notebook `Relevance metrics`.


# AGLOCL: An automatically generated list of curated lists

AGLOCL (pronounced "Aaaaaaaa-glok" -- that is, a scream and the sound a
turkey makes) is an automatically generated list of curated lists on
GitHub.

AGLOCL is not on AGLOCL, because a curated list is of course a list that
is composed and maintained by a human.

The vast majority of lists are in fact not made by a computer, clickbait
notwithstanding, so one almost wonders why anyone would need to say a
list is curated at all.

## Use

So you want your own automatically generated list of curated lists? I
completely understand.

AGLOCL runs on Python 3 and uses the `requests` and `beautifulsoup4`
modules. Create a virtual environment and install those modules there:

    pip install --user virtualenv    # if necessary
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Then run AGLOCL inside the virtual environment:

    ./aglocl.py

This will probably take around 15 minutes, as GitHub doesn't like being
asked for HTTP requests too often in a row. AGLOCL will print messages
to `STDERR` to let you know how it's doing. Once it's done farming for
curated lists, it will update this `README.md` file with its results.

## The list of curated lists


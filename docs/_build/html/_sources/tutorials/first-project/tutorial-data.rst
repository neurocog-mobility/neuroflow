Tutorial data
======================================

| To get started, first let's download the accelerometry data for this tutorial: :download:`tutorial_data_walking.zip <./data/tutorial_data_walking.zip>`
| Extract the data to any location on your computer.

Before diving into NeuroFlow, let's have a quick look at the data we'll be using.
In the main folder, there are 4 subfolders:

::

    tutorial_data_walking
    ├── meta
    ├── sub002
    │   ├── axivity
    │   │   ├── NAPS_UW_001_Visit#01_AXV6_leftankle.cwa
    │   │   ├── NAPS_UW_001_Visit#01_AXV6_rightankle.cwa
    │   │   └── NAPS_UW_001_Visit#01_AXV6_waist.cwa
    │   └── sync
    │       └── NAPS_UW_001_Visit#01_sync.csv
    ├── sub002
    │   ├── axivity
    │   └── sync
    ├── sub002
    │   ├── axivity
    │   └── sync


* ``meta`` contains a file with the trial labels (e.g. "Fast walking", "Timed up-and-go", etc.).
* ``sub001``, ``sub002``, ``sub003`` contain the data folders for subjects 1 to 3, which each contain:
   * ``axivity`` which have the waist and ankle accelerometry data files for the subject.
   * ``sync`` which has the recorded trial timestamps for the session.

Now that we have our data ready, we can create our first NeuroFlow project.
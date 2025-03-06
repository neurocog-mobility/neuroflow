Configuring the Data Catalog
=================================

Move onto select the third code cell (under **3. Setup the data catalog**) and run it.

You should see the name and description of the pipeline you want to set the data catalog for,
along with File/Folder selection buttons for each data source that needs to be configured
(in this case ``input_axivity_dataset`` and ``input_sync_dataset``):

.. figure:: static/out_3.png

When selecting a data source folder, you should choose the directory containing all the data of that
modality. In this case, since the accelerometry (.cwa) and sync (.csv) files are spread across
multiple subfolders in the main ``tutorial_data_walking`` folder, we'll choose the main data
folder as the data source for both Axivity (i.e. accelerometry) and sync input data.

.. tip::

    In the case where no timestamp files exist or you would like to process an entire data 
    collection without splitting into different trials, simply leave the ``input_sync_dataset``
    source blank.

Once a data source is selected, the corresponding selection button will turn green with a checkmark.

Once you've selected both Axivity and sync sources, click ``Register inputs`` to set the Data Catalog -
you should see the confirmation:

.. code:: powershell

    All files successfully transferred.

.. note::

    The file transfer refers to how NeuroFlow creates copies of your data from the source folder into
    the project folder. In this case, all the Axivity and sync data from all subjects in the ``tutorial_data_walking``
    folder has now been placed in ``axivity`` and ``sync`` subfolders in your ``tutorial_pipeline/data/raw`` folder.

With the Data Catalog set, the next step is to set the Parameter Catalog.


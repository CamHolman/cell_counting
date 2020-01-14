Cell Counting
==============================
## Introduction

Tools to count signal positive cells from IHC images. This is designed for detecting Alexa-488 posititve cells with sparse distribution. However, this should be generalizable to different data sets through use of the training algorithm.

Here you can see a randomly chosen example:
![Example Count](references/example_count_2.png)

## Setup 
### Cloning Repository
With git installed, navigate to the folder you wish to contain this repo and run the following line:

    git clone https://github.com/ixianid/cell_counting/
    
This will copy the repository to your local machine. The repo's organization is based on cookiecutter, with some modifications. See the organization below.

### Project Organization

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    |
    ├── data               <- This structure is excluded from github repository
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- Documentation an further instructions (WIP)
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt` for use with virtualenv
    │
    ├── environment.yml    <- The requirements file for producing the usable environment with conda, e.g. 
    |                         generated with 'conda env export > environment.yml
    |
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    |
    ├── cc                 <- Source code for use in this project.
    │   ├── __init__.py         <- Makes cc a Python module
    │   │
    │   ├── preprocess          <- Functions for importing and preprocessing raw data (.czi, .tif) 
    │   │   └── make_dataset.py
    │   │
    │   ├── count               <- Module for counting cells
    │   │   └── count_cells.py
    │   │
    │   ├── models              <- Functions to train model for cell counting - brute force WIP
    │   │   └── train_model.py
    │   │
    │   └── plot                <- Functions for plotting and visualizing data
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org



### Setting up virtual environment

Once the repository is cloned, navigate to the head of the repo to set up the virtual environment. 

##### virtualenv
If you are using virtualenv, run the following line:

    pip install -r requirements.txt

##### conda
If you are using conda, you have two options:

    # Option 1
    conda env create -f environment.yml
    
    # Option 2
    conda create --name <env_name> --file requirements.txt
    
## Test Data
Test czi files can be found under `references/test_data/czi/`. Test TIFFs can be found in `references/test_data/tif/`. Expected counts can be found under `references/test_data/expected_counts/` as CSV files. You can use these to make sure your pipeline is set up correctly.

    CZI Files = [2D, 3Z, 3C]

    TIFF = [2D, 1Z, 1C]

To do so, follow the instuctions below and run the pipeline on the test data.

## Import and Preprocessing 
Importing raw CZI files can be managed through `cc/io` and preprocessing can be handled in `cc/preprocess`. This uses bioformats import through a javabridge, as originally implimented by [cellprofiler](https://cellprofiler.org/). TIf more comfortable, preprocessing can be handled with [FIJI](https://fiji.sc/) and single channel, noise corrected, max-projected TIFFs can be passed directly to the cell counter. 

If you prefer to do preprocessing in FIJI, skip to the `FIJI` section below.


#### CC | Bioformats Import (CZI)
This uses bioformats import through a javabridge, as originally implimented by [cellprofiler](https://cellprofiler.org/). The included implementation will process CZI images taken with three channels. In the intended case, these include:

    1. mCherry
    2. eGFP
    3. DAPI

Each of these channels has multiple z-planes. Each CZI files is imported as a four-dimensional numpy array of the following organization:

    [Y_plane, X_plane, Z_depth, Channel]

To import one CZI file: 



#### CC | Preprocessing
After import, images are stored as 4D numpy arrays. Before couting, a maxprojection will be taken of the z-planes for each channel. 

Preprocessing done here will include a max-projection of the Z axis of each channel to form a single, two-dimensional image for each channel. This means you will have three total 2D images (mCherry, eGFP, DAPI) 


After max projection, noise is removed and edges sharpened with a 3 x 3 [median filter](https://homepages.inf.ed.ac.uk/rbf/HIPR2/median.htm). This helps to remove pixels that differ significantly from their neighbors, which removes noise while deing a resonable job of maintining edges. This is the same process done by FIJI's 'despeckle' inbuilt function. The convolution kernel itself looks and behaves like this:

![3x3 Median Filter Kernel](references/imgs/3-3-kernel-in-median-filter.png)


## Cell Counting
The counted channel is eGFP, in future implementations the signal from the eGFP channel will be cross-referenced with the DAPI channel to ensure a cell body and not a process is being counted.

## Training Model

The current training model is a brute force depth first search for the highest pearson correlation with varying parameters for the Laplacian of Gaussian blob detection algorithm versus manual cell counting. This will be improved, but is functional with time and computing power.

To run the training, manually count ~20 images and record this information in a CSV with unique identifiers for each file. Run the training algorithm:
     
    train_cc(man_counts, imdir, ranges=default_ranges) 

with the CSV (man_counts) and training image directory (imdir) as input. You have the ability to modify the ranges of parameters it will search through to find the highest pearson correlation with the training data. The default range parameters are:

    default_ranges = {
            'min_sigma_low': 1,
            'min_sigma_high': 10,
            'min_sigma_interval':1,
            'max_sigma_low': 20,
            'max_sigma_high': 80,
            'max_sigma_interval': 1,
            'num_sigma_low': 5,
            'num_sigma_high': 40,
            'num_sigma_interval': 1,
            'thresh_low': 0.01,
            'thresh_high': 0.5,
            'thresh_interval': 0.01,
            'overlap_low': 0.01,
            'overlap_high': 0.2,
            'overlap_interval': 0.01
            }    

To choose your own ranges and intervals modify the above dictionary and pass it to 'train_cc'.

After completion, the training algorithm will save a CSV with each pearson correlation and the parameters used for that instance. It will also retrun these parameters as a dictionary Choose the parameters with the highest pearson correlation to proceed. 


## Cell Counting
To count cells make sure 





<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
"# cell_counting" 

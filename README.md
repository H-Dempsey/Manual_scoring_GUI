# Manual Scoring GUI 🐁

At the moment this only works on Windows, I will update this when it works on Mac. <br>
In the video window, the units of time are frames and the speed uses arbitrary units. <br>
To generate the output data, ensure that you click on the "X" button in the top right of the video window, and not the terminal window.

![image](https://user-images.githubusercontent.com/101311642/209245609-7edf5ee1-1ba2-4e52-b23f-ebe55fb55a91.png)

### Installation

Install [Anaconda Navigator](https://www.anaconda.com/products/distribution). <br>
Open Anaconda Prompt (on Mac open terminal and install X-Code when prompted). <br>
Download this repository to your home directory by typing in the line below.
```
git clone https://github.com/H-Dempsey/Manual_scoring_GUI.git
```
If you receive an error about git, install git using the line below, type "Y" when prompted and then re-run the line above.
```
conda install -c anaconda git
```
Change the directory to the place where the downloaded folder is. <br>
```
cd Manual_scoring_GUI
```

Create a conda environment and install the dependencies.
```
conda env create -n MSG -f Dependencies.yaml
```

### Usage
Open Anaconda Prompt (on Mac open terminal). <br>
Change the directory to the place where the git clone was made.
```
cd Manual_scoring_GUI
```

Activate the conda environment.
```
conda activate MSG
```

Run the codes.
```
python Manual_scoring_GUI.py
```

### Acknowledgements

__Author:__ <br>
[Harry Dempsey](https://github.com/H-Dempsey) (Andrews lab and Foldi lab) <br>

__Credits:__ <br>
Laura Milton, Eva Guerrero, Claire Foldi <br>

__About the labs:__ <br>
The [Andrews lab](https://www.monash.edu/discovery-institute/andrews-lab) investigates how the brain senses and responds to hunger. <br>
The [Foldi lab](https://www.monash.edu/discovery-institute/foldi-lab) investigates the biological underpinnings of anorexia nervosa and feeding disorders. <br>

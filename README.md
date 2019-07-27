# Trajectory Hotspot Applied


Presented at [CVPR 2018](http://cvpr2018.thecvf.com/)

## PROJECT STRUCTURE
The overall project Sequence is as follows:

0. import Geolife 'data' folder ~2 GB from **https://www.microsoft.com/en-us/download/details.aspx?id=52367**

1. Create results folder running **create_processing_directories.py** 

2. Parse Raw Data using **data_parser.py**

3. Generate Grid Dictionary with **generate_tiles.py**

4. Network Analysis in **network_results.py**

5. ThroughPut Analysis inside **network_segments.py**

6. Tensor Generator **network_tensor.py**

7. Hotspot Visualization done within **network_visuals.py**


##Setup

All code was developed and tested on MacOS Mojave 10.14.5 with Python 3.7.

You can setup a virtual environment to run the code like this:



```bash
CREATE
python3.7 -m venv trajectory_analysis
OPEN
source ~/env/trajectory_analysis/bin/activate
DEPENDENCIES
pip install -r requirements.txt 
LINK TO WORKING DIRECTORY
echo $PWD > env/lib/python3.7/site-packages/trajectory-hotspots.pth  # Add current directory to python path

CLOSE
deactivate
```


## Contributors:
 
[Matthew Zimmer](https://github.com/matthewzimmer)

[sangoli](https://github.com/sangoli)


## References
**<a href="https://arxiv.org/abs/1803.10892">Social GAN: Socially Acceptable Trajectories with Generative Adversarial Networks</a>**
<br>
<a href="http://web.stanford.edu/~agrim/">Agrim Gupta</a>,
<a href="http://cs.stanford.edu/people/jcjohns/">Justin Johnson</a>,
<a href="http://vision.stanford.edu/feifeili/">Fei-Fei Li</a>,
<a href="http://cvgl.stanford.edu/silvio/">Silvio Savarese</a>,
<a href="http://web.stanford.edu/~alahi/">Alexandre Alahi</a>
<br>




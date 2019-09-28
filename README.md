# Trajectory Hotspot Applied


## PROJECT STRUCTURE
Adjust granularity by modifying ds & dt values on top of scripts. (default set to 200m and 500s)

The overall project Sequence is as follows:

0. import Geolife 'data' folder ~2 GB from **https://www.microsoft.com/en-us/download/details.aspx?id=52367**

1. Parse Raw Data using **data_cleaning.py**

2. Generate Grid Dictionary with **generate_tiles_op.py**

3. Network Analysis in **network_results.py**

4a. Network generator for Tensor **network_segments_tensor.py**

4b. ThroughPut Analysis inside **network_segments_TP.py**

5. Tensor Generator **network_tensor.py**

6. Hotspot Visualization done within **network_visuals.py**


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

[Francisco Cancedda](https://github.com/fcancedda)
 
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




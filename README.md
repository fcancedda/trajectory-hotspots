# Trajectory Hotspot Analysis
**<a href="https://arxiv.org/abs/1803.10892">Social GAN: Socially Acceptable Trajectories with Generative Adversarial Networks</a>**
<br>
<a href="http://web.stanford.edu/~agrim/">Agrim Gupta</a>,
<a href="http://cs.stanford.edu/people/jcjohns/">Justin Johnson</a>,
<a href="http://vision.stanford.edu/feifeili/">Fei-Fei Li</a>,
<a href="http://cvgl.stanford.edu/silvio/">Silvio Savarese</a>,
<a href="http://web.stanford.edu/~alahi/">Alexandre Alahi</a>
<br>

Presented at [CVPR 2018](http://cvpr2018.thecvf.com/)


Human motion is interpersonal, multimodal and follows social conventions. In this paper, we tackle this problem by combining tools from sequence prediction and generative adversarial networks: a recurrent sequence-to-sequence model observes motion histories and predicts future behavior, using a novel pooling mechanism to aggregate information across
people.

Below we show an examples of socially acceptable predictions made by our model in complex scenarios. Each person is denoted by a different color. We denote observed trajectory by dots and predicted trajectory by stars.
<div align='center'>
<img src="images/2.gif"></img>
<img src="images/3.gif"></img>
</div>


If you find this code useful in your research then please cite

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

## Model
Our model consists of three key components: Generator (G), Pooling Module (PM) and Discriminator (D). G is based on encoder-decoder framework where we link the hidden states of encoder and decoder via PM. G takes as input trajectories of all people involved in a scene and outputs corresponding predicted trajectories. D inputs the entire sequence comprising both input trajectory and future prediction and classifies them as “real/fake”.

<div align='center'>
  <img src='images/model.png' width='1000px'>
</div>


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
echo $PWD > env/lib/python3.7/site-packages/sgan.pth  # Add current directory to python path
CLOSE
deactivate
```
## Pretrained Models
You can download pretrained models by running the script `bash scripts/download_models.sh`. This will download the following models:

- `sgan-models/<dataset_name>_<pred_len>.pt`: Contains 10 pretrained models for all five datasets. These models correspond to SGAN-20V-20 in Table 1.
- `sgan-p-models/<dataset_name>_<pred_len>.pt`: Contains 10 pretrained models for all five datasets. These models correspond to SGAN-20VP-20 in Table 1.

Please refer to [Model Zoo](MODEL_ZOO.md) for results.

## Running Models
You can use the script `scripts/evaluate_model.py` to easily run any of the pretrained models on any of the datsets. For example you can replicate the Table 1 results for all datasets for SGAN-20V-20 like this:

```bash
python scripts/evaluate_model.py \
  --model_path models/sgan-models
```

## Citations







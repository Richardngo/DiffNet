To run code

without google colab (requires env setup):
1. install Python 3.10.12
2. pip install tensorflow==2.12.0
3. unzip diffnet-main.rar 
4. unzip data (yelp_10 and yelp_20) into src\data
5. run: run_script.sh

with google colab (no environment setup):
1. use google colab file: diffnet_v2_all_complete.ipynb 
2. unzip diffnet-TPU-ONLY.zip to google colab file directory (commands in diffnet_v2_all_complete.ipynb ) 
3. unzip data (yelp_10 and yelp_20) into src\data
4. ->'runtime' -> 'change runtime type' is set to: -tpu and -high ram (otherwise this will take forver. each run takes 5-8 hours for each of the 8 experiments with tpu and high ram settings)
5. run: google colab file 

Note:
data-tool.zip is not required to run program, but included as it generates yelp_10 and yelp_20 from yelp dataset: https://www.yelp.com/dataset

Code authors:
dharahas10 (main author)
- diffnet-main
- data-tools
- data (yelp_10 yelp-20)
original source: https://github.com/dharahas10/diffnet
johnwang21 (code validation and cloud environment)
- diffnet_v2_all_complete.ipynb 
- diffnet-TPU-ONLY.zip

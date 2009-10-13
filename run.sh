#!/bin/bash
cd data/
edje_cc slider.edc -o ../slider.edj
cd ../
python edje-launcher.py slider.edj

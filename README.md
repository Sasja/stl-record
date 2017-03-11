# stl-record
3d printing records, why not?

currently no audio yet, just one circular sinewave. Also the parameters chosen (depth, amplitude, groove angle, diameter) have not been tested yet!

It has two channels though :)

## set up
im asuming ubuntu here

```sudo apt-get install python-pip meshlab```

```pip install numpy-stl```

## create stl

```python createStl.py```

## view result

```meshlab record.stl```

# stl-record
3d printing records, why not?

currently no wav input yet, just sines. Also the parameters chosen (depth, amplitude, groove angle, diameter, frequency, sample rate) have not been tested yet! just chosen ad hock for developing the code.

It has two channels though :)

## set up
im asuming you are using ubuntu:

```sudo apt-get install python-pip meshlab```

```pip install numpy-stl```

## create stl

```python createStl.py```

## view result

```meshlab record.stl```

![see the groove](/doc/record.png?raw=true)

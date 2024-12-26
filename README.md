# SMT Tweaks

This is a proof of concept script to generate training data for the [SMT-plusplus OMR Model](https://github.com/antoniorv6/SMT-plusplus).

To run, you will need to install the dependencies in [requirements.txt](requirements.txt), and have the Inkscape CLI setup in your PATH. It will generate two files:

- `output.png` - This is the image that the model can train on. 
- `mykern.krn` - This is the Kern notation of the image generated, on which the model can validate its prediction.
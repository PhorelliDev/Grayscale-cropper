# Grayscale-cropper

This is an incredibly crude cropper, intended to detect patients lying in hospital beds.
It makes no (direct) use of machine-learning (although a lot of the underlying mechanics involves such), and functions on the following assumptions:

- The bed sheets are (virtually) white/a uniformly bright color 
- The bed area is (relatively) well-light
- The patient, if present, is wearing (relatively) brightly-colored clothing
- The background is darker and/or noisy in color
- The bed is the largest definite form in the image

This algorithm is amateur in design, and was written in about a working day's worth of time. 
It does not use facial-recognition nor any kind of explicit recognition of humanoid forms and features. 
Created for a 2021 HYRS assignment. 

# Musicians

Scripts and other things that work with musical data.

Currently this is a scratch pad of ideas, but there are plans to flesh it out
into something very practical.

Currently in development. Most of the below are my notes more than a manual.
Many things may not yet be implemented

## Modules

### sequence

For working with musical sequences.

A sequence is a list with the indices called "beats" starting at 1.

#### sequence options

- `shift-style`: how sequence shifts are handled
    - `relative`: shifts are relative to current sequence
    - `absolute`: shifts are relative to original sequence
- `stretch-with`: how to handle filling values when stretching
    - `int`: sets intermediate values to a number
    - `repeat`: sets intermediate values to previous value
    - `interpolate`: sets intermediate values to interpolated values
- `expand-with`: how to handle filling values when expanding
    - `int`: sets remaining values to a number
    - `repeat`: sets remaining values to last value
    - `loop`: loops sequence
- `replace-style`: how to handle replacement if replacement sequence is too long
    - `trim`: trim replacement sequence to fit
    - `expand`: expand sequence to fit replacement

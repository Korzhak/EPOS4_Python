# EPOS4 Python

Python library for working with Maxon EPOS4 through UART without 
using `libEposCmd` library.

**The library is incomplete yet!**

At the moment you can use library with `Profile Position Mode (PPM)` only.

Available connection thorough `UART` only.

## How to use

Folder `epos4` contains code of the library.

Explanation of [example_1.py](examples/example_1.py).

1. Making object of EPOS4. Setting COM for communication with Maxon EPOS4 through UART.

```python
from epos4 import Epos4
from epos4 import definitions as df

e = Epos4('COM_NUM')
```

2. Checking current Operation mode. Set to PPM if it isn't.

```python
om = e.get_operation_mode().get()
if om != df.OM_PPM:
    e.set_operation_mode(df.OM_PPM)
```

3. Checking `Enabled state` and set it

```python
if not e.get_enable_state():
    e.set_enable_state()
```

4. Checking `Fault state`. Moving to position if it isn't

```python
if not e.get_fault_state():
    e.move_to_position(0xFFF)
```

_Clear `Fault state` if it happened_

```python
e.clear_fault_state()
```

_After clearing `Fault state` you have to check `Enable state` again_

```python
if e.get_enable_state():
    e.set_enable_state()
```

5. Don't forget to close connection in the end 

```python
e.close()
```

[OTHER EXAMPLES](examples)
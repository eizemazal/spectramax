# spectramax
Software for the communication with Molecular Devices Spectramax well plate photometers and fluorometers.

Molecular Devices provides a decent selection of well plate readers capable of absorption and fluorescence measurement. However, software for these instruments is costly, and hard to integrate.

Some research helped me identify communication commands and write a Python class to communicate with this instrument successfully. The protocol is simple text based. The class allows to do things that are not performed via standard SoftMaxPro software, for example, it allows to read and write NVRAM values.

I am still working on this project, so the support is yet incomplete.

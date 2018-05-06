#!/bin/bash

zip -r updated *.py
echo '#!/usr/bin/env python3' | cat - updated.zip > updated
chmod +x updated
rm updated.zip
./updated

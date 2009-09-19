#!/usr/bin/env python
""" Management script to check for compliance with
version control workflow & catch files being updated
on the production webserver"""

import ConfigParser
import logging
import os
import unittest
import argparse


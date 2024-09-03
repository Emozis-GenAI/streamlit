import streamlit as st
import websockets
import requests 
import json 
import re

from core.logger import logger
from core.config import configs
from core.utils import *

class Converter:
    def convert_gen(gender, method="value"):
        if method=="value":
            gen_values = {"남": "male", "여": "female", "기타": "other"}
        elif method=="idx":
            gen_values = {"male": 0, "female": 1, "other": 2}

        return gen_values[gender.strip()]
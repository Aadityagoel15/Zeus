from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import asyncpg
import numpy as np
import os
from sklearn.cluster import KMeans

from ..config import DATABASE_CONFIG
from ..services.summarizer import get_text_embedding  # embedding model
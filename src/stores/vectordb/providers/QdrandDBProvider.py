"""Implementing Qdrant Vector DB Provider class"""

import pathlib
import logging
from qdrant_client import models
from ..VectorDBConfig import DistanceMethodConfig
from ..VectorDBInterface import VectorDBInterface


class QdrantDBProvider(VectorDBInterface):
    def __init__(self, db_path: pathlib.Path, distance_method: str) -> None:
        self.client = None
        self.db_path = db_path
        # define distance metric
        # only support cosine and dot
        if distance_method == DistanceMethodConfig.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodConfig.DOT.value:
            self.distance_method = models.Distance.DOT
        self.logger = logging.getLogger(__file__)

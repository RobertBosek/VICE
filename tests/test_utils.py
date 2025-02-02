#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import torch
import unittest
import utils

import numpy as np
import helper
import torch.nn as nn


test_dir = './test'
train_file = 'train_90.npy'
test_file = 'test_10.npy'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class TripletLoadingTestCase(unittest.TestCase):

    @staticmethod
    def save_triplets(train_triplets, test_triplets) -> None:
        if not os.path.exists(test_dir):
            os.mkdir(test_dir)
        with open(os.path.join(test_dir, train_file), 'wb') as f:
            np.save(f, train_triplets)
        with open(os.path.join(test_dir, test_file), 'wb') as f:
            np.save(f, test_triplets)

    def test_loading(self) -> None:
        triplets = helper.create_triplets()
        train_triplets_before, test_triplets_before = helper.create_train_test_split(triplets)
        self.save_triplets(train_triplets_before, test_triplets_before)
        train_triplets_after, test_triplets_after = utils.load_data(device=device, triplets_dir=test_dir)
        shutil.rmtree(test_dir)
        
        np.testing.assert_allclose(train_triplets_before, train_triplets_after)
        np.testing.assert_allclose(test_triplets_before, test_triplets_after)

        train_triplets = train_triplets_after
        test_triplets = test_triplets_after

        self.assertEqual(train_triplets.shape[1], test_triplets.shape[1])
        self.assertEqual(type(train_triplets), type(test_triplets))
        self.assertTrue(isinstance(train_triplets, torch.Tensor))
        self.assertTrue(isinstance(test_triplets, torch.Tensor))

        M = utils.get_nobjects(train_triplets)
        self.assertTrue(type(M) == int)

        hypers = helper.get_hypers()
        self.assertEqual(M, hypers['M'])


class CorrelationTestCase(unittest.TestCase):

    def test_correlation(self) -> None:
        u = np.random.normal(loc=0., scale=1., size=(100,))
        v = np.random.normal(loc=0., scale=1., size=(100,))
        r = utils.pearsonr(u, v)
        self.assertTrue(type(r) == np.float64)
        self.assertTrue(r >= float(-1) and r <= float(1))

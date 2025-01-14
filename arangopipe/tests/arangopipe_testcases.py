#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 15:16:13 2019

@author: Rajiv Sambasivan
"""
import unittest
from arangopipe.arangopipe_admin_api import ArangoPipeAdmin
from arangopipe.arangopipe_api import ArangoPipe
from arangopipe.arangopipe_config import ArangoPipeConfig
import datetime
from arangopipe.rf_dataset_shift_detector import RF_DatasetShiftDetector
import os
import pandas as pd
import sys, traceback

class TestArangopipe(unittest.TestCase):
        
    def setUp(self):
        self.config = ArangoPipeConfig()
        self.config.set_dbconnection(hostname = "localhost", port = 8529,\
                                root_user = "root",\
                                root_user_password = "open sesame")
        self.admin = ArangoPipeAdmin(config = self.config)
        self.ap = ArangoPipe(config = self.config)
        self.provision_project()

    def provision_project(self):
        err_raised = False
        try:
            proj_info = {"name": "Wine-Quality-Regression-Modelling"}
            proj_reg = self.admin.register_project(proj_info)
        except:
            err_raised = True
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60)
            self.assertTrue(err_raised,\
                            'Exception raised while provisioning project')
        
        self.assertFalse(err_raised)
        return
    
    def register_dataset(self):
        ds_info = {"name" : "wine_dataset",\
                   "description": "Wine quality ratings",\
                   "source": "UCI ML Repository" }
        ds_reg = self.ap.register_dataset(ds_info)
        return
    
    def lookup_dataset(self):
        ds_reg = self.ap.lookup_dataset("wine_dataset")
        return
    
    def lookup_featureset(self):
        fs_reg = self.ap.lookup_featureset("wine_no_transformations")
        return
    
    def register_model(self):
   
        model_info = {"name": "elastic_net_wine_model", \
                  "type": "elastic net regression"}
        model_reg = self.ap.register_model(model_info)
        return
    
    def lookup_model(self):
        
        model_reg = self.ap.lookup_model("elastic_net_wine_model")
        return
    
    def log_run(self):

         ds_reg = self.ap.lookup_dataset("wine_dataset")
         fs_reg = self.ap.lookup_featureset("wine_no_transformations")
         model_reg = self.ap.lookup_model("elastic_net_wine_model")
         model_params = { "l1_ratio": 0.1, "alpha": 0.2,\
                         "run_id": "0ef73d9edf08487793c77a1742f4033e"}
         model_perf = { "rmse": 0.7836984021909766, "r2": 0.20673590971167466,\
                        "mae": 0.6142020452688988, "run_id": "0ef73d9edf08487793c77a1742f4033e",\
                        "timestamp": "2019-06-06 12:52:11.190048"}
         run_info = {"dataset" : ds_reg["_key"],\
                        "featureset": fs_reg["_key"],\
                        "run_id": "0ef73d9edf08487793c77a1742f4033e",\
                        "model": model_reg["_key"],\
                        "model-params": model_params,\
                        "model-perf": model_perf,\
                        "pipeline" : "Wine-Regression-Pipeline",\
                        "project": "Wine-Quality-Assessment",\
                        "deployment_tag": "Wine_Elastic_Net_Regression",\
                        "tag": "wine regression model test 1"}
         self.ap.log_run(run_info)
         return
    
    def provision_deployment(self):
    
        ret = self.admin.register_deployment("Wine_Elastic_Net_Regression")
    
        return
        
    
    def register_featureset(self):
        
        fs_info = {"fixed acidity": "float64",\
                   "volatile acidity": "float64",\
                   "citric acid": "float64",\
                   "residual sugar": "float64",\
                   "chlorides": "float64",\
                   "free sulfur dioxide": "float64",\
                   "total sulfur dioxide": "float64",\
                   "density": "float64",\
                   "pH": "float64",\
                   "sulphates": "float64",\
                   "alcohol": "float64",\
                   "quality": "int64",\
                   "name": "wine_no_transformations"
                   }
        ds_reg = self.ap.lookup_dataset("wine_dataset")
        fs_reg = self.ap.register_featureset(fs_info, ds_reg["_key"])
        return
    
    def log_servingperf(self):
        to_date = datetime.datetime.now()
        from_date = to_date - datetime.timedelta(days = 30)
        ex_servingperf = {"rmse": 0.822242, "r2": 0.12678, "mae": 0.62787,\
                          "from_date": str(from_date), "to_date": str(to_date)}
        dep_tag = "Wine_Elastic_Net_Regression"
        user_id = "prvileged user"
        ret = self.ap.log_serving_perf(ex_servingperf, dep_tag, user_id)
       
        return
    
    def dataset_shift_positive(self):
        ds_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "covariate_shift/cal_housing.csv")
        df = pd.read_csv(ds_path)
        req_cols = df.columns.tolist()
        df = df[req_cols]
        df1 = df.query("lat <= -119")
        df2 = df.query("lat > -119")
        rfd = RF_DatasetShiftDetector()
        score = rfd.detect_dataset_shift(df1, df2)
        print ("Detaset shift score : ", score)
        
        return score

    def dataset_shift_negative(self):
        ds_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "covariate_shift/cal_housing.csv")
        df = pd.read_csv(ds_path)
        req_cols = df.columns.tolist()
        df = df[req_cols]
        df1 = df.query("lat <= -119")
        df2 = df1.copy()
        rfd = RF_DatasetShiftDetector()
        score = rfd.detect_dataset_shift(df1, df2)
        print ("Detaset shift score : ", score)
    
        return score
    
    def test_register_dataset(self):
        err_raised = False
        try:
            self.register_dataset()
        except:
            err_raised = True
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60)
            self.assertTrue(err_raised,\
                            'Exception raised while registering dataset')
        self.assertFalse(err_raised)
        return
    
    def test_lookup_dataset(self):
        err_raised = False
        try:
            self.register_dataset()
            self.lookup_dataset()
        except:
            err_raised = True
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60)
            self.assertTrue(err_raised,\
                            'Exception raised while looking up dataset')
        self.assertFalse(err_raised)
        return
    
    def test_register_featureset(self):
        err_raised = False
        try:
            self.register_dataset()
            self.register_featureset()
        except:
            err_raised = True
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60)
            self.assertTrue(err_raised,\
                            'Exception raised while registering featureset')
        self.assertFalse(err_raised)
        return
    
    def test_lookup_featureset(self):
        err_raised = False
        try:
            self.register_dataset()
            self.register_featureset()
            self.lookup_featureset()
        except:
            err_raised = True
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60)
            self.assertTrue(err_raised,\
                            'Exception raised while registering featureset')
        self.assertFalse(err_raised)
        return
    
    
    
    def test_register_model(self):
        err_raised = False
        try:
            self.register_model()
        except:
            err_raised = True
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60)
            self.assertTrue(err_raised,\
                            'Exception raised while registering model')
        self.assertFalse(err_raised)
        return
    
    def test_lookup_model(self):
        err_raised = False
        try:
            self.register_model()
            self.lookup_model()
        except:
            err_raised = True
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60)
            self.assertTrue(err_raised,\
                            'Exception raised while looking up model')
        self.assertFalse(err_raised)
        return
    
    def test_log_run(self):
        err_raised = False
        try:
            self.register_dataset()
            self.register_featureset()
            self.register_model()
            self.log_run()
        except:
            err_raised = True
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60)
            self.assertTrue(err_raised,\
                            'Exception raised while logging performance')
        self.assertFalse(err_raised)
        return
    
    def test_provision_deployment(self):
        err_raised = False
        try:
            self.register_dataset()
            self.register_featureset()
            self.register_model()
            self.log_run()
            self.provision_deployment()
        
        except:
            err_raised = True
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60)
            self.assertTrue(err_raised,\
                            'Exception raised while provisioning deployment')
        self.assertFalse(err_raised)
        return
    
    def test_log_serving_performance(self):
        err_raised = False
        try:
            self.register_dataset()
            self.register_featureset()
            self.register_model()
            self.log_run()
            self.provision_deployment()
            self.log_servingperf()
        
        except:
            err_raised = True
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60)
            self.assertTrue(err_raised,\
                            'Exception raised while logging serving performance')
        self.assertFalse(err_raised)
        return
    
    def test_dataset_shift_positive(self):
        
        score = self.dataset_shift_positive()
        
        self.assertTrue(score > 0.8)
        return
    
    def test_dataset_shift_negative(self):

        score = self.dataset_shift_negative()
        

        self.assertTrue(score < 0.6)
        return
        

    
    def tearDown(self):
        #pass
        self.admin.delete_arangomldb()
        self.ap = None
        self.admin = None
        return
    
if __name__ == '__main__':
    unittest.main()
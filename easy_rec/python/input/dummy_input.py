# -*- encoding:utf-8 -*-
# Copyright (c) Alibaba, Inc. and its affiliates.

import tensorflow as tf

from easy_rec.python.input.input import Input

if tf.__version__ >= '2.0':
  tf = tf.compat.v1


class DummyInput(Input):
  """Dummy memory input.

  Dummy Input is used to debug the performance bottleneck of data pipeline.
  """

  def __init__(self,
               data_config,
               feature_config,
               input_path,
               task_index=0,
               task_num=1,
               input_vals={}):
    super(DummyInput, self).__init__(data_config, feature_config, input_path,
                                     task_index, task_num)
    self._input_vals = input_vals

  def _build(self, mode, params):
    """Build fake constant input.

    Args:
      mode: tf.estimator.ModeKeys.TRAIN / tf.estimator.ModeKeys.EVAL / tf.estimator.ModeKeys.PREDICT
      params: parameters passed by estimator, currently not used

    Returns:
      features tensor dict
      label tensor dict
    """
    features = {}
    for field, field_type, def_val in zip(self._input_fields,
                                          self._input_field_types,
                                          self._input_field_defaults):
      tf_type = self.get_tf_type(field_type)
      def_val = self.get_type_defaults(field_type, default_val=def_val)

      if field in ["opt_content_long_seq__event",        \
                   "time_id",                            \
                   "opt_content_long_seq__primary_type", \
                   "opt_content_long_seq__source_type",  \
                   "opt_content_long_seq__pub_time"]:
        def_val = '123'

      if field in self._input_vals:
        tensor = self._input_vals[field]
      else:
        tensor = tf.constant([def_val] * self._batch_size, dtype=tf_type)
      
      if field in ["opt_content_long_seq__event",        \
                   "time_id",                            \
                   "opt_content_long_seq__primary_type", \
                   "opt_content_long_seq__source_type",  \
                   "opt_content_long_seq__pub_time"]:
        tensor = tf.Print(tensor, [tensor[:1]], message=field)
      features[field] = tensor
    parse_dict = self._preprocess(features)
    return self._get_features(parse_dict), self._get_labels(parse_dict)

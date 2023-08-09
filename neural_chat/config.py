#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Configs for Neural Chat."""

from dataclasses import dataclass, field
from typing import Optional, List
import numpy as np
from transformers import TrainingArguments
from transformers.utils.versions import require_version

@dataclass
class ModelArguments:
    """
    Arguments pertaining to which model/config/tokenizer we are going to fine-tune from.
    """

    model_name_or_path: str = field(
        metadata={"help": "Path to pretrained model or model identifier from huggingface.co/models"}
    )
    config_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained config name or path if not the same as model_name"}
    )
    tokenizer_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained tokenizer name or path if not the same as model_name"}
    )
    cache_dir: Optional[str] = field(
        default=None,
        metadata={"help": "Where to store the pretrained models downloaded from huggingface.co"},
    )
    use_fast_tokenizer: bool = field(
        default=True,
        metadata={"help": "Whether to use one of the fast tokenizer (backed by the tokenizers library) or not."},
    )
    model_revision: str = field(
        default="main",
        metadata={"help": "The specific model version to use (can be a branch name, tag name or commit id)."},
    )
    use_auth_token: bool = field(
        default=False,
        metadata={
            "help": (
                "Will use the token generated when running `huggingface-cli login` (necessary to use this script "
                "with private models)."
            )
        },
    )

@dataclass
class DataTrainingArguments:
    """
    Arguments pertaining to what data we are going to input our model for training and eval.
    """

    dataset_name: Optional[str] = field(
        default=None, metadata={"help": "The name of the dataset to use (via the datasets library)."}
    )
    dataset_config_name: Optional[str] = field(
        default=None, metadata={"help": "The configuration name of the dataset to use (via the datasets library)."}
    )
    train_file: Optional[str] = field(default=None, metadata={"help": "The input training data file (a text file)."})
    validation_file: Optional[str] = field(
        default=None,
        metadata={"help": "An optional input evaluation data file to evaluate the perplexity on (a text file)."},
    )
    max_train_samples: Optional[int] = field(
        default=None,
        metadata={
            "help": (
                "For debugging purposes or quicker training, truncate the number of training examples to this "
                "value if set."
            )
        },
    )
    max_eval_samples: Optional[int] = field(
        default=None,
        metadata={
            "help": "For debugging purposes or quicker training, truncate the number of evaluation examples to this "
            "value if set."
        },
    )

    max_source_length: Optional[int] = field(
        default=512,
        metadata={
            "help": (
                "The maximum total input sequence length after tokenization. Sequences longer "
                "than this will be truncated, sequences shorter will be padded."
            )
        },
    )
    max_target_length: Optional[int] = field(
        default=256,
        metadata={
            "help": (
                "The maximum total sequence length for target text after tokenization. Sequences longer "
                "than this will be truncated, sequences shorter will be padded."
            )
        },
    )

    streaming: bool = field(default=False, metadata={"help": "Enable streaming mode"})
    overwrite_cache: bool = field(
        default=False, metadata={"help": "Overwrite the cached training and evaluation sets"}
    )
    validation_split_percentage: Optional[int] = field(
        default=1,
        metadata={
            "help": "The percentage of the train set used as validation set in case there's no validation split"
        },
    )
    preprocessing_num_workers: Optional[int] = field(
        default=None,
        metadata={"help": "The number of processes to use for the preprocessing."},
    )
    def __post_init__(self):
        if self.streaming:
            require_version("datasets>=2.0.0", "The streaming feature requires `datasets>=2.0.0`")

        if self.dataset_name is None and self.train_file is None and self.validation_file is None:
            raise ValueError("Need either a dataset name or a training/validation file.")
        else:
            if self.train_file is not None:
                extension = self.train_file.split(".")[-1]
                assert extension in ["csv", "json", "txt"], "`train_file` should be a csv, a json or a txt file."
            if self.validation_file is not None:
                extension = self.validation_file.split(".")[-1]
                assert extension in ["csv", "json", "txt"], "`validation_file` should be a csv, a json or a txt file."

@dataclass
class FinetuneArguments:
    """
    Arguments finetuning with lora config.
    """
    lora_rank: int = field(
        default=8,
        metadata={
            "help": "Rank parameter in the LoRA method."
        },
    )
    lora_alpha: int = field(
        default=32,
        metadata={
            "help": "Alpha parameter in the LoRA method."
        },
    )
    lora_dropout: float = field(
        default=0.1,
        metadata={
            "help": "Dropout parameter in the LoRA method."
        },
    )
    lora_target_modules: List[str] = field(
        default_factory=lambda: ["q", "v"],
        metadata={
            "help": "Target modules for the LoRA method."
        },
    )
    peft: Optional[str] = field(
        default="lora",
        metadata={
            "help": (
                "apply peft. default set to lora"
            ),
            "choices": ["lora"],
        },
    )

class FinetuningConfig:
    def __init__(self,
                 model_args: ModelArguments,
                 data_args: DataTrainingArguments,
                 training_args: TrainingArguments,
                 finetune_args: FinetuneArguments):
        self.model_args = model_args
        self.data_args = data_args
        self.training_args = training_args
        self.finetune_args = finetune_args

class OptimizationConfig:
    def __init__(self,
                 mode='latency',
                 device='cpu',
                 backend='ipex',
                 approach="static",
                 precision='bf16',
                 excluded_precisions=[],
                 op_type_dict=None,
                 op_name_dict=None,
                 recipes={}):
        self.mode = mode
        self.device = device
        self.backend = backend
        self.approach = approach
        self.precision = precision
        self.excluded_precisions = excluded_precisions
        self.op_type_dict = op_type_dict
        self.op_name_dict = op_name_dict
        self.recipes = recipes


class NeuralChatConfig:
    def __init__(self, model_name_or_path="meta-llama/Llama-2-70b-hf", inputs=None, device="auto",
                 backend="auto", retrieval=False, retrieval_type=None, txt2Image=False,
                 audio_input=False, audio_output=False, server_mode=True, finetune_config=None,
                 optimize_config=None, use_hpu_graphs=False):
        self.model_name_or_path = model_name_or_path
        self.inputs = inputs
        self.device = device
        self.backend = backend
        self.retrieval = retrieval
        self.retrieval_type = retrieval_type
        self.txt2Image = txt2Image
        self.audio_input = audio_input
        self.audio_output = audio_output
        self.server_mode = server_mode
        self.finetune_config = finetune_config if finetune_config else FinetuningConfig(
            model_args=ModelArguments(),
            data_args=DataTrainingArguments(),
            training_args=TrainingArguments(),
            finetune_args=FinetuneArguments())
        self.optimize_config = optimize_config if optimize_config else OptimizationConfig()
        self.use_hpu_graphs = use_hpu_graphs
